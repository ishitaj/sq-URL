import json
import random, string

import urllib.parse as urlparse

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse

from .models import Squrls
from .forms import SqurlForm
 

# Create your views here.
def index(request):
    """
    This view method gets called when Try sqURL link is clicked on index.html
    sqURLForm is rendered on squrl.html
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form = SqurlForm(request.POST)
        slug = ''
        error = ''
        # check whether it is valid
        if form.is_valid():
            target = form.cleaned_data['target']
            squrl = form.cleaned_data.get('squrl', None)
            # Check if the url exists by parsing and finding th scheme. It is set to 'http' when valid.
            if validate_target_exists(target):
                try:
                    # Search if the target url exists in the database already.
                    # If it does, return the squrl
                    urlobj = Squrls.objects.get(target=target)
                    slug = settings.BASE_SITE + urlobj.squrl
                    error = "This target url was already shortened!"
                except ObjectDoesNotExist:
                    if squrl:
                        try:
                            # Check for existence of squrl in the database to maintain uniqueness
                            if Squrls.objects.get(squrl=squrl):
                                error = "Sorry, Try with a different sqURL! This is already taken!"
                        except ObjectDoesNotExist:
                            # Generate the slug and create a new object in database
                            urlobj = Squrls(target=target, squrl=squrl)
                            urlobj.save()
                            slug = settings.BASE_SITE + urlobj.squrl
                            error = "This target url is being shortened now!"
                    else:
                        # Generate the slug and create a new object in database
                        squrl_id = Squrls.objects.order_by('-squrl_id')[0] + 1
                        slug = get_slug(squrl_id)
                        urlobj = Squrls(target=target, squrl=slug)
                        urlobj.save()
                        slug = settings.BASE_SITE + urlobj.squrl
                        error = "This target url is being shortened now!"
                finally:
                    return render(request, 'index.html',
                                 {'url' : slug,
                                 'error': error,
                                 'form': form,})
            else:
                return render(request, 'index.html',
                             {'error': "The url given to shorten does not exist",})

        # If form is invalid, reload the squrl page
        return HttpResponseRedirect(reverse('squrl:index'))

    # initialize the squrl form
    form = SqurlForm()
    return render(request, 'index.html', {'form': form,})


@csrf_exempt
def api(request):
    """
    This view exposes the functionality of the url shortener via an api.
    """
    if request.method == 'POST':
        # load the request body in json_data
        json_data = json.loads(request.body)
        try:
            # The json body of the POST request must have a key 'url' containing the url to be shortened
            target = json_data['url']
        except KeyError:
            # Raise a 404 error if the key does not exist
            return JsonResponse({'error': 'Please send data with key "url" and value as your target url.'})
        squrl = json_data.get('desired_squrl', None)
        slug = ''
        error = ''
        # Check if the url exists by parsing and finding the scheme. It is 'http' when valid.
        if validate_target_exists(target):
            try:
                # Search if the target url exists in the database already.
                # If it does, return the squrl
                urlobj = Squrls.objects.get(target=target)
                slug = settings.BASE_SITE + urlobj.squrl
                error = "This target url was already shortened!"
            except ObjectDoesNotExist:
                if squrl:
                    try:
                        # Check for existence of squrl in the database to maintain uniqueness
                        if Squrls.objects.get(squrl=squrl):
                            error = "Sorry, Try with a different sqURL! This is already taken!"
                    except ObjectDoesNotExist:
                        # Generate the slug and create a new object in database
                        urlobj = Squrls(target=target, squrl=squrl)
                        urlobj.save()
                        slug = settings.BASE_SITE + urlobj.squrl
                        error = "This target url is being shortened now!"
                else:
                    # Generate the slug and create a new object in database
                    slug = get_slug()
                    urlobj = Squrls(target=target, squrl=slug)
                    urlobj.save()
                    slug = settings.BASE_SITE + urlobj.squrl
                    error = "This target url is being shortened now!"
            finally:
                return JsonResponse({'squrl': slug,
                                     'error': error,})
        else:
            # If url does not exist, return json with error message
            return JsonResponse({'error': 'The url given to shorten does not exist'})

    # If GET is called on /api, redirect to the front-end for manual entry of url
    return HttpResponseRedirect(reverse('squrl:index'))


def db(request):

    squrls = Squrls.objects.all()

    return render(request, 'db.html', {'squrls': squrls,
                                       'BASE_SITE': settings.BASE_SITE})


def redirect(request, slug):
    """
    This view method gets called when GET request is called on the api with squeezed url
    or the href link is clicked on the squrl.html page
    """
    # If the object exists, get it based on the short url passed. If not found, return 404 error.
    url = get_object_or_404(Squrls, squrl=slug)
    url.visits += 1
    url.save()
    # Redirect to the target
    return HttpResponseRedirect(url.target)


def validate_target_exists(target):
    return urlparse.urlparse(target).scheme


def is_target_in_db(slug):
    """ TODO: Possible refactoring
    """
    pass


def is_squrl_available(slug):
    """ TODO: Possible refactoring
    """
    pass


def get_slug(base_10_num):
    """
    This method generates a unique slug of length 7 using random function and returns the unique code
    """
    # We want to generate a code of length 7
    code_len = 7
    # create a string containing all uppercase alphabets, lowercase alphabets and digits. 26 + 26 + 10 = 62
    char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase
    base = len(char_set)
    base_62_num = []

    while code_len > 0:
        remainder = base_10_num % base
        base_62_num.append(remainder)
        base_10_num //= base
        code_len -= 1
    base_62_num.reverse()
    slug = ''.join(char_set[x] for x in base_62_num)

    # This loop will keep running until a unique squrl is found
    while True:
        # Randomly pick 7 characters from the character set and join to form a string
        try:
            # Check for existence in the database to maintain uniqueness
            temp = Squrls.objects.get(squrl=slug)
        except:
            return slug
        finally:
            slug += random.choice(char_set)

    return slug

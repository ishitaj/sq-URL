from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# URL model to create database to store the shortened urls
class Squrls(models.Model):
    """
    Model for squrl url database
    """
    squrl_id = models.AutoField(primary_key=True)
    squrl = models.SlugField(max_length=50, unique=True)
    target = models.URLField(max_length=2000, unique=True)
    squrl_user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    access_date = models.DateTimeField(auto_now=True)
    visits = models.IntegerField(default=0)

    def __str__(self):
        return self.target

    def save(self, *args, **kwargs):
        self.squrl = slugify(self.squrl)
        super(Squrls, self).save(*args, **kwargs)

from django.test import TestCase


class TestCalls(TestCase):
    """
    Class for squrl tests
    """
    def test_get_api_json(self):
        """
        This test checks if valid get call to api gives success after redirection to the squrl page
        """
        response = self.client.get('/api/', headers = {'CLIENTNAME' : 'guest'})
        self.assertTrue(response.status_code, 200)

    def test_post_api_json(self):
        """
        This test checks if valid post call to api gives success after returning json response
        """
        response = self.client.post('/api/', {'url' : 'http://www.google.com'}, headers = {'CLIENTNAME' : 'guest'})
        self.assertTrue(response.status_code, 200)

    def test_call_view_loads(self):
        """
        This test checks if correct template is used to render /
        """
        response = self.client.get('/', headers = {'CLIENTNAME' : 'guest'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_call_view_fails_blank(self):
        """
        This test checks if status 400 happens on empty post request
        """
        response = self.client.post('/', {}, headers = {'CLIENTNAME' : 'guest'})
        self.assertTrue(response.status_code, 400)

    def test_call_view_fails_invalid_json(self):
        """
        This test checks if status 400 happens on requesting with invalid json key
        """
        response = self.client.post('/', {'urla' : 'http://www.google.com'}, headers = {'CLIENTNAME' : 'guest'})
        self.assertTrue(response.status_code, 400)

    def test_call_view_fails_invalid_url(self):
        """
        This test checks if status 400 happens on passing malformed url to json request
        """
        response = self.client.post('/', {'url' : 'googlecom'}, headers = {'CLIENTNAME' : 'guest'})
        self.assertTrue(response.status_code, 400)

    def test_call_view_fails_invalid_method(self):
        """
        This test checks if status 405 happens on passing put request
        """
        response = self.client.put('/', {'url' : 'googlecom'}, headers = {'CLIENTNAME' : 'guest'})
        self.assertTrue(response.status_code, 405)

from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..views import CaloryLimitView, CaloryLimitDetailsView

class CaloryLimitUrlsTest(SimpleTestCase):

    def test_calory_limit_url(self):
        url = reverse('calory_limit')
        self.assertEquals(resolve(url).func.view_class, CaloryLimitView)

    def test_calory_limit_details_url(self):
        url = reverse('calory_limit_details',kwargs={'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, CaloryLimitDetailsView)
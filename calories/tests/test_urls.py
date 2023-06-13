from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..views import (
    CaloryDetailsView, 
    CaloryView, 
    GetCurrentCaloryDetails, 
    EditDeleteCaloryView
    )


class CaloryUrlsTest(SimpleTestCase):

    def test_calory_view_url(self):
        url = reverse('calory_view', kwargs={'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, CaloryView)

    def test_calory_details_view_url(self):
        url = reverse('calory_details_view' , kwargs={'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, CaloryDetailsView)

    def test_edit_delete_calory_url(self):
        url = reverse('edit_delete_calory' , kwargs={'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, EditDeleteCaloryView)

    def test_todays_calory_url(self):
        url = reverse('todays_calory')
        self.assertEquals(resolve(url).func.view_class, GetCurrentCaloryDetails)

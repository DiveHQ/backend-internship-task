from django.urls import reverse, resolve
from django.test import SimpleTestCase
from ..views import RegistrationView, UserDetailsView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
class UserUrlsTest(SimpleTestCase):

    def test_register_user_url(self):
        url = reverse('register_user')
        self.assertEquals(resolve(url).func.view_class, RegistrationView)

    def test_edit_user_details_url(self):
        url = reverse('edit_user_details', kwargs={'pk': '1'})
        self.assertEquals(resolve(url).func.view_class, UserDetailsView)

    def test_token_obtain_pair_url(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url(self):
        url = reverse('token_refresh')
        self.assertEquals(resolve(url).func.view_class, TokenRefreshView)

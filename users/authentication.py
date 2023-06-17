from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication

class TokenAuthentication(BaseTokenAuthentication):
    """
    Extend TokenAuthentication to support custom token header
    """
    keyword = 'Bearer'
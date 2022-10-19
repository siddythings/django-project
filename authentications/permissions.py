from rest_framework.views import APIView

from authentications.auth import JWTAuthentication


class APIViewWithAuthentication(APIView):
    authentication_classes = [JWTAuthentication, ]

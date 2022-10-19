from jose import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from  application.settings import DB

SECRET = "ABCDEF1234"


class JWTAuthentication(BaseAuthentication):
    """
        Authorization for users which can view details of every API.
    """

    def authenticate(self, request):
        token_login = request.COOKIES.get('TOKEN')
        if not token_login and not request.META.get('HTTP_AUTHORIZATION'):
            raise exceptions.AuthenticationFailed('Access Denied. Please login again!')

        token = request.META.get('HTTP_AUTHORIZATION')

        try:
            if token_login:
                token_val = token_login.split(' ')[1]
            else:
                token_val = token.split(' ')[1]
        except:
            token_val = token_login or token
        try:
            payload = jwt.decode(token=token_val, key=SECRET, algorithms='HS256')
            if not payload.get('sub') and payload.get('customer_id'):
                payload['sub'] = payload.get('customer_id')
            user_id = payload.get('sub')
        except Exception as error:
            # error_logger.error("Authentication Error: {0} for Token: {1}".format(error, token))
            raise exceptions.AuthenticationFailed('Session Expired. Please login again')
        request.GET = request.GET.copy()
        request.GET.update(payload)
        if token_login:
            return '', True

        if not user_id:
            raise exceptions.AuthenticationFailed('Access Denied. Please login again!')
        # session_user = DB["login"].find_one({'user_id': int(user_id)})
        user = None
        user = DB["users"].find_one({"id": user_id})
        if user:
            return user, True
        if not user:
            raise exceptions.AuthenticationFailed('Access Denied. Please login again!')
        return user, True

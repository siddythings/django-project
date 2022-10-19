# Python Imports
from random import randint
import urllib
import requests
from rest_framework.views import APIView

# GMS Imports
from application.settings import DB
from utilities.utility import DatetimeUtils
from application.responses import SuccessResponse, BadRequestResponse, ResourceNotFoundResponse
from users.encryptions import EncryptDecrypt, Token
from authentications.permissions import APIViewWithAuthentication


class HomeDashboard(APIViewWithAuthentication):
    """
    This API send OTP
    """
    def get(self, request):
        
        return SuccessResponse(data=100, message="Home Dashboard")
        


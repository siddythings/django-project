# Python Imports
from random import randint
import urllib
import requests
from rest_framework.views import APIView

# GMS Imports
from application.settings import DB
from users.utils import UserServices
from utilities.utility import DatetimeUtils
from application.responses import SuccessResponse, BadRequestResponse, ResourceNotFoundResponse
from users.encryptions import EncryptDecrypt, Token
from authentications.auth import JWTAuthentication


class OTPAPIView(APIView):
    """
    This API send OTP
    """
    def get(self, request):
        requested_data = request.query_params
        mobile = requested_data.get("mobile")
        if not mobile:
            return BadRequestResponse(message="Mobile No. not found")
        user = DB["users"].find_one({'mobile':mobile,"labs":{"$exists":True}},{'_id':0})
        current_time = DatetimeUtils.get_current_time()
        otp = randint(100000,999999)
        if not user:
            return BadRequestResponse(message="User does not exist!")
        


        DB["users"].update_many({"mobile": mobile},
                                            {"$set": {"otp": str(otp), "updated_at": current_time}})
        return SuccessResponse(data=str(otp), message="OTP {} sent".format(otp))
        # return SuccessResponse(data={}, message="Failed to send OTP", data_status=False)


class LoginAPIView(APIView):

    def post(self, request):
        requested_data = request.data
        mobile = requested_data.get("mobile")
        otp = requested_data.get("otp")
        success_login = DB["users"].find_one({'mobile':mobile, 'otp': otp, 'is_active': True},{'_id':0})
        if success_login:
            token = Token.create_token(success_login.get("id"), 90)
            success_login.update({
                "auth_token": token
            })
            res = success_login
            return SuccessResponse(data=res, message="Login Successful :)", data_status=True)
        return SuccessResponse(data={}, message="Login Failed :(", data_status=False)

class UserOTPAPIView(APIView):
    """
    This API send OTP
    """
    def get(self, request):
        requested_data = request.query_params
        mobile = requested_data.get("mobile")
        if not mobile:
            return BadRequestResponse(message="Mobile No. not found")
        
        user = DB["users"].find_one({'mobile':mobile},{'_id':0})
        current_time = DatetimeUtils.get_current_time()
        otp = randint(100000,999999)
        if not user:
            UserServices.create_new_user(mobile,otp)
        else:
            DB["users"].update_many({"mobile": mobile},
                                                {"$set": {"otp": str(otp), "updated_at": current_time}})
        return SuccessResponse(data=str(otp), message="OTP {} sent".format(otp))
        # return SuccessResponse(data={}, message="Failed to send OTP", data_status=False)


class UserLoginAPIView(APIView):

    def post(self, request):
        requested_data = request.data
        mobile = requested_data.get("mobile")
        otp = requested_data.get("otp")
        success_login = DB["users"].find_one({'mobile':mobile, 'otp': otp, 'is_active': True},{'_id':0})
        if success_login:
            token = Token.create_token(success_login.get("id"), 90)
            success_login.update({
                "auth_token": token
            })
            res = success_login
            return SuccessResponse(data=res, message="Login Successful :)", data_status=True)
        return SuccessResponse(data={}, message="Login Failed :(", data_status=False)


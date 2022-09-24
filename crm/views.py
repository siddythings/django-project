from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
import pymongo

from application.settings import DB
from utilities.utility import DatetimeUtils

class CreateUser(APIView):
    def post(self, request):
        request_data = request.data
        request_data.update({
            "created_at": DatetimeUtils.get_current_time()
        })
        DB.leads.insert_one(request_data)
        return SuccessResponse(data = request_data, message="Users")
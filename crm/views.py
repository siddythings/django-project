from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
from bson import ObjectId
import pymongo

from application.settings import DB
from utilities.utility import DatetimeUtils, GeneratorUtils

class CreateUser(APIView):
    def post(self, request):
        request_data = request.data
        request_data.update({
            "created_at": DatetimeUtils.get_current_time()
        })
        DB.leads.insert_one(request_data)
        return SuccessResponse(data = request_data, message="Users")

class Booking(APIView):
    def post(self, request):
        request_data = request.data
        request_data.update({
            "booking_id": GeneratorUtils.get_booking_id(),
            "created_at": DatetimeUtils.get_current_time(),
            "updated_at": DatetimeUtils.get_current_time(),
        })
        DB.bookings.insert_one(request_data)
        return SuccessResponse(data=request_data, message="Booking")
    
    def put(self, request):
        request_data = request.data
        _id = request_data.get("_id")
        if not _id:
            return BadRequestResponse(message="Somethings Went Wrong!")
        
        request_data.pop("_id")
        request_data.update({
            "updated_at": DatetimeUtils.get_current_time()
        })
        DB.bookings.update_one({"_id":ObjectId(_id)},{"$set":request_data})
        return SuccessResponse(data=request_data, message="Payment Recived")
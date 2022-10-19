# Python Imports
from random import randint
import urllib
import requests
from rest_framework.views import APIView

# GMS Imports
from application.settings import DB
from crm_labs.pipeline import LabCrmPiplineServies
from utilities.utility import DatetimeUtils
from application.responses import SuccessResponse, BadRequestResponse, ResourceNotFoundResponse
from users.encryptions import EncryptDecrypt, Token
from authentications.permissions import APIViewWithAuthentication


class HomeDashboard(APIViewWithAuthentication):
    def get(self, request):
        lab_id = request.headers.get("lab", None)
        aggr = LabCrmPiplineServies.home_dashboard(lab_id)
        pipline_aggr_data = list(DB.labs.aggregate(aggr))
        
        pipline_aggr_data  = pipline_aggr_data[0] if pipline_aggr_data else {}
        pipline_aggr_data.update({
            "new_booking_count": pipline_aggr_data.get("new_booking_count",0),
            "completed_booking_count": pipline_aggr_data.get("completed_booking_count",0),
            "processed_booking_count": pipline_aggr_data.get("processed_booking_count",0),
            "canceled_booking_count": pipline_aggr_data.get("canceled_booking_count",0),
        })
        return SuccessResponse(data=pipline_aggr_data, message="Home Dashboard")
        

class BookingAPIView(APIViewWithAuthentication):
    def get(self, request):
        query = request.query_params
        offset = int(query.get("offset",0))
        limit = int(query.get("limit",5))
        lab_id = request.headers.get("lab", None)
        booking_id = query.get("booking_id")
        if booking_id:
            bookings_data = DB.bookings.find_one({'booking_id': booking_id})
        else:
            bookings_data = DB.bookings.find({'lab_id': lab_id}).sort('created_at',-1).skip(offset).limit(limit)
        return SuccessResponse(data=bookings_data, message="Bookings")
    
    def post(self, request):
        query = request.query_params
        request_data = request.data
        booking_id = query.get("booking_id")
        if not booking_id:
            return BadRequestResponse(message="Booking ID Requried!")
        
        lab_id = request.headers.get("lab", None)
        
        bookings_update = DB.bookings.update_one({'lab_id': lab_id, 'booking_id': booking_id},{"$set":{
            "status": request_data.get("status")
        }})
        
        if not bookings_update.modified_count:
            return BadRequestResponse(message="Booking ID Not Found!")
        return SuccessResponse(data=[], message="Bookings")
    
    def patch(self, request):
        query = request.query_params
        request_data = request.data
        booking_id = query.get("booking_id")
        if not booking_id:
            return BadRequestResponse(message="Booking ID Requried!")
        
        lab_id = request.headers.get("lab", None)
        
        bookings_update = DB.bookings.update_one({'lab_id': lab_id, 'booking_id': booking_id},{"$set":{
            "status": request_data.get("status")
        }})
        
        if not bookings_update.modified_count:
            return BadRequestResponse(message="Booking ID Not Found!")
        return SuccessResponse(data=[], message="Bookings")
    
    def delete(self, request):
        return SuccessResponse(data=[], message="Bookings")
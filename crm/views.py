from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from num2words import num2words
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
from bson import ObjectId
import pymongo

from application.settings import BASE_URL, DB
from utilities.utility import DatetimeUtils, GeneratorUtils, fetch_resources

class CreateUser(APIView):
    def post(self, request):
        request_data = request.data
        request_data.update({
            "created_at": DatetimeUtils.get_current_time(),
            "system_customer_id": GeneratorUtils.get_user_id()
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
            "status": "NEW"
        })
        DB.bookings.insert_one(request_data)
        return SuccessResponse(data=request_data, message="Booking")
    
    def put(self, request):
        request_data = request.data
        booking_id = request_data.get("booking_id")
        request_data.update({
            "updated_at": DatetimeUtils.get_current_time(),
            "payment_status": "PAID"
        })
        DB.bookings.update_one({"booking_id":booking_id},{"$set":request_data})
        return SuccessResponse(data=request_data, message="Payment Recived")
    
    def get(self, request):
        query = request.query_params
        booking_id = query.get("booking_id")
        mobile_no = query.get("mobile_no")
        
        if not booking_id and not mobile_no:
            return BadRequestResponse(message="Booking not Found!")
        
        if booking_id:
            booking_details = list(DB.bookings.find({"booking_id":booking_id}))
        
        if mobile_no:
            booking_details = list(DB.bookings.find({"customer_details.customer_number":mobile_no}))
        
        if booking_details:
            for obj in booking_details:
                obj.update({"invoices":{
                    "fileName": "testoin_invoice_{booking_id}".format(booking_id=obj.get("booking_id")),
                    "fileUrl": BASE_URL + "/crm/invoice/?booking_id={booking_id}".format(booking_id=obj.get("booking_id")),
            }})
        return SuccessResponse(data= booking_details, message="Booking Details")

    

class BookingInvoice(APIView):
    def get(self, request):
        requested_data = request.query_params
        if not requested_data.get("booking_id"):
            return BadRequestResponse(message="Booking ID not Found!")
        
        aggr = [
            {
                '$match': {
                    'booking_id': requested_data.get("booking_id")
                }
            }, {
                '$project': {
                    '_id': 0
                }
            }, {
                '$lookup': {
                    'from': 'packages', 
                    'localField': 'package_id', 
                    'foreignField': 'package_id', 
                    'as': 'package_details'
                }
            }
        ]

        booking_details = list(DB.bookings.aggregate(aggr))
        
        if not booking_details:
            return BadRequestResponse(message="Booking ID not Found!")
        
        template = get_template('invoice.html')
        booking_details = booking_details[0]
        total_cost = 0
        
        for obj in booking_details.get("package_details"):
            total_cost += obj.get("mrp")

        booking_details.update({
            "total_cost": total_cost,
            "flat_discount":0,
            "total_number": num2words(total_cost).capitalize()
        })
        html = template.render({'data': booking_details})

        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = \
            f'attachment; filename=  "{"".join("testoin_invoice_{booking_id}".split())}.pdf"'
        pisa.CreatePDF(html, dest=response, link_callback=fetch_resources)
        return response
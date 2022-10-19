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
        


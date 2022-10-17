from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
import pymongo
from bson import ObjectId

from application.settings import DB, RPY_API_KEY

class ScreenPageConfig(APIView):
    def get(self, request):
        query = request.query_params
        config = query.get("config","")
        screen_banners = DB.secreen_config.find_one({"config":config})
        return SuccessResponse(data = screen_banners, message="Homepage Config")

class HomepageCategory(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.test_category.find({})
        return SuccessResponse(data = data, message="Homepage category")

class CityLabs(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.cities.find({'is_active':True},{'_id':0})
        return SuccessResponse(data = data, message="Homepage category")


class Package(APIView):
    def get(self, request):
        query = request.query_params
        to_find = {}
        package_id = query.get("package_id")
        if package_id:
            data = DB.packages.find_one({'_id':ObjectId(package_id)},{'offer_price':1})
            return SuccessResponse(data = data, message="Packages")
        lab = query.get("lab")
        category = query.get("category")
        ratings = query.get("ratings")
        duration = query.get("duration")
        no_of_tests = query.get("no_of_tests")
        sort_by = query.get("sort")

        if sort_by == "low_to_high":
            sort_by = 1
            val = 'offer_price'
        elif sort_by == "high_to_low":
            sort_by = -1
            val = 'offer_price'
        else:
            sort_by = -1
            val = 'recommended'

        if lab:
            to_find.update({
                "lab_name":lab
            })
        
        if category:
            to_find.update({
                "category":category
            })
        
        if ratings:
            to_find.update({
                "ratings":float(ratings)
            })
        
        if duration:
            to_find.update({
                "duration":duration
            })
        
        if no_of_tests:
            to_find.update({
                "no_of_tests":no_of_tests
            })

        data = DB.packages.find(to_find).sort(val,sort_by)

        return SuccessResponse(data = data, message="Packages")

class Labs(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.labs.find({})

        return SuccessResponse(data = data, message="Labs")


class RazorpayKey(APIView):
    # permission_classes_by_action = {
    #     'GET': [OwnerOnlyPermission],
    #     'default': [OwnerOnlyPermission]
    # }

    def get(self, request):
        key = RPY_API_KEY
        key = {
            "key": key
        }
        return SuccessResponse(data=key, message="Key fetched successfully", data_status=True)
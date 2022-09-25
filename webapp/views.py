from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
import pymongo

from application.settings import DB

class ScreenPageConfig(APIView):
    def get(self, request):
        query = request.query_params
        config = query.get("config","")
        screen_banners = DB.secreen_config.find_one({"config":config})
        return SuccessResponse(data = screen_banners, message="Homepage Config")

class HomepageCategory(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.test_category.find({"order":{"$ne":None}}).limit(14).sort('order',1)

        return SuccessResponse(data = data, message="Homepage category")


class Package(APIView):
    def get(self, request):
        query = request.query_params
        to_find = {}
        lab = query.get("lab")
        category = query.get("category")
        ratings = query.get("ratings")
        duration = query.get("duration")
        no_of_tests = query.get("no_of_tests")
        
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

        data = DB.packages.find(to_find)

        return SuccessResponse(data = data, message="Packages")

class Labs(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.labs.find({})

        return SuccessResponse(data = data, message="Labs")



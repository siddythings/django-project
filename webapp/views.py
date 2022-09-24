from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
import pymongo

from application.settings import DB

class HomepageCategory(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.test_category.find({"order":{"$ne":None}}).limit(8).sort('order',1)

        return SuccessResponse(data = data, message="Homepage category")


class Package(APIView):
    def get(self, request):
        query = request.query_params
        data = DB.packages.find({"order":{"$ne":None}})

        return SuccessResponse(data = data, message="Packages")



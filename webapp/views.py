from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
import pymongo
from bson import ObjectId
from webapp.models import ShopItemsModels
from application.settings import DB, RPY_API_KEY
from authentications.permissions import APIViewWithAuthentication

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
        city = query.get("city")
        lab = query.get("lab","")
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
        # if city:
        #     to_find.update({
        #         "city":city
        #     })
        if lab:
            to_find.update({
                "lab_name":{"$in":lab.split(",")}
            })
        
        if category:
            to_find.update({
                "category":category
            })
        
        # if ratings:
        #     to_find.update({
        #         "ratings":float(ratings)
        #     })
        
        # if duration:
        #     to_find.update({
        #         "duration":duration
        #     })
        
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

class ShopAddToCart(APIViewWithAuthentication):
    # permission_classes_by_action = {
    #     'GET': [OwnerOnlyPermission],
    #     'default': [OwnerOnlyPermission]
    # }

    def post(self, request, id):
        request_data = request.data
        user_id = request.GET.get('sub')
        # shop_cart_items = DB.shop_cart_items.find_one({'created_by_id':user_id, 'product_id': id, 'ordered': False},{'_id':0})
        type = request_data.get("type")
        if type:
            ShopItemsModels.create_or_update(user_id, id)
        else:
            ShopItemsModels.remove_item(user_id, id)

        return SuccessResponse(data={}, message="Item added", data_status=True)

class GetCart(APIViewWithAuthentication):
    def get(self, request):
        aggr = [
            {
                '$match': {
                    'created_by_id': '4866f3c4e2394be5b02e55cd7d3e2ead', 
                    'ordered': False
                }
            }, {
                '$lookup': {
                    'from': 'packages', 
                    'localField': 'product_id', 
                    'foreignField': 'package_id', 
                    'as': 'package_details'
                }
            }, {
                '$unwind': {
                    'path': '$package_details'
                }
            }, {
                '$group': {
                    '_id': None, 
                    'mrp_total': {
                        '$sum': '$package_details.mrp'
                    }, 
                    'offer_price_total': {
                        '$sum': '$package_details.offer_price'
                    }, 
                    'items': {
                        '$push': {
                            'package_name': '$package_details.name', 
                            'discription': '$package_details.discription', 
                            'lab_name': '$package_details.lab_name', 
                            'offer_price': '$package_details.offer_price', 
                            'mrp': '$package_details.mrp', 
                            'instruction': '$package_details.instruction'
                        }
                    }
                }
            }
        ]
        cart = list(DB.shop_cart_items.aggregate(aggr))
        
        if cart:
            cart = cart[0]
        
        return SuccessResponse(data=cart, message="Get Cart", data_status=True)
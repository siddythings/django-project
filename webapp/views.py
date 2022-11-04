from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from application.responses import SuccessResponse, NoContentResponse, UnprocessableEntityResponse, \
    BadRequestResponse
import json, requests
import bson
import pymongo
from bson import ObjectId
from utilities.utility import GeneratorUtils, DatetimeUtils
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

class WebAppSearch(APIView):
    def get(self, request):
        query = request.query_params
        value = query.get("value")
        data = DB.packages.find({"$or":[{"category":{"$regex":value,"$options":"i"}},{"name":{"$regex":value,"$options":"i"}}]})

        return SuccessResponse(data = data, message="Search")


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

class DateandBookingSlot(APIViewWithAuthentication):
    def get(self, request):
        rsp = DatetimeUtils.get_today_slot()
        all_slot = DatetimeUtils.get_dated_slot()
        all_slot.insert(0, rsp)
        return SuccessResponse(data=all_slot, message="Date and Slot")

class UserAddress(APIViewWithAuthentication):
    def get(self, request):
        user_id = request.GET.get('sub')
        address = DB.user_address.find({'user_id':user_id})
        return SuccessResponse(data=address,message="User Address")
    
    def post(self, request):
        requested_data = request.data
        user_id = request.GET.get('sub')
        requested_data.update({
            "address_id": GeneratorUtils.get_application_id(),
            "user_id": user_id,
            "created_at": DatetimeUtils.get_current_time()
        })
        DB.user_address.insert_one(requested_data)
        return SuccessResponse(data=requested_data,message="Address Added")
    
    def patch(self, request):
        requested_data = request.data
        user_id = request.GET.get('sub')
        user_address_update = DB.user_address.update_one({'address_id':requested_data.get("address_id")},{"$set":requested_data})
        if user_address_update.modified_count:
            return SuccessResponse(data=requested_data,message="Address Updated")
        return BadRequestResponse(message="Address Failed to Update")

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
        user_id = request.GET.get('sub')
        cart = ShopItemsModels.get_cart(user_id)
        
        return SuccessResponse(data=cart, message="Get Cart", data_status=True)

class Checkout(APIViewWithAuthentication):
    def post(self, request):
        request_data = request.data
        user_id = request.GET.get('sub')
        cart = request_data
        customer_details = request_data.get("customer_details")
        address = request_data.get("address")
        
        # if not customer_details:
        #     return BadRequestResponse(message="Customer Details Not Found")
        # if not address:
        #     return BadRequestResponse(message="Address Not Found")
        order_id = GeneratorUtils.get_order_id()
        cart.update({
            "created_by_id": user_id,
            "order_id": order_id,
            "payment_status": "PAID" if cart.get("payment_type","") == "online" else "UNPAID"
        })
        
        for obj in cart.get("items",[]):
            obj.update({
                "user_id": user_id,
                "created_at": DatetimeUtils.get_current_time(),
                "booking_id": GeneratorUtils.get_booking_id(),
                "status": "NEW",
                "order_id": order_id,
                "payment_status": "PAID" if cart.get("payment_type","") == "online" else "UNPAID"
            })
        
        if  cart.get("items",[]):
            cart.pop('_id')
            DB.orders.insert_one(cart)
            DB.bookings.insert_many(cart.get("items",[]))
            DB.shop_cart_items.update_many({'created_by_id':user_id, 'ordered': False},{'$set':{'ordered': True}})
        return SuccessResponse(data={}, message="Order Placed", data_status=True)

class OrderHistory(APIViewWithAuthentication):
    def get(self, request):
        user_id = request.GET.get('sub')
        orders = DB.orders.find({'created_by_id': user_id})
        return SuccessResponse(data= orders,message="Order History")

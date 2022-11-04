from django.db import models
from utilities.utility import DatetimeUtils
from application.settings import DB

class ShopItemsClass:
    _collection_name = "shop_cart_items"
    
    def create_or_update(self, user_id, item_id):
        cart_item = {
            "product_id": item_id,
            "created_by_id": user_id,
            "ordered":False,
            "updated_at": DatetimeUtils.get_current_time(),
            "created_at": DatetimeUtils.get_current_time()
        }
        DB[self._collection_name].insert_one(cart_item)
        return True
    
    def remove_item(self, user_id, item_id):
        DB[self._collection_name].delete_one({'created_by_id':user_id, 'product_id': item_id, 'ordered': False})
        return True

    def get_cart(self, user_id):
        aggr = [
            {
                '$match': {
                    'created_by_id': user_id, 
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
                            'product_id': '$product_id', 
                            'package_name': '$package_details.name', 
                            'discription': '$package_details.discription', 
                            'lab_name': '$package_details.lab_name', 
                            'lab_id': '$package_details.lab_id', 
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
        else:
            cart = {
                "_id": None,
                "mrp_total": 0,
                "offer_price_total": 0,
                "items" : []
            }
        return cart

ShopItemsModels = ShopItemsClass()
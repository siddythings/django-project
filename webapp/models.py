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

ShopItemsModels = ShopItemsClass()
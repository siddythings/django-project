from utilities.utility import DatetimeUtils
class WebAppServicesClass:
    def create_or_update(self, user_id, item_id, shop_cart_items):
        cart_item = {
            "product_id": item_id,
            "quantity": 1,
            "updated_at": DatetimeUtils.get_current_time(),
            "created_at": DatetimeUtils.get_current_time()
        }
        
        return True
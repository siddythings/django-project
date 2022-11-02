import uuid
from application.settings import DB
from utilities.utility import DatetimeUtils
class UserServicesClass:
    def create_new_user(self, mobile, otp):
        user = { 
            "mobile": mobile,
            "otp": otp,
            "is_active": True,
            "name": "",
            "id": uuid.uuid4().hex,
            "updated_at": DatetimeUtils.get_current_time(),
            "careted_at": DatetimeUtils.get_current_time(),
        }
        DB["users"].insert_one(user)
        return user

UserServices = UserServicesClass()
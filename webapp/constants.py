from application.constants import Enum, instantiate

@instantiate
class CartOprationType(Enum):
    ADD = "ADD"
    REMOVE = "REMOVE"

CART_OPRATIONS = {
    "ADD":1,
    "REMOVE":0
}
from application.constants import Enum, instantiate

@instantiate
class TransactionType(Enum):
    Credit = "credit"
    Debit = "debit"
    Due = "due"

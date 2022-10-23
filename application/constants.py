class Enum:
    def __contains__(self, item: str) -> bool:
        if hasattr(self, "_value_set"):
            return item in self._value_set
        self._value_set = set()
        for key in dir(self):
            if (key.endswith("__") and key.startswith("__")) or key == "_value_set":
                pass
            else:
                self._value_set.add(getattr(self, key))
        return item in self._value_set

def instantiate(cls):
    return cls()

@instantiate
class BookingStatus:
    NEW = "NEW"
    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"
    OPEN = "OPEN"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    

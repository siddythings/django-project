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
    SAMPLE_COLLECTED = "SAMPLE COLLECTED"
    OPEN = "OPEN"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    
ALL_SLOTS = [
        "5:00 AM - 6:00 AM", "6:00 AM - 7:00 AM", "7:00 AM - 8:00 AM", "8:00 AM - 9:00 AM",
        "9:00 AM - 10:00 AM", "10:00 AM - 11:00 AM", "11:00 AM - 12:00 PM","12:00 PM - 1:00 PM",
        "1:00 PM - 2:00 PM","2:00 PM - 3:00 PM","3:00 PM - 4:00 PM", "4:00 PM - 5:00 PM", 
        "5:00 PM - 6:00 PM","6:00 PM - 7:00 PM", "7:00 PM - 8:00 PM"
	]

SLOT_HOURS = [
        {
            "time":5,
            "slot":"5:00 AM - 6:00 AM"
        },
        {
            "time":6,
            "slot":"6:00 AM - 7:00 AM"
        },
        {
            "time":7,
            "slot":"7:00 AM - 8:00 AM"
        },
        {
            "time":8,
            "slot":"8:00 AM - 9:00 AM"
        },
        {
            "time": 9,
            "slot": "9:00 AM - 10:00 AM"
        },
        {
            "time": 10,
            "slot": "10:00 AM - 11:00 AM"
        },
        {
            "time": 11,
            "slot": "11:00 AM - 12:00 PM"
        },
        {
            "time": 12,
            "slot": "12:00 PM - 1:00 PM"
        },
        {
            "time": 14,
            "slot": "1:00 PM - 2:00 PM"
        },
        {
            "time": 13,
            "slot": "2:00 PM - 3:00 PM"
        },
        {
            "time": 15,
            "slot": "3:00 PM - 4:00 PM"
        },
        {
            "time": 16,
            "slot": "4:00 PM - 5:00 PM"
        },
        {
            "time": 17,
            "slot": "5:00 PM - 6:00 PM"
        },
        {
            "time": 18,
            "slot": "6:00 PM - 7:00 PM"
        },
        {
            "time": 19,
            "slot": "7:00 PM - 8:00 PM"
        },
	]
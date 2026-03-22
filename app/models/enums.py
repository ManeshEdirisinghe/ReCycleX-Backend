import enum

class Role(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    PICKUP_AGENT = "PICKUP_AGENT"
    RECYCLING_CENTER = "RECYCLING_CENTER"
    REPAIR_CENTER = "REPAIR_CENTER"

class ItemCondition(str, enum.Enum):
    NEW = "NEW"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    BROKEN = "BROKEN"

class ItemStatus(str, enum.Enum):
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    READY_FOR_PICKUP = "READY_FOR_PICKUP"
    PICKED_UP = "PICKED_UP"
    IN_PROCESSING = "IN_PROCESSING"
    COMPLETED = "COMPLETED"

class PickupStatus(str, enum.Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    IN_TRANSIT = "IN_TRANSIT"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class ProcessType(str, enum.Enum):
    RECYCLING = "RECYCLING"
    REPAIR = "REPAIR"
    DONATION = "DONATION"

class FinalStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    SCRAPPED = "SCRAPPED"
    RETURNED = "RETURNED"

class CenterType(str, enum.Enum):
    RECYCLING = "RECYCLING"
    REPAIR = "REPAIR"

from pydantic import BaseModel
from datetime import date
from typing import Dict
from enum import Enum
from decimal import Decimal

class OrderStatus(str, Enum):
    pending = "Pending"
    preparing = "Preparing"
    out_for_delivery = "Out for Delivery"
    completed = "Completed"
    cancelled = "Cancelled"

class WeeklySummary(BaseModel):
    week_start: date
    week_end: date
    total_orders: int
    completed_orders: int
    total_revenue: Decimal = Decimal("0.00")  
    orders_by_status: Dict[OrderStatus, int]
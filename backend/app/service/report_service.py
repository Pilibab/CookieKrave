from datetime import date, timedelta
from app.model.report import WeeklySummary, OrderStatus
from app.repository.orders_repo import OrderRepository
from decimal import Decimal

class ReportService:
    def __init__(self, repo: OrderRepository) -> None:
        self.order_repo = repo

    def get_weekly_summary(self, week_start: date | None = None) -> WeeklySummary:
        # if no date given, default to current week's Monday
        if week_start is None:
            today = date.today()
            week_start = today - timedelta(days=today.weekday())  # Monday
        
        week_end = week_start + timedelta(days=6)  # Sunday

        # query orders between week_start and week_end
        orders = self.order_repo.get_orders_between(week_start, week_end)

        completed_orders = [o for o in orders if o.order_status == "Completed"]
        amt_completed_orders = [Decimal(o.total_amount) for o in completed_orders]
        # compute the summary
        return WeeklySummary(
            week_start=week_start,
            week_end=week_end,
            total_orders=len(orders),
            completed_orders=len(completed_orders),
            total_revenue=sum(amt_completed_orders, Decimal("0.00")),
            orders_by_status={
                status: sum(1 for o in orders if o.order_status == status.value)
                for status in OrderStatus
            }
        )
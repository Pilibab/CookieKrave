from datetime import date
from fastapi import APIRouter, HTTPException, Depends # 👈 1. Import Depends
from typing import Optional
from app.model.report import WeeklySummary 
from app.service.report_service import ReportService
from app.repository.orders_repo import OrderRepository
from app.db.supabase_client import supabase

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

def get_order_repository() -> OrderRepository:
    return OrderRepository(supabase) # Pass database session here if needed

def get_report_service(
    repo: OrderRepository = Depends(get_order_repository)
) -> ReportService:
    return ReportService(repo=repo)

@router.get(
    "/weekly",                          # 👈 Do NOT put query variables in the path string!
    response_model=WeeklySummary,
    summary="Get weekly order and revenue summary"
)
@router.get("/weekly", 
        response_model=WeeklySummary, 
        summary="Get weekly order and revenue summary")
def get_weekly_summary(
    week_start: Optional[str] = None,
    service: ReportService = Depends(get_report_service)
    ) -> WeeklySummary:
    """
    Fetch the weekly dashboard overview metrics.
    If week_start is omitted, defaults to the current week (Monday–Sunday).
    """
    parsed_date: date | None = None

    if week_start is not None:
        try:
            parsed_date = date.fromisoformat(week_start)  # expects "YYYY-MM-DD"
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid date format. Use YYYY-MM-DD (e.g. 2026-05-26)."
            )

    service = get_report_service()
    summary = service.get_weekly_summary(week_start=parsed_date)
    return summary
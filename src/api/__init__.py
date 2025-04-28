from fastapi import APIRouter
from .admin import admin_router
from .emoloyee import employee_router
from .student import student_router
from .news import news_router


main_router = APIRouter()

main_router.include_router(admin_router)
main_router.include_router(employee_router)
main_router.include_router(student_router)
main_router.include_router(news_router)

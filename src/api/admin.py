from fastapi import APIRouter
from src.utils.auth import *
from src.models import Student , Employee


admin_router = APIRouter(
    tags=["Admin"],
    prefix="/admin"
)

student_crud = MainCrud(model=Student)
employee_crud = MainCrud(model=Employee)

@admin_router.get("/get-student/{id}")
async def get_by_id(
    id: 
    int, db:AsyncSession = Depends(get_db)
    ):
    return await student_crud.get(db=db , id=id)

@admin_router.get("/get-all-students")
async def get_all_students(db: AsyncSession = Depends(get_db)):
    return await student_crud.get_all(db=db)



@admin_router.get("/get-employee/{id}")
async def get_by_id(
    id: int, 
    db: AsyncSession = Depends(get_db)
    ):
    return await employee_crud.get(db=db , id=id)

@admin_router.get("/get-all-employee")
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    return await employee_crud.get_all(db=db)
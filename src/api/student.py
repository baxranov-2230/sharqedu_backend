from fastapi import APIRouter
from src.utils.auth import *
from src.models.students import Student
from src.schemas.student import StudentCreate



student_router = APIRouter(
    tags=["Student"],
    prefix="/student"
)

main_crud = MainCrud(model=Student)

@student_router.post("/create-student")
async def create(
    student_items: StudentCreate ,
    db: AsyncSession = Depends(get_db)):

    return await main_crud.create(db=db , obj_in=student_items)

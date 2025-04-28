from fastapi import APIRouter, UploadFile
from src.utils.auth import *
from src.utils.functions import save_file , format_local_number
from src.models.employees import Employee
from src.schemas.employee import EmployeeCreate



employee_router = APIRouter(
    tags=["Employee"],
    prefix="/employee"
)


employee_crud = MainCrud(model=Employee)

@employee_router.post("/create-employee")
async def create_employee(
    resume_file: UploadFile,
    passport_file: UploadFile,
    diplom_file : UploadFile,
    phone_number : str,
    db: AsyncSession = Depends(get_db)):

    diplom_path = await save_file(file=diplom_file)
    passport_path = await save_file(file=passport_file)
    resume_path = await save_file(file=resume_file)
    phone_number = format_local_number(raw_number=phone_number)


    employee_data = EmployeeCreate(
        diplom=diplom_path,
        passport=passport_path,
        resume=resume_path,
        phone_number=phone_number
    )

    return await employee_crud.create(db=db , obj_in=employee_data)
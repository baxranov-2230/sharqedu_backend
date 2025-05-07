from fastapi import APIRouter
from src.utils.auth import *
from src.models import Student , Employee
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.jwt_auth import *


admin_router = APIRouter(
    tags=["Admin"],
    prefix="/admin"
)

student_crud = MainCrud(model=Student)
employee_crud = MainCrud(model=Employee)


@admin_router.post("/login")
async def login(
    form_data : OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
    ):

    user = await authenticate_user(db=db , username=form_data.username , password=form_data.password)


    access_token = await create_access_token(
        {
            "sub" : user.username,
            "role" : user.role
        }
    )

    refresh_token = await create_refresh_token(
        {
            "sub": user.username,
            "role": user.role
        }
    )

    return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@admin_router.post("/refresh")
async def refresh(
    refresh_token: str,
    token: str = Depends(oauth2_scheme)
):
    tokens = await refresh_access_token(refresh_token=token)

    access_token=tokens.get('access_token')
    refresh_token=tokens.get('refresh_token')
    return {
        'access_token': access_token, 
        'refresh_token': refresh_token
        }
    

@admin_router.get("/get_student/{id}")
async def get_by_id(
    id: 
    int, db:AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
    ):
    return await student_crud.get(db=db , id=id)

@admin_router.get("/get_all_students")
async def get_all_students(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
    ):
    return await student_crud.get_all(db=db)



@admin_router.get("/get_employee/{id}")
async def get_by_id(
    id: int, 
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
    ):
    return await employee_crud.get(db=db , id=id)

@admin_router.get("/get_all_employee")
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
    ):
    return await employee_crud.get_all(db=db)
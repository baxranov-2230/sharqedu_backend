from pydantic import BaseModel


class EmployeeBase(BaseModel):
    diplom: str
    passport: str
    resume: str
    phone_number: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    is_read : bool
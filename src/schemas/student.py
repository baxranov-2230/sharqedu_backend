from pydantic import BaseModel


class StudentBase(BaseModel):
    first_name : str
    direction : str
    phone_number: str


class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    is_read: bool
from pydantic import BaseModel


class StudentBase(BaseModel):
    first_name : str
    # last_name : str
    # father_name : str
    direction : str
    phone_number: str


class StudentCreate(StudentBase):
    pass

class StudentResponse(BaseModel):
    id: int
    phone_number: str
    first_name : str
    # last_name : str
    # father_name : str
    direction : str
    is_read: bool
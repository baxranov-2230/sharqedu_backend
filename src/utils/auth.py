from sqlalchemy.ext.asyncio import AsyncSession  
from fastapi import HTTPException , status , Depends
from typing import TypeVar , Generic , Type , List
from sqlalchemy.future import select 
from sqlalchemy import asc
from pydantic import BaseModel
from .functions import format_local_number
from src.core.base import get_db
from sqlalchemy.exc import SQLAlchemyError
from src.models import Student , Employee
import re



ModelType = TypeVar("ModelType" , bound=BaseModel)
SchemaType = TypeVar("SchemaType")

class MainCrud(Generic[ModelType , SchemaType]):
    def __init__(self , model: Type[ModelType]):
        self.model = model


    async def get(self, db: AsyncSession, id: int) -> ModelType:
        db_obj = await db.get(self.model, id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        if not db_obj.is_read:
            db_obj.is_read = True
            await db.commit()
            await db.refresh(db_obj)
        return db_obj
    
    async def get_all(self, db: AsyncSession, limit: int = 10, offset: int = 0)-> List[ModelType]:
        query = select(self.model).order_by(asc(self.model.is_read)).limit(limit).offset(offset)
        result = await db.execute(query)
        db_obj = result.scalars().all()

        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No records found"
            )
        return db_obj
    
    async def get_by_phone_number(self, db: AsyncSession, phone_number: str) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.phone_number == phone_number))
        student = result.scalars().first()
        if student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A registration request with phone number {phone_number} already exists."
            )
        return student
        

    async def create(self, db: AsyncSession, obj_in: SchemaType) -> ModelType:
        try:
            obj_data = obj_in.model_dump()
            if "phone_number" in obj_data and obj_data["phone_number"]:
                # Validate phone number format (e.g., digits only)
                if not re.match(r"^\d+$", obj_data["phone_number"]):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid phone number format"
                    )
                obj_data["phone_number"] = format_local_number(obj_data["phone_number"])
                await self.get_by_phone_number(db=db, phone_number=obj_data["phone_number"])
            
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except HTTPException as e:
            raise e  
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            )
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error occurred"
            )

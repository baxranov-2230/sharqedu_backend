from sqlalchemy.ext.asyncio import AsyncSession 
from pydantic import BaseModel
from sqlalchemy import select
from src.models import BlogImage , Blog
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from typing import TypeVar
from fastapi import HTTPException , status
from src.schemas.news import NewCreate
from uuid import uuid4


ModelType = TypeVar("ModelType" , bound=BaseModel)
SchemaType = TypeVar("SchemaType")

class BlogCrud():
    def __init__(self, model):
        self.model = model
    

    async def get(self , db: AsyncSession , blog_id: int ):
        stmt = select(Blog).options(joinedload(Blog.images)).where(Blog.id == blog_id)
        result = await db.execute(stmt)
        blog = result.scalars().first()

        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Blog not found"
            )
        
        return {
            "id": blog.id,
            "title": blog.title,
            "body": blog.body,
            "date": blog.date,
            "images": [{
                "id": img.id,
                "images_path": img.image_path
                } for img in blog.images]        
            }
        

    async def get_all(self, db: AsyncSession, limit: int = 10, offset: int = 0):
        try:
            stmt = select(Blog).options(joinedload(Blog.images)).limit(limit).offset(offset)
            result = await db.execute(stmt)
            blogs = result.unique().scalars().all()

            return [
                {
                    "id": blog.id,
                    "title": blog.title,
                    "body": blog.body,
                    "date": blog.date,
                    "images": [{"images_path": img.image_path} for img in blog.images]
                }
                for blog in blogs
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 
    
    async def create(self, db: AsyncSession, db_obj: NewCreate) -> Blog:
            try:
                new_blog = Blog(**db_obj.model_dump())
                db.add(new_blog)
                await db.flush()  
                return new_blog
            except Exception as e:
                await db.rollback()
                raise Exception(f"Failed to create blog: {str(e)}")


    async def update(self , db: AsyncSession , blog_id: int ,db_obj: SchemaType):

        pass
    
    async def delete( self ,db: AsyncSession, blog_id: int):
        try:
            stmt = select(Blog).where(Blog.id == blog_id)
            result = await db.execute(stmt)
            blog = result.scalars().first()

            if not blog:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Blog not found"
                )

            stmt_images = select(BlogImage).where(BlogImage.blog_id == blog_id)
            result = await db.execute(stmt_images)
            blog_images = result.scalars().all()


            for image in blog_images:
                await db.delete(image)


            await db.delete(blog)
            await db.commit()

            return {"message": "Blog and associated images deleted successfully"}

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except HTTPException:
            raise 
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
        
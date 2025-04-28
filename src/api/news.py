from fastapi import APIRouter , UploadFile , File , Depends , Form
from src.core.base import get_db
from src.utils.blog_crud import *
from src.schemas.news import NewCreate
from datetime import date
from src.utils.functions import save_file



from typing import List


news_router = APIRouter(
    tags=["New Apis"],
    prefix="/news"
)

blog_crud = BlogCrud(model=Blog)
@news_router.post("/create")
async def create(
    title: str = Form(...),
    body: str = Form(...),
    date: date = Form(...),
    images: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        new_items = NewCreate(title=title, body=body, date=date)
        blog_data = await blog_crud.create(db=db, db_obj=new_items)
        blog_id = blog_data.id

        saved_images = []
        for image in images:
            image_path = await save_file(file=image)
            new_image = BlogImage(blog_id=blog_id, image_path=image_path)
            db.add(new_image)
            await db.flush()
            saved_images.append(new_image)
        await db.commit()

        blogs_data = await blog_crud.get(db=db , blog_id=blog_id)
        
        return blog_data
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create blog: {str(e)}")






@news_router.get("get-by-id/{new_id}")
async def get_by_id(
    blog_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await blog_crud.get(db=db , blog_id=blog_id)

@news_router.get("/get-all")
async def get_all(
    db:AsyncSession = Depends(get_db)
):
    return await blog_crud.get_all(db=db)

@news_router.put("/update/{new_id}")
async def update_news(
    blog_id: int,
    title: str = Form(None),
    body: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    pass

@news_router.delete("/delete/{new_id}")
async def delete(
    blog_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await blog_crud.delete(db=db , blog_id=blog_id)

@news_router.delete("/{blog_id}/images/{image_id}")
async def get_by_id(
    blog_id: int,
    image_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Blog).options(joinedload(Blog.images)).where(Blog.id == blog_id)
    result = await db.execute(stmt)
    blog = result.unique().scalar_one_or_none()

    if blog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )


    image = next((img for img in blog.images if img.id == image_id), None)
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found in this blog"
        )


    await db.delete(image)
    await db.commit()


    return {"message": "Delete succesfully"}
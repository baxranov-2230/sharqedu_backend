from sqlalchemy import Column , String , Integer , Date , ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from src.core.base import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String , nullable=False)
    body = Column(String ,nullable=False)
    date = Column(Date , default=date.today)

    images = relationship("BlogImage", back_populates="blog", cascade="all, delete-orphan")

class BlogImage(Base):
    __tablename__ = "blog_images"

    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    image_path = Column(String, nullable=False)

    blog = relationship("Blog", back_populates="images")
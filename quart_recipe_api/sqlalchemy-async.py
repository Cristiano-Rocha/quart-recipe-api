from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, Float, String, Boolean, JSON
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update


DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_ession = sessionmaker(engine,expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# Data Model
class Recipe(Base):
    __tablename__ = "recipe"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String) 
    author = Column(String)
    image = Column(String)
    description = Column(String)
    recipeCategory = Column(String)
    channel = Column(String)
    ratingValue Column(Float)
    worstRating = Column(Integer)
    favesCount = Column(Integer)
    commentsCount = Column(Integer)


    def json(self):
        return { "id": self.id
                , "name": self.name
                , "author": self.author
                , "image": self.image
                , "description": self.description
                , "recipeCategory": self.recipeCategory
                , "channel": self.channel
                , "ratingValue": self.ratingValue
                , "worstRating": self.worstRating
                , "favesCount": self.favesCount
                , "commentsCount": self.commentsCount
                }

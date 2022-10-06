from contextlib import asynccontextmanager
from quart import Quart
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, Float, String, Boolean, JSON
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update


DATABASE_URL = "sqlite+aiosqlite:///./recipes.db"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine,expire_on_commit=False, class_=AsyncSession)
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
    ratingValue = Column(Float)
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


class RecipeDAL:
    def __init__(self, db_session):
        self.db_session = db_session


    async def create_recipe(self, name, author, image, description, recipeCategory, channel, ratingValue, worstRating, favesCount, commentsCount ):
        new_recipe = Recipe(
                name=name,
                author=author,
                image=image,
                description=description,
                recipeCategory=recipeCategory,
                channel=channel,
                ratingValue=ratingValue,
                worstRating=worstRating,
                favesCount=favesCount,
                commentsCount=commentsCount
                )
        self.db_session.add(new_recipe)
        await self.db_session.flush()
        return new_recipe.json()


    async def get_all_recipe(self):
        query_result = await self.db_session.execute(select(Recipe).order_by(Recipe.id))
        return [recipe.json() for recipe in query_result.scalars().all() ]

    async def get_recipe(self, recipe_id):
        query = select(Recipe).where(Recipe.id == recipe_id)
        query_result = await self.db_session.execute(query)
        recipe = query_result.one()
        return recipe[0].json() 

app = Quart(__name__)

@app.before_serving
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # This resets the database
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with recipe_dal() as rd:
            await rd.create_recipe(
                    "Arroz Doce",
                    "Cristiano Rocha",
                    "image",
                    "com arroz japones",
                    "Doces",
                    "Comida",
                    "4.0",
                    "1",
                    "20",
                    "3"
                    )



@asynccontextmanager
async def recipe_dal():
    async with async_session() as session:
        async with session.begin():
            yield RecipeDAL(session)


@app.get("/recipes/<int:recipe_id>")
async def get_recipe(recipe_id):
    async with recipe_dal() as rd:
        return await rd.get_recipe(recipe_id)


@app.get("/recipes")
async def get_all_recipe():
    async with recipe_dal() as rd:
        return await rd.get_all_recipe()

if __name__ == "__main__":
    app.run()

from typing import Annotated, List, Type

from fastapi import APIRouter, Depends, HTTPException
from schemas import RecipeCreate, RecipeDetail, RecipeOut
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Recipe

router = APIRouter(
    prefix="/api/recipes",
    tags=["recipes"],
    responses={404: {"description": "Not found"}},
)

session_dependency = Annotated[AsyncSession, Depends(get_session)]


@router.get("/", response_model=List[RecipeOut], summary="Get all recipes(short form)")
async def get_recipes(session: session_dependency):
    result = await session.execute(
        select(Recipe).order_by(Recipe.views.desc(), Recipe.cooking_time)
    )
    return result.scalars().all()


@router.get("/{recipe_id}", response_model=RecipeDetail, summary="Get recipe details")
async def get_recipe(recipe_id: int, session: session_dependency):
    recipe: Type[Recipe] | None = await session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.views += 1
    await session.commit()
    return RecipeDetail(
        id=recipe.id,
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        views=recipe.views,
        ingredients=recipe.ingredients.split("|"),
        description=recipe.description,
    )


@router.post(
    "/", response_model=RecipeOut, status_code=201, summary="Create new recipe"
)
async def create_recipes(recipe: RecipeCreate, session: session_dependency):
    new_recipe = Recipe(
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients="|".join(recipe.ingredients),
        description=recipe.description,
    )
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe

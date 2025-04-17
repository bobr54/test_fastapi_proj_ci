from typing import List
from pydantic import BaseModel, Field, field_validator, conlist


class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    cooking_time: int = Field(..., gt=0, description="Cooking time should be greater than 0")
    ingredients: conlist(str, min_length=1)
    description: str

    @field_validator("ingredients")
    def  check_ingredients(cls, v):
        if any(not ing.strip() for ing in v):
            raise ValueError("The ingredients cannot be empty strings")
        return v

class RecipeOut(BaseModel):
    id: int
    title: str
    cooking_time: int
    views: int

    model_config = {
        "from_attributes": True
    }

class RecipeDetail(RecipeOut):
    ingredients: List[str]
    description: str
from pydantic import BaseModel, Field

from pymacro.db.collections import IngredientsCollection

ingredients_collection = IngredientsCollection()


class Ingredient(BaseModel):
    name: str = Field(None, max_length=255, description="Name of the food item")
    category: str = Field(None, max_length=255, description="Category of the food item")
    calories: float = Field(None, description="Calories in the food item")
    protein: float = Field(None, description="Protein in the food item")
    fat: float = Field(None, description="Fat in the food item")
    carbs: float = Field(None, description="Carbohydrates in the food item")

    @classmethod
    def from_db(cls, name: str):
        doc = ingredients_collection.find_one({"name": name})
        if not doc:
            raise ValueError(f"Ingredient with name '{name}' not found")
        return cls(**doc)

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

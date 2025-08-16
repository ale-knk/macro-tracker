from pydantic import BaseModel, Field

from pymacro.ingredient import Ingredient


class Dish(BaseModel):
    name: str = Field(None, max_length=255, description="Name of the dish")
    ingredients_kv: dict[Ingredient, float] = Field(
        ..., description="Dictionary of ingredients and their quantities"
    )

    @property
    def total_grams(self):
        return sum([quant for quant in self.ingredients_kv.values()])

    @classmethod
    def from_db(cls, name, ing_names: list[str], quantities: list[float]):
        ingredients_kv = {
            Ingredient.from_db(name=name): quant
            for name, quant in zip(ing_names, quantities)
        }
        return cls(name=name, ingredients_kv=ingredients_kv)

    @property
    def calories(self):
        calories = 0
        for ing, quant in self.ingredients_kv.items():
            calories += (ing.calories * quant) / 100
        return calories

    @property
    def protein(self):
        protein = 0
        for ing, quant in self.ingredients_kv.items():
            protein += (ing.protein * quant) / 100
        return protein

    @property
    def fat(self):
        fat = 0
        for ing, quant in self.ingredients_kv.items():
            fat += (ing.fat * quant) / 100
        return fat

    @property
    def carbs(self):
        carbs = 0
        for ing, quant in self.ingredients_kv.items():
            carbs += (ing.carbs * quant) / 100
        return carbs

    def get_macros(self, include_calories=True):
        macros = {"protein": self.protein, "fat": self.fat, "carbs": self.carbs}
        if include_calories:
            macros["calories"] = self.calories
        return macros

    def extract_portion(self, quantity):
        if quantity > self.total_grams:
            raise ValueError(
                "The requested quantity exceeds the total of the original Dish."
            )

        factor = quantity / self.total_grams
        portion_ingredients = {
            ing: quant * factor for ing, quant in self.ingredients_kv.items()
        }

        return Dish(name=self.name, ingredients_kv=portion_ingredients)

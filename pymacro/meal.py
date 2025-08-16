import matplotlib.pyplot as plt
from pydantic import BaseModel, Field

from pymacro.dish import Dish


class Meal(BaseModel):
    name: str = Field(None, description="Name of the meal")
    dishes: list[Dish] = Field(None, description="List of dishes.")

    def add_dish(self, dish: Dish):
        self.dishes.append(dish)

    def remove_dish_by_name(self, name):
        for i, dish in enumerate(self.dishes):
            if dish.name == name:
                self.dishes.pop(i)
                return

    @property
    def calories(self):
        return round(sum(dish.calories for dish in self.dishes),2)

    @property
    def protein(self):
        return round(sum(dish.protein for dish in self.dishes),2)

    @property
    def fat(self):
        return round(sum(dish.fat for dish in self.dishes),2)

    @property
    def carbs(self):
        return round(sum(dish.carbs for dish in self.dishes),2)

    def get_macros(self, return_calories=True):
        macros = {"protein": self.protein, "fat": self.fat, "carbs": self.carbs}
        if return_calories:
            macros["calories"] = self.calories
        return macros

    def plot_macros(self, ax=None, show=False):
        macros = self.get_macros(return_calories=False)
        labels = list(macros.keys())
        sizes = list(macros.values())

        if ax is None:
            fig, ax = plt.subplots()

        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title(f"{self.name}: {self.protein}g protein | {self.calories} kcal")
        ax.legend(labels, title="Macronutrients", loc="upper right")

        if show:
            plt.show()

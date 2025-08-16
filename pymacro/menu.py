import matplotlib.pyplot as plt
from pydantic import BaseModel, Field

from pymacro.meal import Meal


class Menu(BaseModel):
    name: str = Field(None, description="Name of the menu")
    meals: list[Meal] = Field(None, description="List of meals in the menu")

    @property
    def calories(self):
        return sum([meal.calories for meal in self.meals])

    @property
    def protein(self):
        return sum([meal.protein for meal in self.meals])

    @property
    def fat(self):
        return sum([meal.fat for meal in self.meals])

    @property
    def carbs(self):
        return sum([meal.carbs for meal in self.meals])

    def get_macros(self, return_calories=True):
        macros = {"protein": self.protein, "fat": self.fat, "carbs": self.carbs}
        if return_calories:
            macros["calories"] = self.calories
        return macros

    def plot_macros(self, collapse_meals=False):
        if collapse_meals:
            macros = self.get_macros(return_calories=False)
            labels = list(macros.keys())
            sizes = list(macros.values())

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            plt.title(f"{self.name}: {self.protein}g protein | {self.calories} kcal")
            plt.legend(labels, title="Macronutrients", loc="upper right")
            plt.show()

        else:
            num_meals = len(self.meals)
            fig, axes = plt.subplots(1, num_meals, figsize=(5 * num_meals, 5))
            fig.suptitle(f"{self.name}: {self.protein}g protein | {self.calories} kcal")

            if num_meals == 1:
                axes = [axes]

            for ax, meal in zip(axes, self.meals):
                meal.plot_macros(ax=ax)

            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.show()

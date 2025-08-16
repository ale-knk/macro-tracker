import json

from pymacro.db.collections import IngredientsCollection

if __name__ == "__main__":
    PATH = "./data/food_items.json"
    with open(PATH, "r") as f:
        food_items = json.load(f)

    collection = IngredientsCollection()
    collection.insert_many(food_items)

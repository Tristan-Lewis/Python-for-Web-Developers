# ---Imports---
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import Integer, String

# ---Creating engine object---
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# ---Assigning Base---
Base = declarative_base()

# ---Created Session---
Session = sessionmaker(bind=engine)
session = Session()


# ---Creating Base---
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return (
            "<Recipe ID/Name: "
            + str(self.id)
            + "-"
            + self.name
            + "Diff: "
            + self.difficulty
            + ">"
        )

    def __str__(self):
        list_ingredients = self.ingredients.split(", ")
        output = (
            f"\n"
            + f"\nRecipe name: {self.name}"
            + f"\nCooking Time: {self.cooking_time} minutes"
            + f"\nDifficulty: {self.difficulty}"
            + "\nIngredients: \n"
        )
        for ingredient in list_ingredients:
            output += f"\t- {ingredient}\n"
        output
        return output

    def calculate_difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = "Easy"
        if self.cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = "Medium"
        if self.cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = "Intermediate"
        if self.cooking_time >= 10 and len(ingredients) >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if len(self.ingredients == 0):
            return []
        else:
            return self.ingredients.split(", ")


Base.metadata.create_all(engine)


# ---Create recipe function---
def create_recipe():
    try:
        name = str(input("\nEnter recipe name 👉 ")).title()
        while len(name) > 50:
            print("\n\t*Error: Name must be 50 characters or less*")
            name = str(input("\nEnter recipe name  👉 "))
        cooking_time = input("\nEnter cooking time (in minutes) 👉 ")
        while not cooking_time.isnumeric():
            print("\n\t*Error: Cooking must be a numeric value")
            cooking_time = input("\nEnter cooking time (in mintues) 👉 ")
        cooking_time = int(cooking_time)
        ingredients = []
        num = input("\nEnter the number of ingredients in the recipe 👉 ")
        while not num.isnumeric():
            print("\n\t*Error: number of ingredients must be a numeric value")
            num = input("\nEnter the number of ingredients in the recipe 👉 ")
        num = int(num)
        for ingredient in range(num):
            ingredient = str(input("\nEnter ingredient 👉 ")).capitalize()
            while not any(c for c in ingredient if c.isalpha() or c.isspace()):
                print(
                    "\n\t*Error: Ingredients can only contain alphabetic characters or spaces"
                )
                ingredient = str(input("\nEnter ingredient 👉 ")).capitalize()
            ingredients.append(ingredient)
        ingredients = ", ".join(ingredients)
        recipe_entry = Recipe(
            name=name, cooking_time=cooking_time, ingredients=ingredients
        )

        recipe_entry.calculate_difficulty()
        session.add(recipe_entry)
        session.commit()
        print("\n\tRecipe added! 👍\n")
        main_menu()

    except Exception as e:
        print("\nThere was an error creating the recipe...")
        print(e)
        print()
        main_menu()


# ---View all recipes function---
def view_all_recipes():
    recipes_list = session.query(Recipe).all()
    if len(recipes_list) == 0:
        print("\n\tLooks like there are no recipes on the list...")
        main_menu()
    else:
        print()
        print("All recipes:")
        for recipe in recipes_list:
            print(recipe)
        main_menu()


# ---Search ingredients function---
def search_by_ingredients():
    all_ingredients = []
    recipe_count = session.query(Recipe).count()

    if recipe_count == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print()
        main_menu()
    results = session.query(Recipe.ingredients).all()

    for result in results:
        temp_list = result[0].split(", ")
        for item in temp_list:
            if item not in all_ingredients:
                all_ingredients.append(item)

    lst = enumerate(all_ingredients, 1)
    numbered_lst = list(lst)
    print("\nAll Ingredients in database: ")

    for ingredient in numbered_lst:
        print(f"\n\t{ingredient[0]} {ingredient[1]}")
    options = []

    for item in numbered_lst:
        num = item[0]
        options.append(num)
    selected = input(
        "\nEnter number assigned to each ingredient you want to search (seperated by spaces) 👉 "
    ).split()
    search_ingredients = []

    for i in selected:
        if not i.isnumeric() or int(i) not in options:
            print("\n\tError: Only numeric values that match an ingredient accepted.")
            print("\n\tPlease try again.")
            return None
        else:
            i = int(i)
            ingredient = numbered_lst[i - 1][1]
            search_ingredients.append(ingredient)

    condition_list = []

    for ingredient in search_ingredients:
        like_term = str(f"%{ingredient}%")
        condition_list.append(Recipe.ingredients.like(like_term))

    matching_recipes = session.query(Recipe).filter(*condition_list).all()

    if len(matching_recipes) == 0:
        print("\n\tNo recipes matched your search.")
        main_menu()
    else:
        print("\nMatching Recipes: ")
        print()
        for recipe in matching_recipes:
            print(recipe)
        print()
        main_menu()


# ---Edit recipe function---
def edit_recipe():
    recipe_count = session.query(Recipe).count()

    if recipe_count == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print()
        main_menu()

    results = session.query(Recipe.id, Recipe.name).all()
    options = []
    print("\nAll Recipes in database:")

    for result in results:
        print(f"\n\tID: {result[0]} - {result[1]}")
        options.append(result[0])

    choosen = input("\nEnter the ID of the recipe you'd like to edit 👉 ")

    while not choosen.isnumeric():
        print("\n\t*Error: ID must be a numeric value")
        choosen = input("\nEnter the ID of the recipe you'd like to edit 👉 ")
    choosen = int(choosen)

    if choosen not in options:
        print("\n\tOh no, looks like there was no recipe that matched this ID. :(")
        print("\n\tYou'll have to try again.")
        main_menu()

    recipe_to_edit = session.query(Recipe).filter(Recipe.id == choosen).one()
    print("\nRecipe that will be edited: ")
    print(f"\n\t1.  Name: {recipe_to_edit.name}")
    print(f"\n\t2.  Cooking Time: {recipe_to_edit.cooking_time}")
    print(f"\n\t3.  Ingredients: {recipe_to_edit.ingredients}")
    edit_options = [1, 2, 3]
    row_to_edit = input(
        "\nEnter the number matching the recipe attribute you'd like to edit 👉 "
    )

    while not row_to_edit.isnumeric():
        print("\n\t*Error: Choice must be a numeric value")
        row_to_edit = input(
            "\nEnter the number matching the recipe attribute you'd like to edit 👉 "
        )

    row_to_edit = int(row_to_edit)

    if row_to_edit not in edit_options:
        print("\n\tOh no, looks like there was no attribute that matched your choice.")
        print("\n\tYou'll have to try again.")
        main_menu()

    if row_to_edit == 1:
        print()
        print(f"\nUpdating name of {recipe_to_edit.name}")
        print()
        new_name = str(input("\nEnter the new name 👉 ")).title()

        while len(new_name) > 50:
            print("\n\t*Error: Name must be 50 characters or less*")
            new_name = str(input("\nEnter the new name 👉 "))

        try:
            session.query(Recipe).filter(Recipe.id == choosen).update(
                {Recipe.name: new_name}
            )
            session.commit()
            print()
            print("\n\tRecipe updated successfully! 👍")
            print()
            main_menu()
        except Exception as e:
            print("\nThere was an error updating the recipe...")
            print(e)
            print()
            main_menu()

    elif row_to_edit == 2:
        print()
        print(f"\nUpdating the cooking time of {recipe_to_edit.name}")
        print()
        new_time = input("\nEnter cooking time (in minutes) 👉 ")

        while not new_time.isnumeric():
            print("\n\t*Error: Cooking must be a numeric value")
            new_time = input("\nEnter cooking time (in mintues) 👉 ")

        new_time = int(new_time)

        try:
            recipe_update = Recipe(
                name=recipe_to_edit.name,
                cooking_time=new_time,
                ingredients=recipe_to_edit.ingredients,
            )
            recipe_update.calculate_difficulty()
            session.query(Recipe).filter(Recipe.id == choosen).update(
                {
                    Recipe.cooking_time: new_time,
                    Recipe.difficulty: recipe_update.difficulty,
                }
            )
            session.commit()
            print("\n\tRecipe updated successfully! 👍\n")
            main_menu()
        except Exception as e:
            print("\nThere was an error updating the recipe...")
            print(e)
            print()
            main_menu()
    else:
        print(f"\nUpdating the ingredients of {recipe_to_edit.name}")
        print(
            "\n\t***Note: All current ingredients will be replaced by the new entry***"
        )
        new_ingredients = []
        num = input("\nEnter the number of ingredients in the recipe 👉 ")

        while not num.isnumeric():
            print("\n\t*Error: number of ingredients must be a numeric value")
            num = input("\nEnter the number of ingredients in the recipe 👉 ")

        num = int(num)

        try:
            for ingredient in range(num):
                ingredient = str(input("\nEnter ingredient: ")).capitalize()

                while not any(c for c in ingredient if c.isalpha() or c.isspace()):
                    print(
                        "\n\t*Error: Ingredients can only contain alphabetic characters or spaces"
                    )
                    ingredient = str(input("\nEnter ingredient: ")).capitalize()

                new_ingredients.append(ingredient)
            new_ingredients = ", ".join(new_ingredients)
            recipe_update = Recipe(
                name=recipe_to_edit.name,
                cooking_time=recipe_to_edit.cooking_time,
                ingredients=new_ingredients,
            )
            recipe_update.calculate_difficulty()
            session.query(Recipe).filter(Recipe.id == choosen).update(
                {
                    Recipe.ingredients: new_ingredients,
                    Recipe.difficulty: recipe_update.difficulty,
                }
            )
            session.commit()
            print("\n\tRecipe updated successfully! 👍\n")
            main_menu()
        except Exception as e:
            print("\nThere was an error updating the recipe...")
            print(e)
            print()
            main_menu()


# ---Delete recipe function---
def delete_recipe():
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("\n\tLooks like there are no recipes on the list...")
        print()
        main_menu()
    results = session.query(Recipe.id, Recipe.name).all()
    options = []
    print("\nAll Recipes in database:")
    for result in results:
        print(f"\n\tID: {result[0]} - {result[1]}")
        options.append(result[0])
    choosen = input("\nEnter the ID of the recipe you'd like to delete 👉 ")
    while not choosen.isnumeric():
        print("\n\t*Error: ID must be a numeric value")
        choosen = input("\nEnter the ID of the recipe you'd like to edit 👉 ")
    choosen = int(choosen)
    if choosen not in options:
        print("\n\tOh no, looks like there was no recipe that matched this ID.")
        print("\n\tYou'll have to try again.")
        main_menu()
    to_delete = session.query(Recipe).filter(Recipe.id == choosen).one()
    print("\nAre you sure you'd like to delete the following recipe: ")
    print()
    print(to_delete)
    print("\n")
    confirmation = str(input("\nEnter 'yes' to delete or 'no' to cancel 👉 ")).lower()
    while (not confirmation == "yes") and (not confirmation == "no"):
        print("\n\t*Error - only 'yes' or 'no' are acceptable entries*")
        confirmation = str(
            input("\nEnter 'yes' to delete or 'no' to cancel 👉 ")
        ).lower()
    if confirmation == "no":
        print("\n\tClose call...")
        print("\n\t...but nothing was deleted. Phew!")
        main_menu()
    else:
        try:
            session.delete(to_delete)
            session.commit()
            print("\n\tRecipe has been successfully deleted! 👍\n")
            main_menu()
        except Exception as e:
            print("\nThere was an error deleting the recipe...")
            print(e)
            print()
            main_menu()


# ---Main Menu function---
def main_menu():
    choice = ""
    print("\n   ⭐  MAIN MENU ⭐")
    print("\nWhat would you like to do? ")
    print("\n\t1 ⬌  Create a Recipe")
    print("\n\t2 ⬌  View all Recipes")
    print("\n\t3 ⬌  Search for a Recipe")
    print("\n\t4 ⬌  Edit a Recipe")
    print("\n\t5 ⬌  Delete a Recipe")
    print("\nEnter 'quit' to close the application")

    choice = str(input("\nPlease enter the associated number here 👉 "))
    while choice != "quit":
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        else:
            print("\n\tPlease enter a valid command and try again.\n")
            main_menu()
    print("\n\tSee ya!")
    session.close()
    engine.dispose()
    exit()


main_menu()

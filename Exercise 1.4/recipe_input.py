#---Part 1 step 1---👍
import pickle

recipes_list = [];

ingredients_list=[];

all_ingredients = [];


#---Part 1 step 3---👍
def calc_difficulty(recipe):
        if recipe['cooking_time'] < 10 and len(ingredients_list) < 4:
            recipe['difficulty'] = 'Easy'
        if recipe['cooking_time'] < 10 and len(ingredients_list) >= 4:
            recipe['difficulty'] = 'Medium'
        if recipe['cooking_time'] >= 10 and len(ingredients_list) < 4:
            recipe['difficulty'] = 'Intermediate'
        if recipe['cooking_time'] >= 10 and len(ingredients_list) >= 4:
            recipe['difficulty'] = 'Hard'

#---Part 1 step 2---👍
def take_recipe(iteration):

    name = str(input("\nWhat is the name of recipe " + str(iteration + 1) + "?\n"))

    cooking_time = int(input("\nHow long will the recipe take in minutes?\n"))

    number_of_ingredients = int(input("\nHow many ingredients will there be?\n"))

    for number in range(number_of_ingredients):
        ingredient = (input("\nWhat is ingredient " + str(number + 1) + "?\n"))
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients_list}

    calc_difficulty(recipe)

    recipes_list.append(recipe)

    print("\nYour recipe has been added!")
    for recipe in recipes_list:
        print("\nRecipe: " + recipe['name'])
        print("Cooking Time: " + str(recipe['cooking_time']))
        print("Difficulty level: " + recipe['difficulty'])
        print("Ingredients: ")
        for i in recipe['ingredients']:
            print(i)
        print("\n")
    print("Recipe List: " + str(recipes_list))
    print("\n")
    print("All Ingredients: " + str(all_ingredients))
    print("\n")

#-------END OF FUNCTIONS------👍

#---Part 1 step 5---👍
n = int(input("\nHow many recipes would you like to add?\n"))

for number in range(n):
    take_recipe(number)

#---Part 1 step 6---👍
data = {'recipes': recipes_list, 'ingredients': all_ingredients}

filename = input("Enter the filename where you want your recipes: ")

#---Part 1 step 7---👍
updated_file = open(filename, "wb")

pickle.dump(data, updated_file)

updated_file.close()
print("Recipe file has been updated.")
   
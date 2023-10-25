# step 1 + 2
recipes_list = [];

ingredients_list=[];

# step 3
def take_recipe(iteration):
    name = str(input("What is the name of recipe " + str(iteration + 1) + "?\n"))

    cooking_time = int(input("How long will the recipe take in minutes?\n"))

    number_of_ingredients = int(input("How many ingredients will there be?\n"))

    ingredients_list=[]

    for number in range(number_of_ingredients):
# step 5
        ingredient = (input(" What is ingredient " + str(number + 1) + "?\n"))
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)

    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients_list}

    recipes_list.append(recipe)

    for recipe in recipes_list:
        if cooking_time < 10 and len(ingredients_list) < 4:
            recipe['difficulty']='Easy'
        if cooking_time < 10 and len(ingredients_list) >= 4:
            recipe['difficulty']='Medium'
        if cooking_time >= 10 and len(ingredients_list) < 4:
            recipe['difficulty']='Intermediate'
        if cooking_time >= 10 and len(ingredients_list) >= 4:
            recipe['difficulty']='Hard'

    print("Your recipe has been added!")
    # end of function

# step 4
n = int(input("How many recipes would you like to add?\n"))

for number in range(n):
    take_recipe(number)
# Step 6
for recipe in recipes_list:
    print("Recipe: " + recipe["name\n"] + "Cooking Time (min): " + recipe["cooking_time\n"] + "Ingredients:\n" + recipe["ingredients_list"][0] + recipe["ingredients_list"][1] + "Difficulty Level: " + recipe["difficulty"])
# Step 7    
ingredients_list.sort()

for ingredients in ingredients_list:
    print(ingredients)
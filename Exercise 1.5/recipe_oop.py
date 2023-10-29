#---Step 1---🍝
class Recipe(object):

    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficulty = ''

    def calc_difficulty(self, cooking_time, ingredients):
        if (cooking_time < 10) and (len(ingredients) < 4):
            difficulty_level = 'Easy'
        elif (cooking_time < 10) and (len(ingredients) >= 4):
            difficulty_level = 'Medium'
        elif (cooking_time >= 10) and (len(ingredients) < 4):
            difficulty_level = 'Intermediate'
        elif (cooking_time >= 10) and (len(ingredients) >= 4):
            difficulty_level = 'Hard'
        else:
            print('Something bad happened, please try again')
        return difficulty_level
    
    #---Step 2---🍝
    def get_name(self):
        output = 'Recipe name: ' + str(self.name)
        return output

    def set_name(self, name):
        self.name = str(name)

    def get_cooking_time(self):
        output = 'Cooking time: ' + str(self.cooking_time)
        return output

    def set_cooking_time(self, cooking_time):
        self.cooking_time = int(cooking_time)

    def add_ingredients(self, *args):
        self.ingredients = args
        self.update_all_ingredients()

    def get_ingredients(self):
        print('\nIngredients: \n')
        for ingredient in self.ingredients:
            print(' ' + str(ingredient))
        print('\n')

    def get_difficulty(self):
        difficulty = self.calc_difficulty(self.cooking_time, self.ingredients)
        output = 'Difficulty: ' + str(self.cooking_time)
        self.difficulty = difficulty
        return output

    def search_ingredient(self, ingredient, ingredients):
        if (ingredient in ingredients):
            return True
        else:
            return False

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)

    def __str__(self):
        output = '\nName: ' + str(self.name) + \
            '\nCooking time: ' + str(self.cooking_time) + ' minutes' + \
            '\nDifficulty: ' + str(self.difficulty) + \
            '\nIngredients:' + \
            '\n'
        for ingredient in self.ingredients:
            output += ' ' + ingredient + '\n'
        return output
    
    #---Step 3---🍝
    def recipe_search(self, recipes_list, ingredient):
        data = recipes_list
        search_term = ingredient
        for recipe in data:
            if self.search_ingredient(search_term, recipe.ingredients):
                print(recipe)

    def view_recipe(self):
        print('\nName: ' + str(self.name))
        print('Cooking time: ' + str(self.cooking_time)  + ' minutes')
        self.get_ingredients()
#---END OF CLASS---🍝

#---Step 6---
recipes_list = []

#---Step 4---🍝
tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)
tea.get_difficulty()
recipes_list.append(tea)

#---Step 5---🍝
coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time(5)
coffee.get_difficulty()
recipes_list.append(coffee)

cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs',
                     'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)
cake.get_difficulty()
recipes_list.append(cake)

banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients(
    'Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()
recipes_list.append(banana_smoothie)

print('\nRecipes list: ')
for recipe in recipes_list:
    print(recipe)

#---Step 7---🍝
print('Recipes that contain Water: ')
tea.recipe_search(recipes_list, 'Water')

print('Recipes that contain Sugar: ')
tea.recipe_search(recipes_list, 'Sugar')

print('Recipes that contain Bananas: ')
tea.recipe_search(recipes_list, 'Bananas')
#---Part 2 step 1---👍
import pickle

#---Part 2 step 2---👍
def display_recipe(recipe):
    print("")
    print("Recipe: ", recipe["name"])
    print("Cooking Time (mins): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ele in recipe["ingredients"]:
        print("- ", ele)
    print("Difficulty: ", recipe["difficulty"])
    print("")

#---Part 2 step 3---👍
def search_ingredients(data):
    lst = enumerate(data["ingredients"])
    numbered_lst = list(lst)
    print("Ingredients List: ")
    for ele in numbered_lst:
        print(ele[0], ele[1])
    try:
        num = int(input("Enter number for ingredient you would like to search: \n"))
        ingredient_searched = numbered_lst[num][1]
    except ValueError:
        print("Only Intergers accepted\n")
    except:
        print(
            "Oops, your input didn't match the allowed options. Make sure you choose a number that matches an ingredient on the list\n"
        )
    else:
        for ingredient in data["recipes"]:
            if ingredient_searched in ingredient["ingredients"]:
                print(ingredient)
        print("\n")
#------END OF FUNCTIONS-------👍

#---Part 2 step 4---👍
filename = input("Enter filename where you've stored your recipes: \n")

#---Part 2 step 5, 6, 7---👍
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully!\n")
except FileNotFoundError:
    #---Part 2 step 6---👍
    print("Could not find file!\n")
except:
    print("Oops, there was an unexpected error\n")
else:
    #---Part 2 step 7---👍
    file.close()
    search_ingredients(data)
import random
import datetime

class UserProfile:
    """
    Represents a user's profile with their dietary restrictions, preferences, and budget.
    """
    def __init__(self, dietary_restrictions=None, preferred_cuisines=None, budget=None, food_on_hand=None):
        """
        Initializes a UserProfile object.

        Args:
            dietary_restrictions (list, optional): A list of dietary restrictions (e.g., "vegetarian", "gluten-free"). Defaults to None.
            preferred_cuisines (list, optional): A list of preferred cuisines (e.g., "Italian", "Mexican"). Defaults to None.
            budget (float, optional): The user's weekly budget for food. Defaults to None.
            food_on_hand (dict, optional): A dictionary representing the food the user already has (e.g., {"tomatoes": 3, "onions": 2}). Defaults to None.
        """
        self.dietary_restrictions = dietary_restrictions if dietary_restrictions is not None else []
        self.preferred_cuisines = preferred_cuisines if preferred_cuisines is not None else []
        self.budget = budget
        self.food_on_hand = food_on_hand if food_on_hand is not None else {}

    def update_profile(self, dietary_restrictions=None, preferred_cuisines=None, budget=None, food_on_hand=None):
        """
        Updates the user's profile information.

        Args:
            dietary_restrictions (list, optional): A list of dietary restrictions. Defaults to None.
            preferred_cuisines (list, optional): A list of preferred cuisines. Defaults to None.
            budget (float, optional): The user's weekly budget. Defaults to None.
            food_on_hand (dict, optional): A dictionary representing the food the user already has. Defaults to None.
        """
        if dietary_restrictions is not None:
            self.dietary_restrictions = dietary_restrictions
        if preferred_cuisines is not None:
            self.preferred_cuisines = preferred_cuisines
        if budget is not None:  # Allow budget to be set to 0
            self.budget = budget
        if food_on_hand is not None:
            self.food_on_hand = food_on_hand

    def __str__(self):
        return (f"Dietary Restrictions: {self.dietary_restrictions}\n"
                f"Preferred Cuisines: {self.preferred_cuisines}\n"
                f"Budget: {self.budget}\n"
                f"Food on Hand: {self.food_on_hand}")


class Recipe:
    """
    Represents a recipe with its ingredients, instructions, and nutritional information.
    """
    def __init__(self, name, ingredients, instructions, cuisine, dietary_info=None, cost=None):
        """
        Initializes a Recipe object.

        Args:
            name (str): The name of the recipe.
            ingredients (dict): A dictionary of ingredients and their quantities (e.g., {"tomatoes": "2", "onions": "1"}).
            instructions (list): A list of instructions for preparing the recipe.
            cuisine (str): The cuisine of the recipe (e.g., "Italian", "Mexican").
            dietary_info (list, optional): A list of dietary information tags (e.g., "vegetarian", "gluten-free"). Defaults to None.
            cost (float, optional): The estimated cost of the recipe. Defaults to None.
        """
        if not isinstance(ingredients, dict):
            raise TypeError("Ingredients must be a dictionary.")
        if not isinstance(instructions, list):
            raise TypeError("Instructions must be a list.")

        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.cuisine = cuisine
        self.dietary_info = dietary_info if dietary_info is not None else []
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.cuisine})"

    def display_recipe(self):
        """Displays the full recipe details."""
        print(f"\n--- {self.name} ---")
        print(f"Cuisine: {self.cuisine}")
        print("Ingredients:")
        for ingredient, quantity in self.ingredients.items():
            print(f"- {ingredient}: {quantity}")
        print("\nInstructions:")
        for i, step in enumerate(self.instructions):
            print(f"{i+1}. {step}")
        if self.dietary_info:
            print(f"\nDietary Info: {', '.join(self.dietary_info)}")
        if self.cost:
            print(f"Estimated Cost: ${self.cost:.2f}")


class MealPlan:
    """
    Represents a meal plan for a week, including recipes for each meal.
    """
    def __init__(self, user_profile):
        """
        Initializes a MealPlan object.

        Args:
            user_profile (UserProfile): The user's profile.
        """
        if not isinstance(user_profile, UserProfile):
            raise TypeError("user_profile must be a UserProfile object.")

        self.user_profile = user_profile
        self.meals = {
            "Monday": {"Breakfast": None, "Lunch": None, "Dinner": None},
            "Tuesday": {"Breakfast": None, "Lunch": None, "Dinner": None},
            "Wednesday": {"Breakfast": None, "Lunch": None, "Dinner": None},
            "Thursday": {"Breakfast": None, "Lunch": None, "Dinner": None},
            "Friday": {"Breakfast": None, "Lunch": None, "Dinner": None},
            "Saturday": {"Breakfast": None, "Lunch": None, "Dinner": None},
            "Sunday": {"Breakfast": None, "Lunch": None, "Dinner": None}
        }

    def add_recipe(self, day, meal_type, recipe):
        """
        Adds a recipe to the meal plan for a specific day and meal type.

        Args:
            day (str): The day of the week (e.g., "Monday").
            meal_type (str): The meal type (e.g., "Breakfast", "Lunch", "Dinner").
            recipe (Recipe): The recipe to add.
        """
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be a Recipe object.")

        if day in self.meals and meal_type in self.meals[day]:
            self.meals[day][meal_type] = recipe
        else:
            raise ValueError("Invalid day or meal type.")

    def remove_recipe(self, day, meal_type):
        """
        Removes a recipe from the meal plan.

        Args:
            day (str): The day of the week.
            meal_type (str): The meal type.
        """
        if day in self.meals and meal_type in self.meals[day]:
            self.meals[day][meal_type] = None
        else:
            raise ValueError("Invalid day or meal type.")

    def get_shopping_list(self):
        """
        Generates a shopping list based on the meal plan and the user's food on hand.

        Returns:
            dict: A dictionary representing the shopping list, with ingredients and their quantities.
        """
        shopping_list = {}
        for day in self.meals:
            for meal_type in self.meals[day]:
                recipe = self.meals[day][meal_type]
                if recipe:
                    for ingredient, quantity in recipe.ingredients.items():
                        try:
                            quantity = float(quantity)
                        except ValueError:
                            print(f"Warning: Could not convert quantity '{quantity}' for ingredient '{ingredient}' to a number. Skipping this ingredient.")
                            continue  # Skip this ingredient
                        if ingredient in shopping_list:
                            shopping_list[ingredient] += quantity
                        else:
                            shopping_list[ingredient] = quantity

        # Subtract ingredients the user already has
        for ingredient, quantity in self.user_profile.food_on_hand.items():
            if ingredient in shopping_list:
                shopping_list[ingredient] -= quantity
                if shopping_list[ingredient] <= 0:
                    del shopping_list[ingredient]  # Remove if we have enough
            else:
                pass # consider add if needed.

        return {k: round(v, 2) for k, v in shopping_list.items() if v > 0} # only return needed amounts, rounded

    def calculate_total_cost(self):
        """
        Calculates the total estimated cost of the meal plan.

        Returns:
            float: The total cost of the meal plan.
        """
        total_cost = 0
        for day in self.meals:
            for meal_type in self.meals[day]:
                recipe = self.meals[day][meal_type]
                if recipe and recipe.cost:
                    total_cost += recipe.cost
        return round(total_cost, 2)

    def __str__(self):
        """
        Returns a string representation of the meal plan.
        """
        plan_string = ""
        for day, meals in self.meals.items():
            plan_string += f"\n--- {day} ---\n"
            for meal_type, recipe in meals.items():
                recipe_name = recipe.name if recipe else "None"
                plan_string += f"{meal_type}: {recipe_name}\n"
        return plan_string

    def display_meal_plan(self):
        """Displays the meal plan with more details."""
        print("\n--- Meal Plan ---")
        for day, meals in self.meals.items():
            print(f"\n--- {day} ---")
            for meal_type, recipe in meals.items():
                print(f"{meal_type}: ", end="")
                if recipe:
                    print(recipe)
                    #recipe.display_recipe() #Optionally display the full recipe
                else:
                    print("None")


class RecipeDatabase:
    """
    Manages a collection of recipes.
    """
    def __init__(self):
        """
        Initializes a RecipeDatabase object.
        """
        self.recipes = []

    def add_recipe(self, recipe):
        """
        Adds a recipe to the database.

        Args:
            recipe (Recipe): The recipe to add.
        """
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be a Recipe object.")
        self.recipes.append(recipe)

    def search_recipes(self, criteria=None):
        """
        Searches for recipes based on specified criteria.

        Args:
            criteria (dict, optional): A dictionary of search criteria (e.g., {"cuisine": "Italian", "dietary_info": "vegetarian"}). Defaults to None.

        Returns:
            list: A list of recipes that match the search criteria.
        """
        if criteria is None:
            return self.recipes  # Return all recipes if no criteria are specified

        if not isinstance(criteria, dict):
            raise TypeError("criteria must be a dictionary.")

        matching_recipes = []
        for recipe in self.recipes:
            match = True
            for key, value in criteria.items():
                key = key.lower()
                if key == "cuisine":
                    if recipe.cuisine.lower() != value.lower():
                        match = False
                        break
                elif key == "dietary_info":
                    if not isinstance(value, list): #Handles searching for multiple dietary requirements
                        value = [value]
                    for req in value:
                        if req.lower() not in [item.lower() for item in recipe.dietary_info]:
                            match = False
                            break #breaks inner loop.
                    if not match:
                        break #breaks outer loop
                elif key == "ingredients": #Searching by ingredients;  value should be a list.
                    if not isinstance(value, list):
                        raise TypeError("Ingredients criteria must be a list.")
                    for ingredient in value:
                        if ingredient.lower() not in [item.lower() for item in recipe.ingredients.keys()]:
                            match = False
                            break
                    if not match:
                        break #breaks outer loop

                else:
                    print(f"Warning: Unknown search criteria '{key}'.  Skipping.") #Handle unknown keys gracefully

            if match:
                matching_recipes.append(recipe)

        return matching_recipes

    def display_all_recipes(self):
        """Displays a list of all recipes in the database."""
        print("\n--- All Recipes ---")
        if not self.recipes:
            print("No recipes in the database.")
            return

        for recipe in self.recipes:
            print(recipe) #Uses the Recipe.__str__() method

    def get_recipe_by_name(self, name):
        """Returns a recipe object given its name. Returns None if not found."""
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe
        return None


class MindfulMealPlanner:
    """
    Main application class for the Mindful Meal Planner.
    """
    def __init__(self):
        """
        Initializes the MindfulMealPlanner application.
        """
        self.user_profile = UserProfile()
        self.recipe_database = RecipeDatabase()
        self.meal_plan = MealPlan(self.user_profile)

    def create_sample_recipes(self):
        """
        Creates and adds some sample recipes to the recipe database.
        """
        recipe1 = Recipe(
            name="Spaghetti with Tomato Sauce",
            ingredients={"spaghetti": "200", "tomato sauce": "500", "onion": "1", "garlic": "2"},
            instructions=["Cook spaghetti according to package directions.", "Sauté onion and garlic in olive oil.", "Add tomato sauce and simmer for 15 minutes.", "Serve sauce over spaghetti."],
            cuisine="Italian",
            dietary_info=["vegetarian"],
            cost=5.0
        )
        recipe2 = Recipe(
            name="Chicken Tacos",
            ingredients={"chicken breast": "300", "taco shells": "6", "lettuce": "1", "tomato": "2", "salsa": "200"},
            instructions=["Cook chicken breast and shred.", "Fill taco shells with chicken, lettuce, tomato, and salsa."],
            cuisine="Mexican",
            cost=8.0
        )
        recipe3 = Recipe(
            name="Lentil Soup",
            ingredients={"lentils": "1", "carrots": "2", "celery": "2", "vegetable broth": "6", "onion": "1"},
            instructions=["Sauté onion, carrots, and celery in olive oil.", "Add lentils and vegetable broth.", "Simmer for 30 minutes."],
            cuisine="Mediterranean",
            dietary_info=["vegetarian", "vegan"],
            cost=4.0
        )

        recipe4 = Recipe(
            name = "Omelette",
            ingredients = {"eggs": "2", "milk": "0.5", "cheese": "50", "ham": "30"},
            instructions = ["Whisk eggs and milk", "Add cheese and ham", "Cook in pan until golden brown"],
            cuisine = "Breakfast",
            cost = 3.0
        )
        self.recipe_database.add_recipe(recipe1)
        self.recipe_database.add_recipe(recipe2)
        self.recipe_database.add_recipe(recipe3)
        self.recipe_database.add_recipe(recipe4)

    def update_user_profile(self, dietary_restrictions=None, preferred_cuisines=None, budget=None, food_on_hand=None):
        """
        Updates the user's profile.

        Args:
            dietary_restrictions (list, optional): A list of dietary restrictions. Defaults to None.
            preferred_cuisines (list, optional): A list of preferred cuisines. Defaults to None.
            budget (float, optional): The user's weekly budget. Defaults to None.
            food_on_hand (dict, optional): A dictionary representing the food the user already has. Defaults to None.
        """
        self.user_profile.update_profile(dietary_restrictions, preferred_cuisines, budget, food_on_hand)
        self.meal_plan = MealPlan(self.user_profile)  #Recreate meal plan when profile is updated

    def generate_meal_plan(self):
        """
        Generates a meal plan based on the user's profile and the available recipes.

        A more sophisticated implementation would consider dietary restrictions,
        preferred cuisines, budget, and food on hand to create a personalized plan.
        """
        # First, get the recipes available, based on dietary and cuisine preferences.
        search_criteria = {}
        if self.user_profile.dietary_restrictions:
            search_criteria["dietary_info"] = self.user_profile.dietary_restrictions
        if self.user_profile.preferred_cuisines:
             search_criteria["cuisine"] = self.user_profile.preferred_cuisines

        available_recipes = self.recipe_database.search_recipes(search_criteria)

        if not available_recipes:
            print("No recipes found matching your criteria. Try changing your dietary or cuisine preferences, or adding more recipes to the database.")
            return

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        meal_types = ["Breakfast", "Lunch", "Dinner"]

        for day in days:
            for meal_type in meal_types:
                # Filter recipes by dietary and cuisine preferences
                suitable_recipes = available_recipes

                if not suitable_recipes:
                     print(f"No suitable recipes found for {day} {meal_type}.")
                     continue #skip to the next meal

                recipe = random.choice(suitable_recipes)
                try:
                    self.meal_plan.add_recipe(day, meal_type, recipe)
                except ValueError as e:
                    print(f"Error adding recipe: {e}")

    def get_meal_plan(self):
        """
        Returns the current meal plan.

        Returns:
            MealPlan: The current meal plan.
        """
        return self.meal_plan

    def get_shopping_list(self):
        """
        Returns the shopping list based on the current meal plan and user's food on hand.

        Returns:
            dict: A dictionary representing the shopping list.
        """
        return self.meal_plan.get_shopping_list()

    def track_food_waste(self, day, meal_type, waste_amount):
      """Placeholder for waste tracking feature.  Currently does nothing.
      Args:
          day(str): Day of the week
          meal_type(str): Breakfast, Lunch, or Dinner
          waste_amount(float): Amount of wasted food.
      """
      if not isinstance(waste_amount, (int, float)):
          raise TypeError("Waste amount must be a number.")
      print(f"Food Waste Tracking: On {day} for {meal_type}, waste of {waste_amount} recorded.")
      return None

    def add_recipe_to_meal_plan(self, day, meal_type, recipe_name):
        """Adds a specific recipe to the meal plan."""
        recipe = self.recipe_database.get_recipe_by_name(recipe_name)
        if recipe:
            try:
                self.meal_plan.add_recipe(day, meal_type, recipe)
                print(f"Successfully added {recipe_name} to {day} {meal_type}.")
            except ValueError as e:
                print(f"Error adding recipe: {e}")
        else:
            print(f"Recipe '{recipe_name}' not found in the database.")

    def run(self):
        """Runs the main application loop."""
        while True:
            print("\n--- Mindful Meal Planner ---")
            print("1. Update User Profile")
            print("2. Generate Meal Plan")
            print("3. View Meal Plan")
            print("4. Get Shopping List")
            print("5. Add Recipe to Meal Plan")
            print("6. View All Recipes")
            print("7. Search Recipes")
            print("8. Track Food Waste")
            print("9. Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    self.handle_update_profile()
                elif choice == "2":
                    self.generate_meal_plan()
                    print("Meal plan generated.")
                elif choice == "3":
                    self.meal_plan.display_meal_plan()
                elif choice == "4":
                    shopping_list = self.get_shopping_list()
                    print("\n--- Shopping List ---")
                    if shopping_list:
                        for ingredient, quantity in shopping_list.items():
                            print(f"{ingredient}: {quantity}")
                    else:
                        print("Shopping list is empty.")
                elif choice == "5":
                    self.handle_add_recipe_to_meal_plan()
                elif choice == "6":
                    self.recipe_database.display_all_recipes()
                elif choice == "7":
                    self.handle_search_recipes()
                elif choice == "8":
                    self.handle_track_food_waste()
                elif choice == "9":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def handle_update_profile(self):
        """Handles the user profile update process."""
        print("\n--- Update User Profile ---")

        dietary_restrictions_str = input("Enter dietary restrictions (comma-separated, e.g., vegetarian,gluten-free): ")
        dietary_restrictions = [s.strip() for s in dietary_restrictions_str.split(",")] if dietary_restrictions_str else None

        preferred_cuisines_str = input("Enter preferred cuisines (comma-separated, e.g., Italian,Mexican): ")
        preferred_cuisines = [s.strip() for s in preferred_cuisines_str.split(",")] if preferred_cuisines_str else None

        try:
            budget = float(input("Enter weekly budget: ")) if input("Enter weekly budget: ") else None
        except ValueError:
            print("Invalid budget. Please enter a number.")
            return

        food_on_hand_str = input("Enter food on hand (ingredient:quantity, comma-separated, e.g., tomatoes:2,onions:1): ")
        food_on_hand = {}
        if food_on_hand_str:
            try:
                for item in food_on_hand_str.split(","):
                    ingredient, quantity = item.split(":")
                    food_on_hand[ingredient.strip()] = float(quantity.strip())
            except ValueError:
                print("Invalid food on hand format. Please use ingredient:quantity format.")
                return

        self.update_user_profile(dietary_restrictions, preferred_cuisines, budget, food_on_hand)
        print("User profile updated.")

    def handle_add_recipe_to_meal_plan(self):
        """Handles adding a specific recipe to the meal plan."""
        print("\n--- Add Recipe to Meal Plan ---")
        day = input("Enter day of the week (e.g., Monday): ")
        meal_type = input("Enter meal type (Breakfast, Lunch, Dinner): ")
        recipe_name = input("Enter the name of the recipe to add: ")

        self.add_recipe_to_meal_plan(day, meal_type, recipe_name)

    def handle_search_recipes(self):
        """Handles the recipe search process."""
        print("\n--- Search Recipes ---")
        search_term = input("Enter search criteria (cuisine:value or dietary_info:value or ingredients:value1,value2): ")
        try:
            criteria = {}
            if ":" in search_term:
                key, value = search_term.split(":")
                criteria[key.strip()] = [item.strip() for item in value.split(",")] if "," in value else value.strip()

            results = self.recipe_database.search_recipes(criteria)

            if results:
                print("\n--- Search Results ---")
                for recipe in results:
                    print(recipe)
                    #recipe.display_recipe() #Optionally show full recipe details
            else:
                print("No recipes found matching your criteria.")
        except Exception as e:
            print(f"Invalid search criteria: {e}")


    def handle_track_food_waste(self):
        """Handles tracking food waste."""
        print("\n--- Track Food Waste ---")
        day = input("Enter day of the week: ")
        meal_type = input("Enter meal type (Breakfast, Lunch, Dinner): ")
        try:
            waste_amount = float(input("Enter amount of food wasted (in grams or similar unit): "))
            self.track_food_waste(day, meal_type, waste_amount)
        except ValueError:
            print("Invalid waste amount. Please enter a number.")

def main():
    """
    Main function to demonstrate the Mindful Meal Planner application.
    """
    planner = MindfulMealPlanner()
    planner.create_sample_recipes()
    planner.run()


if __name__ == "__main__":
    main()
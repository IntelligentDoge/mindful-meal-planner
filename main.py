```python
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
        self.dietary_restrictions = dietary_restrictions if dietary_restrictions else []
        self.preferred_cuisines = preferred_cuisines if preferred_cuisines else []
        self.budget = budget
        self.food_on_hand = food_on_hand if food_on_hand else {}

    def update_profile(self, dietary_restrictions=None, preferred_cuisines=None, budget=None, food_on_hand=None):
        """
        Updates the user's profile information.

        Args:
            dietary_restrictions (list, optional): A list of dietary restrictions. Defaults to None.
            preferred_cuisines (list, optional): A list of preferred cuisines. Defaults to None.
            budget (float, optional): The user's weekly budget. Defaults to None.
            food_on_hand (dict, optional): A dictionary representing the food the user already has. Defaults to None.
        """
        if dietary_restrictions:
            self.dietary_restrictions = dietary_restrictions
        if preferred_cuisines:
            self.preferred_cuisines = preferred_cuisines
        if budget is not None:  # Allow budget to be set to 0
            self.budget = budget
        if food_on_hand:
            self.food_on_hand = food_on_hand


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
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.cuisine = cuisine
        self.dietary_info = dietary_info if dietary_info else []
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.cuisine})"

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
        if day in self.meals and meal_type in self.meals[day]:
            self.meals[day][meal_type] = recipe
        else:
            print("Invalid day or meal type.")

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
            print("Invalid day or meal type.")

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
                        if ingredient in shopping_list:
                            try:
                                shopping_list[ingredient] += float(quantity) #handles quantities like "1/2" by defaulting to 0.0
                            except ValueError:
                                print(f"Warning: Could not add quantity '{quantity}' for ingredient '{ingredient}'.  Skipping quantity.")
                        else:
                            try:
                                shopping_list[ingredient] = float(quantity)
                            except ValueError:
                                print(f"Warning: Could not add quantity '{quantity}' for ingredient '{ingredient}'. Skipping quantity.")
                                shopping_list[ingredient] = 0.0 #Setting to zero prevents errors when subtracting.


        # Subtract ingredients the user already has
        for ingredient, quantity in self.user_profile.food_on_hand.items():
            if ingredient in shopping_list:
                shopping_list[ingredient] -= quantity
                if shopping_list[ingredient] <= 0:
                    del shopping_list[ingredient]  # Remove if we have enough
            #else: Consider if they should be added into the shopping list if they didn't have the ingredient.

        return {k: v for k, v in shopping_list.items() if v > 0} # only return needed amounts

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
        return total_cost

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
        self.recipes.append(recipe)

    def search_recipes(self, criteria=None):
        """
        Searches for recipes based on specified criteria.

        Args:
            criteria (dict, optional): A dictionary of search criteria (e.g., {"cuisine": "Italian", "dietary_info": "vegetarian"}). Defaults to None.

        Returns:
            list: A list of recipes that match the search criteria.
        """
        if not criteria:
            return self.recipes  # Return all recipes if no criteria are specified

        matching_recipes = []
        for recipe in self.recipes:
            match = True
            for key, value in criteria.items():
                if key == "cuisine" and recipe.cuisine != value:
                    match = False
                    break
                elif key == "dietary_info" and value not in recipe.dietary_info:
                    match = False
                    break
                # Add more criteria checks as needed (e.g., ingredients)
            if match:
                matching_recipes.append(recipe)

        return matching_recipes


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
            ingredients={"spaghetti": "200g", "tomato sauce": "500g", "onion": "1", "garlic": "2 cloves"},
            instructions=["Cook spaghetti according to package directions.", "Sauté onion and garlic in olive oil.", "Add tomato sauce and simmer for 15 minutes.", "Serve sauce over spaghetti."],
            cuisine="Italian",
            dietary_info=["vegetarian"],
            cost=5.0
        )
        recipe2 = Recipe(
            name="Chicken Tacos",
            ingredients={"chicken breast": "300g", "taco shells": "6", "lettuce": "1 head", "tomato": "2", "salsa": "200g"},
            instructions=["Cook chicken breast and shred.", "Fill taco shells with chicken, lettuce, tomato, and salsa."],
            cuisine="Mexican",
            cost=8.0
        )
        recipe3 = Recipe(
            name="Lentil Soup",
            ingredients={"lentils": "1 cup", "carrots": "2", "celery": "2 stalks", "vegetable broth": "6 cups", "onion": "1"},
            instructions=["Sauté onion, carrots, and celery in olive oil.", "Add lentils and vegetable broth.", "Simmer for 30 minutes."],
            cuisine="Mediterranean",
            dietary_info=["vegetarian", "vegan"],
            cost=4.0
        )
        self.recipe_database.add_recipe(recipe1)
        self.recipe_database.add_recipe(recipe2)
        self.recipe_database.add_recipe(recipe3)

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

        This is a simplified implementation that randomly selects recipes.
        A more sophisticated implementation would consider dietary restrictions,
        preferred cuisines, budget, and food on hand to create a personalized plan.
        """
        # First, get the recipes available, based on dietary and cuisine preferences.
        search_criteria = {}
        if self.user_profile.dietary_restrictions:
            #This only works if the recipes are correctly labelled
            search_criteria["dietary_info"] = self.user_profile.dietary_restrictions[0] #Simplifying, using the first entry.
        if self.user_profile.preferred_cuisines:
             search_criteria["cuisine"] = self.user_profile.preferred_cuisines[0] #Simplifying, using the first entry.

        available_recipes = self.recipe_database.search_recipes(search_criteria)

        if not available_recipes:
            print("No recipes found matching your criteria. Try changing your dietary or cuisine preferences, or adding more recipes to the database.")
            return

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        meal_types = ["Breakfast", "Lunch", "Dinner"]

        for day in days:
            for meal_type in meal_types:
                recipe = random.choice(available_recipes)
                self.meal_plan.add_recipe(day, meal_type, recipe)

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
      print(f"Food Waste Tracking: On {day} for {meal_type}, waste of {waste_amount} recorded.")
      return None

def main():
    """
    Main function to demonstrate the Mindful Meal Planner application.
    """
    planner = MindfulMealPlanner()
    planner.create_sample_recipes()

    # Update user profile
    planner.update_user_profile(
        dietary_restrictions=["vegetarian"],
        preferred_cuisines=["Italian"],
        budget=50.0,
        food_on_hand={"tomatoes": 1, "onions": 1}
    )

    # Generate meal plan
    planner.generate_meal_plan()

    # Get meal plan
    meal_plan = planner.get_meal_plan()
    print("\nMeal Plan:")
    print(meal_plan)

    # Get shopping list
    shopping_list = planner.get_shopping_list()
    print("\nShopping List:")
    for ingredient, quantity in shopping_list.items():
        print(f"{ingredient}: {quantity}")

    # Track food waste
    planner.track_food_waste("Monday", "Dinner", 0.25)


if __name__ == "__main__":
    main()
```
import random
import datetime

class UserProfile:
    """Represents a user's profile with dietary restrictions, preferences, and budget."""

    def __init__(self, dietary_restrictions=None, preferred_cuisines=None, budget=None, food_on_hand=None):
        """Initializes a UserProfile object."""
        self.dietary_restrictions = dietary_restrictions if dietary_restrictions is not None else []
        self.preferred_cuisines = preferred_cuisines if preferred_cuisines is not None else []
        self.budget = budget
        self.food_on_hand = food_on_hand if food_on_hand is not None else {}

    def update_profile(self, dietary_restrictions=None, preferred_cuisines=None, budget=None, food_on_hand=None):
        """Updates the user's profile information."""
        if dietary_restrictions is not None:
            self.dietary_restrictions = dietary_restrictions
        if preferred_cuisines is not None:
            self.preferred_cuisines = preferred_cuisines
        if budget is not None:
            self.budget = budget
        if food_on_hand is not None:
            self.food_on_hand = food_on_hand

    def __str__(self):
        return (f"Dietary Restrictions: {', '.join(self.dietary_restrictions) or 'None'}\n"
                f"Preferred Cuisines: {', '.join(self.preferred_cuisines) or 'None'}\n"
                f"Budget: ${self.budget:.2f}" if self.budget is not None else "Budget: None\n"
                f"Food on Hand: {self.food_on_hand or 'None'}")


class Recipe:
    """Represents a recipe with its ingredients, instructions, and nutritional information."""

    def __init__(self, name, ingredients, instructions, cuisine, dietary_info=None, cost=None):
        """Initializes a Recipe object."""
        if not isinstance(ingredients, dict):
            raise TypeError("Ingredients must be a dictionary.")
        if not isinstance(instructions, list):
            raise TypeError("Instructions must be a list.")
        if not name:
            raise ValueError("Recipe name cannot be empty.")
        if not ingredients:
            raise ValueError("Recipe must have at least one ingredient.")
        if not instructions:
            raise ValueError("Recipe must have at least one instruction.")
        if not cuisine:
            raise ValueError("Recipe must have a cuisine type.")

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
            print(f"{i + 1}. {step}")
        if self.dietary_info:
            print(f"\nDietary Info: {', '.join(self.dietary_info)}")
        if self.cost:
            print(f"Estimated Cost: ${self.cost:.2f}")


class MealPlan:
    """Represents a meal plan for a week, including recipes for each meal."""

    def __init__(self, user_profile):
        """Initializes a MealPlan object."""
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
        """Adds a recipe to the meal plan for a specific day and meal type."""
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be a Recipe object.")

        if day in self.meals and meal_type in self.meals[day]:
            self.meals[day][meal_type] = recipe
        else:
            raise ValueError("Invalid day or meal type.")

    def remove_recipe(self, day, meal_type):
        """Removes a recipe from the meal plan."""
        if day in self.meals and meal_type in self.meals[day]:
            self.meals[day][meal_type] = None
        else:
            raise ValueError("Invalid day or meal type.")

    def get_shopping_list(self):
        """Generates a shopping list based on the meal plan and the user's food on hand."""
        shopping_list = {}
        for day in self.meals:
            for meal_type in self.meals[day]:
                recipe = self.meals[day][meal_type]
                if recipe:
                    for ingredient, quantity in recipe.ingredients.items():
                        try:
                            quantity = float(quantity)
                        except ValueError:
                            print(
                                f"Warning: Could not convert quantity '{quantity}' for ingredient '{ingredient}' to a number. Skipping this ingredient.")
                            continue
                        if ingredient in shopping_list:
                            shopping_list[ingredient] += quantity
                        else:
                            shopping_list[ingredient] = quantity

        for ingredient, quantity in self.user_profile.food_on_hand.items():
            if ingredient in shopping_list:
                shopping_list[ingredient] -= quantity
                if shopping_list[ingredient] <= 0:
                    del shopping_list[ingredient]
            else:
                pass

        return {k: round(v, 2) for k, v in shopping_list.items() if v > 0}

    def calculate_total_cost(self):
        """Calculates the total estimated cost of the meal plan."""
        total_cost = 0
        for day in self.meals:
            for meal_type in self.meals[day]:
                recipe = self.meals[day][meal_type]
                if recipe and recipe.cost:
                    total_cost += recipe.cost
        return round(total_cost, 2)

    def __str__(self):
        """Returns a string representation of the meal plan."""
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
                else:
                    print("None")


class RecipeDatabase:
    """Manages a collection of recipes."""

    def __init__(self):
        """Initializes a RecipeDatabase object."""
        self.recipes = []

    def add_recipe(self, recipe):
        """Adds a recipe to the database."""
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be a Recipe object.")
        self.recipes.append(recipe)

    def search_recipes(self, criteria=None):
        """Searches for recipes based on specified criteria."""
        if criteria is None:
            return self.recipes

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
                    if not isinstance(value, list):
                        value = [value]
                    for req in value:
                        if req.lower() not in [item.lower() for item in recipe.dietary_info]:
                            match = False
                            break
                    if not match:
                        break
                elif key == "ingredients":
                    if not isinstance(value, list):
                        raise TypeError("Ingredients criteria must be a list.")
                    for ingredient in value:
                        if ingredient.lower() not in [item.lower() for item in recipe.ingredients.keys()]:
                            match = False
                            break
                    if not match:
                        break
                else:
                    print(f"Warning: Unknown search criteria '{key}'.  Skipping.")

            if match:
                matching_recipes.append(recipe)

        return matching_recipes

    def display_all_recipes(self):
        """Displays a list of all recipes in the database."""
        print("\n--- All Recipes ---")
        if not self.recipes:
            print("No recipes in the database.")
            return

        for i, recipe in enumerate(self.recipes):
            print(f"{i+1}. {recipe}")

    def get_recipe_by_name(self, name):
        """Returns a recipe object given its name."""
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                return recipe
        return None

    def get_recipe_by_index(self, index):
        """Returns a recipe object given its index in the list."""
        try:
            return self.recipes[index]
        except IndexError:
            return None


class MindfulMealPlanner:
    """Main application class for the Mindful Meal Planner."""

    def __init__(self):
        """Initializes the MindfulMealPlanner application."""
        self.user_profile = UserProfile()
        self.recipe_database = RecipeDatabase()
        self.meal_plan = MealPlan(self.user_profile)

    def create_sample_recipes(self):
        """Creates and adds some sample recipes to the recipe database."""
        try:
            recipe1 = Recipe(
                name="Spaghetti with Tomato Sauce",
                ingredients={"spaghetti": "200g", "tomato sauce": "500g", "onion": "1", "garlic": "2 cloves"},
                instructions=["Cook spaghetti.", "Sauté onion and garlic.", "Add tomato sauce and simmer.", "Serve sauce over spaghetti."],
                cuisine="Italian",
                dietary_info=["vegetarian"],
                cost=5.0
            )
            recipe2 = Recipe(
                name="Chicken Tacos",
                ingredients={"chicken breast": "300g", "taco shells": "6", "lettuce": "1 head", "tomato": "2", "salsa": "200g"},
                instructions=["Cook chicken and shred.", "Fill taco shells with chicken, lettuce, tomato, and salsa."],
                cuisine="Mexican",
                cost=8.0
            )
            recipe3 = Recipe(
                name="Lentil Soup",
                ingredients={"lentils": "1 cup", "carrots": "2", "celery": "2 stalks", "vegetable broth": "6 cups", "onion": "1"},
                instructions=["Sauté onion, carrots, and celery.", "Add lentils and vegetable broth.", "Simmer for 30 minutes."],
                cuisine="Mediterranean",
                dietary_info=["vegetarian", "vegan"],
                cost=4.0
            )

            recipe4 = Recipe(
                name="Omelette",
                ingredients={"eggs": "2", "milk": "0.5 cup", "cheese": "50g", "ham": "30g"},
                instructions=["Whisk eggs and milk", "Add cheese and ham", "Cook in pan until golden brown"],
                cuisine="Breakfast",
                cost=3.0
            )
            self.recipe_database.add_recipe(recipe1)
            self.recipe_database.add_recipe(recipe2)
            self.recipe_database.add_recipe(recipe3)
            self.recipe_database.add_recipe(recipe4)
            print("Sample recipes created and added.")
        except ValueError as e:
            print(f"Error creating sample recipes: {e}")
        except TypeError as e:
            print(f"Type Error while creating sample recipes: {e}")
        except Exception as e:
            print(f"Unexpected error creating sample recipes: {e}")

    def update_user_profile(self, dietary_restrictions=None, preferred_cuisines=None, budget=None,
                                food_on_hand=None):
        """Updates the user's profile."""
        self.user_profile.update_profile(dietary_restrictions, preferred_cuisines, budget, food_on_hand)
        self.meal_plan = MealPlan(self.user_profile)

    def generate_meal_plan(self):
        """Generates a meal plan based on the user's profile and the available recipes."""
        search_criteria = {}
        if self.user_profile.dietary_restrictions:
            search_criteria["dietary_info"] = self.user_profile.dietary_restrictions
        if self.user_profile.preferred_cuisines:
            search_criteria["cuisine"] = self.user_profile.preferred_cuisines

        available_recipes = self.recipe_database.search_recipes(search_criteria)

        if not available_recipes:
            print(
                "No recipes found matching your criteria. Try changing your dietary or cuisine preferences, or adding more recipes to the database.")
            return

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        meal_types = ["Breakfast", "Lunch", "Dinner"]

        for day in days:
            for meal_type in meal_types:
                suitable_recipes = available_recipes

                if not suitable_recipes:
                    self.meal_plan.add_recipe(day, meal_type, None) # Set to None if no recipe is found
                    continue

                recipe = random.choice(suitable_recipes)
                try:
                    self.meal_plan.add_recipe(day, meal_type, recipe)
                except ValueError as e:
                    print(f"Error adding recipe: {e}")

    def get_meal_plan(self):
        """Returns the current meal plan."""
        return self.meal_plan

    def get_shopping_list(self):
        """Returns the shopping list."""
        return self.meal_plan.get_shopping_list()

    def track_food_waste(self, day, meal_type, waste_amount):
        """Placeholder for waste tracking feature."""
        if not isinstance(waste_amount, (int, float)):
            raise TypeError("Waste amount must be a number.")
        print(f"Food Waste Tracking: On {day} for {meal_type}, waste of {waste_amount} recorded.")
        return None

    def add_recipe_to_meal_plan(self, day, meal_type, recipe):
        """Adds a specific recipe to the meal plan."""
        if recipe:
            try:
                self.meal_plan.add_recipe(day, meal_type, recipe)
                print(f"Successfully added {recipe.name} to {day} {meal_type}.")
            except ValueError as e:
                print(f"Error adding recipe: {e}")
        else:
            print(f"Recipe not found in the database.")

    def run(self):
        """Runs the main application loop."""
        self.create_sample_recipes()
        while True:
            print("\n--- Mindful Meal Planner ---")
            print("1. Update User Profile")
            print("2. Generate Meal Plan")
            print("3. View Meal Plan")
            print("4. Get Shopping List")
            print("5. Add Recipe to Meal Plan (by name)")
            print("6. Add Recipe to Meal Plan (by list index)")
            print("7. View All Recipes")
            print("8. Search Recipes")
            print("9. Track Food Waste")
            print("10. Add New Recipe")
            print("0. Exit")

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
                    self.handle_add_recipe_to_meal_plan_by_name()
                elif choice == "6":
                    self.handle_add_recipe_to_meal_plan_by_index()
                elif choice == "7":
                    self.recipe_database.display_all_recipes()
                elif choice == "8":
                    self.handle_search_recipes()
                elif choice == "9":
                    self.handle_track_food_waste()
                elif choice == "10":
                    self.handle_add_new_recipe()
                elif choice == "0":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def handle_update_profile(self):
        """Handles the user profile update process."""
        print("\n--- Update User Profile ---")

        dietary_restrictions = self._get_list_input("Enter dietary restrictions (comma-separated, e.g., vegetarian, gluten-free): ")
        preferred_cuisines = self._get_list_input("Enter preferred cuisines (comma-separated, e.g., Italian, Mexican): ")
        budget = self._get_float_input("Enter weekly budget (or leave blank for no budget): ")
        food_on_hand = self._get_food_on_hand_input()

        self.update_user_profile(dietary_restrictions, preferred_cuisines, budget, food_on_hand)
        print("User profile updated.")

    def handle_add_recipe_to_meal_plan_by_name(self):
        """Handles adding a specific recipe to the meal plan by name."""
        print("\n--- Add Recipe to Meal Plan (by name) ---")
        day = self._get_valid_day()
        meal_type = self._get_valid_meal_type()
        recipe_name = input("Enter the name of the recipe to add: ")

        recipe = self.recipe_database.get_recipe_by_name(recipe_name)
        self.add_recipe_to_meal_plan(day, meal_type, recipe)

    def handle_add_recipe_to_meal_plan_by_index(self):
        """Handles adding a specific recipe to the meal plan by index."""
        print("\n--- Add Recipe to Meal Plan (by list index) ---")
        day = self._get_valid_day()
        meal_type = self._get_valid_meal_type()

        self.recipe_database.display_all_recipes()  # Display recipes with indices
        while True:
            try:
                recipe_index = int(input("Enter the index of the recipe to add: ")) - 1  # Adjust for 0-based indexing
                recipe = self.recipe_database.get_recipe_by_index(recipe_index)
                if recipe:
                    break
                else:
                    print("Invalid recipe index. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.add_recipe_to_meal_plan(day, meal_type, recipe)

    def handle_search_recipes(self):
        """Handles the recipe search process."""
        print("\n--- Search Recipes ---")
        print("Search by: ")
        print("1. Cuisine")
        print("2. Dietary Info")
        print("3. Ingredients")
        print("0. Back to Main Menu")  # Added option to go back
        search_type = input("Enter search type (1-3, or 0 to go back): ")

        if search_type == "1":
            cuisine = input("Enter cuisine: ")
            criteria = {"cuisine": cuisine}
        elif search_type == "2":
            dietary_info = self._get_list_input("Enter dietary info (comma-separated): ")
            criteria = {"dietary_info": dietary_info}
        elif search_type == "3":
            ingredients = self._get_list_input("Enter ingredients (comma-separated): ")
            criteria = {"ingredients": ingredients}
        elif search_type == "0":
            return  # Go back to the main menu
        else:
            print("Invalid search type.")
            return

        results = self.recipe_database.search_recipes(criteria)

        if results:
            print("\n--- Search Results ---")
            for i, recipe in enumerate(results):
                print(f"{i+1}. {recipe}")
        else:
            print("No recipes found matching your criteria.")

    def handle_track_food_waste(self):
        """Handles tracking food waste."""
        print("\n--- Track Food Waste ---")
        day = self._get_valid_day()
        meal_type = self._get_valid_meal_type()
        waste_amount = self._get_float_input("Enter amount of food wasted (in grams): ")
        if waste_amount is not None:
            self.track_food_waste(day, meal_type, waste_amount)
        else:
            print("Food waste tracking cancelled.")

    def handle_add_new_recipe(self):
        """Handles adding a new recipe to the database."""
        print("\n--- Add New Recipe ---")
        try:
            name = input("Enter recipe name: ")
            ingredients = self._get_ingredients_input()
            instructions = self._get_list_input("Enter instructions (step-by-step, comma-separated): ")
            cuisine = input("Enter cuisine type: ")
            dietary_info = self._get_list_input("Enter dietary info (comma-separated, or leave empty): ")
            cost = self._get_float_input("Enter estimated cost (or leave empty): ")

            new_recipe = Recipe(name, ingredients, instructions, cuisine, dietary_info, cost)
            self.recipe_database.add_recipe(new_recipe)
            print(f"Recipe '{name}' added successfully.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except TypeError as e:
            print(f"Type error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _get_list_input(self, prompt):
        """Helper function to get a comma-separated list from the user."""
        input_str = input(prompt)
        return [s.strip() for s in input_str.split(",")] if input_str else []

    def _get_float_input(self, prompt):
        """Helper function to get a float from the user with error handling."""
        while True:
            input_str = input(prompt)
            if not input_str:
                return None  # Allows skipping the input
            try:
                return float(input_str)
            except ValueError:
                print("Invalid input. Please enter a number.")

    def _get_food_on_hand_input(self):
        """Helper function to get food on hand information from the user."""
        food_on_hand = {}
        print("Enter your food on hand (ingredient:quantity). Type 'done' when finished.")
        while True:
            item = input("Enter item (or 'done'): ")
            if item.lower() == 'done':
                break
            try:
                ingredient, quantity = item.split(":")
                food_on_hand[ingredient.strip()] = float(quantity.strip())
            except ValueError:
                print("Invalid format. Please use ingredient:quantity.")
        return food_on_hand

    def _get_ingredients_input(self):
        """Helper function to get ingredients from the user."""
        ingredients = {}
        print("Enter ingredients and quantities (ingredient:quantity). Type 'done' when finished.")
        while True:
            item = input("Enter item (or 'done'): ")
            if item.lower() == 'done':
                break
            try:
                ingredient, quantity = item.split(":")
                ingredients[ingredient.strip()] = quantity.strip()
            except ValueError:
                print("Invalid format. Please use ingredient:quantity.")
        return ingredients

    def _get_valid_day(self):
        """Helper function to get a valid day of the week from the user."""
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        while True:
            day = input("Enter day of the week (e.g., Monday): ").capitalize()
            if day in valid_days:
                return day
            else:
                print("Invalid day. Please enter a valid day of the week.")

    def _get_valid_meal_type(self):
        """Helper function to get a valid meal type from the user."""
        valid_meal_types = ["Breakfast", "Lunch", "Dinner"]
        while True:
            meal_type = input("Enter meal type (Breakfast, Lunch, Dinner): ").capitalize()
            if meal_type in valid_meal_types:
                return meal_type
            else:
                print("Invalid meal type. Please enter Breakfast, Lunch, or Dinner.")


def main():
    """Main function to demonstrate the Mindful Meal Planner application."""
    planner = MindfulMealPlanner()
    planner.run()


if __name__ == "__main__":
    main()
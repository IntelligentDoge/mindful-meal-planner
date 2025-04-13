```python
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import random

class MindfulMealPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mindful Meal Planner")
        self.root.geometry("800x600")

        # Data storage (replace with database or file storage in a real application)
        self.recipes = {
            "Spaghetti Bolognese": {"ingredients": ["spaghetti", "ground beef", "tomato sauce", "onion", "garlic"], "dietary": ["none"], "cuisine": "Italian", "cost": 7},
            "Chicken Stir-fry": {"ingredients": ["chicken breast", "broccoli", "carrots", "soy sauce", "rice"], "dietary": ["gluten-free"], "cuisine": "Asian", "cost": 9},
            "Vegetarian Chili": {"ingredients": ["beans", "tomatoes", "corn", "peppers", "onion"], "dietary": ["vegetarian", "vegan"], "cuisine": "Mexican", "cost": 5},
            "Salmon with Roasted Vegetables": {"ingredients": ["salmon", "asparagus", "potatoes", "lemon", "olive oil"], "dietary": ["gluten-free"], "cuisine": "Mediterranean", "cost": 12}
        }
        self.user_preferences = {"dietary_restrictions": [], "cuisine_preferences": [], "budget": 0, "inventory": []}
        self.meal_plan = {}

        # UI elements
        self.create_widgets()

    def create_widgets(self):
        """Creates the main UI elements for the application."""

        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Preferences Tab
        self.preferences_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.preferences_tab, text="Preferences")
        self.create_preferences_tab(self.preferences_tab)

        # Meal Planning Tab
        self.meal_planning_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.meal_planning_tab, text="Meal Planning")
        self.create_meal_planning_tab(self.meal_planning_tab)

        # Recipe Management Tab
        self.recipe_management_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.recipe_management_tab, text="Recipe Management")
        self.create_recipe_management_tab(self.recipe_management_tab)

        # Waste Tracking Tab (Placeholder)
        self.waste_tracking_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.waste_tracking_tab, text="Waste Tracking")
        ttk.Label(self.waste_tracking_tab, text="Waste Tracking features coming soon!").pack(pady=20)


    def create_preferences_tab(self, parent):
        """Creates the UI elements for the Preferences tab."""

        # Dietary Restrictions
        ttk.Label(parent, text="Dietary Restrictions:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.dietary_options = ["vegetarian", "vegan", "gluten-free", "dairy-free"]
        self.dietary_vars = {option: tk.BooleanVar() for option in self.dietary_options}
        for i, option in enumerate(self.dietary_options):
            ttk.Checkbutton(parent, text=option, variable=self.dietary_vars[option]).grid(row=i + 1, column=0, sticky="w", padx=20)

        # Cuisine Preferences
        ttk.Label(parent, text="Cuisine Preferences:").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.cuisine_options = ["Italian", "Asian", "Mexican", "Mediterranean", "American"]
        self.cuisine_vars = {option: tk.BooleanVar() for option in self.cuisine_options}
        for i, option in enumerate(self.cuisine_options):
            ttk.Checkbutton(parent, text=option, variable=self.cuisine_vars[option]).grid(row=i + 1, column=1, sticky="w", padx=20)

        # Budget
        ttk.Label(parent, text="Budget per week:").grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.budget_var = tk.IntVar(value=50)  # Default budget
        ttk.Entry(parent, textvariable=self.budget_var).grid(row=1, column=2, padx=10)

        # Inventory
        ttk.Label(parent, text="Food on Hand (comma separated):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.inventory_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.inventory_var, width=30).grid(row=3, column=0, columnspan=2, padx=10)

        # Save Preferences Button
        ttk.Button(parent, text="Save Preferences", command=self.save_preferences).grid(row=4, column=0, columnspan=3, pady=10)

    def create_meal_planning_tab(self, parent):
         """Creates the UI elements for the Meal Planning tab."""

         # Meal Plan Display (Treeview)
         self.meal_plan_tree = ttk.Treeview(parent, columns=("Day", "Meal", "Recipe"), show="headings")
         self.meal_plan_tree.heading("Day", text="Day")
         self.meal_plan_tree.heading("Meal", text="Meal")
         self.meal_plan_tree.heading("Recipe", text="Recipe")
         self.meal_plan_tree.pack(fill="both", expand=True, padx=10, pady=10)

         # Buttons for generating and clearing the meal plan
         button_frame = ttk.Frame(parent)
         button_frame.pack(pady=5)

         ttk.Button(button_frame, text="Generate Meal Plan", command=self.generate_meal_plan).pack(side="left", padx=5)
         ttk.Button(button_frame, text="Clear Meal Plan", command=self.clear_meal_plan).pack(side="left", padx=5)

         ttk.Button(button_frame, text="Save Meal Plan", command=self.save_meal_plan).pack(side="left", padx=5)  # Add Save Meal Plan button



    def create_recipe_management_tab(self, parent):
        """Creates the UI elements for the Recipe Management tab."""

        # Recipe List (Treeview)
        self.recipe_tree = ttk.Treeview(parent, columns=("Name", "Cuisine", "Cost"), show="headings")
        self.recipe_tree.heading("Name", text="Name")
        self.recipe_tree.heading("Cuisine", text="Cuisine")
        self.recipe_tree.heading("Cost", text="Cost")
        self.recipe_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate recipe list
        self.populate_recipe_list()

        # Recipe Details Frame
        recipe_details_frame = ttk.Frame(parent)
        recipe_details_frame.pack(pady=5)

        ttk.Label(recipe_details_frame, text="Recipe Name:").grid(row=0, column=0, sticky="w", padx=5)
        self.recipe_name_var = tk.StringVar()
        ttk.Entry(recipe_details_frame, textvariable=self.recipe_name_var).grid(row=0, column=1, padx=5)

        ttk.Label(recipe_details_frame, text="Ingredients (comma separated):").grid(row=1, column=0, sticky="w", padx=5)
        self.ingredients_var = tk.StringVar()
        ttk.Entry(recipe_details_frame, textvariable=self.ingredients_var).grid(row=1, column=1, padx=5)

        ttk.Label(recipe_details_frame, text="Cuisine:").grid(row=2, column=0, sticky="w", padx=5)
        self.cuisine_choice = tk.StringVar()
        self.cuisine_choice.set(self.cuisine_options[0]) #set default value
        ttk.Combobox(recipe_details_frame, textvariable=self.cuisine_choice, values = self.cuisine_options).grid(row=2, column=1, padx=5)


        ttk.Label(recipe_details_frame, text="Dietary:").grid(row=3, column=0, sticky="w", padx=5)
        self.dietary_choice = tk.StringVar()
        self.dietary_choice.set(self.dietary_options[0])  # Set a default dietary option
        ttk.Combobox(recipe_details_frame, textvariable=self.dietary_choice, values = self.dietary_options).grid(row=3, column=1, padx=5)



        ttk.Label(recipe_details_frame, text="Cost:").grid(row=4, column=0, sticky="w", padx=5)
        self.cost_var = tk.IntVar()
        ttk.Entry(recipe_details_frame, textvariable=self.cost_var).grid(row=4, column=1, padx=5)

        # Buttons for adding, updating, and deleting recipes
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Add Recipe", command=self.add_recipe).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Recipe", command=self.update_recipe).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Recipe", command=self.delete_recipe).pack(side="left", padx=5)


    def save_preferences(self):
        """Saves the user's preferences from the UI elements."""
        try:
            self.user_preferences["dietary_restrictions"] = [option for option in self.dietary_options if self.dietary_vars[option].get()]
            self.user_preferences["cuisine_preferences"] = [option for option in self.cuisine_options if self.cuisine_vars[option].get()]
            self.user_preferences["budget"] = self.budget_var.get()
            self.user_preferences["inventory"] = [item.strip() for item in self.inventory_var.get().split(",")] if self.inventory_var.get() else []

            messagebox.showinfo("Success", "Preferences saved successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {e}")


    def generate_meal_plan(self):
        """Generates a meal plan based on user preferences and available recipes."""
        try:
            self.clear_meal_plan()  # Clear the previous meal plan

            # Filter recipes based on dietary restrictions and cuisine preferences
            eligible_recipes = []
            for recipe_name, recipe_details in self.recipes.items():
                dietary_ok = all(restriction in recipe_details["dietary"] for restriction in self.user_preferences["dietary_restrictions"]) or not self.user_preferences["dietary_restrictions"]
                cuisine_ok = recipe_details["cuisine"] in self.user_preferences["cuisine_preferences"] or not self.user_preferences["cuisine_preferences"]

                if dietary_ok and cuisine_ok:
                    eligible_recipes.append(recipe_name)

            if not eligible_recipes:
                messagebox.showinfo("Info", "No recipes match your preferences. Please adjust your settings or add more recipes.")
                return

            # Create a meal plan for 7 days (breakfast, lunch, and dinner)
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            meals = ["Breakfast", "Lunch", "Dinner"]

            total_cost = 0
            for day in days:
                for meal in meals:
                    # Randomly select a recipe from the eligible recipes
                    chosen_recipe = random.choice(eligible_recipes)
                    recipe_cost = self.recipes[chosen_recipe]["cost"]

                    # Check if adding this recipe exceeds the budget
                    if total_cost + recipe_cost <= self.user_preferences["budget"]:
                        self.meal_plan.setdefault(day, {})[meal] = chosen_recipe
                        total_cost += recipe_cost
                        self.meal_plan_tree.insert("", "end", values=(day, meal, chosen_recipe))
                    else:
                        # Find an alternative recipe within the budget
                        alternative_recipes = [recipe for recipe in eligible_recipes if self.recipes[recipe]["cost"] <= (self.user_preferences["budget"] - total_cost)]
                        if alternative_recipes:
                            chosen_recipe = random.choice(alternative_recipes)
                            recipe_cost = self.recipes[chosen_recipe]["cost"]
                            self.meal_plan.setdefault(day, {})[meal] = chosen_recipe
                            total_cost += recipe_cost
                            self.meal_plan_tree.insert("", "end", values=(day, meal, chosen_recipe))
                        else:
                            messagebox.showinfo("Info", f"Cannot generate a full meal plan within your budget. Current cost: {total_cost}, Budget: {self.user_preferences['budget']}")
                            return

            messagebox.showinfo("Success", "Meal plan generated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate meal plan: {e}")


    def clear_meal_plan(self):
        """Clears the current meal plan from the UI and the internal data structure."""
        try:
            for item in self.meal_plan_tree.get_children():
                self.meal_plan_tree.delete(item)
            self.meal_plan = {}  # Clear the internal data structure
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear meal plan: {e}")

    def add_recipe(self):
        """Adds a new recipe to the recipe list."""
        try:
            name = self.recipe_name_var.get()
            ingredients = [item.strip() for item in self.ingredients_var.get().split(",")] if self.ingredients_var.get() else []
            cuisine = self.cuisine_choice.get()
            dietary = [self.dietary_choice.get()]
            cost = self.cost_var.get()

            if not name or not ingredients or not cuisine or not cost:
                messagebox.showerror("Error", "All recipe details are required.")
                return

            if name in self.recipes:
                 messagebox.showerror("Error", "Recipe name already exists. Please use a unique name.")
                 return


            self.recipes[name] = {"ingredients": ingredients, "cuisine": cuisine, "dietary": dietary, "cost": cost}
            self.populate_recipe_list()
            messagebox.showinfo("Success", "Recipe added successfully!")
            self.clear_recipe_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add recipe: {e}")

    def update_recipe(self):
          """Updates an existing recipe in the recipe list."""
          try:
            selected_item = self.recipe_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Select a recipe to update.")
                return

            old_name = self.recipe_tree.item(selected_item[0])['values'][0]
            new_name = self.recipe_name_var.get()
            ingredients = [item.strip() for item in self.ingredients_var.get().split(",")] if self.ingredients_var.get() else []
            cuisine = self.cuisine_choice.get()
            dietary = [self.dietary_choice.get()]  # Consider handling multiple dietary options
            cost = self.cost_var.get()

            if not new_name or not ingredients or not cuisine or not cost:
                messagebox.showerror("Error", "All recipe details are required.")
                return

            if new_name != old_name and new_name in self.recipes:
                messagebox.showerror("Error", "Recipe name already exists. Please use a unique name.")
                return


            #Update in self.recipes
            if new_name != old_name:
                self.recipes[new_name] = self.recipes.pop(old_name) # rename the key

            self.recipes[new_name]["ingredients"] = ingredients
            self.recipes[new_name]["cuisine"] = cuisine
            self.recipes[new_name]["dietary"] = dietary
            self.recipes[new_name]["cost"] = cost


            self.populate_recipe_list()
            messagebox.showinfo("Success", "Recipe updated successfully!")
            self.clear_recipe_fields()

          except Exception as e:
              messagebox.showerror("Error", f"Failed to update recipe: {e}")

    def delete_recipe(self):
        """Deletes a recipe from the recipe list."""
        try:
            selected_item = self.recipe_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Select a recipe to delete.")
                return

            name = self.recipe_tree.item(selected_item[0])['values'][0]
            del self.recipes[name]
            self.populate_recipe_list()
            messagebox.showinfo("Success", "Recipe deleted successfully!")
            self.clear_recipe_fields()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete recipe: {e}")


    def populate_recipe_list(self):
        """Populates the recipe list Treeview with the current recipes."""
        try:
            for item in self.recipe_tree.get_children():
                self.recipe_tree.delete(item)

            for name, details in self.recipes.items():
                self.recipe_tree.insert("", "end", values=(name, details["cuisine"], details["cost"]))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to populate recipe list: {e}")

    def clear_recipe_fields(self):
        """Clears the recipe input fields."""
        self.recipe_name_var.set("")
        self.ingredients_var.set("")
        self.cost_var.set(0)

    def save_meal_plan(self):
        """Saves the meal plan to a file."""
        try:
            filename = "meal_plan.txt"  # Default filename
            with open(filename, "w") as file:
                for day, meals in self.meal_plan.items():
                    file.write(f"{day}:\n")
                    for meal, recipe in meals.items():
                        file.write(f"  {meal}: {recipe}\n")
            messagebox.showinfo("Success", f"Meal plan saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save meal plan: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MindfulMealPlannerApp(root)
    root.mainloop()
```
import streamlit as st  # type: ignore
import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os

# Load the environment variables
load_dotenv()

# API key and base URLs
API_KEY = "ea18c7b973154842a3f7b41e2ca655f3"
COMPLEX_SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"
FIND_BY_INGREDIENTS_URL = "https://api.spoonacular.com/recipes/findByIngredients"

# Function to fetch recipes by name or filters
def get_recipes(query, cuisine=None, diet=None, meal_type=None, number=5):
    params = {
        "query": query,
        "apiKey": API_KEY,
        "number": number,
        "cuisine": cuisine,
        "diet": diet,
        "type": meal_type,
    }
    try:
        response = requests.get(COMPLEX_SEARCH_URL, params=params)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            st.error(f"Error fetching recipes: {response.json().get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recipes: {str(e)}")
        return None

# Function to fetch recipes by ingredients
def get_recipes_by_ingredients(ingredients, number=5):
    params = {
        "ingredients": ",".join(ingredients),
        "apiKey": API_KEY,
        "number": number,
    }
    try:
        response = requests.get(FIND_BY_INGREDIENTS_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching recipes: {response.json().get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recipes: {str(e)}")
        return None

# Function to create a shopping list
def create_shopping_list(recipe_id):
    # Simulating the creation of a shopping list
    # Replace with actual data from the API
    ingredients = [
        f"Ingredient {i+1}" for i in range(5)
    ]  # Example ingredients data (replace with actual data)
    shopping_list = "\n".join(ingredients)
    return shopping_list

# Streamlit UI components
st.title("🍴AI-Powered-Recipe Finder by Ingredients APP With Abhi")

st.sidebar.title("Select Menu")
# Add girl png to sidebar
girl_png_path = "girl.png"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(girl_png_path)
except FileNotFoundError:
    st.sidebar.warning("girl.png not found. Please check the file path.")
    
# Add boy png to sidebar
boy_png_path = "boy.png"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(boy_png_path)
except FileNotFoundError:
    st.sidebar.warning("boy.png not found. Please check the file path.")

st.sidebar.title("Developer: Abhishek Kumar")
# Add my jpg to sidebar
my_jpg_path = "pic.jpg"  # Ensure this file is in the same directory as your script

try:
    # Remove use_container_width if it's causing an error
    st.sidebar.image(my_jpg_path)
except FileNotFoundError:
    st.sidebar.warning("pic.jpg not found. Please check the file path.")


# Initialize session state for shopping list
if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = {}

# Tab-based UI
tab1, tab2 = st.tabs(["🔍 Search by Recipe Name", "🥗 Search by Ingredients"])

# Tab 1: Search by Recipe Name
with tab1:
    st.header("Search Recipes by Name")
    query = st.text_input("What recipe would you like to cook?", placeholder="e.g., Biryani")

    cuisine = st.selectbox(
        "Select Cuisine:", ["Any", "Italian", "Mexican", "Indian", "Chinese", "French", "Thai", "Greek"]
    )
    diet = st.selectbox(
        "Select Diet:", ["Any", "Vegetarian", "Vegan", "Gluten Free", "Ketogenic", "Pescatarian"]
    )
    meal_type = st.selectbox(
        "Select Meal Type:", ["Any", "Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]
    )

    cuisine = None if cuisine == "Any" else cuisine
    diet = None if diet == "Any" else diet
    meal_type = None if meal_type == "Any" else meal_type

    if st.button("Search Recipes", key="search_name"):
        if query.strip():
            recipes = get_recipes(query, cuisine, diet, meal_type)
            if recipes:
                for recipe in recipes:
                    st.subheader(recipe["title"])
                    st.image(recipe["image"], width=300)

                    # View details section
                    st.markdown(
                        f"[**View Details**](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']})",
                        unsafe_allow_html=True,
                    )

                    # Shopping list generator (instant generation)
                    if st.button(f"Generate Shopping List for {recipe['title']}", key=f"generate_shopping_list_{recipe['id']}"):
                        # Generate shopping list and store it in session state
                        shopping_list = create_shopping_list(recipe["id"])
                        st.session_state.shopping_list[recipe["id"]] = shopping_list
                        st.success("Shopping list generated!")

                    # Show the generated shopping list immediately if available
                    if recipe["id"] in st.session_state.shopping_list:
                        st.subheader("Generated Shopping List:")
                        st.text(st.session_state.shopping_list[recipe["id"]])
            else:
                st.warning("No recipes found. Try different input or filters.")
        else:
            st.warning("Please enter a recipe name.")

# Tab 2: Search by Ingredients
with tab2:
    st.header("Search Recipes by Ingredients")
    ingredients_input = st.text_input(
        "Enter ingredients (comma-separated):", placeholder="e.g., chicken, rice, onion"
    )

    if st.button("Find Recipes by Ingredients", key="search_ingredients"):
        if ingredients_input.strip():
            ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",")]
            recipes = get_recipes_by_ingredients(ingredients)
            if recipes:
                for recipe in recipes:
                    st.subheader(recipe["title"])
                    st.image(recipe["image"], width=300)

                    # View details section
                    st.markdown(
                        f"[**View Details**](https://spoonacular.com/recipes/{recipe['title'].replace(' ', '-').lower()}-{recipe['id']})",
                        unsafe_allow_html=True,
                    )

                    # Shopping list generator (instant generation)
                    if st.button(f"Generate Shopping List for {recipe['title']}", key=f"generate_shopping_list_{recipe['id']}"):
                        # Generate shopping list and store it in session state
                        shopping_list = create_shopping_list(recipe["id"])
                        st.session_state.shopping_list[recipe["id"]] = shopping_list
                        st.success("Shopping list generated!")

                    # Show the generated shopping list immediately if available
                    if recipe["id"] in st.session_state.shopping_list:
                        st.subheader("Generated Shopping List:")
                        st.text(st.session_state.shopping_list[recipe["id"]])
            else:
                st.warning("No recipes found. Try different ingredients.")
        else:
            st.warning("Please enter some ingredients.")

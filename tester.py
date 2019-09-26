import requests
 
def getRecipeById(id):

    headers={
    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "39e0d510a6msh2032e3c2a8dae62p1d2202jsn13bf3a0ce7dd"
  }
    endpoint = f" https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/products/{id}"
    r = requests.get(endpoint, headers = headers)
    results = r.json()
    print(results)
    return results

def searchRecipes(query):
    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    headers={
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "39e0d510a6msh2032e3c2a8dae62p1d2202jsn13bf3a0ce7dd"
        }
    params = { 
        'query' :query,
        'number' : 2
     }
    r = requests.get(endpoint,params = params, headers = headers)
    results = r.json()
    print(results)
    return results

def filterbyCuisine(cuisine):
    endpoint="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    headers = {
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "39e0d510a6msh2032e3c2a8dae62p1d2202jsn13bf3a0ce7dd"
    }
    params = {
        'cuisine' : cuisine,
        'number'  : 2
    }
    r = requests.get(endpoint,params = params, headers = headers)
    results = r.json()
    print(results)
    return results

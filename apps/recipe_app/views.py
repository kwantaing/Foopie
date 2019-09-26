from django.shortcuts import render, HttpResponse, redirect
from .models import User, Recipe, myRecipe
from django.contrib import messages
import bcrypt
import requests

def getRecipeById(id):

    headers={
    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "70cfe9b480msh6003ae8a99fd83fp1a0e1djsn2384d115aca9"
  }
    endpoint = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{id}/information"
    r = requests.get(endpoint, headers = headers)
    results = r.json()
    return results

def searchRecipes(query):
    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    headers={
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "70cfe9b480msh6003ae8a99fd83fp1a0e1djsn2384d115aca9"
        }
    params = { 
        'query' :query,
        'number' : 10
     }
    r = requests.get(endpoint,params = params, headers = headers)
    results = r.json()
    return results

def randomrecipe():
    endpoint="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"
    headers = {
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "70cfe9b480msh6003ae8a99fd83fp1a0e1djsn2384d115aca9"
    }
    r = requests.get(endpoint,headers = headers)
    results = r.json()
    return results

def filterbyCuisine(cuisine):
    endpoint="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search"
    headers = {
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "70cfe9b480msh6003ae8a99fd83fp1a0e1djsn2384d115aca9"
    }
    params = {
        'cuisine' : cuisine,
        'number'  : 10
    }
    r = requests.get(endpoint,params = params, headers = headers)
    results = r.json()
    return results

def jokes():
    endpoint="https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/jokes/random"
    headers = {
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "70cfe9b480msh6003ae8a99fd83fp1a0e1djsn2384d115aca9"
    }
    r = requests.get(endpoint, headers=headers)
    jokes = r.json()
    return jokes
# Create your views here.
def index(request):
    return render(request, 'index.html')


def browse(request,cuisine):
    context = {
        'user': User.objects.get(id=request.session["id"]),
        "recipes" : filterbyCuisine(cuisine)["results"]
    }
    return render(request, 'browse.html', context)

def test(request):
    context = {
        'recipes' : filterbyCuisine('cambodian')["results"]
    }
    return render(request, 'test.html',context)

def showrecipe(request,id):
    context = {
        'user': User.objects.get(id=request.session["id"]),
        'recipe' : getRecipeById(int(id))
    }
    return render(request,'detail.html',context)

def search(request):
    search = request.POST["search"]
    context = {
        'user': User.objects.get(id=request.session["id"]),
        'recipes' : searchRecipes(search)["results"]
    }
    return render(request, 'browse.html',context)

def surprise(request):
    context = {
        'user': User.objects.get(id=request.session["id"]),
        'recipe' :randomrecipe()["recipes"][0]
    }
    return render(request,'detail.html',context)

def home(request):
    if not "id" in request.session:
        return redirect('/')
    else:
        print(request.session["id"])
        context={
            'user': User.objects.get(id=request.session["id"]),
            'joke' : jokes()["text"],
            'featured1' : randomrecipe()["recipes"][0],
            'featured2' : randomrecipe()["recipes"][0],
            'featured3' : randomrecipe()["recipes"][0],
            'featured4' : randomrecipe()["recipes"][0]
        }
        return render(request, 'home.html',context)


def register(request):
    print("Errors include:")       
    errors = User.objects.register_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.warning(request,value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST["pw"].encode(),bcrypt.gensalt())
        print(hashedpw)
        User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email = request.POST["email"],password = hashedpw)
        request.session["id"]= User.objects.last().id
        return redirect('/welcome')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        request.session["id"] = User.objects.get(email = request.POST["email"]).id
    return redirect('/welcome')

def logout(request):
    del request.session["id"]
    return redirect('/')

def profile(request):
    if "id" not in request.session:
        return redirect('/')
    else:
        context = {
            'user' : User.objects.get(id=request.session["id"]),
        }
        return render(request, "profile.html", context )

def addtoFavorite(request):
    recipe_id = request.POST["recipe_id"]
    title = request.POST["title"]
    instructions = request.POST["instructions"]
    image = request.POST["image"]
    readyInMinutes = request.POST["readyInMinutes"]
    print("RecipeID:",recipe_id)
    print("Title:",title)
    print("Instructions",instructions)
    print("Image",image)
    newfav = Recipe.objects.create(recipe_id = recipe_id, title = title, instructions = instructions, image = image, readyInMinutes = readyInMinutes)
    user = User.objects.get(id=request.session["id"]).favorites.add(newfav)
    return redirect('/profile')

def removefav(request,id):
    user = User.objects.get(id=request.session["id"])
    fav = Recipe.objects.get(id = id)
    user.favorites.remove(fav)
    return redirect('/profile')

def editfav(request,id):
    context = {
        'recipe'  : Recipe.objects.get(id=id)
    }
    return render(request,'edit_fav.html',context)

def add(request):
    new_recipe = myRecipe.objects.create(title=request.POST["title"], servings = request.POST["serving_size"], readyInMinutes=request.POST["readyInMinutes"], ingredients = request.POST["ingredients"], instructions = request.POST["instructions"])
    User.objects.get(id=request.session["id"]).myrecipes.add(new_recipe)
    context = {
        'user' :User.objects.get(id=request.session["id"]),
        'recipe' :myRecipe.objects.last()
    }

    return render(request,'detail.html', context)

def new(request):
    return render(request,'add_recipe.html')

def removeRecipe (request, id):
    user=User.objects.get(id=request.session["id"])
    myrecipe = myRecipe.objects.get(id=id)
    user.myrecipes.remove(myrecipe)
    return redirect('/profile')

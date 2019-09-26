from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import bcrypt
import re

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# Create your models here.
class Reg_Manager(models.Manager):
    def register_validator(self,postData):
        errors = {}
        isValid = True
        if(len(postData["pw"])<8 or len(postData["pwconfirm"])<8):
            errors["password"] = "Please make a valid password over 8 characters"
            isValid = False
        if(postData["pw"]!=postData["pwconfirm"]):
            errors["pwconfirm"] = "Passwords do not match"
            isValid = False
        if len(postData["first_name"])< 2:
            errors["first_name"] = "First Name should be at least 2 characters"
            isValid = False
        if len(postData["last_name"])< 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
            isValid = False
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"
            isValid = False

        users = User.objects.filter(email=postData["email"])
        print("Users with the same email:",len(users)-1)
        if len(users)>0:
            errors["email"]= "email is already registered"
            isValid = False
            
        print(errors)
        return errors
    def login_validator(self,postData):
        errors = {}
        isValid = True
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email"
            isValid = False
        if(len(postData["password"])<1):
            errors["password"] = "wrong password, try again"
            isValid = False
        if isValid == False:
            return errors
        while True:
            try:
                current_user = User.objects.get(email=postData["email"])
                hashedpw = current_user.password.encode()
                print("Hashed Password:",hashedpw)
                if bcrypt.checkpw(postData["password"].encode(),hashedpw):
                    print("password match")
                    break
                else:
                    print("wrong password")
                    errors["password"] = "wrong password, try again"
                    isValid = False
                    break
            except ObjectDoesNotExist:
                    print("unregistered email")
                    errors["unregistered"]= "Email is not registered"
                    isValid = False
                    break
        return errors

        
        

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField()
    password = models.CharField(max_length = 45)
    pwconfirm = models.CharField(max_length = 45)
    created_on = models.DateField(auto_now_add = True)
    objects = Reg_Manager()

    def __str__(self):
        return f"{self.email}"
    
class Recipe(models.Model):
    recipe_id = models.IntegerField()
    title = models.CharField(max_length = 225)
    instructions = models.TextField()
    image = models.URLField()
    readyInMinutes = models.IntegerField()
    favoritedby = models.ManyToManyField(User,related_name = "favorites")

class myRecipe(models.Model):
    title = models.CharField(max_length = 225)
    instructions = models.TextField()
    image = models.URLField()
    readyInMinutes = models.IntegerField()
    servings = models.IntegerField()
    ingredients = models.TextField()
    createdby = models.ManyToManyField(User,related_name = "myrecipes")
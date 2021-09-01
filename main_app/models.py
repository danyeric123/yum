from datetime import date, datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Recipe(models.Model):
  api = IntegerField()
  name = TextField()
  owner = ManyToManyField(User)

class Photo(models.Model):
  user = ForeignKey(User,on_delete=CASCADE)
  url = CharField(max_length=250)
  recipe_id = CharField(max_length=250)

class Review(models.Model):
  author = ForeignKey(User,on_delete=CASCADE)
  content=TextField()
  rating = IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
  recipe_id= IntegerField()
  created_at = DateTimeField(auto_now=True)
  photos = ForeignKey(Photo,on_delete=CASCADE,blank=True, null=True)
  

class Item(models.Model):
  name = CharField(max_length=250)
  aisle = CharField(max_length=250)
  purchased = BooleanField(default=False)
  recipe_id= IntegerField()

class ShoppingList(models.Model):
  user = ForeignKey(User,on_delete=CASCADE)
  items = ManyToManyField(Item,blank=True)
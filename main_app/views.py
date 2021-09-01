from main_app.forms import ReviewForm
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import *
import uuid
import boto3
import requests
import json
import environ
env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

class Home(LoginView):
  template_name = 'home.html'
  
@login_required
def shopping_list_index(request):
  shopping_lists = ShoppingList.objects.filter(user=request.user)
  return render(request, 'main_app/shopping_lists.html', { 'shopping_lists': shopping_lists })

class RecipeList(LoginRequiredMixin,ListView):
  model = Recipe
  
  def get_queryset(self):
      queryset = Recipe.objects.filter(owner= self.request.user)
      return queryset

class RecipeDelete(LoginRequiredMixin,DeleteView):
  model = Recipe

class ShoppingListDetail(LoginRequiredMixin,DetailView):
  model = ShoppingList
  
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["items"] = self.object.items.all()
      return context

def shopping_list(request):
  shopping_list,_ = ShoppingList.objects.get_or_create(user=request.user)
  items = shopping_list.items.all()
  return render(request,'shopping_list.html',{"items":items})
  
class ItemDelete(LoginRequiredMixin,DeleteView):
  model=Item
  success_url = '/shopping_list/'

def add_recipe(request):
  recipe,_ = Recipe.objects.get_or_create(
    api=request.POST.get("api"),
    name=request.POST.get("name")
    )
  recipe.owner.add(request.user)
  return redirect('recipe_list')
  
def about(request):
  return render(request, 'about.html')

# class ReviewCreate(LoginRequiredMixin,CreateView):
#   model = Review
#   fields = ['content','rating']
  
#   def form_valid(self, form):
#     # Assign the logged in user (self.request.user)
#     form.instance.user = self.request.user  # form.instance is the cat
#     # Let the CreateView do its job as usual
#     return super().form_valid(form)

def add_review(request,recipe_id):
  form = ReviewForm(request.POST)
  
  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.recipe_id = recipe_id
    new_review.author = request.user
    new_review.save()
  return redirect('recipe_detail',id=recipe_id)

def search_recipe(request):
  parameters = {
    'apiKey': API_KEY,
    'query': request.GET.get('query'),
    'addRecipeInformation': 'true'
  }
  
  recipes = requests.get(
    'https://api.spoonacular.com/recipes/complexSearch',
    parameters
  ).json()["results"]
  
  return render(request,'search.html',{"recipes":recipes})

def get_recipe(request,id):
  parameters = {
    'apiKey': API_KEY,
  }
  
  recipe = requests.get(
    f'https://api.spoonacular.com/recipes/{id}/information',
    parameters
  ).json()
  
  review_form = ReviewForm()
  
  reviews = Review.objects.filter(recipe_id=id)
  photos = Photo.objects.filter(recipe_id=id)
  
  context = {
    "reviews": reviews,
    "recipe": recipe,
    "form": review_form,
    "photos":photos
  }
  
  return render(request,'recipe_detail.html', context)

def add_to_shopping_list(request,recipe_id):
  # ingredients = request.POST.dict()
  # del ingredients["csrfmiddlewaretoken"]
  # items = []
  # count = 0
  # item = {}
  # for ingredient in ingredients.keys():
  #   if count%2:
  #     item = {}
  #     item["name"] = ingredient
  #     item["recipe_id"] = recipe_id
  #   else:
  #     item["aisle"] = ingredient
  #   items.append(item)
  #   count+=1
  # items_db = []
  # for item in items:
  #   item_db = Item.objects.create(name=item["name"],aisle=item["aisle"],recipe_id=item["recipe_id"])
  #   items_db.append(item_db)
  # print(items_db)
  # new_shopping_list = ShoppingList.objects.create(user=request.user)
  # for item in items_db:
  #   new_shopping_list.items.add(item.id)
  parameters = {
    'apiKey': API_KEY,
  }
  
  recipe_ingredients = requests.get(
    f'https://api.spoonacular.com/recipes/{recipe_id}/information',
    parameters
  ).json()["extendedIngredients"]
  
  items = []
  for ingredient in recipe_ingredients:
    item, _ = Item.objects.get_or_create(
      name=ingredient["originalName"],
      aisle=ingredient["aisle"],
      recipe_id=recipe_id
    )
    items.append(item)
  print(items)
  new_shopping_list, _ = ShoppingList.objects.get_or_create(user=request.user)
  for item in items:
    new_shopping_list.items.add(item.id)
  
  return redirect('recipe_detail',id=recipe_id)

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'my-yum-bucket'


@login_required
def add_photo(request, recipe_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      Photo.objects.get_or_create(url=url, recipe_id=recipe_id,user=request.user)
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('recipe_detail', id=recipe_id)

def convert(obj):
  text = json.dumps(obj, sort_keys=True, indent=2)
  print(text)
  
from django.urls import path
from . import views

urlpatterns = [
  path('', views.Home.as_view(), name='home'),
  path('accounts/signup/', views.signup, name='signup'),
  path('about/', views.about,name='about'),
  path('recipes/<int:id>/',views.get_recipe,name='recipe_detail'),
  path('search/',views.search_recipe,name="search"),
  path('reviews/<int:recipe_id>/',views.add_review,name="add_review"),
  path('add_to_shopping_list/<int:recipe_id>/',views.add_to_shopping_list,name="add_to_shopping_list"),
  path('shopping_list/',views.shopping_list,name="shopping_list"),
  path('item/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),
  path('recipes/',views.RecipeList.as_view(),name='recipe_list'),
  path('recipe/<int:pk>/delete/',views.RecipeDelete.as_view(),name='recipe_delete'),
  path('recipe/add',views.add_recipe,name='add_recipe'),
  path('photo/<int:recipe_id>',views.add_photo,name="add_photo")
]
from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('resep/', views.RecipeListView.as_view(), name='list-resep'),
    path('resep/<int:pk>/', views.RecipeDetailView.as_view(), name='detail-resep'),
    path('resep/tambah-resep/',views.CreateRecipeView.as_view(),name='tambah-resep'),
    path('resep/resep-saya', views.MyRecipesListView.as_view(), name='resep-saya'),
    path('resep/hapus/<int:pk>/', views.RecipeDeleteView.as_view(), name='hapus-resep'),
    path('resep/edit/<int:pk>/', views.RecipeEditView.as_view(), name='edit-resep'),
    path('resep/favorit/', views.MyFavouritesListView.as_view(), name='resep-favorit'),

    path('resep-external/', views.ExternalRecipesView.as_view(), name='resep-external'),
    path('resep-external/<int:idMeal>', views.ExternalDetailView.as_view(), name='detail-resep-external'),
]
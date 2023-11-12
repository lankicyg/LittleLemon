from django.urls import path
from . import views

urlpatterns = [
    #path('books', views.books),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:id>', views.single_item),
    path('categories', views.CategoriesView.as_view()),
]
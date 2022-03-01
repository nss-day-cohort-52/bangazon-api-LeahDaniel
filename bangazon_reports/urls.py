from django.urls import path

from .views import ExpensiveProductList, InexpensiveProductList

urlpatterns = [
    path('expensive', ExpensiveProductList.as_view()),
    path('inexpensive', InexpensiveProductList.as_view()),
]
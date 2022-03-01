from django.urls import path

from .views import (CompleteOrderList, ExpensiveProductList,
                    IncompleteOrderList, InexpensiveProductList,
                    UserFavoriteList)

urlpatterns = [
    path('expensive', ExpensiveProductList.as_view()),
    path('inexpensive', InexpensiveProductList.as_view()),
    path('incomplete', IncompleteOrderList.as_view()),
    path('complete', CompleteOrderList.as_view()),
    path('favorites', UserFavoriteList.as_view()),
]

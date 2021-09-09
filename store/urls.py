from django.urls import path

from .views import ClientsList, ClientDetail, ProductsList, ProductDetail, BillsList, BillDetail, ClientRecords, \
    ClientLoader

urlpatterns = [
    path('clients/', ClientsList.as_view()),
    path('client/<int:pk>/', ClientDetail.as_view()),
    path('client/records/', ClientRecords.as_view()),
    path('clients/loader/', ClientLoader.as_view()),
    path('products/', ProductsList.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    path('bills/', BillsList.as_view()),
    path('bill/<int:pk>/', BillDetail.as_view()),
]

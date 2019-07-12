from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    #trigger the home_page function in view.py
    path('create/', views.create, name='create'),
    #yourapp.com/create - map url to your python function (in views)
    ##make sure you hsve the correct slash. not / this but this \
    #name='' is used so in create-modal, we have lines like
    #<form action="{% url 'create' %}" method="post">
    #which refers to name='create' and thus this url path
    path('edit/<str:movie_id>', views.edit, name='edit'),
    #if you go to yourapp.com/edit/rec9ypbL2u5y76S0T
    #the rec9ypbL2u5y76S0T if the 'id' field of the movie we're editing
    #this part of the url (<str:movie_id>) says this is a dynamically genereated slug thats going to be created by the user
    #(who decides which movie to edit)
    #movie_id gets passed as an arugement to view.edit
    path('delete/<str:movie_id>', views.delete, name='delete'),

]

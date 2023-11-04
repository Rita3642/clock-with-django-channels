from django.urls import path
from . import views

urlpatterns = {
    path('', views.reloj, name='reloj')
}

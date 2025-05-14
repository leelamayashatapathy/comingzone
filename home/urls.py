from django.urls import path
from .views import index,get_data
from.views import BookView,UserApi,RegistrationView,LoginView


urlpatterns = [
    path('api/',index,name='api'),
    path('api/manage-data/',get_data, name='posta'),
    path('api/manage-data/<int:id>/',get_data, name='posta'),
    
    
    ####
    path('api/books/',BookView.as_view(),name="books"),
    path('api/user/',UserApi.as_view(),name="create-user"),
    
    
    ####
    path('api/register/',RegistrationView.as_view(),name='register'),
    path('api/login/',LoginView.as_view(),name='login'),
    
    
    
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('sing-in',views.sign_in, name='sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('about-us', views.about_us, name='about_us'),
    path('writer-home-page', views.writer_home_page, name='writer_home_page'),
    path('reader-home-page', views.reader_home_page, name='reader_home_page'),
]

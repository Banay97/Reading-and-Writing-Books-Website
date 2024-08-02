from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('sing-in',views.sign_in, name='sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('about-us', views.about_us, name='about_us'),
    path('writer-home-page', views.writer_home_page, name='writer_home_page'),
    path('reader-home-page', views.reader_home_page, name='reader_home_page'),
    path('writer-profile-page', views.writer_profile, name='writer_profile'),
    path('reader-profile-page', views.reader_profile, name='reader_profile'),
    path('edit-reader-profile-page', views.edit_reader_profile, name='edit_reader_profile'),
    path('edit-writer-profile-page', views.edit_writer_profile, name='edit_writer_profile'),
    path('create-book', views.create_book, name='create_book'),
    path('edit-book', views.edit_book, name='edit_book'),
    path('delete-book', views.delete_book, name='delete_book'),
    path('create-event', views.create_event, name='create_event'),
    path('edit-event', views.edit_event, name='edit_event'),
    path('delete-event', views.delete_event, name='delete_event'),
    path('view-book', views.view_book_detail, name='view_book_detail'),
    path('view-event', views.view_event_detail, name='view_event_detail'),
]

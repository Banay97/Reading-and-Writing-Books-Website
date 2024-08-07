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
#Edit User's Profile paths     
    path('edit-reader-profile-page/<int:user_id>', views.edit_reader_profile, name='edit_reader_profile'),
    path('edit-writer-profile-page/<int:user_id>', views.edit_writer_profile, name='edit_writer_profile'),
#BOOK CRUD paths
    path('create-book', views.create_book, name='create_book'),
    path('books', views.books, name='books'),
    path('edit-book/<int:book_id>', views.edit_book , name='edit_book'),
    path('view-book-detail/<int:book_id>/', views.view_book_detail, name='view_book_detail'),
    path('delete-book/<int:book_id>', views.delete_book, name='delete_book'),
#Event CRUD paths
    path('create-event', views.create_event, name='create_event'),
    path('edit-event', views.edit_event, name='edit_event'),
    path('delete-event', views.delete_event, name='delete_event'),
    path('view-event', views.view_event_detail, name='view_event_detail'),
#Creating new account, Login to the created account, and log out from the account paths.    
    path('create-account', views.create_account, name='create_account'),
    path('enter-your-account', views.enter_your_account, name='enter_your_account'),
    path('sign-out', views.sign_out, name='sign_out'),

    path('reader-posts', views.reader_posts, name='reader_posts'),
    path('delete-reader-post/<int:post_id>', views.delete_reader_post, name='delete_reader_post'),
    path('post-reader-comment/<int:id>', views.post_reader_comment, name='post_reader_comment'),
    path('delete-reader-comment/<int:comment_id>', views.delete_reader_comment, name='delete_reader_comment'),
    
]

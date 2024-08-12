from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('sing-in',views.sign_in, name='sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    
    path('about-us', views.about_us, name='about_us'),
    path('all-books-page', views.all_books_page, name='all_books_page'),
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
    path('view-book/<int:book_id>/', views.view_book, name='view_book'),
    path('delete-book/<int:book_id>', views.delete_book, name='delete_book'),
    
#Event CRUD paths
    path('create-event', views.create_event, name='create_event'),
    path('view-event/<int:event_id>', views.view_event, name='view_event'),
    path('events', views.events, name='events'),
    path('edit-event/<int:event_id>', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>', views.delete_event, name='delete_event'),
    
#Creating new account, Login to the created account, and log out from the account paths.    
    path('create-account', views.create_account, name='create_account'),
    path('enter-your-account', views.enter_your_account, name='enter_your_account'),
    path('sign-out', views.sign_out, name='sign_out'),

    path('create-posts', views.create_posts, name='create_posts'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('post_comment/<int:id>', views.post_comment, name='post_comment'), #post comment path
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),#delete comment path 
    
    
#Book Club CRUD paths
    path('create-book-club', views.create_book_club, name='create_book_club'),
    path('view-book-club/<int:id>/', views.view_book_club, name='view_book_club'),
    path('clubs', views.clubs, name='clubs'),
    path('edit-book-club/<int:book_club_id>', views.edit_book_club, name='edit_book_club'),
    path('delete-book-club/<int:book_club_id>', views.delete_book_club, name='delete_book_club'), 
    
    
#homePage CRUD paths
    # path('post-home', views.home_page_create_posts, name='home_page_create_posts'),   
    # path('delete-home', views.home_page_delete_post, name='home_page_delete_post'),  
    # path('home-post-comment/<int:id>', views.home_page_post_comment, name='home_page_post_comment'), #post comment path
    # path('home-delete-comment/<int:comment_id>', views.home_page_delete_comment, name='home_page_delete_comment'),#delete comment path 
    
#Adding Books and Likes paths
    # path('add-book-to-library/<int:book_id>', views.add_book_to_library, name='add_book_to_library'),
    # path('like-book/<int:book_id>', views.like_book, name='like_book'), 
    path('reader-posts',views.post_post, name='reader_posts'), 
    path('delete-reader-posts/<int:post_id>', views.delete_reader_post,name='delete_reader_post'),
    path('post-reader-comment/<int:id>',views.post_reader_comment, name='post_reader_comment'),
    path('delete-reader-comment/<int:comment_id>', views.delete_reader_comment, name='delete_reader_comment'),
    path('show-posts',views.show_post_home_page,name='show_post_home_page'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),


]

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
import bcrypt
from .models import User, Book, Notification, Post, Event, BookClub, Comment


# Create your views here.
def home(request):#rendering to the Home Page of the website
    return render(request, 'HomePage.html')

def sign_in(request):#rendering to the Sign In Page of the website and saving the current user info in the session
    # current_user = User.objects.get(username=request.session['username'])
    return render(request, 'SignInPage.html')

def sign_up(request):#rendering to the Sign Up Page of the website and saving the current user info in the session
    # current_user = User.objects.get(username=request.session['username'])
    return render(request, 'SignUpPage.html')

def about_us(request):#rendering to the about us page
    
    #here I have to add a functionality for the comment section in this page to store it in my database.
    context ={ 
    }
    
    return render(request, 'AboutUsPage.html', context)

def all_books_page(request):
    books = Book.objects.all()
    return render(request, 'allBooksPage.html', {'books':books} )

def get_home_page_context(username):
    current_user = User.objects.get(username=username)  # Get the user data descending to the username
    post = Post.objects.all().order_by('-created_at')  # Get all the posts in ascending order
    comment = Comment.objects.all().order_by('created_at')  # Get all the comments in ascending order
    event = Event.objects.all().order_by('created_at')  # Get all the events
    book_club = BookClub.objects.all().order_by('created_at')  # Get all the book clubs
    books = Book.objects.all()
    context = {
        'user': current_user,
        'post': post,
        'comment': comment,
        'event': event,
        'book_club': book_club,
        'book':books,
    }
    
    return context

def writer_home_page(request):#this will render to the writer home page when the user is logged in and check the permissions of the user
    #also making sure that all th user info, posts, and comments,events, and book clubs are added to his/her home page
    if 'username' not in request.session:
        return render(request, 'SignInPage.html')

    context = get_home_page_context(request.session['username'])
    return render(request, 'WriterHomePage.html', context)

def reader_home_page(request):#this will render to the reader home page when the user is logged in and check the permissions of the user
    #also making sure that all th user info, posts, and comments,events, and book clubs are added to his/her home page
    # user_posts = Post.objects.filter(user=request.user.username).order_by('-created_at')

    if 'username' not in request.session:
        return render(request, 'signInPage.html')
    
    context = get_home_page_context(request.session['username'])
    return render(request, 'ReaderHomePage.html',  context)



def writer_profile(request):
    books= Book.objects.all()
    if 'username' not in request.session:
        return render(request, 'WriterProfile.html')
    
    context = get_home_page_context(request.session['username'])
    return render(request, 'WriterProfile.html', context)

def reader_profile(request):
    if 'username' not in request.session:
        return render(request, 'ReaderProfile.html')
    
    context = get_home_page_context(request.session['username'])
    return render(request, 'ReaderProfile.html', context)

def edit_reader_profile(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_writer_profile')
            return redirect('edit_reader_profile', user_id=user_id)
        
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']
            
            # Update user information
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.bio = bio
            
            user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('reader_profile')  # Adjust this to the actual view name
    return render(request, 'EditReaderProfilePage.html', {'user': user})

def edit_writer_profile(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_writer_profile')
            return redirect('edit_writer_profile', user_id=user_id)
        
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            bio = request.POST['bio']
            
            # Update user information
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.bio = bio
            
            user.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('writer_profile')  # Adjust this to the actual view name
        
    return render(request, 'EditWriterProfilePage.html', {'user': user})


#----Book Functions----
def books(request):
    book = Book.objects.all() #query to return a QuerySet of all book objects
    print(book)
    return render(request,'WriterProfile.html', {'books': book})

def create_book(request):
    if request.method == 'POST':
        # Validate the input data
        errors = Book.objects.book_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='create_book')
            return redirect('create_book')
        else:
            title = request.POST.get('title')
            genre = request.POST.get('genre')
            description = request.POST.get('description')
            book_file = request.FILES.get('book_file')

            # Check for existing book with the same title
            if Book.objects.filter(title=title).exists():
                messages.error(request, 'Book with the same title already exists')
                return redirect('create_book')

            # Ensure 'username' is in session and get the user
            if 'username' not in request.session:
                messages.error(request, 'You must be logged in to create a book')
                return redirect('sign_in')  # Adjust this to your login URL

            # Fetch the user associated with the username in the session
            user = User.objects.get(username=request.session['username'])

            # Create the book and assign the author
            book = Book.objects.create(title=title, genre=genre, description=description, book_file=book_file, author=user)

            messages.success(request, 'Book created successfully')
            return redirect( 'writer_profile')

    # For GET request, initialize `book` to an empty dictionary or a default value
    return render(request, 'CreateBook.html', {'book': {}})


def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_book')
            return redirect('edit_book', book_id=book_id)
        else:
            title = request.POST['title']
            genre = request.POST['genre']
            description = request.POST['description']
            book_file = request.FILES.get('book_file')
            book.title =title
            book.genre = genre
            book.description = description
            if book_file:
                book.book_file = book_file
                book.save()
                messages.success(request, 'Book updated successfully')
                return redirect('books') 
    return render(request, 'EditBook.html', {'book': book})

def view_book(request, book_id):
    print(f"book_id: {book_id}")
    book = Book.objects.get(id=book_id)
    return render(request, 'ViewBookPage.html', {'book': book})


def delete_book(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
    # book =Book.objects.get(id=book_id)
    # book.delete()
    # messages.success(request, 'Book deleted successfully')
    # return redirect('books')

def events(request):
    event = Event.objects.all() #query to return a QuerySet of all event objects
    return render(request,'WriterProfile.html', {'event': event})

# ---- Events Functions----
def create_event(request):
    if request.method == 'POST':
        errors = Event.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='create_event')
            return redirect('create_event')

        event_name = request.POST['event_name']
        event_date = request.POST['event_date']
        event_content = request.POST['event_content']
        book_club_id = request.POST.get('book_club')

        # Ensure 'username' is in session and get the user
        if 'username' not in request.session:
            messages.error(request, 'You must be logged in to create an event')
            return redirect('sign_in')  # Adjust this to your login URL

        user = User.objects.get(username=request.session['username'])
        book_club = BookClub.objects.get(id=book_club_id)

        # Create the event and assign the user
        event = Event.objects.create(event_name=event_name, event_date=event_date, event_content=event_content, created_by=user, book_club=book_club)

        messages.success(request, 'Event created successfully')
        return render(request, 'CreateEvent.html')  
    
    # Handle GET request
    book_clubs = BookClub.objects.all()  # Fetch all book clubs for the dropdown
    return render(request, 'CreateEvent.html', {'event': {}, 'book_clubs': book_clubs})
    
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        errors = Event.objects.event_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_event')
            return redirect('edit_event', book_id=event_id)
        else:
            event_name = request.POST['event_name']
            event_date = request.POST['event_date']
            event_content = request.POST['event_content']
            book_file = request.FILES.get('book_file')
            event.event_name =event_name
            event.event_date = event_date
            event.event_content = event_content
            event.save()
            messages.success(request, 'Book updated successfully')
            return redirect('events') 
    return render(request, 'EditEvent.html', {'event': event})

def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    messages.success(request, 'Book Event deleted successfully')
    return redirect('events')

def view_event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'ViewEventDetails.html', {'event': event})



# ---- Book Club Functions ----
def create_book_club(request):
    if request.method == 'POST':
        errors = BookClub.objects.book_club_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='create_book_club')
            return redirect('create_book_club')
        else:
            club_name = request.POST['club_name']
            club_content = request.POST['club_content']
            club_type = request.POST['club_type']

            user = User.objects.get(username=request.session['username'])
            book_club = BookClub.objects.create(club_name=club_name, club_content=club_content, club_type=club_type, owner=user)

            messages.success(request, 'Book club created successfully')
            return redirect('writer_profile')  
    else:
        return render(request, 'CreateBookClub.html')
    
def view_book_club(request, id):
    club = BookClub.objects.get(id=id)
    return render(request, 'ViewBookClub.html', {'club': club})

def edit_book_club(request, book_club_id):
    club = BookClub.objects.get(id=book_club_id)
    if request.method == 'POST':
        errors = BookClub.objects.book_club_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='edit_book_club')
            return redirect('edit_book_club', book_club_id=book_club_id)
        else:
            club_name = request.POST['club_name']
            club_content = request.POST['club_content']
            club_type = request.POST['club_type']
            club.club_name = club_name
            club.club_content = club_content
            club.club_type = club_type
            club.save()
            messages.success(request, 'Book club updated successfully')
            return redirect('writer_profile')
    else:
        return render(request, 'EditBookClub.html', {'club': club}) 
    
def delete_book_club(request, book_club_id):
    club = BookClub.objects.get(id=book_club_id)
    club.delete()
    messages.success(request, 'Book club deleted successfully')
    return redirect('writer_profile')   

def clubs(request):
    book_clubs = BookClub.objects.all()
    return render(request, 'WriterProfile.html', {'book_clubs': book_clubs})  
            

#---- Create account function ------
def create_account(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='sign_up')
            return redirect('sign_up')
        else:
            First_name = request.POST['first_name']
            Last_name = request.POST['last_name']
            username = request.POST['username']
            role = request.POST.get('role')
            date_of_birth = request.POST.get('date_of_birth')
            email = request.POST['email']
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            user = User.objects.create(
                first_name=First_name,
                last_name=Last_name,
                username=username,
                role=role,
                date_of_birth= date_of_birth,
                email=email,
                password=hashed_password
            )
            user.save()
            if user.role == 'writer':
                messages.success(request, 'Registration successful! Please log in.')
                return render(request, 'WriterHomePage.html', {'user': user})
            else:
                messages.success(request, 'Registration successful! Please log in.')
                return render(request, 'ReaderHomePage.html', {'user': user})
    return redirect('sign_up')


# ----- Login to user's account -----
def enter_your_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        posts =Post.objects.all()
        events = Event.objects.all()
        books = Book.objects.all()
        comments=Comment.objects.all()
        
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session['username'] = username
            if user.role == 'writer':
                messages.success(request, 'Welcome!')
                return render(request, 'WriterHomePage.html', {'user': user})
            else:
                messages.success(request, 'Welcome!')
                return render(request, 'ReaderHomePage.html', {'user': user})
        else:
            messages.error(request, 'Invalid email or password', extra_tags='sign_in')
            return redirect('sign_in')
        
    return render(request, 'SignInPage.html')


# ------ Log out from user's account ------
def sign_out(request):
    if request.method == 'POST':
        request.session.flush()# make sure all session data is securely removed
        messages.success(request, 'Logout successful!', extra_tags='sign_out')
        return redirect('home')
    return redirect('home')



# ---- Posts Functions for the writer side
@login_required
def create_posts(request): # posting a post function 
    if request.method == 'POST':
        post_content = request.POST.get('post_content')
        current_user = User.objects.get(username=request.session['username'])
        new_post = Post.objects.create(user=current_user, content=post_content) #create new message and save it in database
        
        # Get the latest 3 messages for the current user
        posts = Post.objects.filter(user=current_user).order_by('-created_at')

        return render(request, 'WriterProfile.html', {'posts': posts, 'current_user': current_user})
    Post.objects.all()
    return redirect('writer_profile')

def delete_post(request, post_id): #delete comment function 
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, 'Post does not exist.')
            return redirect('writer_profile')

        if post.user.username == request.session['username']:
            post.delete()
            messages.success(request, 'Post deleted successfully!', extra_tags='delete')
        else:
            messages.error(request, 'You are not authorized to delete this post.', extra_tags='delete')
        
        return redirect('writer_profile')
    return redirect('writer_profile')

#----- Comments Functionsfor the writer side  ------
@login_required
def post_comment(request, id):
    if request.method == 'POST':
        comment_content = request.POST.get('content')
        if not comment_content:
            messages.error(request, 'Comment cannot be empty.')
            return redirect('writer_profile')
        
        current_user = User.objects.get(username=request.session['username'])
        
        # Ensure that the post exists
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            messages.error(request, 'The post does not exist.')
            return redirect('writer_profile')
        
        # Create the new comment
        Comment.objects.create(user=current_user, post=post, content=comment_content)
        
        # Redirect back to the wall page
        return redirect('writer_profile')
    
    return redirect('writer_profile')



def delete_comment(request, comment_id): #delete comment function 
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            messages.error(request, 'Comment does not exist.')
            return redirect('writer_profile')

        if comment.user.username == request.session['username']:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!', extra_tags='delete')
        else:
            messages.error(request, 'You are not authorized to delete this comment.', extra_tags='delete')
        
        return redirect('writer_profile')
    return redirect('writer_profile')


#Adding Books to Reader Library and Liking Books Functions

# @login_required
# def add_book_to_library(request, book_id):
#     book =Book.objects.get(id=book_id)
#     current_user = User.objects.get(username=request.session['username'])
#     if book not in current_user.library.all():
#         current_user.library.add(book)
#     return redirect('all_books_page')


# def like_book(request, book_id):
#     book = Book.objects.get(id=book_id)
#     current_user = User.objects.get(username=request.session['username'])
#     book.likes +=1
#     book.save()    
#     return redirect('all_books_page')


#---- Post function for the reader side -----
@login_required
def post_post(request):
    if request.method =='POST':
        post_content = request.POST.get('content')
        current_user = User.objects.get(username=request.session['username'])
        new_post = Post.objects.create(user=current_user, content=post_content) #create new message and save it in database
        messages.success(request, "Post Created Successfully!")
        return redirect('reader_profile')
    return redirect('reader_profile')

@login_required
def delete_reader_post(request, post_id):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, 'Post does not exist.')
            return redirect('reader_profile')
        if post.user.username == request.session['username']:
            post.delete()
            messages.success(request, 'Post deleted successfully!', extra_tags='delete')
        else:
            messages.error(request, 'You are not authorized to delete this post.', extra_tags='delete')
            
        return redirect('reader_profile')
    return redirect('reader_profile')

# ---- Comments Function for reader side ----            

@login_required
def post_reader_comment(request, id):
    if request.method == 'POST':
        comment_content = request.POST.get('content')
        if not comment_content:
            messages.error(request, 'Comment cannot be empty.')
            return redirect('reader_profile')
        
        current_user = User.objects.get(username=request.session['username'])
        
        # Ensure that the post exists
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            messages.error(request, 'The post does not exist.')
            return redirect('reader_profile')
        
        # Create the new comment
        Comment.objects.create(user=current_user, post=post, content=comment_content)
        success = 'Comment created successfully for user ' + current_user.username
        # return HttpResponse(success)
        # Redirect back to the wall page
        return redirect('reader_profile')
    
    return redirect('reader_profile')



def delete_reader_comment(request, comment_id): #delete comment function 
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            messages.error(request, 'Comment does not exist.')
            return redirect('reader_profile')

        if comment.user.username == request.session['username']:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!', extra_tags='delete')
        else:
            messages.error(request, 'You are not authorized to delete this comment.', extra_tags='delete')
        
        return redirect('reader_profile')
    return redirect('reader_profile')





























































# def create_account(request):
#     if request.method == 'POST':
#         errors = User.objects.user_validator(request.POST) 
#         if errors:# make sure that there is no error if there send an error message on the page 
#             for key, value in errors.items():
#                 messages.error(request, value, extra_tags='sign_up')
#             return redirect('sign_up')
#         else:
#             first_name  = request.POST.get('first_name')
#             last_name = request.POST.get('last_name')
#             username = request.POST.get('username')
#             role = request.POST.get('role')
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
            
#             user = User.objects.create(first_name=first_name, last_name=last_name, username= username, role= role, email=email, password=hashed_password) #create user
#             user.save()
#             if user.role == 'writer':
#                 messages.success(request, 'Registration successful! Please log in.')
#                 return render(request, 'WriterHomePage.html', {'user': user})
#             else:
#                 messages.success(request, 'Registration successful! Please log in.')
#                 return render(request, 'ReaderHomePage.html', {'user': user})
#     return redirect('sign_up')


# def enter_your_account(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = User.objects.filter(username = username).first()
        
#         if user and bcrypt.checkpw(password.encode(), user.password.encode()):
#             if user.username == 'writer':
#                 request.session['username'] = username
#                 messages.success(request, 'Welcome!')
#                 return redirect('writer_home_page')
#             else:
#                 request.session['username'] = username
#                 messages.success(request, 'Welcome!')
#                 return redirect('reader_home_page')
#         else:
#             messages.error(request, 'Invalid email or password', extra_tags='sign_in') # if not stay at the login and registration page
#             return redirect('sign_in')    
        
#     return render(request, 'SignInPage.html')
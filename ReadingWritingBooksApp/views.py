from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import bcrypt
from .models import User, Book, Notification, Post, Event, BookClub, Comment


# Create your views here.
def home(request):#rendering to the Home Page of the website
    return render(request, 'HomePage.html')

def sign_in(request):#rendering to the Sign In Page of the website and saving the current user info in the session
    current_user = User.objects.get(username=request.session['username'])
    return render(request, 'SignInPage.html', {'user': current_user})

def sign_up(request):#rendering to the Sign Up Page of the website and saving the current user info in the session
    current_user = User.objects.get(username=request.session['username'])
    return render(request, 'SignUpPage.html', {'user': current_user})

def about_us(request):#rendering to the about us page
    
    #here I have to add a functionality for the comment section in this page to store it in my database.
    
    return render(request, 'AboutUsPage.html')

def get_home_page_context(username):
    current_user = User.objects.get(username=username)  # Get the user data according to the username
    post = Post.objects.all().order_by('created_at')  # Get all the posts in ascending order
    comment = Comment.objects.all().order_by('created_at')  # Get all the comments in ascending order
    event = Event.objects.all().order_by('created_at')  # Get all the events
    book_club = BookClub.objects.all().order_by('created_at')  # Get all the book clubs
    
    context = {
        'user': current_user,
        'post': post,
        'comment': comment,
        'event': event,
        'book_club': book_club,
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
    Post.objects.all()
    if 'username' not in request.session:
        return render(request, 'signInPage.html')
    
    context = get_home_page_context(request.session['username'])
    return render(request, 'ReaderHomePage.html', context)



def writer_profile(request):
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

def create_book(request):
    return render(request, 'CreateBook.html')

def edit_book(request):
    return render(request, 'EditBook.html')

def delete_book(request):
    pass
def create_event(request):
    return render(request, 'CreateEvent.html')

def edit_event(request):
    return render(request, 'EditEvent.html')

def delete_event(request):
    pass

def view_book_detail(request):
    return render(request, 'ViewBookPage.html')
def view_event_detail(request):
    return render(request, 'ViewEventDetails.html')

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

def enter_your_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        
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

def sign_out(request):
    if request.method == 'POST':
        request.session.flush()# make sure all session data is securely removed
        messages.success(request, 'Logout successful!', extra_tags='sign_out')
        return redirect('home')
    return redirect('home')


def create_book(request):
    
    if request.method == 'POST':
        title = request.POST['title']
        genre = request.POST['genre']
        description = request.POST['description']
        Book.objects.create(title=title, genre= genre, description=description)
        return redirect('writer_profile')
    books = Book.objects.all()
    return render(request, 'CreateBook.html', {'books': books})


@login_required
def reader_posts(request): # posting a post function 
    Post.objects.all()
    if request.method == 'POST':
        post_content = request.POST.get('post_content')
        current_user = User.objects.get(username=request.session['username'])
        new_post = Post.objects.create(user=current_user, content=post_content) #create new message and save it in database
        
        # Get the latest 3 messages for the current user
        posts = Post.objects.filter(user=current_user).order_by('-created_at')[:3]

        return redirect('reader_home_page')
    return redirect('reader_home_page')

def delete_reader_post(request, post_id): # delete message function
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            messages.error(request, 'Post does not exist.')
            return redirect('reader_home_page')

        if Post.user.username == request.session['username']:
            Post.delete()
            messages.success(request, 'Post deleted successfully!', extra_tags='delete')
        else:
            messages.error(request, 'You are not authorized to delete this post.', extra_tags='delete')
        
        return redirect('reader_home_page')
    return redirect('reader_home_page')

@login_required
def post_reader_comment(request, id):# post comment function
    if request.method == 'POST':
        comment_content = request.POST.get('comment')
        current_user = User.objects.get(email=request.session['username'])
        
        # Ensure that the message exists and is valid
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            messages.error(request, 'The post does not exist.')
            return redirect('reader_home_page')

        # Create the new comment
        new_comment = Comment.objects.create(user=current_user, post=post, comment=comment_content)

        # Redirect back to the wall page
        return redirect('reader_home_page')
    
    return redirect('reader_home_page')

def delete_reader_comment(request, comment_id): #delete comment function 
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            messages.error(request, 'Comment does not exist.')
            return redirect('reader_home_page')

        if comment.user.username == request.session['username']:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!', extra_tags='delete')
        else:
            messages.error(request, 'You are not authorized to delete this comment.', extra_tags='delete')
        
        return redirect('reader_home_page')
    return redirect('reader_home_page')







































































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
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import bcrypt
from .models import User


# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
def home(request):
    return render(request, 'HomePage.html')

def sign_in(request):
    return render(request, 'SignInPage.html')

def sign_up(request):
    return render(request, 'SignUpPage.html')

def about_us(request):
    return render(request, 'AboutUsPage.html')

def writer_home_page(request):
    return render(request, 'WriterHomePage.html')

def reader_home_page(request):
    return render(request, 'ReaderHomePage.html')

def writer_profile(request):
    return render(request, 'WriterProfile.html')

def reader_profile(request):
    return render(request, 'ReaderProfile.html')

def edit_reader_profile(request):
    return render(request, 'EditReaderProfilePage.html')

def edit_writer_profile(request):
    return render(request, 'EditWriterProfilePage.html')

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

def create_account(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='sign_up')
            return redirect('sign_up')
        else:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            role = request.POST.get('role')
            date_of_birth = request.POST.get('date_of_birth')
            email = request.POST['email']
            password = request.POST['password']
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
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
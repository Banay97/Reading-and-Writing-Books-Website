from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
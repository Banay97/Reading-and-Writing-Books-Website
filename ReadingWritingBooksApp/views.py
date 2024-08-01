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
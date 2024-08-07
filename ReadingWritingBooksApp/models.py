from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData, is_creation=False):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters long'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters long'

        if len(postData['username']) < 5:
            errors['username'] = 'Username should be at least 5 characters long'   

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"    

        if len(postData['email']) < 10:
            errors['email'] = 'Email should be at least 10 characters long'    

        if is_creation:
            if len(postData['password']) < 8:
                errors['password'] = 'Password should be at least 8 characters long'

            if postData['password'] != postData['confirm_password']:
                errors['confirm_password'] = 'Passwords do not match'
        
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 5:
            errors['title'] = 'Title should be at least 5 characters long'
        if len(postData['description']) < 10:
            errors['description'] = 'Description should be at least 10 characters long'
        return errors      
            
class User(models.Model):
    ROLE_CHOICES = [
        ('writer', 'Writer'),
        ('reader', 'Reader'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.username}'

class Book(models.Model):
    title = models.CharField(max_length=100)
    genre =models.CharField(max_length=50)
    description = models.TextField()
    book_file = models.FileField(upload_to ='book_files/', blank=True)
    cover_image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    author = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateField(auto_now=True)

    objects = BookManager()
    
    def __str__(self):
        return f'{self.title} - {self.author}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    status = models.BooleanField()
    context = models.TextField()
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class BookClub(models.Model):
    club_name = models.CharField(max_length=45)
    club_content = models.CharField(max_length=255)
    club_type = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_clubs')
    
    def __str__(self):
        return self.club_name

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    event_content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    event_date = models.DateField()
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='events')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    
    def __str__(self):
        return self.event_name

    
class Post(models.Model):
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content    
        
class Comment(models.Model):
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default=True)
    
    def __str__(self):
        return f'commented by {self.user} on {self.post}'

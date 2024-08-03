from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
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

        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters long'

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'
        
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
    
    


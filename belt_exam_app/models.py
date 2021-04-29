from django.db import models
import re
from datetime import datetime

# managers are here
class UserManager(models.Manager):
    def validator(self,postData):
        errors={}
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name'])<2:
            errors['first_name']='First name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name']='First name should only be letters'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name']='Last name should only be letters'
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password']='Password should be at lesat 8 charictors'
        elif postData['password'] != postData['confirm_pw']:
                errors['password'] = 'Confirm PW does not match the password!'
        user=Users.objects.filter(email=postData['email'])
        if user:
            errors['email']='Email is already exist'
        return errors

class TripManager(models.Manager):
    def validator(self,postData):
        today=datetime.today().date()
        year=datetime.today().year
        errors={}
        if len(postData['dest'])<=0:
            errors['dest']='A destenation must be provided!'
        elif len(postData['dest'])<3:
            errors['dest']='A destenation must consist of at least 3 characters!'
        if len(postData['start_date'])<=0:
            errors['start_date']='Start date must be provided!'
        if len(postData['end_date'])<=0:
            errors['end_date']='End date must be provided!'
        if postData['start_date'] < str(today) or postData['end_date'] < postData['start_date']:
            errors['start_date']='Travel time is not allowed!'
        if len(postData['plan'])<=0:
            errors['plan']='A plan must be provided!'
        elif len(postData['plan'])<3:
            errors['plan']='A plan must consist of at least 3 characters!'
        return errors

# models are here.
class Users(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest=models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    plan=models.TextField()
    created_by=models.name = models.ForeignKey(Users, related_name='trips_created', on_delete=models.CASCADE)
    users_who_join=models.ManyToManyField(Users,related_name="joined_trips")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
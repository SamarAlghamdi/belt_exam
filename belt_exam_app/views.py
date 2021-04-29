from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime

# Create your views here.
def index(request):
    if 'user' in request.session:
        context={
            'user': Users.objects.get(id=request.session['user']),
            'trips':Trip.objects.all() 
        } 
        return render(request,'home.html', context)
    else:
        return redirect("/login")
# Login and reg ####################################################
def login(request):
    return render(request,'login.html')
def login_form(request):
    if 'user' in request.session:
        return redirect("/")
    else:
        if request.method=="POST":
            user=Users.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['user'] = logged_user.id
                    # messages.success(request,"Successfully logged in") #maybe  delete
                    return redirect("/")
                else:
                    messages.error(request,"Invalid login")
                    return redirect("/login")
            else:
                messages.error(request,"Invalid login")
                return redirect("/login")

def registration(request):
    if 'user' in request.session:
        return redirect("/")
    if 'errors' in request.session:
        return render(request,'reg.html', {'errors': request.session['errors']})
    else:
        request.session['errors'] = {}
        return redirect("/registration")
def register_form(request):
    errors = Users.objects.validator(request.POST)
    if len(errors)>0:
        request.session['errors'] = errors
        print(request.session['errors'])
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/registration")
    else:
        if request.method=="POST":
            password=request.POST['password']
            passHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            newUser = Users.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],
            password=passHash)
            request.session['user'] = newUser.id
            del request.session['errors']
            messages.success(request,"User successfully created")
        return redirect("/login")

def logout(request):
    request.session.flush()
    return redirect("/")

def create_trip(request):
    if 'user' in request.session:
        context={
            'user': Users.objects.get(id=request.session['user']),
        } 
        return render(request,'create_trip.html',context)
    else:
        return redirect("/")
def create_trip_form(request):
    errors = Trip.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/trips/new")
    else:
        if request.method=="POST":
            user=Users.objects.get(id=request.session['user'])
            trip=Trip.objects.create(dest=request.POST['dest'],start_date=request.POST['start_date'],end_date=request.POST['end_date'],
            plan=request.POST['plan'], created_by=user)
            return redirect("/")

def delete_trip(request,id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect("/")

def edit_trip(request,id):
    if 'user' in request.session:
        context={
            'user': Users.objects.get(id=request.session['user']),
            'trip': Trip.objects.get(id=id)
        } 
        return render(request,'edit_trip.html',context)
    else:
        return redirect("/")
def edit_trip_form(request,id):
    errors = Trip.objects.validator(request.POST)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect(f"/trips/edit/{id}")
    else:
        if request.method=="POST":
            trip=Trip.objects.get(id=id)
            trip.dest=request.POST['dest']
            trip.start_date=request.POST['start_date']
            trip.end_date=request.POST['end_date']
            trip.plan=request.POST['plan']
            trip.save()
            return redirect("/")

def read(request,id):
    if 'user' in request.session:
        context={
            'user': Users.objects.get(id=request.session['user']),
            'trip': Trip.objects.get(id=id)
        } 
        return render(request,'trip_details.html',context)
    else:
        return redirect("/")

def join(request,id):
    trip = Trip.objects.get(id=id)
    user = Users.objects.get(id=request.session['user'])
    if (user.id == trip.created_by.id):
        return redirect("/")
    else:
        trip.users_who_join.add(user)
        trip.save()
        return redirect("/")

def cancel_join(request,id):
    trip = Trip.objects.get(id=id)
    user = Users.objects.get(id=request.session['user'])
    trip.users_who_join.remove(user)
    trip.save()
    return redirect("/")

    
# #######################################################



# def delete_message(request, id):
#     message = Messages.objects.get(id=id)
#     date_created=message.created_at.date()
#     tody = datetime.today().date()
#     if tody == date_created:
#         created_hour = message.created_at.timestamp()
#         minute = datetime.today().timestamp()
#         result = minute - created_hour
#         if int(result) < 1800:
#             message.delete() 
#     return redirect("/")
    
print '*'*25, 'VIEWS.PY', '*'*25

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote

def index ( request ):
    print '*'*25, "LOGGED IN USER:", request.session['logged_in_user_id']
    if not request.session["logged_in_user_id"]:
        return render( request, "python_belt/index.html" )
    else:
        return redirect( "/python_belt/quotes" )
    
def signup( request ):
    if not request.session['logged_in_user_id']: #IF LOGGED IN ALREADY, THEN GOES TO QUOTES
        errors = User.objects.signup_validation( request.POST )
        if errors:
            messages.error( request, errors )
            return redirect( "/python_belt" )
        else:
            request.session['logged_in_user_id'] = User.objects.get( email = request.POST['email'] ).id
            messages.success( request, "Your user data has been saved" )
            return redirect( "/python_belt/quotes" )
    else:
        return redirect( "/python_belt/quotes" )

def login( request ):
    print "*"*25, "VIEWS.PY LOGIN ROUTE", "*"*25
    if not request.session['logged_in_user_id']:#IF LOGGED IN ALREADY, THEN GOES TO QUOTES
        errors = User.objects.login_validation( request.POST )
        if errors:
            messages.error( request, errors )
            return redirect( "/python_belt" )
        else:
            request.session['logged_in_user_id'] = User.objects.get( email = request.POST['email'] ).id
            return redirect( "/python_belt/quotes" )
    else:
        return redirect( "/python_belt/quotes" )

def logout( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/python_belt" )
    else:
        request.session['logged_in_user_id'] = False
        return redirect( "/python_belt" )

def quotes( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/python_belt" )
    else:
        print '*'*25, 'QUOTES, LOGGES IN USER:', request.session['logged_in_user_id']
        page_data = {
            "alias": User.objects.get( id = request.session['logged_in_user_id'] ).alias,
            "users": User.objects.all(),
            "quotable_quotes": Quote.objects.exclude( faved_users = User.objects.get( id = request.session['logged_in_user_id'] ) ),
            "fav_quotes": Quote.objects.filter( faved_users = User.objects.get( id = request.session['logged_in_user_id'] ) )
        }
        print '*'*25, 'QUOTES, LOGGES IN USER:', request.session['logged_in_user_id']
        
        return render( request, "python_belt/quotes.html", page_data )

def quote_create( request ):
    if not request.session['logged_in_user_id']:
        return redirect( "/python_belt" )
    else:
        errors = Quote.objects.validator( request.POST, request.session['logged_in_user_id'] )
        return redirect( "/python_belt/quotes" )


def user_show( request, id ):
    if not request.session['logged_in_user_id']:
        return redirect( "/python_belt" )
    else:
        page_data = {
            "count": Quote.objects.filter( user = User.objects.get( id = request.session['logged_in_user_id'] ) ).count(),
            "fav_quotes": Quote.objects.filter( faved_users = User.objects.get( id = request.session['logged_in_user_id'] ) ),
            "alias": User.objects.get( id = request.session['logged_in_user_id'] ).alias,
            "fav_quotes": Quote.objects.all()
        }

        return render( request, "python_belt/user.html", page_data )
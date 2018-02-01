print '*'*25, 'VIEWS.PY', '*'*25

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote


def index ( request ):
    if "logged_in_user_id" not in request.session:
        return render( request, "python_belt/index.html" )
    else:
        return redirect( "/python_belt/quotes" )
    
def signup( request ):
    if "logged_in_user_id" not in request.session: #IF LOGGED IN ALREADY, THEN GOES TO QUOTES
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
    if "logged_in_user_id" not in request.session:#IF LOGGED IN ALREADY, THEN GOES TO QUOTES
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
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else:
        # request.session['logged_in_user_id'] = False
        request.session.flush()
        return redirect( "/python_belt" )

def quotes( request ):
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else:
        print '*'*25, 'QUOTES, LOGGES IN USER:', request.session['logged_in_user_id']
        user = User.objects.get( id = request.session['logged_in_user_id'] )
        page_data = {
            "alias": user.alias,
            "quotable_quotes": Quote.objects.exclude( faved_users = user ),
            "fav_quotes": user.faved_quotes.all()
        }
        print '*'*25, 'QUOTES, LOGGES IN USER:', request.session['logged_in_user_id']
        
        return render( request, "python_belt/quotes.html", page_data )

def quote_fav( request, id ):
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else:
        q = Quote.objects.get( id = id )
        u = User.objects.get( id = request.session['logged_in_user_id'] )
        u.faved_quotes.add(q)
        return redirect( "/python_belt/quotes" )

def quote_unfav( request, id ):
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else:
        q = Quote.objects.get( id = id )
        u = User.objects.get( id = request.session['logged_in_user_id'] )
        u.faved_quotes.remove(q)
        return redirect( "/python_belt/quotes" )

def quote_destroy( request, id ):
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else:
        q = Quote.objects.get( id = id )
        q.delete()
        return redirect( "/python_belt/quotes" )

def quote_create( request ):
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else: # REDIRECTING BACK TO QUOTES IN ANY CASE, AND SHOWING ERRORS IF ANY
        errors = Quote.objects.validator( request.POST, request.session['logged_in_user_id'] )
        messages.error( request, errors )
        return redirect( "/python_belt/quotes" )

def user_show( request, id ):
    if "logged_in_user_id" not in request.session:
        return redirect( "/python_belt" )
    else:
        u = User.objects.get( id = id )
        page_data = {
            "alias": User.objects.get( id = request.session['logged_in_user_id'] ).alias,
            "count": u.quotes.all().count(),
            "quotes": u.quotes.all(),
            "posted_by": User.objects.get( id = id ).alias
        }

        return render( request, "python_belt/user.html", page_data )
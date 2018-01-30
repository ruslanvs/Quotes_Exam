from __future__ import unicode_literals
print '*'*25, 'MODELS.PY', '*'*25

from django.db import models
import re, bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager( models.Manager ):
    def signup_validation( self, post_data ):
        errors = {}
        nlen_min = 2
        pwlen_min = 8

        # VALIDATE NAME
        if len( post_data['name'] ) < nlen_min: # LENGTH
            errors["name"] = "Name cannot be less than " + str( nlen_min ) + " characters. "

        # elif not str.isalpha( str( post_data['name'] ) ): # CONVENTIONS
        #     errors["name"] = "Invalid characters in the name. "
    
        # VALIDATE ALIAS
        if len( post_data['alias'] ) < nlen_min: # LENGTH
            errors["alias"] = "Alias cannot be less than " + str( nlen_min ) + " characters. "

        elif not str.isalpha( str( post_data['alias'] ) ): # CONVENTIONS
            errors["alias"] = "Invalid characters in the alias. "

        # VALIDATE EMAIL
        if not email_regex.match( post_data['email'] ): # CONVENTIONS
            errors["email"] = post_data['email'] + "is not a valid email. "

        else: # UNIQUENESS
            existing_user = User.objects.filter( email = post_data['email'] ).first()
            if existing_user:
                errors["email"] = "Email " + post_data['email'] + " is already in use"

        # VALIDATE PASSWORD CONVENTIONS AND CONFIRMATION
        if len( str( post_data['pw'] ) ) < pwlen_min:
            errors["pw"] = "Password should have at least " + str( pwlen_min ) + " characters"
        elif post_data['pw'] != post_data['pwc']:
            errors["pw"] = "Password confirmation does not match"

        if errors:
            print "*"*25, "SIGNUP ERRORS: ", errors, "FORM DATA: ", post_data
            return errors
        else: # SUCCESS - ADD NEW USER INTO THE DATABASE
            print "*"*25, "VALIDATION SUCCESSFUL. FORM DATA: ", post_data
            User.objects.create(
                name = post_data['name'],
                alias = post_data['alias'],
                email = post_data['email'],
                pw = bcrypt.hashpw( post_data['pw'].encode(), bcrypt.gensalt() ),
                bd = post_data['bd']
            )

    def login_validation( self, post_data ):
        
        # EMAIL VALIDATION
        errors = {}
        if not email_regex.match( post_data['email'] ): # EMAIL CONVENTIONS
            errors["email"] = post_data['email'] + " is not a valid email. "
        else:
            existing_user = User.objects.filter( email = post_data['email'] ).first()
            if not existing_user:
                errors["email"] = "Email " + post_data['email'] + " is not registered with any user"
            else: # CHECK PW
                if not bcrypt.checkpw( post_data['pw'].encode(), User.objects.get( email = post_data['email'] ).pw.encode() ):
                    errors["pw"] = "Wrong password"
        print "*"*25, "LOGIN ERRORS:", errors
        return errors

class QuoteManager( models.Manager ):
    def validator( self, post_data, user_id ):
        errors = {}
        Quote.objects.create(
            author = post_data['author'],
            content = post_data['content'],
            user = User.objects.get( id = user_id )
        )
        return errors


class User( models.Model ):
    name = models.CharField( max_length = 255 )
    alias = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    pw = models.CharField( max_length = 255 )
    bd = models.DateTimeField( blank = True )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = UserManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", name: " + self.name + ", alias: " + self.alias

class Quote( models.Model ):
    author = models.CharField( max_length = 255 )
    content = models.TextField( max_length = 1000 )
    user = models.ForeignKey( User, related_name = "quotes" )
    faved_users = models.ManyToManyField( User, related_name="faved_quotes" )
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )
    objects = QuoteManager()
    def __unicode__( self ):
        return "id: " + str( self.id ) + ", author: " + self.author + ", content: " + self.content

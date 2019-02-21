from django.shortcuts import render, redirect
from apps.login_registration.models import User
from .models import Message, Comment
from django.contrib import messages
import bcrypt

def logout(request):
    request.session.pop('user')
    request.session.pop('user_id')
    return redirect('../login_registration/index')

def dashboard_index(request):
    
    user = User.objects.get(id=request.session['user_id'])
    user_level = user.user_level
    
    users = User.objects.all()

    context = {
        "users":users,
        "user_level": user_level
    }
    
    return render(request, 'dashboard/dashboard_index.html', context)

def get_profile_edit_form(request, user_id):

    user = User.objects.get(id=request.session['user_id'])
    user_level = user.user_level

    user = User.objects.get(id=user_id)

    context = {        
        "user_level": user_level,
        "user": user
    }
    return render(request, 'dashboard/user_profile_edit.html', context)

def get_message_page(request, user_id):

    user = User.objects.get(id=user_id)
    messages = Message.objects.filter(user=user)
    context = {
        "messages":messages,
        "user": user
    }
    return render(request, 'dashboard/message.html', context)

def remove_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect(dashboard_index)


def get_user_registation_form(request):
    return render(request, 'dashboard/user_registration.html')

def register(request):
        
    errors = User.objects.basic_validator(request.POST)
    
    print(len(errors))
    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        return redirect(get_user_registation_form)
    else:
        
        # check if the email exist or not
        user = User.objects.filter(email=request.POST['email'])

        if user:
            messages.error(request, "This email address already exist", extra_tags="email")
            return redirect(get_user_registation_form)

        hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], hashpw=hashedPw)
        
        return redirect(dashboard_index)

def udpate_information(request, user_id):

    errors = User.objects.user_info_validator(request.POST)

    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        return redirect('get_profile_edit_form', user_id=user_id)
    else:
        
        # check if the email exist or not
        user = User.objects.filter(email=request.POST['email']).exclude(id=user_id)

        if user:
            messages.error(request, "This email address already exist", extra_tags="email")
            return redirect(get_user_registation_form)
        
        user = User.objects.get(id=user_id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.user_level = request.POST['user_level']
        user.save()
        return redirect(dashboard_index)

def change_password(request, user_id):

    errors = User.objects.user_password_validator(request.POST)

    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        return redirect('get_profile_edit_form', user_id=user_id)
    else:

        hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = User.objects.get(id=user_id)
        user.hashpw = hashedPw        
        user.save()

        request.session.pop('user')
        request.session.pop('user_id')

        return redirect('/login/get_login_page')

def edit_description(request, user_id):
    user = User.objects.get(id=user_id)
    user.description = request.POST['description']        
    user.save()
    return redirect(dashboard_index)

def save_post(request, user_id):

    user = User.objects.get(id=user_id)
    Message.objects.create(msg_content=request.POST['message'], user=user)

    return redirect('get_message_page', user_id)

def save_comment(request, msg_id):

    user = User.objects.get(id=request.session['user_id'])
    print(user)
    msg = Message.objects.get(id=msg_id)
    print(msg)
    Comment.objects.create(reply_content=request.POST['comment'], message=msg, user=user)

    return redirect('get_message_page', request.session['user_id'])
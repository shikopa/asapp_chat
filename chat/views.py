from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.template import RequestContext
from models import ChatRoom


def login_user(request):
    context = RequestContext(request)
    logout(request)  # Logout

    if request.POST:
        username = request.POST.get('username', '')
        if not username:
            raise Http404('Please enter a Username.')
        user = authenticate(username=username, password='')
        if user is not None:
            login(request, user)

            # Create Chat Rooms
            ChatRoom.create_rooms(user)
            next = request.POST.get('next', '')
            print 'next....... : ', next
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/available_chats/')
        else:
            raise Http404('Username does not exist. {0}'.format(username))

    context = {
        'next': request.GET.get('next', '')
    }

    return render_to_response('login.html', context, RequestContext(request))


def logout_user(request):
    logout(request)

    return HttpResponseRedirect('/')


def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/available_chats/')
    return render(request, "login.html")

@login_required
def available_chats(request):
    """
    List of available Chats for the logged in User
    """

    context = {
        'available_users': User.objects.all().exclude(username=request.user.username)
    }

    return render(request, "chat/available_chats.html", context=context)


@login_required
def chat_room(request, username):
    """
    :param username: The username the logged in user wants to chat with
    """

    if not username:
        raise Http404('Please provide Username inorder to chat.')

    if request.user.username.lower() == username.lower():
        return HttpResponseRedirect('/available_chats/')

    user = get_object_or_404(User, username=username)


    chat_room = ChatRoom.get_room(request.user, user)  # Get a chat room for the chat, create's it if one does not exist.

    # Obtain all the messages in the Chat, order in ascending order of date created
    messages = reversed(chat_room.messages.order_by('created_dt'))
    context = {
        'username': username,
        'chat_room': chat_room,
        'messages': messages,
    }

    return render(request, "chat/chat_room.html", context=context)
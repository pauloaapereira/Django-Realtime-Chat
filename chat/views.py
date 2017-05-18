import json

from django.shortcuts import render
from .models import Message
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# this view is the base view
def chat_index(request):

    # UNCOMMENT THE LINES BEFORE IF YOU WANT THE APP TO DELETE SOME MESSAGES WHEN THERE ARE MANY

    #------ counts the existing messages on db
    #msgsLen = Message.objects.all().count()

    #------ if there are more than 100 messages, deletes the first four hundred messages
    #if msgsLen > 500:
    #    for message in Message.objects.all()[:400]:
    #        message.delete()

    # passes all the messages to the context
    context = {
        'messages': Message.objects.all()
    }

    # and returns it to the page
    return render(request, 'chat_index.html', context)

# this view must be csrf exempted to be able to accept XMLHttpRequests
@csrf_exempt
def save_message(request):
    # if the request method is a POST request
    if request.method == 'POST':
        # content sent via XMLHttpRequests can be accessed in request.body
        # and it comes in a JSON string, that's why we use json library to
        # turn it into a normal dictionary again
        msg_obj = json.loads(request.body.decode('utf-8'))

        # tries to create the message and save it in the db
        try:
            msg = Message.objects.create(user_name=msg_obj['user_name'], message=msg_obj['message'])
            msg.save()
        # if some error occurs it will print the error in the django console and return a HttpResponse
        # containing a error value, which will be received by nodejs socket.io
        except:
            print("error saving message")
            return HttpResponse("error")

        # if there aren't any errors, it returns a HttpResponse containing a success value, which will
        # be received by nodejs socket.io
        return HttpResponse("success")

    # if it is a GET request (someone trying to access to the link or something)
    # returns to the main page without doing anything
    else:
        return HttpResponseRedirect('/')

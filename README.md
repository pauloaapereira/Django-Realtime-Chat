# Django-Realtime-Chat
This is an example project. Every important instruction is commented, so feel free to check it.
To run it:
  - open a console, go to the folder nodejs and type:
  ```
  node index.js
  ```
  - go to root of the project and type, if in Windows:
  ```
  python manage.py runserver 0:8000  // this will run the server to every hosts on the port 8000 (you can choose any port you want, but you will have to open it anyway in the firewall)
  ```
  or
  ```
  python manage.py runserver localhost:8000 // this will run the server to your host on the port 8000 (you can choose any port you want, but you will have to open it anyway in the firewall)
  ```
  - if it Linux:
  ```
  ./manage.py runserver 0:8000  // this will run the server to every hosts on the port 8000 (you can choose any port you want, but you will have to open it anyway in the firewall)
  ```
  or
  ```
  ./manage.py runserver localhost:8000 // this will run the server to your host on the port 8000 (you can choose any port you want, but you will have to open it anyway in the firewall)  
  ```
  
# NodeJS and Socket.IO in Django - Realtime Operations

Implementing realtime in Django may seem difficult, but it really isn't that hard. This may not be the best way to do it, but it is certainly a simple and effective way.

# I want to implement this in my project! How can i do it?

In order to run NodeJS, obviously you need to install NodeJS:
  - https://nodejs.org/en/download/
  
Create a Django project anywhere you want with the usual command:
  - django-admin createproject <projectname>

In your Django project folder, create a folder named "nodejs" and run this commands on the console (needs Node.JS):
  - npm init
    insert any name you want when asked, and just keep pressing Enter until it ends
  - npm install --save socket.io xmlhttprequest
  
Next, still in the same folder, create the file:
  - index.js

In that file insert this:

```
var http = require('http').createServer().listen(4000);
var io = require('socket.io')(http);
var XMLHttpRequest = require('xmlhttprequest').XMLHttpRequest;

// creating an instance of XMLHttpRequest
var xhttp = new XMLHttpRequest();

// host of the server
var host = 'localhost';
var port = '8000';

// when a connection happens (client enters on the website)
io.on('connection', function(socket) {

    // if the event with the name 'message' comes from the client with the argument 'msgObject',
    // which is an object with the format: {'user_name': < name >, 'message': < message >},
    // it emits for every connected client that a message has been sent, sending the message to the event
    // 'getMessage' in the client side
    socket.on('message', function(msgObject) {
        // emits the msgObject to the client
        io.emit('getMessage', msgObject);

        // url of the view that will process, in this case, it is the save_message view, located on the app 'chat'
        var url = 'http://' + host +':' + port + '/save_message/';

        // when the request finishes
        xhttp.onreadystatechange = function() {
            // it checks if the request was succeeded
            if(this.readyState === 4 && this.status === 200) {
                // if the value returned from the view is error
                if(xhttp.responseText === "error")
                    console.log("error saving message");
                // if the value returned from the view is success
                else if(xhttp.responseText === "success")
                    console.log("the message was posted successfully");
            }
        };

        // prepares to send
        xhttp.open('POST', url, true);
        // sends the data to the view
        xhttp.send(JSON.stringify(msgObject));
    });

});
```

This is the file where the nodejs server will be running with socket.io, and where the http requests to Django will be done.
Everything is explained on the comments.

Now, i will assume that you already had an application named 'chat', and a template ready to put some HTML on it. If you don't, just check the example project that i left for you.

In the template, add this scripts to the begin of <body>:

```
<!-- this is just a CDN to use jquery -->
<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>

<!-- this one is important to get things to work -->
<script src="http://localhost:4000/socket.io/socket.io.js"></script>
```

now add these ones to the end of <body>, one more time, everything is explained on the comments:

```
<script>

    // host of the server
    var host = 'localhost';
    var nodejs_port = '4000';

    var socket = io(host + ':' + nodejs_port);

    // when the document is ready, scrolls down the page to the last page if there are messages
    $(function() {
        updateScroll();
    });

    // on the form submit
    $('form').submit(function() {
        // gets the elements by ids
        var msg = $('#message');
        var name = $('#name');

        // if the message and the name aren't empty or aren't spaces,
        if(msg.val().trim() !== "" && name.val().trim() !== "") {
            // creates the message object
            msgObject = {
                'user_name': name.val().trim(),
                'message': msg.val().trim()
            };

            // emits the msgObject to the server
            socket.emit('message', msgObject);
        }

        // clear the message element
        msg.val('');
        // returns false to avoid the form to reload the page
        return false;
    });

    // receives the message object from the server
    socket.on('getMessage', function(msgObject) {
        // gets the fields of the message
        var name = msgObject.user_name;
        var msg = msgObject.message;

        var icon = $('<span class="input-group-addon" style="text-shadow: 1px 1px 1px #000; background-color: rgb(66, 133, 244); color: #fff" ></span>').append(name);
        var msgItem = $('<input type="text" class="form-control" readonly style="background-color: #fff" />').val(msg);
        var input_group = $('<div class="input-group"></div>').append(icon, msgItem);

        // appends the message to the screen
        $('#messages-list').append(input_group);

        // updates the scroll
        updateScroll();
    });

    function updateScroll(){
        var element = document.getElementById("messages-list");
        element.scrollTop = element.scrollHeight;
    }
</script>
```

For this configurations i have this views and urls:

chat/views.py:
```
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

```

chat/urls.py:
```
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.chat_index, name='chat_index'),
    # url used to process the xmlhttprequests done by nodejs socket.io
    url(r'^save_message/$', views.save_message, name='chat_save_message'),
]
```

chat/models.py:
```
from django.db import models

# Message model
class Message(models.Model):
    user_name = models.CharField(max_length=20)
    message = models.CharField(max_length=140)

```

main root app/urls.py:
```
from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('chat.urls')),
]
```

I hope you enjoy it!

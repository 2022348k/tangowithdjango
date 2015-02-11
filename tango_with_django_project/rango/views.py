from django.shortcuts import render

from django.http import HttpResponse

#def index(request):
    #return HttpResponse("Rango says hey there world. <br/> <a href='/rango/about'>About</a>!")

def about(request):
    context_dict = {'boldmessage': "This Tutorial has been put together by Dimitrios Kolovopoulos, 2022348k"}
    return render(request, 'rango/about.html', context_dict)



def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'rango/index.html', context_dict)

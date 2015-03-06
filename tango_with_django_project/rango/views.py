from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from django.contrib.auth.models import User

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response

def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0
    context_dict = {'student_name': "Georgios Kampanos", 'student_number': "2021259K", 'visits': count}
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
    context_dict = {'cat_slug': category_name_slug}

    #result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            context_dict = {'search_results': run_query(query)}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

        #update views
        category.views += 1
        category.save()

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'cat_slug': category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)



def register(request):

    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

@login_required
def register_profile(request):
     
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
 
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
 
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()
        
    return render(request,"registration/profile_registration.html",{'profile_form': profile_form})

#@login_required
#def register_profile_2(request):
#     if request.method == 'POST':
#         profile_form = UserProfileForm(data=request.POST, instance = request.user.profile)
# 
#         if profile_form.is_valid():
#             profile_form.save()
# #             if 'picture' in request.FILES:
# #                 profile.picture = request.FILES['picture']
#             return HttpResponseRedirect('/rango/')
#         else:
#             user = request.user
#             profile = user.profile
#             form = UserProfileForm(instance = profile)
#         
#     args = {}
#     args.update(csrf(request))
#     args['form'] = form
    
  #  return render(request, 'registration/profile_registration.html', args)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")



@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            pages = Page.objects.all().filter(id = request.GET['page_id'])
            if len(pages) == 0:
                return HttpResponseRedirect('/rango/404/')

            #get the page, update the views and update on server
            page = pages[0]
            page.views += 1
            page.save()

    return HttpResponseRedirect(page.url)


def error_page(request):
    return render(request, 'rango/404.html')

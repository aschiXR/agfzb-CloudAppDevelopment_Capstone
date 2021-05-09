from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import related models
from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
    

    
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, notify for invalid username or password
            messages.add_message(request, messages.WARNING, 'wrong username or password')
            return redirect('djangoapp:index')
    else:
        # if not, redirect to login page
        return redirect('djangoapp:index')


    
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'logged out succesfully')
    return redirect('djangoapp:index')



# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    #if it is a POST request, perform registration procedures
    elif request.method == 'POST':
    # Get user details from request.POST dictionary
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password1 = request.POST['psw1']
        password2 = request.POST['psw2']
        # Check inserted passwords match
        if not password1 == password2:
            messages.add_message(request, messages.WARNING, 'specified passwords not matching')
            return render(request, 'djangoapp/registration.html', context)
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
            print('user already exists {}, {}, {}'.format(\
                    User.first_name, User.last_name, User.username))
        except:
            # If not confirm it is a new user
            print('this is a new user {}!'.format(username))
        # If it is a new user
        if not user_exist:
            user = User.objects.create_user(username=username, \
                    first_name=firstname, \
                    last_name=lastname, \
                    password=password1)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'created a new user')
            return redirect('djangoapp:index')
        else:
            messages.add_message(request, messages.WARNING, 'inserted username already exists')
            return render(request, 'djangoapp/registration.html', context)


        
# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # get url from django settings
        url = settings.CP_API_URL + "dealership"
        cp_cl_api_key = settings.CP_API_KEY
        # retrieve dealerships stored on cloud
        dealership_list = get_dealers_from_cf(url=url,cp_cl_api_key=cp_cl_api_key)
        context['dealership_list'] = dealership_list
        return render(request, 'djangoapp/index.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # get url and key from django settings
        url_review = settings.CP_API_URL + "review"
        url_dealer = settings.CP_API_URL + "dealership"
        cp_cl_api_key = settings.CP_API_KEY
        # get dealer details
        dealer_by_id = get_dealer_by_id(
            url=url_dealer,
            cp_cl_api_key=cp_cl_api_key,
            dealer_id=dealer_id
        )
        if dealer_by_id is None:
            # if dealer not on remote server cannot redirect to index with message
            messages.add_message(request, messages.WARNING, \
                    'Dealer does not exist, try again later...')
            return redirect('djangoapp:index')
        context['dealer_name'] = dealer_by_id.full_name
        # retrieve dealership review stored on cloud
        dealer_reviews = get_dealer_reviews_from_cf(
            url=url_review,
            cp_cl_api_key=cp_cl_api_key,
            dealer_id=dealer_id
        )
        context['dealer_reviews'] = dealer_reviews
        # forward dealer id
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    context['dealer_id'] = dealer_id
    # check if user is authenticated
    sessionid = request.COOKIES.get('sessionid')
    if sessionid is None:
        return HttpResponseForbidden("Not Authorized: please login to post reviews")
    # get url and key from django settings
    url_review = settings.CP_API_URL + "review"
    url_dealer = settings.CP_API_URL + "dealership"
    cp_cl_api_key = settings.CP_API_KEY
    # if GET request render submission form
    if request.method == "GET":
        # get dealer details
        dealer_by_id = get_dealer_by_id(
            url=url_dealer,
            cp_cl_api_key=cp_cl_api_key,
            dealer_id=dealer_id
        )
        if dealer_by_id is None:
            # if dealer not on remote server cannot redirect to index with message
            messages.add_message(request, messages.WARNING, \
                    'Dealer does not exist, try again later...')
            return redirect('djangoapp:index')
        context['dealer_name'] = dealer_by_id.full_name
        # get dealer cars
        cars = CarModel.objects.filter(DealerId=dealer_id)
        if len(cars) == 0:
            messages.add_message(request, messages.WARNING, \
                    'The dealer does not sell any car!')
        context['cars'] = cars
        # render submission form
        return render(request, 'djangoapp/add_review.html', context)
    # if POST request submit new review
    elif request.method == "POST":
        # get user information
        user = User.objects.get(username=request.user)
        # prepare json_payload to post
        review = dict()
        review['id'] = user.pk
        review['name'] = user.first_name + " " + user.last_name
        review['dealership'] = dealer_id
        review['review'] = request.POST['review']
        if review['review'] == "":
            # check review is not empty
            messages.add_message(request, messages.WARNING, \
                    'Review not posted: empty reviews are not accepted')
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        if 'purchase' in request.POST:
            # payload if uer purchased a car
            review['purchase'] = True
            review['purchase_date'] = request.POST['date']
            if review['purchase_date'] == "":
                # check a date has been selected
                messages.add_message(request, messages.WARNING, \
                    'Review not posted: please insert purchase date')
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            try:
                # dealer must sell cars in order to leave a review for a purchase
                car_id = request.POST['carInformation']
                purchased_car = CarModel.objects.get(pk=car_id)
                review['car_make'] = purchased_car.CarMake.Name
                review['car_model'] = purchased_car.Name
                review['car_year'] = purchased_car.Year.strftime("%Y")
            except:
                messages.add_message(request, messages.WARNING, \
                    'Review not posted: dealer sells no car, cannot post \
                    reviews for purchases')
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            # payload if user did not purchase a car
            review['purchase'] = False
        json_payload=dict()
        json_payload['review']= review
        print("json_payload: {}".format(json_payload))
        # post review on remote service
        post_response = post_request(
            url=url_review,
            json_payload=json_payload,
            cp_cl_api_key=cp_cl_api_key
        )
        print("post_response: {}".format(post_response))
        try:
            if post_response['ok']:
                # if post submission succesfull
                messages.add_message(request, messages.SUCCESS, \
                        'Review has been posted succesully')
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        except:
            print("post failed")
        messages.add_message(request, messages.WARNING, \
                'Review not posted: something wrong happened while \
                sending the post request to the server')
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


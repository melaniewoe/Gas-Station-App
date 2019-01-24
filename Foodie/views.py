# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from Foodie.models import Category
from Foodie.models import Page
from Foodie.form import CategoryForm
from Foodie.form import PageForm 
from Foodie.form import UserForm, UserProfileForm
from django.shortcuts import render
import requests
from populate import populate1, populate
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
import json

# working on item.special
### try to convert from unicode to list. 
### might need some picture
def index(request):
	context_dict = {}

	a =requests.get('http://brsapkota-test.apigee.net/gas/listofday?year=2017&month=4&day=27')
	b = a.json()
	price_list = b['Pricelist']
	date = price_list[0]['date'][:10]
	

	page_list = Page.objects.all()
	store = Category.objects.all()

	###########avg price
	avg_reg_price = []
	for item in page_list:
		if str(item.category) == 'gas':	
		 	avg_reg_price.append(item.regularprice)
	avg_reg_price_result = round(sum(avg_reg_price)/len(avg_reg_price),2) 


	avg_prem_price = []
	for item in page_list:
		if str(item.category) == 'gas':
			avg_prem_price.append(item.premiumprice)

	avg_prem_price_result = round(sum(avg_prem_price)/len(avg_prem_price),2)

	avg_mid_price = []
	for item in page_list:
		if str(item.category) == 'gas':
			avg_mid_price.append(item.midprice)

	avg_mid_price_result = round(sum(avg_mid_price)/len(avg_mid_price),2)

	############min price
	reg_price = []
	for item in page_list:
		if str(item.category) == 'gas':
			if str(item.regularprice) != 'None':
		 		reg_price.append(item.regularprice)
	min_reg_price = min(reg_price)
	print min_reg_price

	

	context_dict = {'store': store, 'pages': page_list, 'average_reg_price': avg_reg_price_result, 'average_prem_price': avg_prem_price_result, 'average_mid_price': avg_mid_price_result, 'date': date}

	return render(request, 'Saya/index.html', context_dict)

def contact(request):
	context_dict = {}

	
	return render(request, 'Saya/contact.html', context_dict)

def get_location():
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	return float(lat),float(lon) 

def privacy(request):
	context_dict = {}

	return render(request, 'Saya/privacy.html', context_dict) 

def about(request):
	context_dict = {}
	
	return render(request, 'Saya/about.html', context_dict) 
def location(request):
	context_dict = {}
	local = []
	geolocator = Nominatim()
	page_list = Page.objects.all()
	for item in page_list:
		l = geolocator.geocode(item.address)
		local.append(l)

	lat,lon = get_location()
	page = zip(page_list,local)
	context_dict = {'pages':page, 'lat':lat, 'lon':lon}
	
	return render(request, 'Saya/location1.html', context_dict)


def special(request):
	context_dict = {}
	page_list = Page.objects.all()[:7]

	for item in page_list:
		item.special = item.special.split("!")
	lat, lon = get_location()
	context_dict= {'pages':page_list,'lat':lat, 'lon': lon }

	return render(request, 'Saya/special_offer.html', context_dict)

# DONE !!!!
def page(request, page_name_slug):
    context_dict ={}
    local =[]
    geolocator = Nominatim()
    try:
        print (page_name_slug)
        page = Page.objects.get(slugP = page_name_slug)
        context_dict['item'] = page
        page.special = page.special.split("!")
        local = geolocator.geocode(page.address)
        context_dict ['local'] = local

        print local.latitude, local.longitude
        print local.address

    except Page.DoesNotExist:
        print "cant find this page."

    return render(request, 'Saya/page.html', context_dict)



def upload(request):
	login_required()
	context_dict = {}
	
	if request.method == 'POST':
		link = request.POST
		if 'http' in link['APIlink']:
			populate1(link['APIlink'])
		else:
			return HttpResponse("It's not a link....!!!")

	return render(request, 'Saya/upload.html', context_dict)

def register(request):
    context = RequestContext(request)

    
    registered = False

    
    if request.method == 'POST':
        
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'Saya/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):

	context = RequestContext(request)

	print context, "This is context"
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']


		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:

				login(request, user)
				return HttpResponseRedirect('/Foodie/')
			else:

				return HttpResponse("Your account is disable. Please contact Nguyen to resolve this")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login info: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login credential.")
	else:
		return render_to_response('registration/login.html', {}, context)




# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	logout(request)

	# Take the user back to the homepage.
	return HttpResponseRedirect('/Foodie/')
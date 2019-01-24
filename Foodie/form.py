from django import forms
from Foodie.models import Page ,Category
from Foodie.admin import UserProfile
from easy_thumbnails.fields import ThumbnailerImageField
from decimal import Decimal
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
	name  = forms.CharField(max_length=128, help_text="Enter store type:")
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Category
		fields = ('name',)


class PageForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Store name:")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	midprice = forms.DecimalField(max_digits=20, help_text="Medium Gas Price:")
	premiumprice = forms.DecimalField(max_digits=20, help_text="Premium Price:")
	regularprice = forms.DecimalField(max_digits=20, help_text="Regular Price:")
	feature = forms.BooleanField(initial=False, help_text="Feature:")  # Special store run for promo. 
	special = forms.CharField(max_length=128, help_text="Special:")  # speciual menu. 
	address = forms.CharField(max_length=128, help_text="Address:")  
	image = forms.ImageField(help_text="Store location:")	# image if needed. 
	des = forms.CharField(max_length=999, help_text="Store Description:")
	slugP = forms.CharField(widget=forms.HiddenInput(), required=False)
	
	class Meta:
		model = Page
		exclude = ('category',)
		# or field =('title' , 'url' , 'views'....)
	
	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		if url and not url.startswith('http://'):
			url='http://' + url
			cleaned_data['url'] = url

		return cleaned_data

#### need to work on import form into the admin system.
#### make a login page. 
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)



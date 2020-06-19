from django import forms
from .models import Crop, Bid

class CropForm(forms.ModelForm):
	class Meta:
		model = Crop
		fields = ('cat', 'name', 'quantity', 'unit', 'description', 'pickup', 'image')

class BidForm(forms.ModelForm):
	class Meta:
		model = Bid
		fields = ['value',]
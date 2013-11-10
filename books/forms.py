from django import forms
from books.models import Review


CHOICES = (
	    ('book','search by book title'),
	    ('author','search by author'),
	    ('publisher','search by publisher'),
	)

class ReviewForm(forms.ModelForm):

    class Meta:

        model = Review#bind the form to the model
        fields = ('name_of_reviewer', 'text',)#specify what fields to show
        widgets={
        	'text': forms.Textarea(attrs={'cols': 80, 'rows':20}),
        }#customize fields

class SearchForm(forms.Form):
	query = forms.CharField(max_length=50, required=True)
	search_creteria = forms.ChoiceField(widget=forms.RadioSelect(),choices=CHOICES, required=True)
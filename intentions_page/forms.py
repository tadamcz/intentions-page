from django import forms

from intentions_page.models import Intention

class IntentionEditForm(forms.ModelForm):
	class Meta:
		model = Intention
		fields = ('completed','neverminded')

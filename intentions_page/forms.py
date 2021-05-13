from django import forms
from crispy_forms.helper import FormHelper

from intentions_page.models import Intention, Note

class IntentionEditForm(forms.ModelForm):
	class Meta:
		model = Intention
		fields = ('completed','neverminded')

class NoteEditForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ('content',)

	helper = FormHelper()
	helper.form_show_labels = False

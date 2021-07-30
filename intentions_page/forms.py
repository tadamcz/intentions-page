from django import forms
from crispy_forms.helper import FormHelper

from intentions_page.models import Intention, Note, IntentionsDraft

class IntentionEditForm(forms.ModelForm):
	class Meta:
		model = Intention
		fields = ('completed','neverminded')

class IntentionsDraftEditForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if self.instance.content:
			rows = len(self.instance.content.splitlines())
		else:
			rows = 1
		self.fields['content'].widget.attrs = {'rows': rows, 'placeholder':'Add intentions (one per line)'}

	class Meta:
		model = IntentionsDraft
		fields = ('content',)

	helper = FormHelper()
	helper.form_show_labels = False

class NoteEditForm(forms.ModelForm):
	class Meta:
		model = Note
		fields = ('content',)

	helper = FormHelper()
	helper.form_show_labels = False

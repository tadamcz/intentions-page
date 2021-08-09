from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from intentions_page.models import Intention, Note, IntentionsDraft

class IntentionEditForm(forms.ModelForm):
	class Meta:
		model = Intention
		fields = ('completed','neverminded')

class IntentionsDraftEditForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# This sizing code is later overridden by js autosize
		# but it's a good idea to have something approximately correct already in the HTML before the JS comes in.
		# The code here will produce the same height as JS if all intentions take up one line or less.
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

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# For notes, we can't make very good assumptions for the number of rows that autosize will pick,
		# so we use a constant number of rows
		self.fields['content'].widget.attrs = {'rows': 2}

	helper = FormHelper()
	helper.form_show_labels = False

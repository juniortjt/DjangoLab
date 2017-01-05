from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Document

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'document', 'published_date')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class ContactForm(forms.Form):
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':10, 'cols':100}),
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "Message:"


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )


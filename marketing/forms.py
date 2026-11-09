from django import forms
from django.utils.translation import gettext_lazy as _
from .models import NewsletterSubscriber

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError(_("That email is already on the list."))
        return email

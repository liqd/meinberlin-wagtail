from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings


class FeedbackForm(forms.Form):
    answer = forms.CharField(label='Ihr Feedback zu mein.berlin.de:',
        widget=forms.Textarea(attrs={'rows': 4}),
        max_length=1000,
        required=False)
    sender_address = forms.EmailField(label='Wenn Sie eine Antwort bekommen möchten, geben Sie bitte Ihre email-Adresse an (optional):',
        required=False)


def feedback_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = 'meinberlin feedback'
            qa = 'Ihr Feedback zu mein.berlin.de:\n\n' + form.cleaned_data['answer'] + '\n\n'
            email = 'Nutzer-Email: ' + form.cleaned_data['sender_address'] + '\n\n'
            message = qa + email
            recipients = [settings.FEEDBACK_TO_EMAIL]

            send_mail(subject, message, None, recipients, fail_silently=False)
            return HttpResponseRedirect('/w')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    return render(request, 'meinberlin/feedback_page.html', {'form': form})

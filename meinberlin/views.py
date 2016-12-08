from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings


class FeedbackForm(forms.Form):
    answer1 = forms.CharField(label='Was gefällt Ihnen an den Inhalten von mein.berlin.de?',
        max_length=1000,
        required=False)
    answer2 = forms.CharField(label='Was missfällt Ihnen an den Inhalten von mein.berlin.de?',
        max_length=1000,
        required=False)
    answer3 = forms.CharField(label='Was gefällt Ihnen an der technischen Umsetzung von mein.berlin.de?',
        max_length=1000,
        required=False)
    answer4 = forms.CharField(label='Was missfällt Ihnen an der technischen Umsetzung von mein.berlin.de?',
        max_length=1000,
        required=False)
    sender_address = forms.EmailField(label='Wenn Sie eine Antwort bekommen möchten, geben Sie bitte Ihre email-Adresse an (optional):',
        required=False)


def feedback_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print('trying to post the form')
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = 'meinberlin feedback'
            qa1 = 'Was gefällt Ihnen an den Inhalten von mein.berlin.de?\n\n' + form.cleaned_data['answer1'] + '\n\n'
            qa2 = 'Was missfällt Ihnen an den Inhalten von mein.berlin.de?\n\n' + form.cleaned_data['answer2'] + '\n\n'
            qa3 = 'Was gefällt Ihnen an der technischen Umsetzung von mein.berlin.de?\n\n' + form.cleaned_data['answer3'] + '\n\n'
            qa4 = 'Was missfällt Ihnen an der technischen Umsetzung von mein.berlin.de?\n\n' + form.cleaned_data['answer4'] + '\n\n'
            email = 'Nutzer-Email: ' + form.cleaned_data['sender_address'] + '\n\n'
            message = qa1 + qa2 + qa3 + qa4 + email
            recipients = [settings.FEEDBACK_TO_EMAIL]

            send_mail(subject, message, None, recipients, fail_silently=False)
            return HttpResponseRedirect('/w')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()

    return render(request, 'meinberlin/feedback_page.html', {'form': form})

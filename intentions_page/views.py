from intentions_page.forms import IntentionEditForm
from intentions_page.models import Intention
import django.utils.timezone as timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponse
from intentions_page.models import get_working_day_date


def home(request):
    if request.user.is_authenticated:
        working_day_date = get_working_day_date()

        intentions = Intention.objects.filter(creator=request.user, date=working_day_date)
        for i in intentions:
            i.edit_form = IntentionEditForm(instance=i)

        context = {
            'date': working_day_date,
            'intentions': intentions
        }
        return render(request, 'pages/home.html', context)
    else:
        return render(request, 'pages/welcome.html')


@login_required
def history(request):
    intentions_by_date = {}
    intentions = Intention.objects.filter(creator=request.user)

    today = timezone.now().date()

    if intentions:
        start_date = intentions.last().date
        num_days = (today - start_date).days + 1

        date_range = (today - timezone.timedelta(days=x) for x in range(num_days))

        for date in date_range:
            intentions_for_day = intentions.filter(date=date)

            for i in intentions_for_day:
                i.edit_form = IntentionEditForm(instance=i)

            intentions_by_date[date] = intentions_for_day

    context = {
        'intentions_by_date': intentions_by_date
    }

    return render(request, 'pages/history.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        intentions = request.POST['list'].splitlines()
        intentions.reverse()
        for i in intentions:
            if not i.isspace() and not i == "":
                Intention.objects.create(title=i, creator=request.user)

    return redirect('home')


@login_required
def edit(request, primary_key):
    intention = Intention.objects.get(id=primary_key)

    if intention.creator != get_user(request):
        raise PermissionDenied

    if request.method == 'POST':
        form = IntentionEditForm(request.POST, instance=intention)
        form.save()

    return redirect(request.headers.get('Referer', 'home'))


@login_required
def append(request, primary_key):
    if request.method == 'POST':
        intention = Intention.objects.get(id=primary_key)

        if intention.creator != get_user(request):
            raise PermissionDenied

        intention.title += ' ' + request.POST['append']
        intention.save()

    return redirect(request.headers.get('Referer', 'home'))


def feedback(request):
    email = request.POST.get("email")
    message = request.POST.get("message")
    message = message.replace('\n', '<br>')
    path = request.path

    html = f"<html>" \
           f"<br><b>path: </b>{path}" \
           f"<br><b>email: </b>{email}" \
           f"<br><b>message: </b>{message}" \
           f"</html>"

    result = send_mail("Feedback on intentions.page", message, recipient_list=['tmkadamcz@gmail.com'], html_message=html, from_email=email)

    if result is 1:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)

def privacy_policy(request):
    return render(request, "privacy-policy.html")

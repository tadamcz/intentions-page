from intentions_page.forms import IntentionEditForm
from intentions_page.models import Intention
import django.utils.timezone as timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.core.exceptions import PermissionDenied

def home(request):
    if request.user.is_authenticated:
        today = timezone.now().date()
        intentions = Intention.objects.filter(creator=request.user, date=today)
        for i in intentions:
            i.edit_form = IntentionEditForm(instance=i)

        context = {
            'date': today,
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
        title = request.POST['title']
        Intention.objects.create(title=title, creator=request.user)

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

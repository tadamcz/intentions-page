from django.db import transaction

from intentions_page.forms import IntentionEditForm, NoteEditForm, IntentionsDraftEditForm
from intentions_page.models import Intention, Note, IntentionsDraft
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
        tomorrow_date = working_day_date + timezone.timedelta(days=1)

        tomorrow_draft_field = get_or_init_intentions_draft_field(request.user, tomorrow_date)
        today_draft_field = get_or_init_intentions_draft_field(request.user, working_day_date)

        content_by_date = create_day_range(working_day_date, working_day_date, request.user)
        content_by_date[working_day_date]['note'].collapse = True

        context = {
            'content_by_date': content_by_date,
            'tomorrow_draft_field':tomorrow_draft_field,
            'today_draft_field':today_draft_field,
        }

        return render(request, 'pages/home.html', context)
    else:
        return render(request, 'pages/welcome.html')

def get_or_init_intentions_draft_field(user, date):
    draft = IntentionsDraft.objects.filter(creator=user, date=date).first()
    if not draft:
        draft = IntentionsDraft(creator=user, date=date)
        draft.save()
    return IntentionsDraftEditForm(instance=draft)

@login_required
def history(request):
    intentions = Intention.objects.filter(creator=request.user)
    notes = Note.objects.filter(creator=request.user)

    end_date = get_working_day_date()

    start_date_candidates = [end_date]
    if intentions:
        start_date_candidates.append(intentions.last().date)
    if notes:
        start_date_candidates.append(notes.last().date)

    start_date = min(start_date_candidates)

    day_range = create_day_range(start_date, end_date, request.user)

    context = {
        'content_by_date': day_range
    }

    return render(request, 'pages/history.html', context)

def create_day(date, user):

    intentions = Intention.objects.filter(creator=user, date=date)

    for i in intentions:
        i.edit_form = IntentionEditForm(instance=i)

    note = Note.objects.filter(creator=user, date=date).first()
    if not note:
        note = Note(creator=user, date=date)
        note.save()

    note.edit_form = NoteEditForm(instance=note)
    note.collapse = False

    return {'intentions': intentions, 'note': note}

def create_day_range(start,end,user):
    day_range = {}

    num_days = (end - start).days + 1

    date_range = (end - timezone.timedelta(days=x) for x in range(num_days))

    for date in date_range:
        day_range[date] = create_day(date, user)

    return day_range

@login_required
def promote_draft_to_intentions(request):
    intentions = request.POST['content'].splitlines()
    for i in intentions:
        if not i.isspace() and not i == "":
            Intention.objects.create(title=i, creator=request.user)

    IntentionsDraft.objects.filter(creator=request.user, date=get_working_day_date()).delete()

    return redirect('home')


@login_required
def edit(request, primary_key):
    intention = Intention.objects.get(id=primary_key)

    if intention.creator != get_user(request):
        raise PermissionDenied

    if request.method == 'POST':
        intention.edit_form = IntentionEditForm(request.POST, instance=intention)
        intention.edit_form.save()

    return render(request, "components/single_intention.html", context={'intention': intention})

@login_required
def append(request, primary_key):
    if request.method == 'POST':
        intention = Intention.objects.get(id=primary_key)

        if intention.creator != get_user(request):
            raise PermissionDenied

        intention.title += ' ' + request.POST['append']
        intention.save()

    return redirect(request.headers.get('Referer', 'home'))

@login_required
def note(request, primary_key):
    if request.method == 'POST':
        note = Note.objects.get(id=primary_key)
        return autosave_field(request, note)

@login_required
def intentions_draft(request, primary_key):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                draft = IntentionsDraft.objects.select_for_update().get(id=primary_key)
                return autosave_field(request, draft)
        except IntentionsDraft.DoesNotExist:  # It would be cleaner not to send these requests in the first place
            return HttpResponse(status=200)

def autosave_field(request, object):
    if object.creator != get_user(request):
        raise PermissionDenied
    if object.version < int(request.POST['version']):
        object.content = request.POST['content']
        object.version = request.POST['version']
        object.save()
    return HttpResponse(status=200)


def privacy_policy(request):
    return render(request, "privacy-policy.html")

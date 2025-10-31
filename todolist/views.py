from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import TrigramSimilarity


# Create your views here.

@login_required
def home_view(request):
    """
    صفحه اصلی — خوش‌آمدگویی + لینک به بخش‌ها
    """
    context = {
        'user': request.user,
    }
    return render(request, 'todolist_templates/main/home.html', context)

@login_required
def event_list_view(request):
    events = None
    if request.user.events:
        events = Event.objects.filter(user=request.user)
        if events:
            paginator = Paginator(events, 3)
            page_number = request.GET.get('page', 1)
            try:
                events = paginator.page(page_number)
            except EmptyPage:
                events = paginator.page(1)
            except PageNotAnInteger:
                events = paginator.page(paginator.num_pages)
    return render(request, 'todolist_templates/main/event-list.html', {'events': events})


@login_required
def event_list_by_category_view(request, category_slug):
    events = None
    if request.user.events:
        events = Event.objects.filter(user=request.user, status=category_slug)
        if events:
            paginator = Paginator(events, 3)
            page_number = request.GET.get('page', 1)
            try:
                events = paginator.page(page_number)
            except EmptyPage:
                events = paginator.page(1)
            except PageNotAnInteger:
                events = paginator.page(paginator.num_pages)
    return render(request, 'todolist_templates/main/event-list.html', {'events': events})


@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def event_detail_view(request, pk):
    event = get_object_or_404(Event, id=pk, user=request.user)
    return render(request, 'todolist_templates/main/event-detail.html', {'event': event})


@login_required
def add_event_view(request):
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('todolist:event-list')
    else:
        form = AddEventForm()
    return render(request, 'todolist_templates/forms/add-event.html', {'form': form})


@login_required
def edit_event_view(request, pk):
    event = get_object_or_404(Event, id=pk, user=request.user)
    if request.method == "POST":
        form = AddEventForm(data=request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('todolist:event-list')
    else:
        form = AddEventForm(instance=event)
    return render(request, 'todolist_templates/forms/edit-event.html', {'form': form})


@login_required
def delete_event_view(request, pk):
    event = get_object_or_404(Event, id=pk)
    event.delete()
    return redirect('todolist:event-list')


@login_required
@require_POST
def event_status_change_view(request):
    event_id = request.POST.get('event_id')
    if event_id:
        event = get_object_or_404(Event, id=event_id, user=request.user)
        if event.status == 'UN':
            event.status = 'DO'
            done_now = True
        else:
            event.status = 'UN'
            done_now = False
        event.save()
        return JsonResponse({'done_now': done_now})
    return JsonResponse({'error': 'event id not exist !'})


def event_search_view(request):
    events = []
    query = None
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
        result_by_title = Event.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(
            similarity__gt=0.3)
        result_by_description = Event.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(
            similarity__gt=0.2)
        events = (result_by_title | result_by_description).distinct().order_by('-similarity')
    return render(request, 'todolist_templates/main/event-list.html', {'events': events})


@login_required
def task_list_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todolist_templates/main/task_list.html', {'tasks': tasks})


@login_required
def add_task_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todolist:task_list')
    else:
        form = TaskForm()
    return render(request, 'todolist_templates/forms/add_task.html', {'form': form})


@login_required
def toggle_task_view(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect('todolist:task_list')


@login_required
def delete_task_view(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect('todolist:task_list')


@login_required
def task_list_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todolist_templates/main/task_list.html', {'tasks': tasks})


@login_required
def add_task_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todolist:task_list')
    else:
        form = TaskForm()
    return render(request, 'todolist_templates/forms/add_task.html', {'form': form})


@login_required
def toggle_task_view(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.is_done = not task.is_done
    task.save()
    return redirect('todolist:task_list')


@login_required
def delete_task_view(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()
    return redirect('todolist:task_list')

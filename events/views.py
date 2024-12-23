from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from .models import Event
from .forms import EventForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Event

@login_required
def dashboard(request):
    now = timezone.now()
    events = Event.objects.filter(user=request.user)
    
    # Calculate statistics
    total_events = events.count()
    upcoming_events_count = events.filter(date__gte=now).count()
    passed_events = events.filter(date__lt=now).order_by('-date')
    passed_events_count = passed_events.count()
    
    # Get monthly data
    monthly_counts = list(events.annotate(month=TruncMonth('date'))
                         .values('month')
                         .annotate(count=Count('id'))
                         .order_by('month'))
    
    # Format the dates for JSON serialization
    formatted_monthly_counts = []
    for item in monthly_counts:
        formatted_monthly_counts.append({
            'month': item['month'].strftime('%Y-%m-%d'),
            'count': item['count']
        })
    
    # Get category data
    category_counts = list(events.values('category')
                         .annotate(count=Count('id'))
                         .order_by('category'))
    
    # Get recent events
    recent_events = events.order_by('-date')[:5]

    context = {
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'passed_events_count': passed_events_count,
        'passed_events': passed_events,
        'monthly_counts': json.dumps(formatted_monthly_counts),
        'category_counts': json.dumps(category_counts),
        'recent_events': recent_events,
    }
    
    return render(request, 'events/dashboard.html', context)





@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user).order_by('date')
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/event_list.html', {'page_obj': page_obj})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('events:event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('events:event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def event_search(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(user=request.user, name__icontains=query).order_by('date')
    return render(request, 'events/event_search_results.html', {'events': events, 'query': query})

@login_required
def event_stats(request):
    monthly_counts = Event.objects.filter(user=request.user).annotate(month=TruncMonth('date')).values('month').annotate(count=Count('id')).order_by('month')
    category_counts = Event.objects.filter(user=request.user).values('category').annotate(count=Count('id'))
    
    return JsonResponse({
        'monthly_counts': list(monthly_counts),
        'category_counts': list(category_counts),
    })


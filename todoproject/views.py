'''
THIS RIGHT HERE IS THE TODOPROJECT MAIN VIEWS.PY
'''
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from todoapp.models import Todo
from Journalapp.models import Journal, DailyQuote
from django.utils.timezone import now
from django.core.paginator import Paginator

# Home view (this will show the home page)
def home(request):
    # Get today's quote or none
    today = now().date()
    quote = DailyQuote.objects.filter(date=today).first()
    if not quote:  # If no quote exists for today, create a fallback
        quote = {
            'quote': "Welcome to TodoApp! Start your day with productivity!",
            'date': today,
        }

    # Fetch todos and journals
    todos = Todo.objects.all()
    journals = Journal.objects.all()

    # Prepare context to send to the template
    context = {
        'todos': todos,
        'journals': journals,
        'quote': quote,
        'current_time': now().strftime('%H:%M'),
    }
    return render(request, 'home.html', context)


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, 'home.html', {'login_form': form})

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to login after signup
    else:
        form = UserCreationForm()
    return render(request, 'home.html', {'signup_form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout
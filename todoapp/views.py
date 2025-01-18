'''
VIEWS OF TODO APP 
'''
from django.shortcuts import render, redirect, get_object_or_404 
from .models import Todo, LongTermGoal
from datetime import datetime
from .forms import LongTermGoalForm
from django.contrib.auth.decorators import login_required

def todo_list(request):
    """Fetches all tasks, filters them into completed and pending,
    and long-term goals, then renders the todo_list.html template."""
    todos = Todo.objects.all()
    completed_tasks = todos.filter(completed=True)
    pending_tasks = todos.filter(completed=False)
    
    long_term_goals = LongTermGoal.objects.all()

    return render(request, 'todoapp/todo_list.html', {
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'long_term_goals': long_term_goals
    })

def add_task(request):
    """Handles POST requests to create a new task.
    Extracts data from the form and creates a new Todo object.
    Redirects to the todo_list view upon success."""
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details', '')
        context = request.POST.get('context', '')
        time = request.POST.get('time', '')
        date = request.POST.get('date', '')
        due_date = request.POST.get('due_date')
        is_long_term_goal = request.POST.get('is_long_term_goal', False)
        
        

        Todo.objects.create(
            title=title,
            details=details,
            context=context,
            time=time,
            date=date,
            due_date=due_date,
            is_long_term_goal=is_long_term_goal,
        )
        return redirect('todo_list')
    
    return render(request, 'todoapp/add_task.html')

def complete_task(request, id):
    """Marks a task as completed by retrieving it by ID,
    setting the completed field to True, and saving it.
    Redirects to the todo_list view upon success."""
    todo = Todo.objects.get(id=id)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

def long_term_goals(request):
    """Fetches all tasks marked as long-term goals and
    renders the long_term_goals.html template."""
    long_term_goals = Todo.objects.filter(is_long_term_goal=True)
    return render(request, 'todoapp/long_term_goals.html', {'long_term_goals': long_term_goals})

def add_long_term_goal(request):
    """Handles POST requests to create a new long-term goal.
    Extracts data from the form and creates a new LongTermGoal object.
    Redirects to the long_term_goals view upon success with error handling."""
    if request.method == 'POST':
        form = LongTermGoalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_all_long_term_goals')  # Redirect to correct view
        else:
            return render(request, 'todoapp/add_long_term_goal.html', {'form': form, 'error': 'Please correct the errors below.'})
    
    form = LongTermGoalForm()
    return render(request, 'todoapp/add_long_term_goal.html', {'form': form})
def view_all_tasks(request):
    """Fetches all tasks, orders them by due date,
    and renders the view_all_tasks.html template."""
    todos = Todo.objects.all().order_by('due_date')
    return render(request, 'todoapp/view_all_tasks.html', {'tasks': todos})

def view_all_long_term_goals(request):
    """Fetches all long-term goals and renders the
    view_all_long_term_goals.html template."""
    todos = Todo.objects.all()
    
    long_term_goals = LongTermGoal.objects.all()
    
    return render(request, 'todoapp/view_all_long_term_goals.html', {'long_term_goals': long_term_goals})

def delete_task(request, id):
    '''Deletes a task by ID and redirects to the view_all_tasks view.'''
    print(f"Request to delete task with id: {id}")
    try:
        task = get_object_or_404(Todo, id=id)
        task.delete()
        return redirect('view_all_tasks')
    except Exception as e:
        print(f"Error deleting task: {e}")
        return HttpResponseNotFound("Task not found.")
def delete_long_term_goal(request, id):
    """Deletes a long-term goal by ID and redirects to the view_all_long_term_goals view."""
    goal = get_object_or_404(LongTermGoal, id=id)
    goal.delete()
    return redirect('view_all_long_term_goals')

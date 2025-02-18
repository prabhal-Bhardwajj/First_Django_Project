'''
VIEWS OF JOURNAL 
'''
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
#Password protection to be added !!!
from django.contrib import messages
from .models import Journal, DailyQuote , JournalCategory
#-----------------------------------------
from todoapp.models import LongTermGoal
#-----------------------------------------
from django.utils.timezone import now
from .forms import JournalForm
from django.template.loader import get_template
#------------------------------------------
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import check_password
#------------------------------------------
from django.db.models import Q
#------------------------------------------
from django.db.models import Count
from django.shortcuts import render

import os

from xhtml2pdf import pisa

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

'''
Home view: Renders the homepage of the application.
Fetches today's daily quote (if available) and passes it to the template for display.
'''
def home(request):
    today = now().date()  # Get today's date
    daily_quote = DailyQuote.objects.filter(date=today).first()  # Fetch today's daily quote
    return render(request, 'home.html', {'daily_quote': daily_quote})

'''
Index view: Displays the main page of the JournalApp, listing all journal entries.
Retrieves today's daily quote for display within the JournalApp.
'''
def index(request):
    journals = Journal.objects.all().order_by('-created_at')[:1]  # Get journals sorted by creation date
    today = now().date()  # Get today's date
    daily_quote = DailyQuote.objects.filter(date=today).first()  # Fetch today's daily quote
    return render(request, 'Journalapp/index.html', {'journals': journals, 'daily_quote': daily_quote})

'''
Journal list view: Lists all journal entries in reverse chronological order (most recent first).
'''
def journal_list(request):
   
    # Get query parameters for search and category filtering
    search_query = request.GET.get('q', '')  # Search term
    category_name = request.GET.get('category', '')  # Selected category

    # Base queryset: All journals ordered by creation date
    journals = Journal.objects.all().order_by('-created_at')

    # Apply category filter if provided
    if category_name:
        journals = journals.filter(category=category_name)

    # Apply search filter if provided
    if search_query:
        journals = journals.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    # Pagination logic
    paginator = Paginator(journals, 5)  # Show 10 journals per page
    page = request.GET.get('page')  # Get the current page number from the request

    try:
        journals = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        journals = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        journals = paginator.page(paginator.num_pages)

    # Pass data to the template
    return render(request, 'Journalapp/journal_list.html', {
        'journals': journals,
        'category_name': category_name,
        'search_query': search_query,
        'categories': JournalCategory.choices,  # Pass all categories for filtering
    })
def journal_by_category(request, category_name):
    journals = Journal.objects.filter(category=category_name).order_by('-created_at')
    return render(request, 'Journalapp/journal_list.html', {'journals': journals, 'category_name': category_name})
'''
Add journal view: Handles the creation of a new journal entry.
Processes a submitted form on POST; otherwise, displays an empty form for user input.
'''
def add_journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            # Save the journal entry
            journal = form.save(commit=False)

            # Hash the password before saving, if provided
            if journal.password:
                from django.contrib.auth.hashers import make_password
                journal.password = make_password(journal.password)

            # Save the journal entry
            journal.save()

            # If this is a long-term goal, create a LongTermGoal and associate it with the journal
            if form.cleaned_data['long_term_goal']:
                long_term_goal = LongTermGoal.objects.create(
                    title=journal.title,
                    details=journal.content,
                    due_date=journal.due_date
                )
                # Optionally, associate the journal with the long-term goal
                journal.long_term_goal = long_term_goal
                journal.save()

            messages.success(request, "Journal entry added successfully!")
            return redirect('journal_list')  # Redirect to journal list
    else:
        form = JournalForm()

    return render(request, 'journalapp/add_journal.html', {'form': form})

'''
Journal detail view: Displays details of a specific journal entry identified by its ID.
Returns a 404 error if the journal does not exist.
'''
def detail(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)  # Fetch journal by ID or return 404
    return render(request, 'Journalapp/detail.html', {'journal': journal})

'''
Journal for goal view: Displays a journal entry along with its associated long-term goal (if any).
If no goal is linked, passes None for the goal.
'''
def journal_for_goal(request, journal_id):
    journal = get_object_or_404(Journal, id=journal_id)  # Fetch journal by ID
    long_term_goal = journal.goal if journal.goal else None  # Check for associated goal
    return render(request, 'Journalapp/journal_detail.html', {
        'journal': journal,
        'long_term_goal': long_term_goal,
    })


'''
Add Daily Quote View: 
This view allows users to perform the following actions:
1. Add a new daily quote for today's date.
2. Set an existing quote as today's daily quote.
3. Delete a quote from the database.

The page also displays a list of all existing quotes, ordered by their date.
'''
def add_daily_quote(request):
    # Step 1: Get today's date to associate the quote with the current day
    today = now().date()

    # Step 2: Fetch all quotes from the database, sorted by the most recent date first
    all_quotes = DailyQuote.objects.all().order_by('-date')

    # Step 3: Check if the form was submitted (i.e., a POST request was made)
    if request.method == 'POST':
        # Determine the action based on the button clicked in the form
        action = request.POST.get('action')

        # Case 1: Save a new quote or update today's quote
        if action in ['save_home', 'save_stay']:
            # Fetch the text of the quote entered by the user
            quote_text = request.POST.get('quote')
            if quote_text:  # Ensure the quote text is not empty
                # Add a new quote or update today's quote with the entered text
                DailyQuote.objects.update_or_create(
                    date=today,  # Associate the quote with today's date
                    defaults={'quote': quote_text}  # Update or set the quote text
                )

            # Redirect based on the button clicked:
            # - "save_home": Go to the homepage to view the new quote
            # - "save_stay": Stay on the current page to add another quote
            return redirect('home' if action == 'save_home' else 'add_daily_quote')

        # Case 2: Set an existing quote as today's daily quote
        elif action == 'set_home':
            # Get the ID of the selected quote from the form
            quote_id = request.POST.get('quote_id')

            # Fetch the selected quote from the database or show a 404 error if not found
            selected_quote = get_object_or_404(DailyQuote, id=quote_id)

            # Update today's daily quote to match the selected quote
            DailyQuote.objects.update_or_create(
                date=today,  # Associate the quote with today's date
                defaults={'quote': selected_quote.quote}  # Set today's quote to the selected quote
            )

            # Redirect to the homepage to display the selected quote
            return redirect('home')

        # Case 3: Delete an existing quote
        elif action == 'delete':
            # Get the ID of the quote to be deleted from the form
            quote_id = request.POST.get('quote_id')

            # Fetch the quote to delete or show a 404 error if not found
            quote_to_delete = get_object_or_404(DailyQuote, id=quote_id)

            # Delete the quote from the database
            quote_to_delete.delete()

            # Stay on the current page after deletion
            return redirect('add_daily_quote')

    # Step 4: Render the "add_daily_quote.html" template
    # Pass the list of all quotes to the template for display
    return render(request, 'Journalapp/add_daily_quote.html', {'all_quotes': all_quotes})

'''
Set home quote view: Updates today's daily quote to an existing selected quote.
Redirects to the homepage after updating.
'''
def set_home_quote(request):
    if request.method == 'POST':
        quote_id = request.POST.get('quote')  # Fetch the selected quote ID
        selected_quote = get_object_or_404(DailyQuote, id=quote_id)  # Fetch quote by ID
        today = now().date()  # Get today's date
        DailyQuote.objects.update_or_create(
            date=today,
            defaults={'quote': selected_quote.quote}
        )
        return redirect('home')  # Redirect to homepage

'''
Delete journal view: Deletes a specific journal entry identified by its ID.
Processes deletions only on POST requests.
'''
def delete_journal(request, id):
    journal = get_object_or_404(Journal, id=id)  # Fetch journal by ID or return 404
    if request.method == 'POST':
        journal.delete()  # Delete the journal entry
        return redirect('journal_list')  # Redirect to journal list after deletion

'''
Journal detail view: Displays a detailed view of a journal entry along with its associated goal (if any).
Logs the available templates in the directory for debugging purposes.
Added the Password Protection for user selected journals
'''
def journal_detail(request, journal_id):
    """
    View to display the details of a journal entry.
    If the entry is password-protected, prompt the user for the password.
    """
    journal = get_object_or_404(Journal, id=journal_id)  # Fetch journal by ID
    
    # If the journal is password-protected
    if journal.is_protected():
        # Check if the user has submitted the correct password
        if request.method == "POST":
            entered_password = request.POST.get("password")
            if check_password(entered_password, journal.password):  # Compare entered password with stored hash
                request.session[f'journal_access_{journal_id}'] = True  # Grant access for this session
            else:
                messages.error(request, "Incorrect password. Please try again.")
                return render(request, 'journalapp/password_prompt.html', {'journal': journal})
        
        # If not authenticated in the current session
        elif not request.session.get(f'journal_access_{journal_id}', False):
            return render(request, 'journalapp/password_prompt.html', {'journal': journal})
    
    # Fetch associated long-term goal if present
    long_term_goal = getattr(journal, 'goal', None)
    
    # Render journal detail view if access is granted
    return render(request, 'journalapp/journal_detail.html', {
        'journal': journal,
        'long_term_goal': long_term_goal,
    })


'''
Quote list view: Lists all daily quotes in reverse chronological order (most recent first).
'''
def quote_list(request):
    quotes = DailyQuote.objects.all().order_by('-date')  # Fetch all quotes ordered by date
    return render(request, 'Journalapp/quote_list.html', {'quotes': quotes})

def edit_journal(request, journal_id):
    """
    View to edit an existing journal entry.
    """
    journal = get_object_or_404(Journal, id=journal_id)  # Fetch the journal by ID
    if request.method == 'POST':
        form = JournalForm(request.POST, instance=journal)  # Bind form to the journal instance
        if form.is_valid():
            form.save()  # Save the updated journal
            messages.success(request, "Journal updated successfully!")
            return redirect('journal_list')  # Redirect to journal list after saving
    else:
        form = JournalForm(instance=journal)  # Pre-fill form with the journal's data

    return render(request, 'Journalapp/edit_journal.html', {'form': form, 'journal': journal})

'''
This is just added for exporting pdf for the Journals
'''
def export_journal_pdf(request, journal_id):
    """
    Generates a PDF for the specified journal entry using xhtml2pdf.
    """
    journal = get_object_or_404(Journal, id=journal_id)

    # Render the journal data into a template
    template_path = 'Journalapp/journal_pdf_template.html'
    context = {'journal': journal}
    html = get_template(template_path).render(context)

    '''This will  Create the PDF'''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{journal.title}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    ''' This is an error response under the tests.py 
    but there seems no error yet.'''
    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{pisa_status.err}</pre>')

    return response

def journal_analytics(request):
    mood_stats = Journal.objects.values('mood').annotate(count=Count('mood'))
    entry_count = Journal.objects.count()
    return render(request, 'journalapp/analytics.html', {'mood_stats': mood_stats, 'entry_count': entry_count})
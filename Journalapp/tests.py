from django.test import TestCase, Client
from django.urls import reverse
from .models import Journal, DailyQuote, JournalCategory
from todoapp.models import LongTermGoal
from django.utils.timezone import now
'''
python manage.py test Journalapp
'''

'''
D:\python\visual code\TODO\todoenv\todoproject\Journalapp\tests.py
January 18, 2025 - 23:03:32
Creating test database for alias 'default'...
.........
----------------------------------------------------------------------
Ran 11 tests in 0.832s

OK
'''
class JournalAppTests(TestCase):
    def setUp(self):
        """
        Set up Sample data for testing.
        """
        
        self.journal = Journal.objects.create(
            title="Test Journal",
            content="<div>Test Journal 12345 </div>",
            category=JournalCategory.PERSONAL,
            priority="medium",
            password=None,
            long_term_goal=False
        )

        
        self.daily_quote = DailyQuote.objects.create(
            quote="This is a Test quote 12345.",
            date=now().date(),
            is_homepage=True
        )

        
        self.client = Client()

    def test_home_view(self):
        
        response = self.client.get(reverse('home'))  
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.daily_quote.quote)  

    def test_journal_list_view(self):
        
        response = self.client.get(reverse('journal_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.journal.title)  

    def test_add_journal_view(self):
        
        response = self.client.post(reverse('add_journal'), {
            'title': 'New Test 12345',
            'content': 'This is a test.',
            'category': JournalCategory.WORK,
            'priority': 'high',
            'long_term_goal': False,
            'password': ''
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Journal.objects.filter(title='New Test Journal').exists())

    def test_journal_detail_view(self):
        
        response = self.client.get(reverse('detail', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.journal.title)  # Check if journal title is in the response

    def test_password_protected_journal(self):
                
        self.journal.password = "test12345"
        self.journal.save()

        
        response = self.client.get(reverse('detail', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'journalapp/password_prompt.html')

        
        response = self.client.post(reverse('detail', args=[self.journal.id]), {
            'password': 'test12345'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.journal.title)

    def test_export_journal_pdf_view(self):
        response = self.client.get(reverse('export_journal_pdf', args=[self.journal.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')  # works fine
        self.assertIn(b'%PDF', response.content)  # Fixed HttpResponse 

    def test_filter_by_category(self):
        
        response = self.client.get(reverse('journal_list') + f'?category={JournalCategory.PERSONAL}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.journal.title)

    def test_quote_list_view(self):
        
        response = self.client.get(reverse('quote_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.daily_quote.quote)

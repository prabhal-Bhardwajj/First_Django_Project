# Generated by Django 5.1.5 on 2025-02-14 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Journalapp', '0005_remove_journal_catgories_journal_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='mood',
            field=models.CharField(choices=[('Happy', 'Happy'), ('Furious', 'Furious'), ('Confused', 'Confused'), ('Bored', 'Bored'), ('Calm', 'Calm'), ('Depressed', 'Depressed'), ('Disgusted', 'Disgusted'), ('Euphoric', 'Euphoric'), ('Frustrated', 'Frustrated'), ('Guilty', 'Guilty'), ('Hopeful', 'Hopeful'), ('Hurt', 'Hurt'), ('Jealous', 'Jealous'), ('Lonely', 'Lonely'), ('Loving', 'Loving'), ('Nervous', 'Nervous'), ('Overwhelmed', 'Overwhelmed'), ('Proud', 'Proud'), ('Scared', 'Scared'), ('Shocked', 'Shocked'), ('Surprised', 'Surprised'), ('Sad', 'Sad'), ('Angry', 'Angry'), ('Anxious', 'Anxious'), ('Excited', 'Excited'), ('Relaxed', 'Relaxed'), ('Tired', 'Tired'), ('Romantic', 'Romantic'), ('Careless', 'Careless'), ('Erotic', 'Erotic'), ('Grateful', 'Grateful'), ('Inspired', 'Inspired'), ('Motivated', 'Motivated'), ('Peaceful', 'Peaceful'), ('Confident', 'Confident'), ('Ashamed', 'Ashamed'), ('Embarrassed', 'Embarrassed'), ('Resentful', 'Resentful'), ('Indifferent', 'Indifferent'), ('Hopeless', 'Hopeless'), ('Disappointed', 'Disappointed'), ('Disapproving', 'Disapproving'), ('Disbelieving', 'Disbelieving'), ('Discouraged', 'Discouraged'), ('Disconnected', 'Disconnected'), ('Stressed', 'Stressed'), ('Neutral', 'Neutral'), ('Unmarked', 'Unmarked')], default='Unmarked', max_length=20),
        ),
        migrations.AlterField(
            model_name='journal',
            name='category',
            field=models.CharField(choices=[('Personal', 'Personal'), ('Gratitude', 'Gratitude'), ('Insight', 'Insight'), ('Reflection', 'Reflection'), ('Mindbyte', 'Mindbyte'), ('Mathematics', 'Mathematics'), ('Astrology', 'Astrology'), ('Machine_Learning', 'Machine_Learning'), ('Programming', 'Programming'), ('Literature', 'Literature'), ('Poetry', 'Poetry'), ('Cinema', 'Cinema'), ('Philosophy', 'Philosophy'), ('Religion', 'Religion'), ('Information', 'Information'), ('Thoughts', 'Thoughts'), ('Tasks', 'Tasks'), ('Notes', 'Notes'), ('News', 'News'), ('Random', 'Random'), ('Work', 'Work'), ('Study', 'Study'), ('Finance', 'Finance'), ('Travel', 'Travel'), ('Recipes', 'Recipes'), ('Projects', 'Projects'), ('Ideas', 'Ideas'), ('Health', 'Health'), ('Reminders', 'Reminders'), ('Polity', 'Polity'), ('Economy', 'Economy'), ('Geography', 'Geography'), ('History', 'History'), ('Science & Tech', 'Science & Tech'), ('Environment', 'Environment'), ('Current Affairs', 'Current Affairs'), ('Unmarked', 'Unmarked')], default='Unmarked', max_length=30),
        ),
    ]

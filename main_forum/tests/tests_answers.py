from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from main_forum.models.question_model import Question
from django.utils.text import slugify
from django_quill.fields import QuillField
import os
import json

# Override database settings for testing
@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }
)
class QuestionModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test question with QuillField content
        quill_content = json.dumps({
            'html': '<p>I need help understanding how to write effective unit tests in Django.</p>',
            'delta': {
                'ops': [
                    {'insert': 'I need help understanding how to write effective unit tests in Django.\n'}
                ]
            }
        })
        
        # Create a test question
        self.question = Question.objects.create(
            author=self.user,
            subject='How to write unit tests?',
            content=quill_content,
            status=1  # Published
        )
        # Add tags using taggit
        self.question.tags.add('python', 'testing')

    def test_question_creation(self):
        """Test that a question can be created with proper attributes"""
        self.assertEqual(self.question.subject, 'How to write unit tests?')
        self.assertEqual(self.question.author, self.user)
        self.assertEqual(
            self.question.content.html,
            '<p>I need help understanding how to write effective unit tests in Django.</p>'
        )
        self.assertEqual(self.question.status, 1)  # Published
        self.assertEqual(self.question.slug, slugify('How to write unit tests?'))
        self.assertIsNotNone(self.question.created_on)
        self.assertEqual(str(self.question), 'How to write unit tests?')  # Testing __str__ method
        self.assertEqual(sorted(list(self.question.tags.names())), sorted(['python', 'testing']))
        
    def test_voting_system(self):
        """Test the voting functionality"""
        # Create another user to test voting
        voter = User.objects.create_user(
            username='voter',
            email='voter@example.com',
            password='voterpass123'
        )
        
        # Test upvoting
        self.question.upvotes.add(voter)
        self.assertEqual(self.question.number_of_upvotes(), 1)
        
        # Test downvoting
        self.question.downvotes.add(voter)
        self.assertEqual(self.question.number_of_downvotes(), 1)
        
        # Test net votes
        self.assertEqual(self.question.net_votes, 0)  # Should be 0 as we have 1 upvote and 1 downvote

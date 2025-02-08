# main_forum/tests/tests_questions.py

from django.test import TestCase
from django.contrib.auth.models import User
from main_forum.models.question_model import Question
import json

class SimpleQuestionTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test that we can create a user and verify their details"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_question_creation(self):
        """Test that we can create a question with the required fields"""
        # Create QuillField content
        quill_content = json.dumps({
            'html': '<p>This is a test question content</p>',
            'delta': {
                'ops': [
                    {'insert': 'This is a test question content\n'}
                ]
            }
        })
        
        question = Question.objects.create(
            author=self.user,
            subject='Test Question',
            content=quill_content,
            status=1  # Published
        )
        
        # Verify the question was created with correct attributes
        self.assertEqual(question.subject, 'Test Question')
        self.assertEqual(question.author, self.user)
        self.assertEqual(question.status, 1)
        self.assertIsNotNone(question.created_on)

    def test_user_login(self):
        """Test that we can log in with the created user"""
        login_successful = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_successful)
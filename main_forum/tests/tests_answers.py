from django.test import TestCase
from django.contrib.auth.models import User
from main_forum.models.question_model import Question
from main_forum.models.answer_model import Answer
import json

class SimpleAnswerTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create QuillField content for question
        quill_content = json.dumps({
            'html': '<p>This is a test question content</p>',
            'delta': {
                'ops': [
                    {'insert': 'This is a test question content\n'}
                ]
            }
        })
        
        # Create a simple question
        self.question = Question.objects.create(
            author=self.user,
            subject='Test Question',
            content=quill_content,
            status=1  # Published
        )

    def test_answer_creation(self):
        """Test that we can create an answer for a question"""
        # Create QuillField content for answer
        answer_content = json.dumps({
            'html': '<p>This is a test answer</p>',
            'delta': {
                'ops': [
                    {'insert': 'This is a test answer\n'}
                ]
            }
        })
        
        answer = Answer.objects.create(
            author=self.user,
            question=self.question,
            body=answer_content,
            status=1  # Published
        )
        
        self.assertEqual(answer.author, self.user)
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.status, 1)
        self.assertTrue(answer.approved)  # Should be True by default

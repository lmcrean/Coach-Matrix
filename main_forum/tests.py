from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main_forum.models import Question, Answer
from django.utils import timezone
import json

class QuestionAnswerTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='testpassword123')
        self.user2 = User.objects.create_user(username='user2', password='testpassword123')
        
        # Simulate correct JSON structure for QuillField content
        quill_content = json.dumps({
            "delta": {
                "ops": [{"insert": "Test Content\n"}]
            },
            "html": "<p>Test Content</p>"
        })

        # Create a question with the simulated QuillField content
        self.question = Question.objects.create(
            title='Test Question',
            content=quill_content,  # Directly use the JSON string
            subject='Test Subject',
            status=1,
            author=self.user1,
            created_on=timezone.now(),
        )

    def test_question_creation(self):
        # Check that the question was created in setUp
        self.assertEqual(Question.objects.count(), 1)

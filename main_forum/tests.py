from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main_forum.models import Question, Answer
from django.utils import timezone

class QuestionAnswerTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='testpassword123')
        self.user2 = User.objects.create_user(username='user2', password='testpassword123')
        # Create a question to answer
        self.question = Question.objects.create(
            title='Test Question',
            content='Test Content',
            subject='Test Subject',
            status=1,
            author=self.user1,
            created_on=timezone.now(),
        )

    def test_question_creation(self):
        # Check that the question was created in setUp
        self.assertEqual(Question.objects.count(), 1)

    def test_answer_creation(self):
        # Simulate logging in
        self.client.login(username='user2', password='testpassword123')
        
        # Define data for the form to submit an answer
        answer_data = {
            'body': 'Test Answer',
            'status': 1,
        }
        
        # Simulate submitting the form to submit an answer
        response = self.client.post(reverse('submit_answer', args=[self.question.id]), answer_data)
        
        # Check that an answer was created
        self.assertEqual(Answer.objects.count(), 1)
        
        # Check that the answer is associated with the correct question
        answer = Answer.objects.first()
        self.assertEqual(answer.question, self.question)
        
        # Check that the response redirects to the question detail page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.question.get_absolute_url())

    def test_unauthenticated_user_cannot_answer(self):
        # Try to post an answer without logging in
        answer_data = {
            'body': 'Test Answer',
            'status': 1,
        }
        
        response = self.client.post(reverse('submit_answer', args=[self.question.id]), answer_data)
        
        # Check that no answer was created
        self.assertEqual(Answer.objects.count(), 0)
        
        # Check that the response is a redirect to the login page
        self.assertEqual(response.status_code, 302)
# main_forum/tests/tests_questions.py

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import psycopg2
from urllib.parse import urlparse
import os
import logging

class UserQuestionTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        # Initialize the WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Parsing the database URL from the environment variable
        database_url = os.getenv('DATABASE_URL')
        if database_url is None:
            raise ValueError("The DATABASE_URL environment variable is not set.")
        
        parsed_url = urlparse(database_url)
        self.conn = psycopg2.connect(
            dbname=parsed_url.path[1:],
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )

    def tearDown(self):
        self.conn.close()

        # Helper methods
    def check_user_exists(self, email):
        with self.conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM auth_user WHERE email = %s", (email,))
            return cur.fetchone()[0] > 0

    def add_user(self, user):
        self.driver.get(f"{self.live_server_url}/signup/")  # Adjust the URL to your signup route
        self.driver.find_element(By.NAME, "email").send_keys(user["email"])
        self.driver.find_element(By.NAME, "username").send_keys(user["username"])
        self.driver.find_element(By.NAME, "password").send_keys(user["password"])
        self.driver.find_element(By.NAME, "password2").send_keys(user["password"])  # Assuming you have password confirmation
        self.driver.find_element(By.ID, "submit-signup").click()

    def log_in(self, email, password):
        self.driver.get(f"{self.live_server_url}/login/")  # Adjust the URL to your login route
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.ID, "submit-login").click()

    def add_question(self, question):
        self.driver.get(f"{self.live_server_url}/ask_question/")  # Adjust the URL to your question route
        self.driver.find_element(By.NAME, "subject_line").send_keys(question["subject"])
        self.driver.find_element(By.NAME, "content").send_keys(question["content"])
        # Assuming you have a way to select tags, adjust selector accordingly
        tag_selector = f"input[name='tags'][value='{question['tags']}']"
        self.driver.find_element(By.CSS_SELECTOR, tag_selector).click()
        self.driver.find_element(By.ID, "submit-question").click()

    def log_out(self):
        self.driver.get(f"{self.live_server_url}/logout/")  # Adjust the URL to your logout route
        # Assuming you have a logout button
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "submit-logout"))).click()

        # Test methods
    def test_user_creation_and_login(self):
        users = [
            {"email": "user1@example.com", "username": "user1", "password": "password1"},
            {"email": "user2@example.com", "username": "user2", "password": "password2"},
            {"email": "user3@example.com", "username": "user3", "password": "password3"}
        ]
        
        for user in users:
            if not self.check_user_exists(user["email"]):
                self.add_user(user)
                logging.info(f"Created user: {user['email']}")
            self.log_in(user["email"], user["password"])
            self.log_out()

    def test_add_question(self):
        # This test assumes that a user is already created and can log in
        self.log_in("user1@example.com", "password1")
        questions = [
            {
                "subject": "Seeking effective Classroom Management Strategies",
                "content": "In a classroom of 30 high school students, I'm seeking effective management strategies.",
                "tags": "behavior_management"
            },
            {
                "subject": "How can I apply more Interactive Teaching Methods in my Science Classes?",
                "content": "Teaching a diverse group of middle schoolers science, seeking interactive teaching methods.",
                "tags": "planning"
            },
            {
                "subject": "Looking to incorporate more technology into my teaching for a class of 20 students.",
                "content": "My class is 20 students, seeking innovative ways to integrate technology that enhances learning.",
                "tags": "planning"
            }
        ]
        
        for question in questions:
            self.add_question(question)
            # Check if question was added, this could be done by verifying the page or checking the database
            # Example assertion
            page_source = self.driver.page_source
            self.assertIn(question["subject"], page_source)
        
        self.log_out()
import os
import psycopg2
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Define users to be created
users = [
    {"email": "user1@example.com", "username": "user1", "password": "password1"},
    {"email": "user2@example.com", "username": "user2", "password": "password2"},
    {"email": "user3@example.com", "username": "user3", "password": "password3"}
]

# Parsing the database URL from the environment variable
database_url = os.getenv('DATABASE_URL')
parsed_url = urlparse(database_url)
dbname = parsed_url.path[1:]
user = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port

# Define questions to be added
questions = [
    {
        "subject": "Seeking effective Classroom Management Strategies",
        "content": "In a classroom of 30 high school students, I'm seeking effective management strategies. Already tried group work with mixed results. Looking for advice on individualized attention within this large group.",
        "tags": "behavior_management"
    },
    {
        "subject": "Interactive Teaching Methods",
        "content": "Teaching a diverse group of middle schoolers science, seeking interactive teaching methods that can engage students of varying skill levels. Utilized lab experiments, looking for more inclusive activities.",
        "tags": "planning"
    },
    {
        "subject": "Incorporating Technology in Teaching",
        "content": "Looking to incorporate more technology into my teaching for a class of 20 students. Used basic PowerPoint presentations, seeking innovative ways to integrate technology that enhances learning.",
        "tags": "planning"
    }
]


# Function to check if a user already exists in the database
def check_user_exists(conn, email):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
        return cur.fetchone()[0] > 0

# Function to add a user through the web form
def add_user(driver, user):
    driver.get("http://127.0.0.1:8000/")  # Navigate to the main page
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up"))).click()
    driver.find_element(By.NAME, "email").send_keys(user["email"])
    driver.find_element(By.NAME, "username").send_keys(user["username"])
    driver.find_element(By.NAME, "password").send_keys(user["password"])
    driver.find_element(By.ID, "submit").click()

def log_in(driver, email, password):
    # Navigate to the login page
    driver.get("http://127.0.0.1:8000/")
    # Click the login button
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Login"))).click()
    # Fill in the login form
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.ID, "submit-login").click()  # Make sure this is the correct ID for the login button

def add_question(driver, question, tag_selector):
    # Navigate to the ask_question page
    driver.get("http://127.0.0.1:8000/ask_question/") 
    # Fill in the question form
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "subject_line")))
    driver.find_element(By.NAME, "subject_line").send_keys(question["subject"])
    driver.find_element(By.NAME, "content").send_keys(question["content"])
    # Select the tag
    driver.find_element(By.CSS_SELECTOR, tag_selector).click()
    # Submit the form
    driver.find_element(By.ID, "submit-question").click()  # Make sure this is the correct ID for the submit button

def log_out(driver):
    # Navigate to the logout page
    driver.get("http://127.0.0.1:8000/accounts/logout/")
    # Wait for the logout button to be clickable and click it to confirm logout
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-signup"))).click()


def main():
    logging.basicConfig(level=logging.INFO)
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    driver = webdriver.Chrome()  # Adjust as necessary

    try:
        for i, user in enumerate(users):
            if not check_user_exists(conn, user["email"]):
                add_user(driver, user)
                logging.info(f"Created user: {user['email']}")
            # Log in the user
            log_in(driver, user["email"], user["password"])
            # Each user asks a question
            if i < len(questions) and not check_question_exists(conn, questions[i]["subject"]):
                # The tag_selector needs to be specific to the tag you want to click for each question
                tag_selector = f"input[name='tags'][value='{questions[i]['tags']}']"
                add_question(driver, questions[i], tag_selector)
                logging.info(f"Added question: {questions[i]['subject']}")
            else:
                logging.info(f"User already exists or no question available, skipped: {user['email']}")
            # Log out the user
            log_out(driver)

    finally:
        conn.close()
        driver.quit()

if __name__ == "__main__":
    main()

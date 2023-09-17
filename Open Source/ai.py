from colorama import Fore, Style, init
from github import Github
import os
import time
import platform

# Function to clear the terminal screen based on the current OS
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

clear_screen()

Title = "Lucky AI - Soon to be VERY ADVANCED (BETA)"
os.system("title " + Title)

# Initialize colorama for colored terminal output
init(autoreset=True)

GITHUB_TOKEN = "YOUR GITHUB TOKEN HERE" # GITHUB TOKEN
REPO_NAME = "GITHUB REPO NAME" # GITHUB REPO NAME
QUESTION_FILE = "questions.txt"  # FILE

clear_screen()

# Initialize the GitHub instance using the token
g = Github(GITHUB_TOKEN)

# Get the user or organization that owns the repository
user = g.get_user()

clear_screen()

# Get or create the repository
try:
    repo = user.get_repo(REPO_NAME)
except Exception as e:
    print(f"Repository '{REPO_NAME}' not found. Creating a new one...")
    repo = user.create_repo(REPO_NAME)

# Function to retrieve the answer from the GitHub repository
def get_answer(question):
    try:
        content = repo.get_contents(QUESTION_FILE)
        questions_and_answers = content.decoded_content.decode('utf-8').split('\n')
        for line in questions_and_answers:
            q, a = line.split('|', 1)
            if q.strip().lower() == question.strip().lower():
                return a.strip()
        return None
    except Exception as e:
        return None

# Function to add a new question and answer to the GitHub repository
def add_question(question, answer):
    try:
        if answer.strip().lower() != "declined to answer":
            content = repo.get_contents(QUESTION_FILE)
            current_content = content.decoded_content.decode('utf-8')
            new_content = f"{current_content.rstrip()}\n{question.strip()} | {answer.strip()}"
            repo.update_file(QUESTION_FILE, f"Update question: {question}", new_content, content.sha)
            print(f"{Fore.GREEN}AI: Question '{question}' added to the repository.{Style.RESET_ALL}")
        else:
            print(f"{Fore.MAGENTA}AI: The question was declined and not added to the repository.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}AI: Error adding question: {e}{Style.RESET_ALL}")

# Welcome message
print(f"{Fore.CYAN}AI: Welcome to the Q&A Bot! Ask me anything, type !commands for commands, or type 'exit' to quit.{Style.RESET_ALL}")

# Main loop
while True:
    user_input = input(f"{Fore.BLUE}User:{Style.RESET_ALL} ").strip()

    if user_input.lower() == 'exit':
        break

    if user_input.lower() == '!clear':  # Check if the user wants to clear the console
        clear_screen()
        continue

    # Split the input to extract the question and answer (if available)
    parts = user_input.split('|', 1)

    if len(parts) == 2:
        question, answer = parts[0].strip(), parts[1].strip()
        add_question(question, answer)
        print(f"{Fore.GREEN}AI: Question '{question}' and answer added to the repository.{Style.RESET_ALL}")
    else:
        question = user_input
        answer = get_answer(question)
        if answer:
            print(f"{Fore.MAGENTA}AI: {answer}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}AI: I don't know the answer to that question.{Style.RESET_ALL}")
            user_answer = input(f"{Fore.BLUE}User:{Style.RESET_ALL} Do you want to provide an answer? (yes/no): ").strip().lower()
            if user_answer == "yes":
                user_answer = input(f"{Fore.BLUE}User:{Style.RESET_ALL} What's the answer to this question? ").strip()
                add_question(question, user_answer)
            else:
                print(f"{Fore.MAGENTA}AI: Your decision to decline has been recorded.{Style.RESET_ALL}")
                add_question(question, "Declined to answer")

# Print a goodbye message
print(f"{Fore.CYAN}AI: Goodbye! Thank you for using Lucky AI.{Style.RESET_ALL}")

# file_handler.py
import csv

def load_users(file_path):
    """Load users from a CSV file. Returns an empty list if the file doesn't exist."""
    users = []
    try:
        with open(file_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append(row)
    except FileNotFoundError:
        pass  # First run — no file yet, return empty list
    return users

def save_users(file_path, users):
    """Save a list of user dicts to a CSV file."""
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "password"])
        writer.writeheader()
        writer.writerows(users)
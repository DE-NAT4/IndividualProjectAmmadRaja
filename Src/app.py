import users
import file_handler
from pathlib import Path

def main_menu():
    """Display the main menu and return the user's choice."""
    print("\n--- User Management ---")
    print("1: Add User")
    print("2: View Users")
    print("3: Enable/Disable User")
    print("4: Test Login")
    print("0: Exit")
    return input("Enter your choice: ").strip()

def main():
    base = Path(__file__).resolve().parent.parent / "data"
    base.mkdir(exist_ok=True) #Added this so it automatically creates data folder without manually having to do it 
    active_path = base / "active_users.csv"            # ← path #1
    disabled_path = base / "disabled_users.csv"        # ← path #2
    
    #Below we essentially "Run this function. Whatever it gives me back, store it in this variable."
    #This essentially calls the load_users function in file handler which first returns an empty list then if the csv has any items it appends to the list "users"
    #Then finally users list is returned and stored as variable acitve_users which then gets passed onto users.py through the menu.
    active_users = file_handler.load_users(active_path)        # ← call list #1
    disabled_users = file_handler.load_users(disabled_path)    # ← call list #2
    
    while True:
        choice = main_menu()
        match choice:
            case "0":
                print("Exiting...")
                break
            case "1": users.add_user(active_users, disabled_users)
            case "2": users.view_users(active_users, disabled_users)
            case "3": users.toggle_user(active_users, disabled_users)
            case "4": users.test_login(active_users)
            case _:   print("Invalid choice")
    
    file_handler.save_users(active_path, active_users)         # ← save #1
    file_handler.save_users(disabled_path, disabled_users)     # ← save #2

main()
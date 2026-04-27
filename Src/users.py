def add_user(active_users, disabled_users):
    """
    Prompt for a username and password, then add a new user to the
    active list. Rejects the username if it already exists in EITHER
    list — usernames must be unique across the whole system.
    """
    # Ask for the username and strip whitespace so " alice" and "alice"
    # aren't treated as different users.
    name = input("Enter new username: ").strip()
    
    # Empty usernames don't make sense — bail out early.
    if not name:
        print("Username cannot be empty.")
        return
    
    # Check both lists for duplicates. We combine them with + so we only
    # write the loop once. This creates a temporary combined list just
    # for the check; the originals are untouched.
    for user in active_users + disabled_users:
        if user["name"] == name:
            print(f"A user named '{name}' already exists.")
            return
    
    # Username is unique — now ask for the password.
    password = input("Enter password: ").strip()
    
    # Build the user dict and append it to the active list.
    # New users are active by default — they go straight into active_users.
    # .append mutates the list in place, so main()'s list is updated too.
    active_users.append({"name": name, "password": password})
    print(f"User '{name}' added successfully.")
    

def view_users(active_users, disabled_users):
    """
    Display all users, grouped by status. The status isn't stored on
    each user — it's implied by which list they're in. This function
    shows the heading; the names underneath inherit that status.
    """
    # Active section
    print("\n--- Active Users ---")
    if not active_users:
        # Empty list — show a placeholder so the user knows it's empty,
        # not that the program glitched.
        print("  (none)")
    else:
        for user in active_users:
            # We don't print the password
            print(f"  {user['name']}")
    
    # Disabled section — same pattern.
    print("\n--- Disabled Users ---")
    if not disabled_users:
        print("  (none)")
    else:
        for user in disabled_users:
            print(f"  {user['name']}")


def _move_user(from_list, to_list):
    """
    Internal helper: show the users in `from_list` with indexes,
    ask which one to move, and move them to `to_list`.
    Both disable and enable are the same operation in opposite directions,
    so we write it once and call it twice with the lists swapped.
    """
    # Nothing to move — bail out early with a friendly message.
    if not from_list:
        print("No users available.")
        return
    
    # Show users with their index so the user can pick by number,
    for i, user in enumerate(from_list):
        print(f"  {i}: {user['name']}")
    
    choice = input("Enter the number of the user: ").strip()
    
    # Validate that the input is a number. .isdigit() returns False
    # for empty strings, "abc", "-1", etc. — anything not a non-negative integer.
    if not choice.isdigit():
        print("Please enter a valid number.")
        return
    
    idx = int(choice)
    
    # Validate that the number is actually a valid index for the list.
    if idx < 0 or idx >= len(from_list):
        print("That number is out of range.")
        return
    
    # Remove the user from the source list and capture the dict.
    user = from_list.pop(idx)
    
    # Append to the destination list. Both .pop and .append mutate
    # in place, so the lists in main() reflect the change immediately.
    to_list.append(user)
    print(f"User '{user['name']}' disabled.")
    
def toggle_user(active_users, disabled_users):
    """
    Sub-menu for enabling or disabling users. Disable moves a user
    from active → disabled; enable moves them disabled → active.
    The actual move is delegated to _move_user.
    """
    print("\n--- Enable / Disable ---")
    print("1: Disable an active user")
    print("2: Enable a disabled user")
    print("3: Return to main menu")
    choice = input("Enter your choice: ").strip()
    
    match choice:
        case "1":
            # Disable: move FROM active TO disabled.
            _move_user(active_users, disabled_users)
        case "2":
            # Enable: move FROM disabled TO active. Same helper, swapped args.
            _move_user(disabled_users, active_users)
        case "3":
            # User changed their mind — just return without doing anything.
            return
        case _:
            print("Invalid choice.")


def test_login(active_users):
    """
    Stretch goal: verify a username/password combination against the
    active users list. Disabled users cannot log in (which is the
    whole point of disabling them).
    
    passwords are stored and compared as plain text
    """
    name = input("Username: ").strip()
    password = input("Password: ").strip()
    
    # Loop through active users looking for a match on BOTH fields.
    for user in active_users:
        if user["name"] == name and user["password"] == password:
            print("ACCESS GRANTED")
        else:
            print("ACCESS DENIED: wrong password.")
        return
    
    print("ACCESS DENIED: no such active user")
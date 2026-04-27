Testing

Test 1 — Add users
Input: Menu 1, username alice, password pw1. Then menu 1 again, username bob, password pw2.
Expected: Both users added successfully.
Screenshot: ![Test 1](screenshots/Test%201.png)


Test 2 — View users
Input: Menu 2.
Expected: Active section shows alice and bob. Disabled section shows (none).
Screenshot: ![Test 2](screenshots/Test%202.png)

Test 3 — Disable a user and view it
Input: Menu 3 → 1 (disable) → 0 (alice's index).
Expected: User 'alice' moved.
Screenshot: ![Test 3](screenshots/Test%203.png)

Test 4 — Login as active user
Input: Menu 4, username bob, password pw2.
Expected: ACCESS GRANTED.
Screenshot: ![Test 4](screenshots/Test%204.png)

Test 5 — Login as disabled user
Input: Menu 4, username alice, password pw1.
Expected: ACCESS DENIED — no such active user. Even though her password is correct, alice is disabled and cannot log in.
Screenshot: ![Test 5](screenshots/Test%205.png)

Test 6 — Exit and check persistence
Input: Menu 0.
Expected: Program exits cleanly. The CSV files in data/ reflect the final state — bob in active_users.csv, alice in disabled_users.csv.
Screenshot of terminal: ![Test 6 terminal](screenshots/Test%206.1.png)
Screenshot of CSV contents: ![Test 6 active CSV](screenshots/Test%206.2.png) ![Test 6 disabled CSV](screenshots/Test%206.3.png)
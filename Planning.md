# Planning for the project

## 1 — Project structure
Created `src/` and `data/` folders. The idea was to keep source code separate from runtime data

## 2 — Working out what functions we need
Started by mapping the pseudocode against features:
- Add user
- View active and disabled users
- Enable/disable users (toggle between lists)
- Test login (stretch)
- Save and load to CSV (stretch)

My first instinct was to have an initial menu that asked "do you want to make an active user or a disabled user." Talked it through and realised that's not actually what the brief is asking for — the menu in the pseudocode is flat (1 = add, 2 = view, 3 = toggle, 0 = exit), and every new user starts active by default. Disabling is a separate action, not a separate creation path. Adjusted the plan.

## 3 — File structure: three modules
Decided to split the code into three files instead of one:
- `app.py` — the main menu loop, the entry point
- `users.py` — all the user operations (add, view, toggle, login)
- `file_handler.py` — only handles loading and saving CSVs

The reasoning was **separation of concerns**: each file should have one job. `app.py` is the "presentation layer" (it talks to the user), `users.py` is the "business logic" (it knows what it means to add or disable a user), and `file_handler.py` is the "persistence layer" (it knows how to read/write CSVs). If I ever wanted to swap CSV for a database, I'd only have to touch `file_handler.py`. None of the other code would care.

This is similar to the team project where we did products/orders/couriers, but I had to think about whether to copy that exact structure or not.

## 4 — Where do the lists live?
This was the part that took the most thinking. At first I thought maybe `file_handler.py` should hold the active and disabled lists, since that's the file that creates them when loading. But after talking it through, that mixes responsibilities — the file handler would end up doing both "read/write the disk" and "be the source of truth for user data." Two jobs, not one.

The cleaner answer: the lists live as **local variables inside `main()` in `app.py`**. The file handler just returns them when called and receives them when saving. It never holds them between calls. `users.py` also just takes them as arguments — it never stores them either. Both helper modules are stateless. `main()` is the only thing that "owns" the lists.

This made me think about how production systems work — the lists wouldn't actually live in Python at all in a real app, they'd be in a database. The app would just query "give me active users" each time. Our `file_handler.py` is basically pretending to be a tiny database.

## 5 — One CSV file or two?
Real design decision here. Two options:
- **Option A:** One file, with a `status` column on each row (active/disabled).
- **Option B:** Two separate files (`active_users.csv` and `disabled_users.csv`).

Went with **B (two files)** because the pseudocode says "ACTIVE USER LIST" and "DISABLED USER LIST" as two separate things.

The trade off this creates: the status of a user isn't stored anywhere on the user record itself — it's implied by which list (which file) they're in. So when I print users in `view_users`, the status comes from the section heading ("--- Active Users ---"), not from any field on the user dict. Felt a bit off at first but it works fine for this scope.

## 6 — Two file paths, one generic loader
Since I went with two files, I needed two file paths in `main()`:

```python
base = Path(__file__).resolve().parent.parent / "data"
active_path = base / "active_users.csv"
disabled_path = base / "disabled_users.csv"
```

Used `Path(__file__).resolve().parent.parent` so the path is relative to where the script lives, not where it's run from. I learned this in a previous project — if you use a relative path like `"data/users.csv"`, it breaks the moment someone runs the script from a different folder. Anchoring to `__file__` makes it robust.

The file handler functions (`load_users` and `save_users`) take a path as an argument and don't care which file they're working on. So I call each one twice in `main()` — once for active, once for disabled. This avoided having two near-identical functions like `load_active()` and `load_disabled()`. One generic function, two calls = no duplicated code.

## 7 — When to save and load
Picked the simplest pattern: **load once at startup, save once at exit.** All changes during the program just mutate the in-memory lists. The CSV catches up when `main()` ends.

The alternative would be saving after every action (every add, every toggle), which is safer if the program crashes mid-run, but adds disk I/O and makes `users.py` need to know about file paths. For a small CLI tool, save-at-exit is fine, and it keeps `users.py` pure (no file I/O at all in there).

## 8 — How list mutation actually works (this was important)
At one point I asked: "if I disable a user inside `toggle_user`, will the change actually show up when I view users later?" Turns out yes, because Python passes lists **by reference**. When `main()` passes `active_users` into a function, the function isn't getting a copy — it's getting the same list. So `.append()`, `.pop()`, `.remove()` all change the original. The function "sees" `main()`'s list directly.

If I'd written `active_users = active_users + [new_user]` instead of `active_users.append(new_user)`, that would create a new local list and the change wouldn't escape the function. 

Worth knowing because this is how every helper function in `users.py` works — they all mutate the lists in place, which is why the changes "stick."

## 9 — Sub-menu for enable/disable
Inside `toggle_user`, I have a small sub-menu (1 = disable, 2 = enable, 3 = cancel). At first I considered nested menus per entity (an "active users menu" and a "disabled users menu"), like my group project did for products/orders/couriers. However this project is different products and orders were genuinely different things with different operations, but active and disabled users are the same thing in different states. So the flat main menu plus one sub-menu inside `toggle_user` was cleaner.

I also factored disable and enable into a single internal helper `_move_user(from_list, to_list)` because they're literally the same operation with the lists swapped. Disable = move from active to disabled. Enable = move from disabled to active. Same code, different arguments.

## 10 — Input validation
Spent a bit of time making sure user input doesn't crash the program. If someone types "abc" when asked for a number, or hits enter without typing anything, or picks an out-of-range index — none of that should kill the program. Used `.isdigit()` to check before converting to int, then range checked before indexing. 

Also stopped using `int(input(...))` for the menu and just compared strings (`case "1":` instead of `case 1:`). Means the menu can't crash from bad input either.

## 11 — Login feedback
Originally `test_login` just said "ACCESS DENIED" with no detail. So I split it into two messages: "no such active user" vs "incorrect password." Added a comment in the function explaining 

## 12 — Setting up venv and gitignore
Late in the project I added a virtual environment (`.venv/`) even though the project doesn't actually use any third-party packages. Reasoning: it's the standard Python workflow and worth practising even when not strictly needed. Also added a `.gitignore` to keep `__pycache__/`, `.venv/`, the data CSVs out of the repo.

The CSV ignore was a deliberate choice they're runtime data, generated by users, not part of the source. Anyone cloning the repo gets a clean slate. To stop the empty `data/` folder disappearing from Git (Git doesn't track empty folders), I considered adding a `.gitkeep` placeholder, and also made sure the path code handles the case where the file doesn't exist yet (the `try/except FileNotFoundError` in `load_users`).

## 13 — One bug worth recording
At first the CSVs were being saved into `src/` instead of `data/`. The bug was in the path:
- `Path(__file__).resolve().parent` resolves to the folder `app.py` is in, which is `src/`.
- I needed to go up one more level and into `data/`, so `parent.parent / "data"`.

Same pattern from the group café project, I'd just forgotten to apply it.

## Summary of decisions
- Three modules, separated by concern (app / logic / persistence)
- Lists owned by `main()`, passed as arguments to helpers
- Two CSV files (matching pseudocode) — one generic loader called twice
- Load at start, save at exit
- Mutate lists in place, never rebind
- Flat main menu + sub-menu inside `toggle_user`
- Specific login error messages 
- Venv and gitignore set up properly even though they aren't needed for tis project
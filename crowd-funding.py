import re , json , os
from datetime import datetime

current_user = None
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

# print(json.dumps(users, indent=4))

            # Register Function called if choice = 1
def register():
    print("\n--- User Registration ---")

    username_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{2,}$'
    while True:
        username = input("Enter your username: ").strip().lower()
        if username == "":
            print("Username can't be empty.")
        elif len(username) < 3:
            print("Username must be at least 3 characters.")
        elif not re.match(username_pattern, username):
            print("Invalid username. It must start with a letter and contain only letters, digits, or underscore.")
        elif username in users:
            print("Username already exists.")
        else:
            break
    print(f"Username set: {username}")

    while True:
        firstname = input("Enter your first name: ").strip()
        if firstname == "":
            print("First name cannot be empty.")
        elif len(firstname) < 3:
            print("First name must be at least 3 characters.")
        elif not firstname.isalpha():
            print("First name must contain only letters.")
        else:
            firstname = firstname.capitalize()
            break

    while True:
        lastname = input("Enter your last name: ").strip()
        if lastname == "":
            print("Last name cannot be empty.")
        elif len(lastname) < 3:
            print("Last name must be at least 3 characters.")
        elif not lastname.isalpha():
            print("Last name must contain only letters.")
        else:
            lastname = lastname.capitalize()
            break

    email_pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    while True:
        email = input("Enter your email address: ").strip().lower()
        if not re.match(email_pattern, email):
            print("Invalid email. Use format like: example@example.com")
        elif any(user['email'] == email for user in users.values()):
            print("Email is already registered.")
        else:
            break
    print("Email set.")

    while True:
        password = input("Enter your password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        if password != confirm_password:
            print("Passwords do not match.")
        elif len(password) < 8:
            print("Password must be at least 8 characters.")
        else:
            break
    print("\u2705 Password set.")

    while True:
        phone_number = input("Enter your phone number (11 digits): ").strip()
        if not re.match(r'^01[0-9]{9}$', phone_number):
            print("Invalid phone number. Must be 11 digits and start with 01.")
        else:
            break
    print("Phone number set.")

    users[username] = {
        "first_name": firstname,
        "last_name": lastname,
        "email": email,
        "password": password,
        "phone": phone_number,
        "is_active": False
    }
    save_users(users)

    print("\nRegistration Successful!")
    print("Please activate your account before login.")

            # Login Function called if choice = 2

def login():
    print("\n--- Login ---")
    email = input("Enter your email: ").strip().lower()
    password = input("Enter your password: ").strip()

    for username, user in users.items():
        if user["email"] == email:
            if user["password"] != password:
                print("Incorrect password.")
                return

            if not user.get("is_active", False):
                print("Your account is not activated.")
                choice = input("Would you like to activate it now? (y/n): ").strip().lower()
                if choice == "y":
                    user["is_active"] = True
                    save_users(users)
                    print("Your account has been activated!")
                    print(f"Welcome, {user['first_name']}!")
                else:
                    print("Account not activated. Please activate later to log in.")
                return

            print(f"Login successful. Welcome, {user['first_name']}!")
            global current_user
            current_user = username
            return

    print("Email not found.")

            # PROJECTS SECTION

PROJECTS_FILE = "projects.json"

def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as p:
            return json.load(p)
    return {}

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as p:
        return json.dump(projects, p , indent=4)

projects = load_projects()

            # Create Project

def create_project():
    global current_user
    if not current_user:
        print("You must be logged in to create a project.")
        return

    print("\nPlease Enter Your Project Info:\n")

    # Title validation
    while True:
        title = input("Title: ").strip().capitalize()
        if not title:
            print("Title cannot be empty.")
        elif not title.replace(" " , "").isalpha():
            print("Title Should be alpha characters.")
        else:
            break

    # Details validation
    while True:
        details = input("Details: ").strip()
        if not details:
            print("Details cannot be empty.")
        elif len(details) < 10:
            print("Details should be more than 10 charaters")
        else:
            break

    # Target validation
    while True:
        try:
            total_target = int(input("Total target (in EGP): ").strip())
            if total_target <= 0:
                print("Target must be a positive number.")
            else:
                break
        except ValueError:
            print("Target must be an integer.")

    # Date format
    date_format = "%Y-%m-%d"

    # Start date validation
    while True:
        try:
            start_str = input("Start Date (YYYY-MM-DD): ").strip()
            start_time = datetime.strptime(start_str, date_format).date()
            if start_time <= datetime.today().date():
                print("Start date must be after today.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # End date validation
    while True:
        try:
            end_str = input("End Date (YYYY-MM-DD): ").strip()
            end_time = datetime.strptime(end_str, date_format).date()
            if end_time <= start_time:
                print("End date must be after start date.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    # Add project to the global projects dict with a new ID
    new_id = str(len(projects) + 1)
    projects[new_id] = {
        "title": title,
        "details": details,
        "target": total_target,
        "currency": "EGP",
        "start_time": str(start_time),
        "end_time": str(end_time),
        "owner": current_user
    }

    # Save to JSON
    save_projects(projects)

    print("\nProject added and saved successfully!")
    for key, value in projects[new_id].items():
        print(f"{key.capitalize()}: {value}")

        # View Projects

def view_project():
    if projects:
        print("\nAll Projects:\n")
        for pid, proj in projects.items():
            print(f"Project ID: {pid}")
            print(f"Title: {proj.get('title', '')}")
            print(f"Owner: {proj.get('owner', 'N/A')}")
            print(f"Target: {proj.get('target', 0)} {proj.get('currency', '')}")
            print(f"Duration: {proj.get('start_time')} → {proj.get('end_time')}")
            print("-" * 40)
    else:
        print("\nNo projects found.")

        # Edit Project

def edit_project():
    global current_user
    if not current_user:
        print("You must be logged in.")
        return

    my_projects = {pid: p for pid, p in projects.items() if p["owner"] == current_user}

    if not my_projects:
        print("You have no projects to edit.")
        return

    print("\nYour Projects:")
    for pid, p in my_projects.items():
        print(f"{pid}: {p['title']}")

    selected_id = input("Enter project ID to edit: ").strip()
    if selected_id not in my_projects:
        print("Invalid project ID.")
        return

    project = my_projects[selected_id]

    new_title = input(f"New Title (leave empty to keep '{project['title']}'): ").strip()
    if new_title:
        project["title"] = new_title

    new_details = input(f"New Details (leave empty to keep current): ").strip()
    if new_details:
        project["details"] = new_details

    new_target = input(f"New Target (leave empty to keep {project['target']}): ").strip()
    if new_target.isdigit():
        project["target"] = int(new_target)

    projects[selected_id] = project
    save_projects(projects)
    print("Project updated.")

        # Delete Project

def delete_project():
    global current_user
    if not current_user:
        print("You must be logged in.")
        return

    my_projects = {pid: p for pid, p in projects.items() if p["owner"] == current_user}

    if not my_projects:
        print("You have no projects to delete.")
        return

    print("\n Your Projects:")
    for pid, p in my_projects.items():
        print(f"{pid}: {p['title']}")

    selected_id = input("Enter project ID to delete: ").strip()
    if selected_id not in my_projects:
        print("Invalid project ID.")
        return

    confirm = input(f"Are you sure you want to delete '{projects[selected_id]['title']}'? (y/n): ").strip().lower()
    if confirm == "y":
        del projects[selected_id]
        save_projects(projects)
        print("Project deleted.")
    else:
        print("Deletion cancelled.")

def main_menu():
    while True:
        print("\n*********** Welcome to our Crowd-Funding Page ***********")
        print("1. Authentication System")
        if current_user:
            print("2. Projects")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            while True:
                print("\n--- Authentication System ---")
                print("1. Register")
                print("2. Login")
                print("3. Back to Main Menu")

                auth_choice = input("Enter your choice: ").strip()

                if auth_choice == "1":
                    register()
                elif auth_choice == "2":
                    login()
                elif auth_choice == "3":
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == "2":
            while True:
                print("\n************ Projects Menu ************")
                print("1. Create a Project")
                print("2. View All Projects")
                print("3. Edit Your Projects")
                print("4. Delete Your Projects")
                print("5. Back to Main Menu")

                pro_choice = input("Enter your choice: ").strip()

                if pro_choice == "1":
                    create_project()
                elif pro_choice == "2":
                    view_project()
                elif pro_choice == "3":
                    edit_project()
                elif pro_choice == "4":
                    delete_project()
                else:
                    break
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the app
main_menu()

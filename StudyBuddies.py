from guizero import App, Box, PushButton, TextBox, Text
import os

# ----- USER CLASS -----
class User:
    def __init__(self, email, password, name, times, major, topics, location, days):
        self.email = email
        self.password = password
        self.name = name
        self.times = times
        self.major = major
        self.topics = topics
        self.location = location
        self.days = days

    def to_line(self):
        return self.email + "|" + self.password + "|" + self.name + "|" + ",".join(self.times) + "|" + self.major + "|" + ",".join(self.topics) + "|" + self.location + "|" + ",".join(self.days) + "\n"

# ----- FILE FUNCTIONS -----
def create_user_from_line(line):
    parts = line.strip().split("|")
    return User(
        email=parts[0],
        password=parts[1],
        name=parts[2],
        times=parts[3].split(","),
        major=parts[4],
        topics=parts[5].split(","),
        location=parts[6],
        days=parts[7].split(",")
    )

def load_users():
    users = []
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as f:
            for line in f:
                if line.strip():
                    users.append(create_user_from_line(line))
    return users

def save_user(user):
    with open("accounts.txt", "a") as f:
        f.write(user.to_line())

def email_exists(email):
    for user in load_users():
        if user.email == email:
            return True
    return False

def login_success(email, password):
    for user in load_users():
        if user.email == email and user.password == password:
            return user
    return None

def create_dummy_users():
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as f:
            contents = f.read()
            if "alice@example.com" in contents:
                return  # already added
    dummy_users = [
        User("alice@example.com", "password123", "Alice", ["14:00", "16:00"], "CS", ["AI", "ML"], "Library", ["Monday", "Wednesday"]),
        User("bob@example.com", "securepass", "Bob", ["14:00", "15:00"], "CS", ["ML", "Data Science"], "Library", ["Wednesday", "Friday"]),
        User("charlie@example.com", "mathrules", "Charlie", ["10:00"], "Math", ["Calculus"], "Cafeteria", ["Tuesday"]),
        User("dana@example.com", "coolpass456", "Dana", ["14:00", "16:00"], "CS", ["AI"], "Library", ["Monday", "Wednesday"]),
        User("testuser@example.com", "supersecure", "TestUser", ["13:00", "14:00"], "CS", ["AI", "Security"], "Library", ["Thursday"]),
    ]
    for user in dummy_users:
        save_user(user)

# ----- GUI ACTIONS -----
def show_signup():
    login_box.hide()
    signup_box.show()

def show_login():
    signup_box.hide()
    login_box.show()

def do_signup():
    email = signup_email.value
    password = signup_password.value
    name = signup_name.value
    times = signup_times.value.split(",")
    major = signup_major.value
    topics = signup_topics.value.split(",")
    location = signup_location.value
    days = signup_days.value.split(",")

    if email == "" or password == "" or name == "":
        signup_message.value = "Please fill in all required fields."
        return
    if "@" not in email or "." not in email:
        signup_message.value = "Please use a valid email address."
        return
    if len(password) < 8 or len(password) > 15:
        signup_message.value = "Password must be 8–15 characters."
        return
    if email_exists(email):
        signup_message.value = "That email already exists."
        return

    user = User(email, password, name, times, major, topics, location, days)
    save_user(user)
    signup_message.value = "Signup successful! Please log in."
    signup_box.hide()
    login_box.show()

def do_login():
    email = login_email.value
    password = login_password.value
    user = login_success(email, password)
    if user:
        login_box.hide()
        show_main_app(user)
    else:
        login_message.value = "Invalid login. Try again."

def show_main_app(user):
    name_box.value = user.name
    major_box.value = user.major
    time_box.value = ",".join(user.times)
    topic_box.value = ",".join(user.topics)
    location_box.value = user.location
    days_box.value = ",".join(user.days)
    main_box.show()

def find_matches(current_user):
    matches = []
    for user in load_users():
        if user.email == current_user.email:
            continue
        if any(topic in current_user.topics for topic in user.topics):
            matches.append(user)
        elif any(time in current_user.times for time in user.times):
            matches.append(user)
        elif user.major == current_user.major or user.location == current_user.location:
            matches.append(user)
    return matches

def on_find_matches():
    name = name_box.value
    major = major_box.value
    times = time_box.value.split(",")
    topics = topic_box.value.split(",")
    location = location_box.value
    days = days_box.value.split(",")
    email = login_email.value
    password = login_password.value

    user = User(email, password, name, times, major, topics, location, days)
    matches = find_matches(user)

    results_output = ""
    if matches:
        for match in matches:
            results_output += "Match Found: " + match.name + "\n"
            results_output += "Times: " + ", ".join(match.times) + "\n"
            results_output += "Topics: " + ", ".join(match.topics) + "\n"
            results_output += "Location: " + match.location + "\n"
            results_output += "Days: " + ", ".join(match.days) + "\n"
            results_output += "-" * 40 + "\n"
    else:
        results_output = "No matches found.\n"

    results_text.value = results_output

# ----- GUI SETUP -----
app = App("Study Buddy Finder", width=600, height=700)

# Load dummy users
create_dummy_users()

# --- LOGIN BOX ---
login_box = Box(app, layout="grid")
Text(login_box, text="Email:", grid=[0, 0])
login_email = TextBox(login_box, grid=[1, 0])
Text(login_box, text="Password:", grid=[0, 1])
login_password = TextBox(login_box, grid=[1, 1])
login_message = Text(login_box, text="", grid=[0, 2, 2, 1])
PushButton(login_box, text="Login", command=do_login, grid=[0, 3, 2, 1])
PushButton(login_box, text="Go to Sign Up", command=show_signup, grid=[0, 4, 2, 1])

# --- SIGNUP BOX ---
signup_box = Box(app, layout="grid")
signup_box.hide()
Text(signup_box, text="Email:", grid=[0, 0])
signup_email = TextBox(signup_box, grid=[1, 0])
Text(signup_box, text="Password:", grid=[0, 1])
signup_password = TextBox(signup_box, grid=[1, 1])
Text(signup_box, text="Name:", grid=[0, 2])
signup_name = TextBox(signup_box, grid=[1, 2])
Text(signup_box, text="Major:", grid=[0, 3])
signup_major = TextBox(signup_box, grid=[1, 3])
Text(signup_box, text="Times:", grid=[0, 4])
signup_times = TextBox(signup_box, grid=[1, 4])
Text(signup_box, text="Topics:", grid=[0, 5])
signup_topics = TextBox(signup_box, grid=[1, 5])
Text(signup_box, text="Location:", grid=[0, 6])
signup_location = TextBox(signup_box, grid=[1, 6])
Text(signup_box, text="Days:", grid=[0, 7])
signup_days = TextBox(signup_box, grid=[1, 7])
signup_message = Text(signup_box, text="", grid=[0, 8, 2, 1])
PushButton(signup_box, text="Create Account", command=do_signup, grid=[0, 9, 2, 1])
PushButton(signup_box, text="Back to Login", command=show_login, grid=[0, 10, 2, 1])

# --- MAIN BOX ---
main_box = Box(app, layout="grid")
main_box.hide()
Text(main_box, text="Name:", grid=[0, 0])
name_box = TextBox(main_box, grid=[1, 0])
Text(main_box, text="Major:", grid=[0, 1])
major_box = TextBox(main_box, grid=[1, 1])
Text(main_box, text="Time Availability:", grid=[0, 2])
time_box = TextBox(main_box, grid=[1, 2])
Text(main_box, text="Study Topics:", grid=[0, 3])
topic_box = TextBox(main_box, grid=[1, 3])
Text(main_box, text="Location:", grid=[0, 4])
location_box = TextBox(main_box, grid=[1, 4])
Text(main_box, text="Days of Study:", grid=[0, 5])
days_box = TextBox(main_box, grid=[1, 5])
PushButton(main_box, text="Find Matches", command=on_find_matches, grid=[0, 6, 2, 1])
results_text = TextBox(main_box, multiline=True, width=80, height=30, grid=[0, 7, 2, 1])

app.display()


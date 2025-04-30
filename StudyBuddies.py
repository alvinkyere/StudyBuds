from guizero import App, Box, PushButton, TextBox, Text
import os

# Function to load students from the file
def load_students():
    students = []
    if os.path.exists("students.txt"):
        with open("students.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                students.append({
                    "name": data[0],
                    "course": data[1],
                    "study_times": data[2].split(";"),
                    "study_topics": data[3].split(";")
                })
    return students

# Function to save new student to the file
def save_student(name, course, study_times, study_topics):
    with open("students.txt", "a") as file:
        file.write(f"{name},{course},{';'.join(study_times)},{';'.join(study_topics)}\n")

# Function to find matching students
def find_matches(name, course, study_times, study_topics):
    students = load_students()
    matches = []
    
    for student in students:
        if student["course"] == course:
            # Compare study times and topics
            common_times = set(student["study_times"]).intersection(set(study_times))
            common_topics = set(student["study_topics"]).intersection(set(study_topics))
            
            if common_times and common_topics:
                matches.append({
                    "name": student["name"],
                    "common_times": list(common_times),
                    "common_topics": list(common_topics)
                })
    return matches

# Function to handle the "Find Matches" button click
def on_find_matches():
    # Get the data from the text boxes
    name = name_textbox.value
    course = course_textbox.value
    study_times = study_times_textbox.value.split(",")
    study_topics = study_topics_textbox.value.split(",")
    
    # Save the new student data to the file
    save_student(name, course, study_times, study_topics)
    
    # Find matches
    matches = find_matches(name, course, study_times, study_topics)
    
    # Clear the previous results
    results_text.clear()
    
    # Show the matches (if any)
    if matches:
        for match in matches:
            results_text.append(f"Match: {match['name']}\n")
            results_text.append(f"Common Study Times: {', '.join(match['common_times'])}\n")
            results_text.append(f"Common Study Topics: {', '.join(match['common_topics'])}\n")
            results_text.append("\n" + "-"*40 + "\n")
    else:
        results_text.append("No matching study groups found.\n")

# Set up the GUI app
app = App("Study Group Finder", width=500, height=600)

# Set up the input fields and labels
box = Box(app, layout="grid")

name_label = Text(box, text="Your Name:", grid=[0, 0])
name_textbox = TextBox(box, grid=[1, 0])

course_label = Text(box, text="Course:", grid=[0, 1])
course_textbox = TextBox(box, grid=[1, 1])

study_times_label = Text(box, text="Study Times (comma separated):", grid=[0, 2])
study_times_textbox = TextBox(box, grid=[1, 2])

study_topics_label = Text(box, text="Study Topics (comma separated):", grid=[0, 3])
study_topics_textbox = TextBox(box, grid=[1, 3])

# Button to find matches
find_matches_button = PushButton(box, text="Find Matches", command=on_find_matches, grid=[0, 4, 2, 1])

# Text area to display results
results_text = Text(box, text="", width=50, height=20, grid=[0, 5, 2, 1])

# Start the app
app.display()

"""
import os
from typing import List
from guizero import App, Box, PushButton, TextBox, Text, Window

# User class
class User:
    def __init__(self, name, time_availability, major, topic_of_study, location_of_study, days_of_study):
        self.name = name
        self.time_availability = time_availability
        self.major = major
        self.topic_of_study = topic_of_study
        self.location_of_study = location_of_study
        self.days_of_study = days_of_study

    def to_line(self):
        return f"{self.name}|{','.join(self.time_availability)}|{self.major}|{','.join(self.topic_of_study)}|{self.location_of_study}|{','.join(self.days_of_study)}\n"

    @staticmethod
    def from_line(line):
        parts = line.strip().split("|")
        return User(
            name=parts[0],
            time_availability=parts[1].split(","),
            major=parts[2],
            topic_of_study=parts[3].split(","),
            location_of_study=parts[4],
            days_of_study=parts[5].split(",")
        )

# File operations

def save_user(user: User, filename="users.txt"):
    with open(filename, "a") as f:
        f.write(user.to_line())

def load_users(filename="users.txt") -> List[User]:
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return [User.from_line(line) for line in f if line.strip()]

def find_matches(current_user: User, filename="users.txt") -> List[User]:
    users = load_users(filename)
    matches = []
    match_levels = {1: [], 2: [], 3: [], 4: []}  # Priority buckets

    for user in users:
        if user.name == current_user.name:
            continue

        common_topics = set(user.topic_of_study).intersection(current_user.topic_of_study)
        common_times = set(user.time_availability).intersection(current_user.time_availability)
        same_major = user.major == current_user.major
        same_location = user.location_of_study == current_user.location_of_study

        if common_topics:
            match_levels[1].append(user)
        elif common_times:
            match_levels[2].append(user)
        elif same_major:
            match_levels[3].append(user)
        elif same_location:
            match_levels[4].append(user)

    for level in range(1, 5):
        if match_levels[level]:
            matches = match_levels[level]
            break

    return matches

def create_dummy_users():
    dummy_users = [
        User("Alice", ["14:00", "16:00"], "CS", ["AI", "ML"], "Library", ["Monday", "Wednesday"]),
        User("Bob", ["14:00", "15:00"], "CS", ["ML", "Data Science"], "Library", ["Wednesday", "Friday"]),
        User("Charlie", ["10:00"], "Math", ["Calculus"], "Cafeteria", ["Tuesday"]),
        User("Dana", ["14:00", "16:00"], "CS", ["AI"], "Library", ["Monday", "Wednesday"]),
    ]
    for user in dummy_users:
        save_user(user)

# GUI logic

def on_find_matches():
    name = name_textbox.value
    major = major_textbox.value
    time_availability = time_textbox.value.split(",")
    topics = topic_textbox.value.split(",")
    location = location_textbox.value
    days = days_textbox.value.split(",")

    new_user = User(name, time_availability, major, topics, location, days)
    save_user(new_user)

    matches = find_matches(new_user)
    results_window = Window(app, title="Matching Results", width=500, height=400)
    results_box = Box(results_window, layout="auto")

    if matches:
        for match in matches:
            Text(results_box, text=f"\nMatch Found: {match.name}")
            Text(results_box, text=f"Times: {', '.join(match.time_availability)}")
            Text(results_box, text=f"Topics: {', '.join(match.topic_of_study)}")
            Text(results_box, text=f"Location: {match.location_of_study}")
            Text(results_box, text=f"Days: {', '.join(match.days_of_study)}")
            Text(results_box, text="-"*40)
    else:
        Text(results_box, text="No matches found.")

# GUI setup
app = App("Study Buddy Finder", width=600, height=600)
box = Box(app, layout="grid")

name_label = Text(box, text="Name:", grid=[0,0])
name_textbox = TextBox(box, grid=[1,0])

major_label = Text(box, text="Major:", grid=[0,1])
major_textbox = TextBox(box, grid=[1,1])

time_label = Text(box, text="Time Availability (comma-separated):", grid=[0,2])
time_textbox = TextBox(box, grid=[1,2])

topic_label = Text(box, text="Study Topics (comma-separated):", grid=[0,3])
topic_textbox = TextBox(box, grid=[1,3])

location_label = Text(box, text="Location:", grid=[0,4])
location_textbox = TextBox(box, grid=[1,4])

days_label = Text(box, text="Days of Study (comma-separated):", grid=[0,5])
days_textbox = TextBox(box, grid=[1,5])

find_button = PushButton(box, text="Find Matches", command=on_find_matches, grid=[0,6,2,1])

# Uncomment the following line once to generate dummy users:
create_dummy_users()

app.display()
"""

"""
Version 2
import os
from typing import List
from guizero import App, Box, PushButton, TextBox, Text

# User class
class User:
    def __init__(self, name, time_availability, major, topic_of_study, location_of_study, days_of_study):
        self.name = name
        self.time_availability = time_availability
        self.major = major
        self.topic_of_study = topic_of_study
        self.location_of_study = location_of_study
        self.days_of_study = days_of_study

    def to_line(self):
        return f"{self.name}|{','.join(self.time_availability)}|{self.major}|{','.join(self.topic_of_study)}|{self.location_of_study}|{','.join(self.days_of_study)}\n"

    @staticmethod
    def from_line(line):
        parts = line.strip().split("|")
        return User(
            name=parts[0],
            time_availability=parts[1].split(","),
            major=parts[2],
            topic_of_study=parts[3].split(","),
            location_of_study=parts[4],
            days_of_study=parts[5].split(",")
        )

# File operations

def save_user(user: User, filename="users.txt"):
    with open(filename, "a") as f:
        f.write(user.to_line())

def load_users(filename="users.txt") -> List[User]:
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return [User.from_line(line) for line in f if line.strip()]

def find_matches(current_user: User, filename="users.txt") -> List[User]:
    users = load_users(filename)
    matches = []
    match_levels = {1: [], 2: [], 3: [], 4: []}  # Priority buckets

    for user in users:
        if user.name == current_user.name:
            continue

        common_topics = set(user.topic_of_study).intersection(current_user.topic_of_study)
        common_times = set(user.time_availability).intersection(current_user.time_availability)
        same_major = user.major == current_user.major
        same_location = user.location_of_study == current_user.location_of_study

        if common_topics:
            match_levels[1].append(user)
        elif common_times:
            match_levels[2].append(user)
        elif same_major:
            match_levels[3].append(user)
        elif same_location:
            match_levels[4].append(user)

    for level in range(1, 5):
        if match_levels[level]:
            matches = match_levels[level]
            break

    return matches

def create_dummy_users():
    dummy_users = [
        User("Alice", ["14:00", "16:00"], "CS", ["AI", "ML"], "Library", ["Monday", "Wednesday"]),
        User("Bob", ["14:00", "15:00"], "CS", ["ML", "Data Science"], "Library", ["Wednesday", "Friday"]),
        User("Charlie", ["10:00"], "Math", ["Calculus"], "Cafeteria", ["Tuesday"]),
        User("Dana", ["14:00", "16:00"], "CS", ["AI"], "Library", ["Monday", "Wednesday"]),
    ]
    for user in dummy_users:
        save_user(user)

# GUI logic

def on_find_matches():
    name = name_textbox.value
    major = major_textbox.value
    time_availability = time_textbox.value.split(",")
    topics = topic_textbox.value.split(",")
    location = location_textbox.value
    days = days_textbox.value.split(",")

    new_user = User(name, time_availability, major, topics, location, days)
    save_user(new_user)

    matches = find_matches(new_user)
    results_text.clear()
    if matches:
        for match in matches:
            results_text.append(f"Match Found: {match.name}\n")
            results_text.append(f"Times: {', '.join(match.time_availability)}\n")
            results_text.append(f"Topics: {', '.join(match.topic_of_study)}\n")
            results_text.append(f"Location: {match.location_of_study}\n")
            results_text.append(f"Days: {', '.join(match.days_of_study)}\n")
            results_text.append("-"*40 + "\n")
    else:
        results_text.append("No matches found.\n")

# GUI setup
app = App("Study Buddy Finder", width=600, height=600)
box = Box(app, layout="grid")

name_label = Text(box, text="Name:", grid=[0,0])
name_textbox = TextBox(box, grid=[1,0])

major_label = Text(box, text="Major:", grid=[0,1])
major_textbox = TextBox(box, grid=[1,1])

time_label = Text(box, text="Time Availability (comma-separated):", grid=[0,2])
time_textbox = TextBox(box, grid=[1,2])

topic_label = Text(box, text="Study Topics (comma-separated):", grid=[0,3])
topic_textbox = TextBox(box, grid=[1,3])

location_label = Text(box, text="Location:", grid=[0,4])
location_textbox = TextBox(box, grid=[1,4])

days_label = Text(box, text="Days of Study (comma-separated):", grid=[0,5])
days_textbox = TextBox(box, grid=[1,5])

find_button = PushButton(box, text="Find Matches", command=on_find_matches, grid=[0,6,2,1])

results_text = Text(box, text="", width=60, height=20, grid=[0,7,2,1])

# Uncomment the following line once to generate dummy users:
create_dummy_users()

app.display()

"""

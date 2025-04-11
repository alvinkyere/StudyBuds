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

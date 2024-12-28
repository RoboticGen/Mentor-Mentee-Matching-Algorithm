import os, csv, json, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(BASE_DIR, 'tables')
mentoring_slots_table = os.path.join(TABLES, 'Mentoring-Slots.csv')
mentors_table = os.path.join(TABLES, 'Mentors-List.csv')
configuration_file = os.path.join(BASE_DIR, 'configs.json')
csv_data:list[dict] = []
menstors_data:list[dict] = []
mentors:set = set()
slots:set = set()
students:set = set()
student_preferences:dict = {}
mentor_availabilities:dict = {}

HEADER:list = ['\ufeffDisplay Name', 'Day', 'Type', 'This Week Slot', 'Next Week Slot', 'This Week Slot as String', 'Successful Mentoring Slots', 'Starting Time', 'Available Mentors', 'Students (Preferred)', 'Duration', 'Mentoring Slots']

def read_csv(file_path:str)->csv.DictReader:
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            csv_data.append(row)

def read_json(file_path:str)->dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def get_time_in_date_time_format(time:str)->datetime.datetime:
    return datetime.datetime.strptime(time, '%m/%d/%Y %I:%M %p')

# Read the data
csv_file_content = read_csv(mentoring_slots_table)
configs = read_json(configuration_file)

# Extract mentors, students, and slots from CSV data
for row in csv_data:
    mentors = mentors.union(row['Available Mentors'].split(','))
    time = datetime.datetime.strptime(row['This Week Slot as String'], '%m/%d/%Y %I:%M %p')
    students = students.union(row['Students (Preferred)'].split(','))
    slots.add(time)

mentors.remove('')
print("Mentors:", mentors)
print("Available Slots:", slots)
print("Students:", students)

# Build student preferences and mentor availabilities
for student in students:
    student_preferences[student] = []
    for row in csv_data:
        if student in row['Students (Preferred)'].split(','):
            student_preferences[student].append(get_time_in_date_time_format(row['This Week Slot as String']))

for mentor in mentors:
    mentor_availabilities[mentor] = []
    for row in csv_data:
        if mentor in row['Available Mentors'].split(','):
            mentor_availabilities[mentor].append(get_time_in_date_time_format(row['This Week Slot as String']))

# Gale-Shapley Algorithm for Matching Mentors and Students
def gale_shapley(mentors:set, students:set, mentor_availabilities:dict, student_preferences:dict, max_students_per_mentor:int = 5)->dict:
    mentor_matches = {}
    student_matches = {}
    student_preferences = {student: set(preferences) for student, preferences in student_preferences.items()}
    mentor_availabilities = {mentor: set(availabilities) for mentor, availabilities in mentor_availabilities.items()}

    while len(mentor_matches) < len(mentors):
        for mentor in mentors:
            if mentor not in mentor_matches:
                for availability in mentor_availabilities[mentor]:
                    for student in student_preferences:
                        if student not in student_matches:
                            if availability in student_preferences[student]:
                                mentor_matches[mentor] = student
                                student_matches[student] = mentor
                                break
                    if mentor in mentor_matches:
                        break

    return mentor_matches


# Run the Gale-Shapley algorithm
matches = gale_shapley(mentors, students, mentor_availabilities, student_preferences)

# Output the matches
print("Mentor-Mentee Matches:")
for mentor, student in matches.items():
    print(f"{mentor} is matched with {student} at their preferred slot.")

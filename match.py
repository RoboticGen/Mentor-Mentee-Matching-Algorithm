import os, csv

BASE_PATH:str = os.path.dirname(os.path.abspath(__file__))
TABLES_PATH:str = os.path.join(BASE_PATH, 'tables')
STUDENT_MENTORING_SLOTS:str = os.path.join(TABLES_PATH, 'Students-Mentoring.csv')
MAX_AVAILABLE_SLOTS:int = 0
MAX_AVAILABLE_MENTORS:int = 0

mentees = dict()
mentors = set()

Headers = ['Display Name', 'Parent Number WITH CODE', 'Mentoring Type', 'Pathways Level', 'Preferred Mentors', 
           'Preferred Mentoring Timeslots (from Preferred Mentors)', 'Preferred Time Slots', 'Previous Slot Mentor', 
           'Previous Slot Mentors', 'Validate Previous Mentor', "Previous Slot Mentor's Availability", 'Previous Timeslot', 
           'Validate Previous Timeslot', 'Is Previous Slot Mentor Available', 'Is Any Preferred Mentor Available in Previous Mentoring Slot', 
           'Is Any Preferred Mentor Available in Preferred Mentoring Slot', 'Previous Timeslot Type', 'Next Timeslot', 'Next Slot Mentor', 
           'Current Project']

csv_data:list[dict] = list()

def read_csv(file_path:str)->csv.DictReader:
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=Headers)
        for row in csv_reader:
            csv_data.append(row)

def calculate_priority_score(mentees:dict)->dict:
    max_priority_for_avisable_slot = (MAX_AVAILABLE_SLOTS+1)*5
    max_priority_for_mentor = (MAX_AVAILABLE_MENTORS+1)*5
    for mentee, details in mentees.items():
        num_of_mentors = len(details['Preferred Mentors'].split(','))
        num_of_time_slots_available = 0
        number_of_prefered_slots = len(details['Preferred Time Slots'].split(','))
        number_of_mentor_available_slots = len(details['Preferred Mentoring Timeslots (from Preferred Mentors)'].split(','))
        for slot in details['Preferred Time Slots'].split(','):
            if slot in details['Preferred Mentoring Timeslots (from Preferred Mentors)'].split(','):
                num_of_time_slots_available += 1
        priority_score = max_priority_for_avisable_slot - num_of_time_slots_available*5 + max_priority_for_mentor - num_of_mentors*5
        mentees[mentee]['Priority Score'] = priority_score
        print(f"{mentee} : Prefered Slots - {number_of_prefered_slots} | Available slots - {num_of_time_slots_available} | Number of mentors - {num_of_mentors} | Priority Score: {priority_score}")

read_csv(STUDENT_MENTORING_SLOTS)
csv_data.pop(0)

for row in csv_data:
    mentees[row['Display Name']] = {"Preferred Mentors": row['Preferred Mentors'],"Preferred Time Slots": row['Preferred Time Slots'], "Previous Slot Mentor": row['Previous Slot Mentor'],'Preferred Mentoring Timeslots (from Preferred Mentors)': row['Preferred Mentoring Timeslots (from Preferred Mentors)']}
    mentors_list = row['Preferred Mentors'].split(',')
    if len(mentors_list) > MAX_AVAILABLE_MENTORS:
        MAX_AVAILABLE_MENTORS = len(mentors_list)
    prefrred_slots = row['Preferred Time Slots'].split(',')
    if len(prefrred_slots) > MAX_AVAILABLE_SLOTS:
        MAX_AVAILABLE_SLOTS = len(prefrred_slots)
    mentors = mentors.union(mentors_list)

print("Max Available Mentors:", MAX_AVAILABLE_MENTORS)
print("Max Available Slots:", MAX_AVAILABLE_SLOTS)

# print("Mentees:", mentees)
# print("Mentors:", mentors)

calculate_priority_score(mentees)
# print("Mentees:", mentees)

sorted_mentees = sorted(mentees.items(), key=lambda item: item[1]['Priority Score'], reverse=True)
print("Sorted Mentees:", sorted_mentees)

def simple_matching(mentees: dict, mentors: set) -> dict:
    mentor_matches = {mentor: None for mentor in mentors}  
    mentee_matches = {mentee: None for mentee, _ in mentees} 
    
    for mentee, details in sorted_mentees:
        preferred_mentors = details['Preferred Mentors'].split(',')
        
        for mentor in preferred_mentors:
            if mentor_matches[mentor] is None:  
                mentor_matches[mentor] = mentee
                mentee_matches[mentee] = mentor
                break  
    
    return mentee_matches

print(simple_matching(sorted_mentees, mentors))
import random

# List of days and time slots
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
time_slots = ['09:00 - 10:00', '10:00 - 11:00', '11:15 - 12:15', '12:15 - 1:15', '1:45 - 2:45', '2:45 - 3:45']



def A(prompt):
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
        exit()

#-----------------------------TEACHERS---------------------------------#
        
num_teachers = int(A("Enter the number of teachers: "))
teachers = []
for i in range(1, num_teachers + 1):
    teacher_name = A(f"Enter the name of teacher {i}: ")
    teachers.append(teacher_name)
    
#----------------------------SUBJECTS----------------------------------#
num_subjects = int(A("Enter the number of subjects: "))
subjects = []
for i in range(1, num_subjects + 1):
    subject_name = A(f"Enter the name of subject {i}: ")
    subjects.append(subject_name)

 
    
def generate_timetable(class_name):
    timetable = {}
    for day in days:
        timetable[day] = {}
        for time_slot in time_slots:
                teacher=teachers.pop(0)
                subject=subjects.pop(0)
                timetable[day][time_slot] = {'Teacher': teacher, 'Subject': subject}
                teachers.append(teacher)
                subjects.append(subject)
                
    
    return timetable

#----------------NUMBER OF CLASSES------------------#

def main():
    classes = []
    num_classes = int(A("Enter the number of classes: "))
    for i in range(1, num_classes + 1):
        class_name = A(f"Enter the name of class {i}: ")
        classes.append(class_name)
##        class_name = A(f"Enter the name of class : ")
        
        timetable = generate_timetable(class_name)
        print("\nTimetable for", class_name)
        for day in days:
            print(day)
            for time_slot in time_slots:
                entry = timetable[day][time_slot]
                print(f"{time_slot} : {entry['Teacher']} - {entry['Subject']}")
            print()
 
if __name__ == "__main__":
    main()

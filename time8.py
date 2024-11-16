from tabulate import tabulate
import random as r
#------------------- List of days and time slots------------------------#

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
time_slots = ['09:00 - 10:00', '10:00 - 11:00', '11:15 - 12:15 (LAB)', '12:15 - 1:15 (LAB)','1:15 - 1:45','1:45 - 2:45', '2:45 - 3:45','3:45 - 4:45']

def A(prompt):
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
        exit()

#-----------------------------TEACHERS---------------------------------#

def TEACH(num_teachers):
    teachers = []
    for i in range(1, num_teachers + 1):
        teacher_name = A(f"Enter the name of teacher {i}: ")
        teachers.append(teacher_name)
    return teachers

#----------------------------SUBJECTS----------------------------------#

def SUB(num_subjects):
    subjects = []
    for i in range(1, num_subjects + 1):
        subject_name = A(f"Enter the name of subject {i}: ")
        subjects.append(subject_name)
    return subjects

def GT(teachers, subjects):
    timetable = {}
    lab_slots = ['11:15 - 12:15 (LAB)', '12:15 - 1:15 (LAB)']
    break_slot = '1:15 - 1:45'
    free_slots = ['1:45 - 2:45', '2:45 - 3:45', '3:45 - 4:45']

    for day in days:
        timetable[day] = {}
        for time_slot in time_slots:
            timetable[day][time_slot] = {'Teacher': '', 'Subject': ''}

    # Assign LAB slots
    for i, day in enumerate(days):
        if i < len(teachers):
            timetable[day][lab_slots[0]] = {'Teacher': teachers[i], 'Subject': subjects[i]}
            timetable[day][lab_slots[1]] = {'Teacher': teachers[i], 'Subject': subjects[i]}

    # Assign Breaks
    for day in days:
        timetable[day][break_slot] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}

    # Assign other slots randomly
    for day in days:
        for time_slot in time_slots:
            if time_slot not in lab_slots + [break_slot]:
                teacher = teachers.pop(0)
                subject = subjects.pop(0)
                timetable[day][time_slot] = {'Teacher': teacher, 'Subject': subject}
                teachers.append(teacher)
                subjects.append(subject)

    # Assign random free periods
    for day in days:
        for time_slot in free_slots:
            if r.choice([True, False]):
                timetable[day][time_slot] = {'Teacher': '', 'Subject': ''}

    return timetable



def PT(class_name, timetable):
    table = [[""] + time_slots]  

    for day in days:
        row = [day]  
        for time_slot in time_slots:
            entry = timetable[day][time_slot]
            cell_value = f"{entry['Teacher']} - {entry['Subject']}"
            row.append(cell_value)
        table.append(row)

    print("\nTimetable for", class_name)
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def main():
    num_classes = int(A("Enter the number of classes: "))
    num_teachers = int(A("Enter the number of teachers: "))
    num_subjects = int(A("Enter the number of subjects: "))
    
    for _ in range(num_classes):
        class_name = A("Enter the name of class: ")
        teachers = TEACH(num_teachers)
        subjects = SUB(num_subjects)
        timetable = GT(teachers, subjects)
        
        PT(class_name, timetable)

if __name__ == "__main__":
    main()

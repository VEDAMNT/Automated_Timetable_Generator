from tabulate import tabulate

#------------------- List of days and time slots------------------------#

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
time_slots = ['09:00 - 10:00', '10:00 - 11:00', '11:15 - 12:15', '12:15 - 1:15', '1:45 - 2:45', '2:45 - 3:45','3:45 - 4:45']

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
    for day in days:
        timetable[day] = {}
        for time_slot in time_slots:
            teacher = teachers.pop(0)
            subject = subjects.pop(0)
            timetable[day][time_slot] = {'Teacher': teacher, 'Subject': subject}
            teachers.append(teacher)
            subjects.append(subject)
    return timetable

def print_timetable(class_name, timetable):
    table = [[""] + time_slots]  # Initialize the table with time slots as the header

    for day in days:
        row = [day]  # Initialize each row with the day
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
        
        print_timetable(class_name, timetable)

if __name__ == "__main__":
    main()

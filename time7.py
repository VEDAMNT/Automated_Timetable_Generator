from tabulate import tabulate
import random as r
#------------------- List of days and time slots------------------------#

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
time_slots = ['09:00 - 10:00', '10:00 - 11:00','11:00 - 11:15', '11:15 - 12:15 (LAB)', '12:15 - 1:15 (LAB)','1:15 - 1:45','1:45 - 2:45', '2:45 - 3:45','3:45 - 4:45']

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

    free = ['1:45 - 2:45', '2:45 - 3:45', '3:45 - 4:45']

    timetable['Monday']['11:00 - 11:15'] = {'Teacher': '| SHORT', 'Subject': 'BREAK |'}
    timetable['Tuesday']['11:00 - 11:15'] = {'Teacher': '| SHORT', 'Subject': 'BREAK |'}
    timetable['Wednesday']['11:00 - 11:15'] = {'Teacher': '| SHORT', 'Subject': 'BREAK |'}
    timetable['Thursday']['11:00 - 11:15'] = {'Teacher': '| SHORT', 'Subject': 'BREAK |'}
    timetable['Friday']['11:00 - 11:15'] = {'Teacher': '| SHORT', 'Subject': 'BREAK |'}
    
    timetable['Monday']['1:15 - 1:45'] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}
    timetable['Tuesday']['1:15 - 1:45'] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}
    timetable['Wednesday']['1:15 - 1:45'] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}
    timetable['Thursday']['1:15 - 1:45'] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}
    timetable['Friday']['1:15 - 1:45'] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}
    
    A1 = teachers[0]
    A2 = subjects[0]
    timetable['Monday']['11:15 - 12:15 (LAB)'] = {'Teacher': A1, 'Subject': A2}
    timetable['Monday']['12:15 - 1:15 (LAB)'] = {'Teacher': A1, 'Subject': A2}

    B1 = teachers[1]
    B2 = subjects[1]
    timetable['Tuesday']['11:15 - 12:15 (LAB)'] = {'Teacher': B1, 'Subject': B2}
    timetable['Tuesday']['12:15 - 1:15 (LAB)'] = {'Teacher': B1, 'Subject': B2}
    
    C1 = teachers[2]
    C2 = subjects[2]
    timetable['Wednesday']['11:15 - 12:15 (LAB)'] = {'Teacher': C1, 'Subject': C2}
    timetable['Wednesday']['12:15 - 1:15 (LAB)'] = {'Teacher': C1, 'Subject': C2}
    
    D1 = teachers[3]
    D2 = subjects[3]
    timetable['Thursday']['11:15 - 12:15 (LAB)'] = {'Teacher': D1, 'Subject': D2}
    timetable['Thursday']['12:15 - 1:15 (LAB)'] = {'Teacher': D1, 'Subject': D2}

    E1 = teachers[4]
    E2 = subjects[4]
    timetable['Friday']['11:15 - 12:15 (LAB)'] = {'Teacher': E1, 'Subject': E2}
    timetable['Friday']['12:15 - 1:15 (LAB)'] = {'Teacher': E1, 'Subject': E2}
    
    for time_slot in free:
        if timetable['Friday'][time_slot]['Teacher'] == '' and timetable['Friday'][time_slot]['Subject'] == '':
            continue  
        else:
            if r.choice([True, True]):
                timetable['Friday'][time_slot] = {'Teacher': '', 'Subject': ''}
                
    for time_slot in free:
        if timetable['Thursday'][time_slot]['Teacher'] == '' and timetable['Thursday'][time_slot]['Subject'] == '':
            continue  
        else:
            if r.choice([False, True]):
                timetable['Thursday'][time_slot] = {'Teacher': '', 'Subject': ''}
                
    for time_slot in free:
        if timetable['Wednesday'][time_slot]['Teacher'] == '' and timetable['Wednesday'][time_slot]['Subject'] == '':
            continue  
        else:
            if r.choice([True, False]):
                timetable['Wednesday'][time_slot] = {'Teacher': '', 'Subject': ''}
                
    for time_slot in free:
        if timetable['Tuesday'][time_slot]['Teacher'] == '' and timetable['Wednesday'][time_slot]['Subject'] == '':
            continue  
        else:
            if r.choice([False, False]):
                timetable['Tuesday'][time_slot] = {'Teacher': '', 'Subject': ''}
                
    for time_slot in free:
        if timetable['Monday'][time_slot]['Teacher'] == '' and timetable['Wednesday'][time_slot]['Subject'] == '':
            continue  
        else:
            if r.choice([True, False]):
                timetable['Monday'][time_slot] = {'Teacher': '', 'Subject': ''}
                
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


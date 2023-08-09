def A(prompt):
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
        exit()

def B():
    num_slots = int(A("Enter the number of time slots: "))
    time_slots = []
    for i in range(1, num_slots + 1):
        time_slot = A(f"Enter time slot {i} (e.g., 9:00 AM - 10:00 AM): ")
        time_slots.append(time_slot)
    return time_slots

def C():
    num_teachers = int(A("Enter the number of teachers: "))
    teachers = []
    for i in range(1, num_teachers + 1):
        teacher_name = A(f"Enter the name of teacher {i}: ")
        teachers.append(teacher_name)
    return teachers

def D():
    num_subjects = int(A("Enter the number of subjects: "))
    subjects = []
    for i in range(1, num_subjects + 1):
        subject_name = A(f"Enter the name of subject {i}: ")
        subjects.append(subject_name)
    return subjects

def generate_timetable(classes, time_slots, teachers, subjects):
    timetable = {}
    for class_name in classes:
        class_timetable = {}
        for time_slot in time_slots:
            teacher = teachers.pop(0)
            subject = subjects.pop(0)
            class_timetable[time_slot] = {'teacher': teacher, 'subject': subject}
            teachers.append(teacher)
            subjects.append(subject)
        timetable[class_name] = class_timetable
    return timetable

def print_timetable(timetable):
    for class_name, class_timetable in timetable.items():
        print(f"\nClass: {class_name}")
        for time_slot, details in class_timetable.items():
            print(f"{time_slot}: Teacher - {details['teacher']}, Subject - {details['subject']}")

def main():
    classes = []
    num_classes = int(A("Enter the number of classes: "))
    for i in range(1, num_classes + 1):
        class_name = A(f"Enter the name of class {i}: ")
        classes.append(class_name)

    time_slots = B()
    teachers = C()
    subjects = D()

##    if len(teachers) < num_classes * len(time_slots) or len(subjects) < num_classes * len(time_slots):
##        print("Insufficient number of teachers or subjects.")
##        exit()

    timetable = generate_timetable(classes, time_slots, teachers, subjects)
    print("\nTimetable Generated:")
    print_timetable(timetable)

if __name__ == "__main__":
    main()



from flask import Flask, render_template, request
import random as r

app = Flask(__name__)

# ------------------- List of days and time slots ------------------------#
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
time_slots = ['09:00 - 10:00', '10:00 - 11:00', '11:00 - 11:15', '11:15 - 12:15 (LAB)', '12:15 - 1:15 (LAB)', '1:15 - 1:45', '1:45 - 2:45', '2:45 - 3:45', '3:45 - 4:45']

def GT(class_name, teachers, subjects):
    timetable = {}

    lab_slots = ['11:15 - 12:15 (LAB)', '12:15 - 1:15 (LAB)']
    break_slots = ['11:00 - 11:15', '1:15 - 1:45']  # New break slot
    free_slots = ['09:00 - 10:00', '10:00 - 11:00', '1:45 - 2:45', '2:45 - 3:45', '3:45 - 4:45']

    # Initialize timetable for the class
    for day in days:
        timetable[day] = {}
        for time_slot in time_slots:
            timetable[day][time_slot] = {'Teacher': '', 'Subject': ''}

    # Assign LAB slots (fixed assignment)
    for i, day in enumerate(days):
        if i < len(teachers):
            timetable[day][lab_slots[0]] = {'Teacher': teachers[i], 'Subject': subjects[i]}
            timetable[day][lab_slots[1]] = {'Teacher': teachers[i], 'Subject': subjects[i]}

    # Assign Break (only the new break slot, '11:00 - 11:15')
    for day in days:
        timetable[day][break_slots[0]] = {'Teacher': '| SHORT', 'Subject': 'BREAK |'}
        timetable[day][break_slots[1]] = {'Teacher': '| LONG', 'Subject': 'BREAK |'}

    # Handle teacher and subject assignments in non-LAB and non-Break slots
    remaining_slots = [time_slot for time_slot in time_slots if time_slot not in lab_slots + break_slots]
    
    available_teachers = teachers[:]
    available_subjects = subjects[:]

    for day in days:
        random_assignments = []
        for time_slot in remaining_slots:
            if available_teachers and available_subjects:
                teacher = r.choice(available_teachers)
                subject = r.choice(available_subjects)
                available_teachers.remove(teacher)
                available_subjects.remove(subject)
                random_assignments.append({'Teacher': teacher, 'Subject': subject})
            else:
                random_assignments.append({'Teacher': '', 'Subject': ''})

        # Assign the random assignments to the timetable
        for idx, time_slot in enumerate(remaining_slots):
            timetable[day][time_slot] = random_assignments[idx]

    # Randomly assign some free periods in specific slots
    for day in days:
        for time_slot in free_slots:
            if r.choice([True, False]):
                timetable[day][time_slot] = {'Teacher': '', 'Subject': ''}

    return timetable

@app.route('/', methods=['GET', 'POST'])
def index():
    tables = {}  # Initialize tables variable to avoid undefined error
    if request.method == 'POST':
        # Get form data for class name, teachers, and subjects
        class_name = request.form.get('class_name')
        teachers = request.form.getlist('teachers')
        subjects = request.form.getlist('subjects')
        
        # Generate the timetable for this class
        timetable = GT(class_name, teachers, subjects)
        
        # Get timetable in table format for this class
        table = [[""] + time_slots]
        for day in days:
            row = [day]
            for time_slot in time_slots:
                entry = timetable[day][time_slot]
                cell_value = f"{entry['Teacher']} - {entry['Subject']}"
                row.append(cell_value)
            table.append(row)
        
        # Store the generated timetable
        tables[class_name] = table

        return render_template('index.html', tables=tables)

    return render_template('index.html', tables=tables)

if __name__ == "__main__":
    app.run(debug=True)

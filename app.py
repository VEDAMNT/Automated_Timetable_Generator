from flask import Flask, render_template, request, jsonify, Response
import random as r
import json
from datetime import datetime
import csv
import io

app = Flask(__name__)

# ------------------- Configuration ------------------------#
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIME_SLOTS = [
    '09:00 - 10:00', '10:00 - 11:00', '11:00 - 11:15', 
    '11:15 - 12:15', '12:15 - 1:15', '1:15 - 1:45', 
    '1:45 - 2:45', '2:45 - 3:45', '3:45 - 4:45'
]

class TimetableGenerator:
    def __init__(self):
        self.lab_slots = ['11:15 - 12:15', '12:15 - 1:15']
        self.break_slots = ['11:00 - 11:15', '1:15 - 1:45']
        self.teaching_slots = [slot for slot in TIME_SLOTS if slot not in self.lab_slots + self.break_slots]
        self.global_teacher_schedule = {}  # Track teacher assignments across all classes
        self.teacher_subjects = {}  # Map teachers to their subjects
        
    def reset_global_schedule(self):
        """Reset global teacher schedule for new generation"""
        self.global_teacher_schedule = {}
        for day in DAYS:
            self.global_teacher_schedule[day] = {}
            for slot in TIME_SLOTS:
                self.global_teacher_schedule[day][slot] = []
    
    def is_teacher_available(self, teacher, day, time_slot):
        """Check if teacher is available at given day and time"""
        return teacher not in self.global_teacher_schedule[day][time_slot]
    
    def assign_teacher_to_slot(self, teacher, day, time_slot):
        """Assign teacher to a specific slot globally"""
        if teacher not in self.global_teacher_schedule[day][time_slot]:
            self.global_teacher_schedule[day][time_slot].append(teacher)
    
    def create_teacher_subject_mapping(self, all_classes_data):
        """Create mapping of teachers to their subjects"""
        self.teacher_subjects = {}
        for class_data in all_classes_data:
            teachers = class_data['teachers']
            subjects = class_data['subjects']
            for teacher, subject in zip(teachers, subjects):
                if teacher not in self.teacher_subjects:
                    self.teacher_subjects[teacher] = []
                if subject not in self.teacher_subjects[teacher]:
                    self.teacher_subjects[teacher].append(subject)
    
    def generate_single_timetable(self, class_name, teachers, subjects):
        """Generate timetable for a single class with constraint satisfaction"""
        timetable = {}
        
        # Initialize timetable
        for day in DAYS:
            timetable[day] = {}
            for time_slot in TIME_SLOTS:
                timetable[day][time_slot] = {'Teacher': '', 'Subject': '', 'Type': ''}
        
        # Assign break slots
        for day in DAYS:
            timetable[day]['11:00 - 11:15'] = {
                'Teacher': '| SHORT', 
                'Subject': 'BREAK |', 
                'Type': 'BREAK'
            }
            timetable[day]['1:15 - 1:45'] = {
                'Teacher': '| LONG', 
                'Subject': 'BREAK |', 
                'Type': 'BREAK'
            }
        
        # Assign lab slots (2 consecutive lab periods per day for first few days)
        lab_assignments = 0
        for day in DAYS:
            if lab_assignments < len(teachers):
                teacher = teachers[lab_assignments]
                subject = subjects[lab_assignments]
                
                # Check if teacher is available for both lab slots
                if (self.is_teacher_available(teacher, day, self.lab_slots[0]) and 
                    self.is_teacher_available(teacher, day, self.lab_slots[1])):
                    
                    for lab_slot in self.lab_slots:
                        timetable[day][lab_slot] = {
                            'Teacher': teacher, 
                            'Subject': f"{subject} (LAB)", 
                            'Type': 'LAB'
                        }
                        self.assign_teacher_to_slot(teacher, day, lab_slot)
                    lab_assignments += 1
        
        # Assign regular teaching slots using constraint satisfaction
        teacher_subject_pairs = list(zip(teachers, subjects))
        
        for day in DAYS:
            available_pairs = teacher_subject_pairs.copy()
            r.shuffle(available_pairs)  # Randomize for variety
            
            for time_slot in self.teaching_slots:
                assigned = False
                attempts = 0
                max_attempts = len(available_pairs) * 2
                
                while not assigned and attempts < max_attempts and available_pairs:
                    # Try to find an available teacher
                    for i, (teacher, subject) in enumerate(available_pairs):
                        if self.is_teacher_available(teacher, day, time_slot):
                            timetable[day][time_slot] = {
                                'Teacher': teacher, 
                                'Subject': subject, 
                                'Type': 'REGULAR'
                            }
                            self.assign_teacher_to_slot(teacher, day, time_slot)
                            available_pairs.pop(i)
                            assigned = True
                            break
                    attempts += 1
                
                # If no teacher is available, mark as free period
                if not assigned:
                    timetable[day][time_slot] = {
                        'Teacher': 'FREE', 
                        'Subject': 'PERIOD', 
                        'Type': 'FREE'
                    }
        
        return timetable
    
    def generate_multiple_timetables(self, classes_data):
        """Generate timetables for multiple classes with global constraint satisfaction"""
        self.reset_global_schedule()
        self.create_teacher_subject_mapping(classes_data)
        
        all_timetables = {}
        
        # Sort classes by priority (classes with more teachers/subjects get priority)
        sorted_classes = sorted(classes_data, 
                              key=lambda x: len(x['teachers']), 
                              reverse=True)
        
        for class_data in sorted_classes:
            class_name = class_data['class_name']
            teachers = class_data['teachers']
            subjects = class_data['subjects']
            
            timetable = self.generate_single_timetable(class_name, teachers, subjects)
            all_timetables[class_name] = timetable
        
        return all_timetables
    
    def validate_timetables(self, all_timetables):
        """Validate that no teacher conflicts exist"""
        conflicts = []
        
        for day in DAYS:
            for time_slot in TIME_SLOTS:
                teachers_in_slot = []
                for class_name, timetable in all_timetables.items():
                    teacher = timetable[day][time_slot]['Teacher']
                    if teacher and teacher not in ['| SHORT', '| LONG', 'FREE']:
                        teachers_in_slot.append((teacher, class_name))
                
                # Check for conflicts
                teacher_names = [t[0] for t in teachers_in_slot]
                if len(teacher_names) != len(set(teacher_names)):
                    conflicts.append({
                        'day': day,
                        'time_slot': time_slot,
                        'conflicting_assignments': teachers_in_slot
                    })
        
        return conflicts

# Global timetable generator instance
timetable_gen = TimetableGenerator()

def convert_to_table_format(timetables):
    """Convert timetables dictionary to table format for display"""
    tables = {}
    
    for class_name, timetable in timetables.items():
        table = [["Time/Day"] + DAYS]
        
        for time_slot in TIME_SLOTS:
            row = [time_slot]
            for day in DAYS:
                entry = timetable[day][time_slot]
                if entry['Type'] == 'BREAK':
                    cell_value = entry['Subject']
                elif entry['Type'] == 'FREE':
                    cell_value = "FREE PERIOD"
                elif entry['Teacher'] and entry['Subject']:
                    cell_value = f"{entry['Teacher']}\n{entry['Subject']}"
                else:
                    cell_value = "FREE PERIOD"
                row.append(cell_value)
            table.append(row)
        
        tables[class_name] = table
    
    return tables

def export_to_csv(timetables):
    """Export timetables to CSV format"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    for class_name, timetable in timetables.items():
        writer.writerow([f"Timetable for {class_name}"])
        writer.writerow(["Time/Day"] + DAYS)
        
        for time_slot in TIME_SLOTS:
            row = [time_slot]
            for day in DAYS:
                entry = timetable[day][time_slot]
                if entry['Type'] == 'BREAK':
                    cell_value = entry['Subject']
                elif entry['Type'] == 'FREE':
                    cell_value = "FREE PERIOD"
                elif entry['Teacher'] and entry['Subject']:
                    cell_value = f"{entry['Teacher']} - {entry['Subject']}"
                else:
                    cell_value = "FREE PERIOD"
                row.append(cell_value)
            writer.writerow(row)
        
        writer.writerow([])  # Empty row between classes
    
    return output.getvalue()

def export_to_html_pdf(timetables):
    """Export timetables to HTML format (can be printed as PDF)"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Academic Timetables - {datetime.now().strftime('%Y-%m-%d')}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ text-align: center; color: #333; margin-bottom: 30px; }}
            h2 {{ color: #667eea; margin-top: 40px; margin-bottom: 20px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 11px; }}
            th {{ background-color: #f8f9fa; font-weight: bold; }}
            .time-col {{ background-color: #e9ecef; font-weight: bold; }}
            .break-cell {{ background-color: #fff3cd; color: #856404; }}
            .lab-cell {{ background-color: #d1ecf1; color: #0c5460; }}
            .free-cell {{ background-color: #f8d7da; color: #721c24; }}
            .regular-cell {{ background-color: #d4edda; color: #155724; }}
            .page-break {{ page-break-before: always; }}
            @media print {{ body {{ margin: 10px; }} h2 {{ page-break-before: always; }} }}
        </style>
    </head>
    <body>
        <h1>Academic Timetables</h1>
        <p style="text-align: center; color: #666; margin-bottom: 40px;">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    """
    
    for i, (class_name, timetable) in enumerate(timetables.items()):
        if i > 0:
            html_content += '<div class="page-break"></div>'
        
        html_content += f'<h2>{class_name}</h2>'
        html_content += '<table>'
        
        # Header row
        html_content += '<tr><th class="time-col">Time/Day</th>'
        for day in DAYS:
            html_content += f'<th>{day}</th>'
        html_content += '</tr>'
        
        # Time slots
        for time_slot in TIME_SLOTS:
            html_content += f'<tr><td class="time-col">{time_slot}</td>'
            for day in DAYS:
                entry = timetable[day][time_slot]
                cell_class = ''
                cell_content = ''
                
                if entry['Type'] == 'BREAK':
                    cell_class = 'break-cell'
                    cell_content = entry['Subject']
                elif entry['Type'] == 'FREE':
                    cell_class = 'free-cell'
                    cell_content = 'FREE PERIOD'
                elif entry['Type'] == 'LAB':
                    cell_class = 'lab-cell'
                    cell_content = f"{entry['Teacher']}<br><small>{entry['Subject']}</small>"
                elif entry['Teacher'] and entry['Subject']:
                    cell_class = 'regular-cell'
                    cell_content = f"{entry['Teacher']}<br><small>{entry['Subject']}</small>"
                else:
                    cell_class = 'free-cell'
                    cell_content = 'FREE PERIOD'
                
                html_content += f'<td class="{cell_class}">{cell_content}</td>'
            html_content += '</tr>'
        
        html_content += '</table>'
    
    html_content += '''
        <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #ccc; text-align: center; color: #666; font-size: 12px;">
            <p>To save as PDF: Use your browser's print function and select "Save as PDF"</p>
        </div>
    </body>
    </html>
    '''
    
    return html_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_timetables', methods=['POST'])
def generate_timetables():
    try:
        data = request.get_json()
        classes_data = data.get('classes', [])
        
        if not classes_data:
            return jsonify({'error': 'No classes data provided'}), 400
        
        # Generate timetables
        timetables = timetable_gen.generate_multiple_timetables(classes_data)
        
        # Validate for conflicts
        conflicts = timetable_gen.validate_timetables(timetables)
        
        # Convert to table format for display
        tables = convert_to_table_format(timetables)
        
        return jsonify({
            'success': True,
            'tables': tables,
            'conflicts': conflicts,
            'teacher_subjects': timetable_gen.teacher_subjects
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_csv')
def export_csv():
    try:
        # Get timetables data from request
        sample_data = request.args.get('data')
        if not sample_data:
            return "No data to export", 400
        
        timetables_data = json.loads(sample_data)
        csv_content = export_to_csv(timetables_data)
        
        # Create a proper file response
        output = io.BytesIO()
        output.write(csv_content.encode('utf-8'))
        output.seek(0)
        
        from flask import Response
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=timetables_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
        )
    
    except Exception as e:
        return f"Error exporting CSV: {str(e)}", 500

@app.route('/export_pdf')
def export_pdf():
    try:
        sample_data = request.args.get('data')
        if not sample_data:
            return "No data to export", 400
        
        timetables_data = json.loads(sample_data)
        html_content = export_to_html_pdf(timetables_data)
        
        return Response(
            html_content,
            mimetype='text/html',
            headers={'Content-Disposition': f'inline; filename=timetables_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'}
        )
    
    except Exception as e:
        return f"Error exporting PDF: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)

# TIMELYNX

A Flask-based web application for generating academic timetables with constraint satisfaction. Users can schedule classes, assign teachers and subjects, and export timetables as CSV or HTML (printable as PDF). The application ensures no teacher conflicts and includes fixed break and lab slots.

## Features

* **Dynamic Class Configuration:** Add/remove classes and teacher-subject pairs via a user-friendly web interface.
* **Constraint-Based Scheduling:** Generates timetables ensuring no teacher is double-booked across classes.
* **Conflict Detection:** Identifies and reports scheduling conflicts (e.g., a teacher assigned to multiple classes at the same time).
* **Export Options:**

  * Export timetables as CSV files.
  * Export timetables as styled HTML, which can be printed as PDF using the browser's "Save as PDF" feature.
* **Responsive UI:** Clean, responsive design with color-coded timetable cells (breaks, labs, free periods, regular classes).
* **Auto-Save:** Form data is saved to localStorage every 30 seconds to prevent data loss.
* **Keyboard Shortcuts:** Ctrl+Enter to generate timetables, Ctrl+N to add a new class.

## Prerequisites

* **Python:** Version 3.6 or higher.
* **Web Browser:** Chrome, Firefox, or any modern browser with JavaScript enabled.
* **Internet Connection:** Required for loading Font Awesome icons via CDN.

## Installation

### Clone the Repository:

```bash
git clone <repository-url>
cd academic-timetable-generator
```

### Set Up a Virtual Environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies:

```bash
pip install flask
```

### Optional: For server-side PDF generation:

```bash
pip install weasyprint
```

## Project Structure

```
academic-timetable-generator/
├── app.py
├── templates/
│   └── index.html
├── README.md
```

* `app.py`: Main Flask application with backend logic.
* `templates/index.html`: Frontend HTML with CSS and JavaScript for the UI.

## Usage

### Run the Application:

```bash
python app.py
```

* The app will start in debug mode at `http://127.0.0.1:5000`.

### Access the Web Interface:

* Open a browser and navigate to `http://127.0.0.1:5000`.

### Generate Timetables:

1. Add classes using the "Add New Class" button.
2. For each class, enter a class name and add teacher-subject pairs (e.g., "ProfA: Math", "ProfB: Physics").
3. Click "Generate Timetables" or press Ctrl+Enter to create schedules.
4. View generated timetables, which include:

   * Fixed breaks (11:00-11:15, 1:15-1:45).
   * Lab slots (11:15-12:15, 12:15-1:15 for some teachers).
   * Regular and free periods.
5. Check for conflicts (e.g., a teacher scheduled in multiple classes at the same time).

### Export Timetables:

* **CSV:** Click "Export CSV" to download a `.csv` file with all timetables.
* **PDF:** Click "Export PDF" to open a styled HTML page. Use the browser's Print > Save as PDF to generate a PDF.

## Sample Input

```
Class: "CS101"
Teacher: "ProfA", Subject: "Math"
Teacher: "ProfB", Subject: "Physics (LAB)"

Class: "CS102"
Teacher: "ProfA", Subject: "Algorithms"
Teacher: "ProfC", Subject: "Database"
```

## Expected Output

* Timetables for each class with breaks, labs, and regular/free periods.
* Conflicts reported if ProfA is scheduled in both classes at the same time.
* CSV file with formatted timetables.
* HTML page with styled tables, ready for printing to PDF.

## Configuration

### Time Slots:

Defined in `app.py`:

```python
TIME_SLOTS = [
    '09:00 - 10:00', '10:00 - 11:00', '11:00 - 11:15',
    '11:15 - 12:15', '12:15 - 1:15', '1:15 - 1:45',
    '1:45 - 2:45', '2:45 - 3:45', '3:45 - 4:45'
]
```

* Breaks: 11:00-11:15 (short), 1:15-1:45 (long).
* Lab slots: 11:15-12:15, 12:15-1:15.

### Days:

* Monday to Friday (configurable in `DAYS` list).

## Limitations

* **PDF Export:** Relies on browser printing, which may lead to inconsistent formatting. Consider using WeasyPrint for server-side PDF generation.
* **Data Persistence:** Timetable data is not stored server-side; refreshing the page may require regenerating timetables for exports.
* **Scalability:** The iterative scheduling algorithm may be slow for large numbers of classes or teachers.
* **Security:** Lacks input sanitization and CSRF protection.

## Improvements

### Server-Side PDF Generation:

Install WeasyPrint and modify `export_pdf` route:

```python
from weasyprint import HTML

@app.route('/export_pdf')
def export_pdf():
    timetables = session.get('timetables')
    html_content = export_to_html_pdf(timetables)
    pdf_buffer = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return Response(
        pdf_buffer,
        mimetype='application/pdf',
        headers={'Content-Disposition': f'attachment; filename=timetables_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'}
    )
```

### Session Storage:

Use Flask’s session:

```python
from flask import session
app.config['SECRET_KEY'] = 'your-secret-key'
```

### Security Enhancements:

* Sanitize inputs with bleach:

```bash
pip install bleach
```

* Add CSRF protection with Flask-WTF:

```bash
pip install flask-wtf
```

### Form Data Restoration:

* Complete the `loadFormData` function in `index.html` to restore saved form data from localStorage.

### Testing:

Add unit tests with `unittest` or `pytest`:

```python
import unittest
from app import TimetableGenerator

class TestTimetableGenerator(unittest.TestCase):
    def test_generate_single_timetable(self):
        generator = TimetableGenerator()
        timetable = generator.generate_single_timetable('CS101', ['ProfA'], ['Math'])
        self.assertEqual(timetable['Monday']['11:00 - 11:15']['Type'], 'BREAK')
```

## Troubleshooting

* **Blank Page:** Ensure `index.html` is in the `templates` folder and Flask is running.
* **Export Errors:** Regenerate timetables before exporting, as data is not persisted after page refresh.
* **Conflicts Not Detected:** Verify teacher names are identical across classes (case-sensitive).
* **Slow Generation:** For large datasets, consider using a constraint solver like `python-constraint`.

## License

MIT License. See LICENSE for details.

## Contact

For issues or contributions, open a GitHub issue or pull request at <repository-url>.

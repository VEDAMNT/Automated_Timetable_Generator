import unittest
import time
from app import generate_timetable, initialize_timetable, assign_fixed_slots, timetable_to_table

class TestTimetableGenerator(unittest.TestCase):
    def setUp(self):
        self.class_name = "Class 10A"
        self.teachers = ["Mr. Smith", "Ms. Johnson"]
        self.subjects = ["Math", "Physics"]
        self.timetable = generate_timetable(self.class_name, self.teachers, self.subjects)

    def test_timetable_not_none(self):
        """Test that a timetable is generated successfully."""
        self.assertIsNotNone(self.timetable, "Timetable generation failed.")

    def test_lab_slots_assigned(self):
        """Test that lab slots are assigned correctly."""
        for i, day in enumerate(['Monday', 'Tuesday']):
            for lab_slot in ['11:15 - 12:15 (LAB)', '12:15 - 1:15 (LAB)']:
                self.assertEqual(
                    self.timetable[day][lab_slot]['Teacher'], self.teachers[i],
                    f"Lab slot {lab_slot} on {day} not assigned to {self.teachers[i]}."
                )
                self.assertEqual(
                    self.timetable[day][lab_slot]['Subject'], self.subjects[i],
                    f"Lab slot {lab_slot} on {day} not assigned to {self.subjects[i]}."
                )

    def test_break_slots_assigned(self):
        """Test that break slots are assigned correctly."""
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            self.assertEqual(
                self.timetable[day]['11:00 - 11:15']['Subject'], 'BREAK |',
                f"Short break slot on {day} not assigned."
            )
            self.assertEqual(
                self.timetable[day]['1:15 - 1:45']['Subject'], 'BREAK |',
                f"Long break slot on {day} not assigned."
            )

    def test_no_teacher_conflict_in_day(self):
        """Test that no teacher is double-booked in the same time slot."""
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            free_slots = [slot for slot in TIME_SLOTS if slot not in LAB_SLOTS + BREAK_SLOTS]
            teachers_in_day = [
                self.timetable[day][slot]['Teacher'] for slot in free_slots
                if self.timetable[day][slot]['Teacher']
            ]
            self.assertEqual(
                len(teachers_in_day), len(set(teachers_in_day)),
                f"Teacher conflict detected on {day}."
            )

    def test_subject_distribution(self):
        """Test that each subject appears at least once."""
        subject_counts = {s: 0 for s in self.subjects}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for slot in TIME_SLOTS:
                subject = self.timetable[day][slot]['Subject']
                if subject in subject_counts:
                    subject_counts[subject] += 1
        for subject, count in subject_counts.items():
            self.assertGreaterEqual(
                count, 1,
                f"Subject {subject} does not appear in the timetable."
            )

    def test_generation_speed(self):
        """Test that timetable generation is reasonably fast (< 1 second)."""
        start_time = time.time()
        generate_timetable(self.class_name, self.teachers, self.subjects)
        elapsed_time = time.time() - start_time
        self.assertLess(
            elapsed_time, 1.0,
            f"Timetable generation took too long: {elapsed_time} seconds."
        )

if __name__ == '__main__':
    unittest.main()

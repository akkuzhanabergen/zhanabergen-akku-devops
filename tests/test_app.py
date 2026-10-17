import unittest

from app.main import student_info, student_page


class StudentApplicationTests(unittest.TestCase):
    def test_default_student_information(self):
        self.assertEqual(student_info({}), {
            "Name": "Akku",
            "Surname": "Zhanabergen",
            "Group": "IT2-2309",
            "Student ID": "37667",
        })

    def test_environment_variables_override_defaults(self):
        info = student_info({"STUDENT_NAME": "Example", "STUDENT_ID": "999"})
        self.assertEqual(info["Name"], "Example")
        self.assertEqual(info["Student ID"], "999")
        self.assertEqual(info["Surname"], "Zhanabergen")

    def test_html_escapes_environment_values(self):
        page = student_page(student_info({"STUDENT_NAME": "<Akku>"}))
        self.assertIn("&lt;Akku&gt;", page)
        self.assertNotIn("<Akku>", page)


if __name__ == "__main__":
    unittest.main()

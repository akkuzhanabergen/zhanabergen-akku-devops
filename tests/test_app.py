import unittest
from http.server import HTTPServer
from threading import Thread
from urllib.request import urlopen

from app.main import StudentHandler, student_info, student_page


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

    def test_health_endpoint_returns_ok(self):
        server = HTTPServer(("127.0.0.1", 0), StudentHandler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f"http://127.0.0.1:{server.server_port}/health") as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.read(), b"OK\n")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()

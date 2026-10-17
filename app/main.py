"""Small student information server for the DevOps laboratory."""

import os
from html import escape
from http.server import BaseHTTPRequestHandler, HTTPServer


def student_info(environ=None):
    values = os.environ if environ is None else environ
    return {
        "Name": values.get("STUDENT_NAME", "Akku"),
        "Surname": values.get("STUDENT_SURNAME", "Zhanabergen"),
        "Group": values.get("STUDENT_GROUP", "IT2-2309"),
        "Student ID": values.get("STUDENT_ID", "37667"),
    }


def student_page(info):
    rows = "\n".join(
        f"<p><strong>{label}:</strong> {escape(value)}</p>"
        for label, value in info.items()
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<title>DevOps Student Application</title></head><body>'
        '<h1>DevOps Student Application</h1>'
        f"{rows}<p>Application is running successfully!</p>"
        "</body></html>"
    )


class StudentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = b"OK\n"
            content_type = "text/plain; charset=utf-8"
        elif self.path == "/":
            body = student_page(student_info()).encode("utf-8")
            content_type = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    info = student_info()
    print("===============================", flush=True)
    print("DevOps Student Application", flush=True)
    print("===============================", flush=True)
    for label, value in info.items():
        print(f"{label}: {value}", flush=True)
    print("Application is running successfully!", flush=True)
    HTTPServer(("0.0.0.0", int(os.getenv("APP_PORT", "8000"))), StudentHandler).serve_forever()

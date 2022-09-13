import requests
import re


class InstalingAPI:
    def __init__(self):
        # Simulate a real web browser
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

        # Initialize a requests session
        self.req_ses = self.__initialize_requests_session()

    def log_in(self, username, password):
        self.student_page = self.req_ses.post("https://instaling.pl/teacher.php?page=teacherActions/", data={
            "action": "login",
            "from": "",
            "log_email": username,
            "log_password": password
        })

        # Get user ID
        self.instaling_id = re.findall(
            "\/ling2\/html_app\/app.php\?child_id=\d\d\d\d\d\d\d", self.student_page.text)
        self.instaling_id = self.instaling_id[0].strip(
            "/ling2/html_app/app.php?child_id=")

    # Initialize requests session
    def __initialize_requests_session(self):
        req_ses = requests.Session()
        req_ses.headers["User-Agent"] = self.USER_AGENT
        return req_ses

    def __debug_request(self):
        print(self.req_ses.get("https://ifconfig.me/").text)

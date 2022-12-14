from .instaling_exceptions import *
from bs4 import BeautifulSoup
import latest_user_agents
import requests
import time


class InstalingAPI:
    def __init__(self):
        self.USER_AGENT = latest_user_agents.get_latest_user_agents()[0]
        # TODO: Update this string automatically
        self.VERSION_STRING = "C65E24B29F60B1231EC23D979C9707D2"

        # Initialize a requests session
        self.req_ses = self.__initialize_requests_session()

    def log_in(self, username, password):
        self.student_page = self.req_ses.post("https://instaling.pl/teacher.php?page=teacherActions", data={
            "action": "login",
            "from": "",
            "log_email": username,
            "log_password": password
        })

        try:
            # Get user ID
            soup = BeautifulSoup(self.student_page.text, "html.parser")
            id_button = soup.find("a", class_="btn-session")
            href_contents = id_button.get("href")
            self.instaling_id = href_contents[len(href_contents) - 7:]
        except AttributeError:
            raise WrongPasswordException
        finally:
            # Set username and password as attributes
            self.username = username
            self.password = password

    def is_session_new(self):
        return self.req_ses.post("https://instaling.pl/ling2/server/actions/init_session.php", data={
            "child_id": self.instaling_id,
            "repeat": "",
            "start": "",
            "end": ""
        }).json()["is_new"]

    def generate_next_word(self):
        generate_word_json = self.req_ses.post("https://instaling.pl/ling2/server/actions/generate_next_word.php", data={
            "child_id": self.instaling_id,
            "date": round(time.time()) * 1000
        }).json()

        try:
            word_id = generate_word_json["id"]
            usage_example = generate_word_json["usage_example"]
            polish_word = generate_word_json["translations"]
            has_audio = generate_word_json["has_audio"]

            return {"word_id": word_id, "usage_example": usage_example, "polish_word": polish_word, "has_audio": has_audio}
        except KeyError:
            raise SessionCompleteException

    def submit_answer(self, word_id, answer):
        answer_json = self.req_ses.post("https://instaling.pl/ling2/server/actions/save_answer.php", data={
            "child_id": self.instaling_id,
            "word_id": word_id,
            "answer": answer,
            "version": self.VERSION_STRING
        }).json()

        english_word = answer_json["word"]

        return {"english_word": english_word}

    def reveal_answer(self, word_id):
        # word_path = self.req_ses.get(f"https://instaling.pl/ling2/server/actions/getAudioUrl.php?id={word_id}").json()
        # revealed_answer = re.findall() # TODO: ADD REGEX
        print("reveal_answer() Incomplete!!!!!")

    # Initialize requests session
    def __initialize_requests_session(self):
        req_ses = requests.Session()
        req_ses.headers["User-Agent"] = self.USER_AGENT
        return req_ses

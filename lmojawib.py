import re
import requests
import tkinter as tk
from tkinter import ttk
import pyperclip

class AnswerFetcherGUI:
    """
    A GUI application for fetching answers from a URL.

    Attributes:
        window (tk.Tk): The main application window.
        style (ttk.Style): The style configuration for the widgets.
        url_label (ttk.Label): The label for the URL entry.
        url_entry (ttk.Entry): The entry field for the URL.
        fetch_button (ttk.Button): The button for fetching answers.
        clear_button (ttk.Button): The button for clearing the text.
        copy_button (ttk.Button): The button for copying answers.
        result_label (ttk.Label): The label for displaying the result.
        answers_text (tk.Text): The text widget for displaying the answers.
    """

    def __init__(self):
        """
        Initializes the AnswerFetcherGUI class by creating the main application window and configuring the style.
        """
        self.window = tk.Tk()
        self.window.title("Answer Fetcher")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('calibri', 10, 'bold'), borderwidth='4')
        self.style.configure('TLabel', font=('calibri', 12))

        self.create_widgets()

    def create_widgets(self):
        """
        Creates the widgets for the GUI application, including labels, entry fields, buttons, and text widgets.
        """
        self.url_label = ttk.Label(self.window, text="URL:")
        self.url_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.url_entry = ttk.Entry(self.window, width=50)
        self.url_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        self.fetch_button = ttk.Button(self.window, text="Fetch Answers", command=self.fetch_answers)
        self.fetch_button.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        self.clear_button = ttk.Button(self.window, text="Clear", command=self.clear_text)
        self.clear_button.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        self.copy_button = ttk.Button(self.window, text="Copy Answers", command=self.copy_answers)
        self.copy_button.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        self.result_label = ttk.Label(self.window, text="")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.answers_text = tk.Text(self.window, height=10, width=60)
        self.answers_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def fetch_answers(self):
        """
        Fetches the answers from the provided URL and displays them in the answers_text widget.
        """
        url = self.url_entry.get()

        activity_id = self.extract_activity_id(url)
        if activity_id is None:
            self.show_error("Invalid URL format.")
            return

        full_url = self.get_full_url_from_file(activity_id)
        if full_url:
            output = self.fetch_correct_answers(full_url)
            if output:
                self.result_label.config(text="Powered By GROOZA101")
                self.answers_text.delete(1.0, tk.END)
                for answer in output:
                    self.answers_text.insert(tk.END, answer + "\n")
            else:
                self.show_info("No result found.")
        else:
            self.show_info("Result not found in file.")

    def extract_activity_id(self, url):
        """
        Extracts the activity ID from the provided URL.

        Args:
            url (str): The URL to extract the activity ID from.

        Returns:
            str: The extracted activity ID, or None if not found.
        """
        match = re.search(r'/activity/([^/]+)/exercise', url)
        if match:
            return match.group(1)
        return None

    def get_full_url_from_file(self, activity_id):
        """
        Retrieves the full URL from a file based on the provided activity ID.

        Args:
            activity_id (str): The activity ID to search for in the file.

        Returns:
            str: The full URL corresponding to the activity ID, or None if not found.
        """
        try:
            with open('final_correct_response.txt', 'r') as file:
                for line in file:
                    if activity_id in line:
                        return line.strip()
        except FileNotFoundError:
            self.show_error("File not found!")
        return None

    def fetch_correct_answers(self, full_url):
        """
        Fetches the correct answers from the provided full URL.

        Args:
            full_url (str): The full URL to fetch the answers from.

        Returns:
            list: A list of correct answers, or None if an error occurred.
        """
        headers = {
            'Host': 'app.ofppt-langues.ma',
            'X-Device-Uuid': 'c4369295-36a2-4d7b-bd6f-d805f76a5a60',
            'X-Altissia-Token': '1c9b5e0c51828d85bedbf26b940ffa7bdc5aa8c0407002c234e6c23ccd8087fc',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        try:
            response = requests.get(full_url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            content = response.json()
            if 'content' in content and 'items' in content['content'] and content['content']['items']:
                correct_answers_list = []
                if 'content' in content and 'items' in content['content']:
                    for item in content['content']['items']:
                        correct_answers = item.get('correctAnswers')
                        if correct_answers:
                            correct_answers_list.extend(correct_answers)
                flattened_correct_answers = [answer for sublist in correct_answers_list for answer in sublist]
                return flattened_correct_answers
        except requests.RequestException as e:
            self.show_error(f"An error occurred: {e}")
        return None

    def clear_text(self):
        """
        Clears the text in the answers_text widget.
        """
        self.answers_text.delete(1.0, tk.END)

    def copy_answers(self):
        """
        Copies the answers from the answers_text widget to the clipboard.
        """
        answers = self.answers_text.get(1.0, tk.END)
        pyperclip.copy(answers)

    def show_error(self, message):
        """
        Displays an error message dialog box.

        Args:
            message (str): The error message to display.
        """
        mb.showerror("Error", message)

    def show_info(self, message):
        """
        Displays an information message dialog box.

        Args:
            message (str): The information message to display.
        """
        mb.showinfo("Info", message)

    def run(self):
        """
        Runs the GUI application by starting the main event loop.
        """
        self.window.mainloop()

if __name__ == "__main__":
    answer_fetcher_gui = AnswerFetcherGUI()
    answer_fetcher_gui.run()

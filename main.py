#!venv/Script/python
import csv
import datetime
import os
import time

import colorama as colorama
import openai
from dotenv import load_dotenv

load_dotenv('.env')

debug = os.environ.get('DEBUG').strip().lower()
debug = True if debug == 'true' else False

def print_r(text):
    print(colorama.Fore.LIGHTRED_EX + text + colorama.Fore.RESET)

def print_y(text):
    print(colorama.Fore.LIGHTYELLOW_EX + text + colorama.Fore.RESET)
def print_g(text):
    print(colorama.Fore.LIGHTGREEN_EX + text + colorama.Fore.RESET)


def print_b(text):
    print(colorama.Fore.LIGHTBLUE_EX + text + colorama.Fore.RESET)
class BlogsMdGenerator:
    def __init__(self):
        self.object = None
        self.object_path = os.environ.get('OBJECT_PATH').strip()
        self.blogs_config_dict = None
        self.csv_export_directory = None
        self.set_csv_export_path()
        self.load_topics()
        self.api_key = os.environ.get('OPENAI_API_KEY').strip()
        self.delay = int(os.environ.get('DELAY'))

    def set_csv_export_path(self):
        directory = os.environ.get('CSV_FILES_DIRECTORY')
        if directory:
            directory = directory.strip()
            csv_local_path = os.path.join(os.curdir, directory)
            if not os.path.exists(csv_local_path):
                os.makedirs(csv_local_path)
            self.csv_export_directory = csv_local_path
        else:
            print_r("[*]---> Please mention export path as CSV_FILES_DIRECTORY in .env file ")

    def remove_special_characters(self, path):
        invalid = '<>:"|?*%^&#@$~'
        for c in invalid:
            if c in path:
                path = path.replace(c, '')
        return path

    def load_topics(self):
        with open('topics.csv', 'r') as f:
            self.blogs_config_dict = list(csv.DictReader(f))
            if debug:
                print_b('[*]---> your dict', self.blogs_config_dict)
        with open(self.object_path, 'r') as f:
            self.object = f.read()
            if debug:
                print_b('[*]---> your object path = ', self.object_path)
                print_b('[*]---> and object  = ', self.object)

    def populate_object(self, blog_spec):
        if debug:
            print_g(f"{blog_spec}")
        b = blog_spec
        TITLE = b['Topic'].strip() if b['Title'].strip() == '' else b['Title'].strip()
        COVER_IMAGE = b['Cover Image Url'].strip()
        DATE = datetime.datetime.now().strftime('%Y_%m_%d') if b['Date'] == '' else b['Date'].strip()
        AUTHER_NAME = 'Hasnain Haider' if b['Auther Name'] == '' else b['Auther Name']
        AUTHER_PIC = b['Auther Pic']
        O_IMAGE_URL = b['O_IMAGE_URL']
        EXCERPT = b['EXCERPT']
        KEYWORDS = b['KEYWORDS']

        object = self.object
        if debug:
            print_b(f"[*]---> Before \n{object}")
        object = object.replace('--TITLE--', TITLE).replace('--COVER_IMAGE--', COVER_IMAGE) \
            .replace('--DATE--', DATE).replace('--O_IMAGE_URL--', O_IMAGE_URL) \
            .replace('--EXCERT--', EXCERPT).replace('--AUTHER_NAME--', AUTHER_NAME) \
            .replace('--AUTHER-PIC--', AUTHER_PIC)
        if debug:
            print_g(f"[*]---> After \n{object}")
        return object

    def gpt_response(self, prompt=None):
        try:
            print_g('[*]---> Waiting for ChatGPT...')
            openai.api_key = self.api_key
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                temperature=0.8,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response['choices'][0].text
        except Exception as e:
            print_r(f"[*]---> GPT Request Failed, Please check internet {str(e)}")
            return None

    def generate_blogs(self):
        for i, blog in enumerate(self.blogs_config_dict):
            # print(blog.keys())
            print_g(f"[*]---> Topic {i + 1} of {len(self.blogs_config_dict)} loaded from ChatGPT successfully. ")
            topic_to_search = blog['Topic'].strip()
            words_count = int(blog['Words'].strip())
            blog['File Name'] = blog['Topic'].strip().replace(' ', '-') if blog['File Name'] == '' else blog[
                'File Name']
            # # file_name = f'{topic[2].strip()}{datetime.datetime.now().strftime("_%d_%m_%Y_%H_%M")}.md'
            prompt = f'write me an article with headings and subheadings that must have minimum of {words_count}\
             words on topic "{topic_to_search}" as a markdown format'
            Text = ''
            try:
                while (True):

                    gpt_text = self.gpt_response(prompt=prompt)
                    Text += gpt_text
                    words_grabed = len(Text.split())
                    if words_grabed >= words_count:
                        break
                    else:
                        prompt = f"please add more words and headings to this blog '{' '.join(Text.split('')[-300:])}', you just created."
                        print_y(f"[*]---> Adding more words to blog having {words_grabed}/{words_count} words<---[*]")

                self.export_as_md(Text, blog, i)
                Text = ''
            except Exception as e:
                print_r(f"Something went wrong, please check logs. {e}")

            time.sleep(self.delay)
        return "Success"

    def export_as_md(self, gpt_text, blog, i):
        object = self.populate_object(blog_spec=blog)
        if object:
            if gpt_text:
                self.export(blog, object + "\n" + gpt_text)
        else:
            print_r(f"Could not compose Markdown, check templates at line {i + 1}")

    def export(self, blog, text):
        try:
            file = f"{self.remove_special_characters(blog['File Name'])}.md"
            path = os.path.join(self.csv_export_directory, file)
            with open(path, 'w') as f:
                f.write(text)
                print(f"FILE [ {file} ] of {len(text.split(' '))} words EXPORTED SUCCESSFULLY ")
        except Exception as e:
            print(f"Failed to Export {file} because {str(e)}")


if __name__ == "__main__":
    bmg = BlogsMdGenerator()
    print(bmg.generate_blogs())

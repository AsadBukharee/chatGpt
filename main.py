#!venv/Script/python
import csv
import datetime
import os
import time

import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
CSV_FILES = os.path.join(os.curdir, "csv_files")

WAQFY_KA_TIME = 5  # IN SECONDS.
if not os.path.exists(CSV_FILES):
    os.makedirs(CSV_FILES)


def load_topics():
    with open('topics.csv', 'r') as f:
        reader = csv.reader(f)
        topics = list(reader)
    return topics


def load_object(text="", file='./templates/object.md', topic=[], offset=3):
    TITLE = topic[offset + 3] if topic[offset + 3] != '' else topic[offset + 0]
    COVER_IMAGE = topic[offset + 4] if topic[offset + 4] != '' else topic[offset + 4]
    DATE = topic[offset + 5] if topic[offset + 5] != '' else datetime.datetime.now().strftime('%Y_%m_%d')
    AUTHER_NAME = topic[offset + 6] if topic[offset + 6] != '' else topic[offset + 6]
    AUTHER_PIC = topic[offset + 7] if topic[offset + 7] != '' else topic[offset + 7]
    O_IMAGE_URL = topic[offset + 8] if topic[offset + 8] != '' else topic[offset + 8]
    EXCERPT = topic[offset + 9] if topic[offset + 9] != '' else topic[offset + 9]
    KEYWORDS = topic[10:]
    object = ""
    with open(file, 'r') as f:
        object = f.read()
        # print(object)
    object = object.replace('--TITLE--',TITLE).replace('--COVER_IMAGE--',COVER_IMAGE)\
       .replace('--DATE--',DATE).replace('--O_IMAGE_URL--',O_IMAGE_URL)\
       .replace('--EXCERT--',EXCERPT).replace('--AUTHER_NAME--',AUTHER_NAME)\
       .replace('--AUTHER-PIC--',AUTHER_PIC)
    # print(object)
    if text and object:
        text = f"{object}\n{text}"
        return text
    return None

def main():
    topics = load_topics()
    offset = 3
    for i, topic in enumerate(topics):
        if i > 0:
            try:
                topic_to_search = topic[0].strip()
                words_count = topic[1].strip()
                file_name = f'{topic[2].strip()}.md'
                prompt = f'write me an article that must have minimum of {words_count} words on topic "{topic_to_search}" as a markdown format'
                print(prompt)
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=2048,
                    temperature=0.8,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                print(f"Topic {i + 1} of {len(topics)} loaded from ChatGPT successfully. ")
            except Exception as e:
                print("GPT Request Failed, Please check internet", str(e))
            time.sleep(WAQFY_KA_TIME)
            try:
                text = response['choices'][0].text
                text = load_object(text,topic=topic,offset=0,)
                if text:
                    with open(os.path.join(CSV_FILES, file_name), 'w') as f:
                        f.write(text)
                    print(f"FILE {file_name} of {len(text.split(' '))} words EXPORTED SUCCESSFULLY ")
                    print("Going to sleep for 10 seconds.")
                else:
                    print(f"Could not compose Markdown, check templates at line {i+1}")
            except Exception as e:
                print("File Export Failed", str(e))


if __name__ == "__main__":
    main()

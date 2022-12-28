import csv
import os
import time

import openai

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY
CSV_FILES = os.path.join(os.curdir, "csv_files")
WAQFY_KA_TIME=5 # IN SECONDS.
if not os.path.exists(CSV_FILES):
    os.makedirs(CSV_FILES)


def load_topics():
    with open('topics.csv', 'r') as f:
        reader = csv.reader(f)
        topics = list(reader)
    return topics


def main():
    topics = load_topics()
    for i,topic in enumerate(topics):
        try:
            topic_to_search= topic[0].strip()
            words_count= topic[1].strip()
            file_name= f'{topic[2].strip()}.md'
            prompt = f'write me an article of {words_count} words on topic "{topic_to_search}" as a markdown format'
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=1024,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(f"Topice {i+1} of {len(topics)} exported successfully. ")
        except Exception as e:
            print("GPT Request Failed",e.__str__())
        time.sleep(WAQFY_KA_TIME)
        try:
            text = response['choices'][0].text
            with open(os.path.join(CSV_FILES, file_name), 'w') as f:
                f.write(text)
            print(f"FILE {file_name} of {len(text.split(' '))} words EXPORTED SUCCESSFULLY ")
            print("Going to sleep for 10 seconds.")
        except Exception as e:
            print("File Export Failes",e.__str__())

if __name__ == "__main__":
    main()

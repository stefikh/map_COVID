import json
import re
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Country_and_message1 not clean.json')

sample_json = ''

with open(filename, "r", encoding="utf-8") as file:
  sample_json+=file.read()

glossary = json.loads(sample_json)
dict_messages = {}
for message in glossary:
    glavnoe_message = glossary[message][1].split("',")
    for element in glavnoe_message:
        list_messages = []
        if 'text' in element:
            malenkoe_message = element.split("\\n")
            for new in malenkoe_message:
                text = str(new)
                if re.findall(r'[Cc]ovid|COVID|[Кк]оронавирус[а-я]*|[Оо]чаг|[Зз]аражен[а-я]|[Пп]андем[а-я]|[Ээ]пидеми[а-я]|[Вв]ирус[а-я]*', text):
                    text = re.sub(r"'},",'', text)
                    text = re.sub(r"'text':", '', text)
                    list_messages.append(text)
        if len(list_messages) != 0:
            dict_messages[message] = glossary[message][0], list_messages
with open ('Country_and_message1 clean.json', 'w', encoding="utf-8") as file:
    json.dump(dict_messages, file, ensure_ascii=False)


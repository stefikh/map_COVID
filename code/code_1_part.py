import os
import json
import re

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'bbc.json')

#из всех новостей берём те, что про коронавирус и записываем в файл

sample_json = ''
with open(filename, "r", encoding="utf-8") as file:
  sample_json += file.read()
glossary = json.loads(sample_json)
covid_dict = {}
for elem in glossary:
    text = str(glossary[elem])
    if re.findall(r'[Cc]ovid|COVID|коронавирус|[Пп]андем[а-я]', text):
        covid_dict[elem] = text
with open ('Covid_dict.json', 'w', encoding="utf-8") as file:
    json.dump(covid_dict, file, ensure_ascii=False)

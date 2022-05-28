import json
import re

sample_json = ''
with open("/Users/katia/Desktop/news_dict.json", "r", encoding="utf-8") as file:
  sample_json += file.read()
glossary = json.loads(sample_json)
covid_dict = {}
for elem in glossary:
    text = str(glossary[elem])
    if re.findall(r'[Cc]ovid|COVID|коронавирус|[Пп]андем[а-я]', text):
        covid_dict[elem] = text
with open ('/Users/katia/Desktop/Covid_dict.json', 'w', encoding="utf-8") as file:
    json.dump(covid_dict, file, ensure_ascii=False)
    # for key, val in news_dict.items():
#       file.write('{}:{}\n'.format(key,val))

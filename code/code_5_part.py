#Удаляем из файла сам текст сообщений и проверяем, что ничего не потерялось
import os
import json
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Country_and_coord_and_dynFULL.json')

sample_json = ''
with open(filename, "r", encoding="utf-8") as file:
    sample_json += file.read()

glossary = json.loads(sample_json)

new_glossary = {}

glossary_countries_count = 0
new_glossary_countries_count = 0

for date in glossary:
    countries = glossary[date][0]
    for country in countries:
        glossary_countries_count += 1

for date in glossary:
    new_glossary[date] = glossary[date][0]
    
for date in new_glossary:
    countries = new_glossary[date]
    for country in countries:
        new_glossary_countries_count += 1
        
print(len(glossary), glossary_countries_count)
print(len(new_glossary), new_glossary_countries_count)

with open ('Country_and_coord_and_dynFULL_no_text.json', 'w', encoding="utf-8") as file:
    json.dump(new_glossary, file, ensure_ascii=False)

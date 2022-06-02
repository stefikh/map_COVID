#код с регуляркой, присваивающий 0/1 в зависимости от динамики эпидемситуации

import re
import json
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Covid_dict.json')

countgooddyn = 0
countbaddyn = 0
sample_json = ''
with open("data1.json", "r", encoding="utf-8") as file:
  sample_json+=file.read()

glossary = json.loads(sample_json)

print(len(glossary))
for date in glossary:
    if len(glossary[date][0]) == 1:
        countries = glossary[date][0] 
        text = glossary[date][1]
        if re.findall(r'[Мм]иновал|[Оо]слабл[а-я]+|[Сс]нят[а-я]+|[Уу]пад[а-я]+|[Сс]ниж[а-я]+|[Вв]ыходит|[Сс]мягч[а-я]+|[Пп]ад[а-я]*|[Зз]амедл[а-я]+|[Уу]был[а-я]+|[Сс]нима[а-я]+', text):
            for country in countries:
                countries[country]["dyn"] = 1
                countgooddyn += 1
        if re.findall(r'[Пп]ик[а]|[Вв]спышк[а-я]|[Пп]ревы[а-я]+|[Уу]велич[а-я]+|[А-Яа-я]+?рекорд[а-я]+|[Уу]худш[а-я]+|[Р-р][ао]ст[а-я]+|[Зз]акры[а-я]+|[Вв]в[ео]д[а-я]т([а-я]+)?|[Мм]аксим[а-я]+|[Вв]ы?рост[а-я]+|[Пп]рирост[а-я]|[Сс]кач[а-я]+|более|снова|[Уу]сил[а-я]+|выросло', text):
            for country in countries:
                countries[country]["dyn"] = 0
                countbaddyn += 1
    print(glossary[date][0])
with open ('Country_and_coord_and_dynFULL.json', 'w', encoding="utf-8") as file:
    json.dump(new_glossary, file, ensure_ascii=False)


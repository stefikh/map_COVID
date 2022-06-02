import os
import json
import re
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc, MorphVocab

segmenter = Segmenter()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)
morph_vocab = MorphVocab()

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Covid_dict.json')

#часть кода, где выкачиваем локации и записываем в словарь формата: "2020-01-22T14:33:33": ["Китае", "Ухань", "Хубэй", "США", "Таиланда", "Южной Кореи"]

sample_json = ''

with open(filename, "r", encoding="utf-8") as file:
  sample_json+=file.read()

glossary = json.loads(sample_json)
dict_local = {}
for message in glossary:
   locals = []
   doc = Doc(glossary[message])
   text = glossary[message]
   doc.segment(segmenter)
   doc.tag_ner(ner_tagger)
   for span in doc.spans:
          span.normalize(morph_vocab)
          if span.type == 'LOC':
              locals.append(span.normal)
          dict_local[message] = locals, glossary[message]
with open ('Country_and_message.json', 'w', encoding="utf-8") as file:
    json.dump(dict_local, file, ensure_ascii=False)


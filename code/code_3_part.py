#1. Убирает повторы в странах
#2. Переводит их на английский
#3. Присваивает каждому населенному пункту координаты
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, Doc, MorphVocab, NewsSyntaxParser, NewsMorphTagger
import os
import json
from deep_translator import GoogleTranslator
import geopy
import geopandas
from geopandas.tools import geocode
from geopy.geocoders import Nominatim


segmenter = Segmenter()
emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)
morph_tagger = NewsMorphTagger(emb)
morph_vocab = MorphVocab()
syntax_parser = NewsSyntaxParser(emb)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Country_and_message1 not clean.json')

sample_json = ''

with open(filename, "r", encoding="utf-8") as file:
  sample_json+=file.read()

glossary = json.loads(sample_json)

#print(len(glossary))
for date in glossary:
        countries = glossary[date][0]
        new_countries = []
        for country in countries:
            doc = Doc(country)
            doc.segment(segmenter)
            doc.tag_morph(morph_tagger)
            doc.tag_ner(ner_tagger)
            doc.parse_syntax(syntax_parser)
            for span in doc.spans:
                span.normalize(morph_vocab)  
                new_country = span.normal
                to_translate = new_country
                eng_country = GoogleTranslator(source='auto', target='en').translate(to_translate)
                if eng_country not in new_countries:
                    new_countries.append(eng_country)
        glossary[date][0] = new_countries   
for date in glossary:
        countries = glossary[date][0]
        countries_with_coord = {}
        for country in countries:
            location = geocode(country, provider="nominatim" , user_agent = 'my_request')
            point = location.geometry.iloc[0]
            longitude = point.x
            latitude = point.y
            country_with_coord = {}
            country_with_coord["lon"] = longitude
            country_with_coord["lat"] = latitude
            countries_with_coord[country] = country_with_coord
        glossary[date][0] = countries_with_coord
        print(glossary[date][0])
with open ('Country_and_coord1.json', 'w', encoding="utf-8") as file:
    json.dump(glossary, file, ensure_ascii=False)


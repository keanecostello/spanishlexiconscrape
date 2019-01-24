import re
import pandas as pd

df = pd.read_csv("etym_scrape_results.csv", index_col=0)
df.columns = ["word", "desc"]


def get_time(txt):
    times = re.findall("[0-9].* cent.", txt)
    if len(times) > 0:
        return times[0]
    else:
        return "No Time Found"


def get_lang(txt):
    languages = ["Spanish", "Portugese", "Romanian", "Latin", "Italian", "French", "Catalan", "Basque",
                 "Vulgar Latin", "Arabic", "Andalusian Arabic", "Andalusian", "Old Spanish", "Galician", "Nahuatl",
                 "Ancient Greek","Quechua","German","Romany","Gothic","Celtic","Germanic","Japanese","Mapuche","Tanga",
                 "Tarusa","Amoy","Middle Low German","Proto-celtic","Taino","Persian","Occitan"]
    all_langs = re.findall("(?<=from ){}".format("|".join(languages)), txt)
    if len(all_langs) > 0:
        return all_langs[0]
    else:
        return "No Language Found"


def get_pos(txt):
    parts_of_speech = ["Adjective", "Verb", "Adverb", "Preposition", "Noun", "Pronoun", "Conjunction", "Interjection"]
    pos_find = re.findall("|".join(parts_of_speech), txt)
    if len(pos_find) > 1:
        return pos_find[1]
    elif len(pos_find) > 0:
        return pos_find[0]
    else:
        return "No POS found"


def get_info(row):
    txt = row.desc
    time = get_time(txt)
    pos = get_pos(txt)
    lang = get_lang(txt)
    return list(row) + [time, lang, pos]


parsed_df = df.apply(get_info, axis=1, result_type="expand")
parsed_df.columns = ["word", "desc", "time", "lang", "pos"]

parsed_df.to_csv("etym_parsed_good.csv")
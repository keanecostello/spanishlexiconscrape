import pandas as pd

df = pd.read_csv("etym_parsed_good.csv")
no_lang_df = df[df.lang == "No Language Found"]

new_langs = []

start_indx = 640
number_new = 100
end_indx = min(start_indx+number_new, len(no_lang_df))

for indx, desc in enumerate((no_lang_df.desc[start_indx:end_indx])):
    print("\n\nRow {}\n".format(start_indx+indx))
    print(desc)
    new_langs.append(input("Add New Language or Press Enter to Skip\n"))

new_langs = list(set([lang for lang in new_langs if lang != '']))

print("""\n\nPlease Add {} To Your List of Languages in `parse_it_up.py`.
 Replace `start_indx` in this script with the last `Row __` printed to the console ONLY IF NO NEW LANGUAGES WERE ADDED.
 Re-run""".format(new_langs))


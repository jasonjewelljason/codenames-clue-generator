# Gets and filters GloVe vectors to only save the top ~100k words, taken from Keith Vertanen's match8 word list

from tqdm import tqdm
import requests
import zipfile
import os

glove_url = 'https://nlp.stanford.edu/data/glove.42B.300d.zip'
wordlist_url = 'https://www.keithv.com/software/wlist/wlist_match8.zip'

glove_zip = 'glove.42B.300d.zip'
match8zip = 'wlist_match8.zip'

# Download
r = requests.get(glove_url)
if r.status_code == 200:
    with open(glove_zip, 'wb') as f:
        f.write(r.content)

r = requests.get(wordlist_url)
if r.status_code == 200:
    with open(match8zip, 'wb') as f:
        f.write(r.content)

# Unzip
with zipfile.ZipFile(glovezip, 'r') as zip_ref:
    zip_ref.extractall()
with zipfile.ZipFile(match8zip, 'r') as zip_ref:
    zip_ref.extractall()

# Remove zipped files
os.remove(glove_zip)
os.remove(match8zip)

# Filter and save new file
glove_file = 'glove.42B.300d.txt'
match8file = 'wlist_match8.txt'

acceptable_words = {line[:-1] for line in open(match8file)}
filtered_lines = [line for line in tqdm(open(glove_file)) if line.split()[0] in acceptable_words]

print('length: ', len(filtered_lines))

new_glove_file = 'glove.42B.300d.filtered.txt'

with open(new_glove_file, 'w') as f:
    f.write("".join(filtered_lines))

os.remove(glove_file)

from tqdm import tqdm

filtered_lines = []
match8file = 'wlist_match8.txt'
glove_file = 'glove.42B.300d.txt'

acceptable_words = {line[:-1] for line in open(match8file)}
filtered_lines = [line.split() for line in tqdm(open(glove_file)) if line.split()[0] in acceptable_words]

print('length: ', len(filtered_lines))

new_glove_file = 'glove.42B.300d.filtered.txt'

with open(new_glove_file, 'w') as f:
    f.write("".join(filtered_lines))

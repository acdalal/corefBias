import os,sys
from collections import defaultdict

input_file = sys.argv[1]
original_file = sys.argv[2]
output_file = sys.argv[3]

all_words = []
index_token = defaultdict(lambda:[])
name_count = defaultdict(lambda:-1)
name_index = defaultdict(lambda: [])
line_no = 0
cur_order = 0
for line in open(input_file).readlines():
    if line.startswith("#begin"):
        index_token = defaultdict(lambda: {})
        """@index_token: in this sentence, which token needs to be anonymized. return {sentence_no1:{index1:(ori_word,TOKEN1), index2:(ori_word,TOKEN2)}, sentence_no2:...}"""
        name_count = defaultdict(lambda:0)
        """@name_count={name:its order}: the order of each name occurring in this document. e.g. {John:0} means John is the first name occuring in the document"""
        name_index = defaultdict(lambda: [])
        """@name_index = {name:(sentence_no, word_index)}: the index for this name in one sentence. e.g. {John:(2,3)} means John is the 3rd word in the 2nd sentence."""
        continue
    if line.startswith("#end"):
        """after scanning one document, replace the sentence_no-th [] in all_words to the {word_index:token}. All_words only contains the result for all the texts, not covering begin/end document and empty lines."""
        cur_order = 0
        for lineno in index_token:
            all_words[lineno] = index_token[lineno]
        continue
    all_words.append([])
    if "B-PER" in line: #for one sentence
        words = line.strip().split()
        index = 0
        for word in words:
            if "PER" in word:
                real_word = word.split('__')[0]
                if real_word not in name_count:
                    name_count[real_word] = cur_order #{John:1, Mary:2}
                    cur_order += 1
                name_index[real_word].append((line_no,index)) #{"x":[(2,5)..]}
            index += 1

        for name in name_count:
            for index in name_index[name]:
                index_token[index[0]][index[1]] = (name,"ANON_" + str(name_count[name]))
    line_no += 1
assert len(all_words) == line_no
# print(all_words)
#print(all_words)
#print(index_token)

new_file = []
file_position = 0

for line in open(original_file).readlines():
    if line.startswith("#begin"):
        new_file.append(line)
        continue
    elif line.startswith("#end"):
        new_file.append(line)
        continue
    elif len(line) != 0:
        words = line.split()
        if all_words[file_position] != []:
            for word_index in all_words[file_position]:
                ori, token = all_words[file_position][word_index]
                words[word_index] = words[word_index].replace(ori, token,1)
        #print(words)
        new_file.append(" ".join(words))
    file_position += 1
#print(new_file)

with open(output_file, 'w') as f:
    for line in new_file:
        f.write(line + "\n")


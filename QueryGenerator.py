lexicons = ["immigrant", "xenophobia", "misogyny"]
insults = "insults"

def name_to_lexicon(file_name):
    return "lexicons\\" + file_name + "_lexicon.txt"

def file_to_list(file_path):
    file = open(file_path)
    result = file.readlines()
    for i in range(len(result)):
        result[i] = result[i].strip()
    return result

insult_list = file_to_list(name_to_lexicon(insults))

for lexicon in lexicons:
    word_list = file_to_list("lexicons\\" + lexicon + "_lexicon.txt")
    for word in word_list:
        if insult_list.count(word) >= 0:
            word_list.remove(word)
    query = " OR ".join(word_list)
    query += " lang:en"
    if lexicon == "misogyny":
        print(query)
    file = open("queries\\" + lexicon + "_query.txt", "w")
    file.write(query)
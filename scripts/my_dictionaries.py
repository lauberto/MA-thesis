import re

def get_att_dict():
    with open('att_verbs.txt', 'r', encoding='utf-8') as f:
        att_verbs = f.read()

    att_verbs = re.split('[\n,]', att_verbs)
    att_verbs = [x.strip() for x in att_verbs if x]
    att_verbs = set(att_verbs)
    return att_verbs
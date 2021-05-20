import prodrop_check
from my_dictionaries import get_wh_tokens, get_att_dict

PUNKT = '?!'
ATT_VERBS = get_att_dict()
WH_QUESTIONS = get_wh_tokens()
OTHER_TAGS = ['PUNCT', 'SYM', 'X', ]
CLASS_DICT = {'FALSE' : 0, 'TRUE': 1, 'coreference resolution': 2, }


def preprocess(text: str):
    if text[-1] != '.' and text[-1] not in PUNKT:
        text = text + '.'
    return text


def class2id(class_string: str):
    return CLASS_DICT.get(class_string)


def count_conj(conllu_sents: list, conj_type: str):
    conj_count = 0

    for sent in conllu_sents:
        for token in sent:
            if token['upos'] == conj_type:
                conj_count += 1
    return conj_count


def count_tokens(conllu_sents: list):
    count = 0

    for sent in conllu_sents:
        for token in sent:
            if token['upos'] not in OTHER_TAGS:
                count += 1
    return count


def count_null_pron(conllu_sents: list):
    null_pron_list = prodrop_check.detect_null_pron_heads(conllu_sents)
    return len(null_pron_list)


def count_overt_pron(conllu_sents: list):
    overt_pron_list = prodrop_check.detect_overt_pron_heads(conllu_sents)
    return len(overt_pron_list)


def count_adjuncts(conllu_sents: list):
    adjunct_count = 0

    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'advcl':
                adjunct_count += 1
    return adjunct_count


def count_whquestions(conllu_sents: list):
    whquestion_count = 0

    for sent in conllu_sents:
        for token in sent:
            if token['form'] in WH_QUESTIONS:
                whquestion_count += 1
    return whquestion_count


def count_relclauses(conllu_sents: list):
    relclauses_count = 0

    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'acl:relcl':
                relclauses_count += 1
    return relclauses_count


def get_root_id(conllu_sents: list):
    root_id = 0

    for sent in conllu_sents:
        for token in sent:
            if token['head'] == 0:
                root_id = token['id']
    return root_id


def get_root_length(conllu_sents: list):
    root_length = 0

    for sent in conllu_sents:
        for token in sent:
            if token['head'] == 0:
                root_length = len(token['form'])
    return root_length


def get_root_dependents(conllu_sents: list):
    root_id = get_root_id(conllu_sents)
    dependents = list()

    for sent in conllu_sents:
        for token in sent:
            if token['head'] == root_id:
                dependents.append(token['id'])
    return dependents


def count_root_dependents(conllu_sents: list):
    dependents = get_root_dependents(conllu_sents)
    return len(dependents)


def get_root_pos(conllu_sents: list):
    
    for sent in conllu_sents:
        for token in sent:
            if token['head'] == 0 and token['upos'] == 'VERB':
                return 1
            else:
                return 0


def is_there_exact_string_match(conllu_sents: list):
    root_str = ''
    match = 0

    for sent in conllu_sents:
        for token in sent:
            if token['head'] == 0:
                root_str = token['form']
    for sent in conllu_sents:
        for token in sent:
            if token['form'] == root_str:
                match = 1
    return match


def count_root_case_dep(conllu_sents: list, case: str):
    dependents = get_root_dependents(conllu_sents)
    count = 0
    for sent in conllu_sents:
        for token in sent:
            if (
                token['id'] in dependents and 
                token['feats'] and
                'Case' in token['feats'] and 
                token['feats']['Case'] == case
            ):
                count += 1
    return count


def is_there_att_verb(conllu_sents:list):
    att_verb = 0

    for sent in conllu_sents:
        for token in sent:
            if token['lemma'] in ATT_VERBS:
                att_verb = 1
    return att_verb


def count_case_nodes(conllu_sents: list, case: str):
    count = 0
    for sent in conllu_sents:
        for token in sent:
            if (
                token['feats'] and
                'Case' in token['feats'] and 
                token['feats']['Case'] == case
            ):
                count += 1
    return count
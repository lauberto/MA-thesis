from my_dictionaries import get_att_dict


ATT_VERBS = get_att_dict()
CLAUSES_DEPREL = ['csubj', 'ccomp', 'xcomp', 'advcl', 'acl']

def detect_overt_pron_heads(conllu_sents: list) -> list:
    overt_prons = list()
    for sent in conllu_sents:
        overt_prons = [token['head'] for token in sent if token['upos'] == 'PRON']
    return overt_prons


def detect_null_pron_heads(conllu_sents: list) -> list:
    '''
    it detects the tokens to the left of which,
    a null pronoun is assumed
    '''
    ACCEPTED_POS = ['PRON', 'NOUN', 'PROPN', 'DET', 'ADJ', 'NUM']
    candidate_predicates = dict()
    null_prons = list()
    for sent in conllu_sents:
        for token in sent:
            if token['feats'] and 'VerbForm' in token['feats'] and token['feats']['VerbForm'] == 'Fin':
                candidate_predicates[token['id']] = dict()
                candidate_predicates[token['id']]['predicate'] = token
                candidate_predicates[token['id']]['dependents'] = list()

        for token in sent:
            if token['head'] in candidate_predicates.keys():
                candidate_predicates[token['head']]['dependents'].append(token['upos'])
                
    for x in candidate_predicates.values():
        if any(item in x['dependents'] for item in ACCEPTED_POS):
            continue
        else:
            null_prons.append(x['predicate']['id'])
    return null_prons


def subclause_check(conllu_sents: list, overt_prons: list, null_prons: list):
    ## 'chto_count' decides whether the voter can submit a vote for a given sentence or not
    clauses_count = 0
    chto_count = 0
    comma_position = 0
    sconj = {'id': 0, 'head': 0}
    att_verb_position = 0
    embedded_verb = 0

    for sent in conllu_sents:
        for token in sent:
            if token['form'] == 'что': 
                sconj['id'] = token['id']
                sconj['head'] = token['head']
                chto_count += 1
            if token['deprel'] in CLAUSES_DEPREL:
                clauses_count += 1

    if chto_count == clauses_count:
        for sent in conllu_sents:
            for token in sent:
                if token['form'] == ',' and token['id'] < sconj['id']:
                    comma_position = token['id']
            for token in sent:
                if token['upos'] == 'VERB' and token['id'] < comma_position:
                    att_verb_position = token['id']
            for token in sent:
                if token['id'] == sconj['head']:
                    embedded_verb = token['id']
                
        if att_verb_position < comma_position and comma_position < sconj['id'] and embedded_verb in null_prons:
            return 'coreference resolution'
        elif (
            att_verb_position < comma_position and comma_position < sconj['id'] and
            any(i > sconj['id'] and i == sconj['head'] for i in overt_prons)
            ):
            return 'TRUE'
        else:
            return 'FALSE'
    return None


def subclause_check_attitude(conllu_sents: list, overt_prons: list, null_prons: list):
    ## 'chto_count' decides whether the voter can submit a vote for a given sentence or not
    clauses_count = 0
    chto_count = 0
    comma_position = 0
    sconj = {'id': 0, 'head': 0}
    att_verb_position = 0
    embedded_verb = 0
    
    for sent in conllu_sents:
        for token in sent:
            if token['form'] == 'что': 
                sconj['id'] = token['id']
                sconj['head'] = token['head']
                chto_count += 1
            if token['deprel'] in CLAUSES_DEPREL:
                clauses_count += 1

    if chto_count == clauses_count:
        for sent in conllu_sents:
            for token in sent:
                if token['form'] == ',' and token['id'] < sconj['id']:
                    comma_position = token['id']
            for token in sent:
                if token['lemma'] in ATT_VERBS and token['id'] < comma_position:
                    att_verb_position = token['id']
            for token in sent:
                if token['id'] == sconj['head']:
                    embedded_verb = token['id']
                
        if att_verb_position < comma_position and comma_position < sconj['id'] and embedded_verb in null_prons:
            return 'coreference resolution'
        elif (
            att_verb_position < comma_position and comma_position < sconj['id'] and
            any(i > sconj['id'] and i == sconj['head'] for i in overt_prons)
            ):
            return 'TRUE'
        else:
            return 'FALSE'
    return None


def adjuncts_check(conllu_sents: list, overt_prons: list, null_prons: list):
    advcl_nodes = list()

    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'advcl':
                advcl_nodes.append(token['id'])
    if advcl_nodes:
        if any(item in advcl_nodes for item in null_prons):
            return 'coreference resolution'
        elif any(item in advcl_nodes for item in overt_prons):
            return 'TRUE'
        else:
            return 'FALSE'
    return None
from my_dictionaries import get_att_dict, get_wh_tokens


ATT_VERBS = get_att_dict()
WH_QUESTIONS = get_wh_tokens()
CLAUSES_DEPREL = ['csubj', 'ccomp', 'xcomp', 'advcl', 'acl', ]
SUBJ_DEPREL= ['nsubj', 'csubj', ]
SUBJ_LIST = ['чтобы', 'чтоб', ]

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
    candidate_predicates = dict()
    null_prons = list()
    for sent in conllu_sents:
        for token in sent:
            if (token['feats'] and 'VerbForm' in token['feats'] and token['feats']['VerbForm'] == 'Fin') or (token['deprel'] == 'ccomp'):
                candidate_predicates[token['id']] = dict()
                candidate_predicates[token['id']]['predicate'] = token
                candidate_predicates[token['id']]['dependents'] = list()

        for token in sent:
            if token['head'] in candidate_predicates.keys():
                candidate_predicates[token['head']]['dependents'].append(token['deprel'])
                
    for x in candidate_predicates.values():
        if any(item in x['dependents'] for item in SUBJ_DEPREL):
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
    embedded_verb = {'id': 0, 'upos': ''}

    for sent in conllu_sents:
        for token in sent:
            if token['form'] == 'что': 
                sconj['id'] = token['id']
                sconj['head'] = token['head']
                chto_count += 1
            if token['deprel'] in CLAUSES_DEPREL:
                clauses_count += 1
        for token in sent:
            if token['id'] == sconj['head']:
                embedded_verb['upos'] = token['upos']

    # if chto_count == clauses_count and embedded_verb['upos'] == 'VERB':
    for sent in conllu_sents:
        for token in sent:
            if token['form'] == ',' and token['id'] < sconj['id']:
                comma_position = token['id']
        for token in sent:
            if token['upos'] == 'VERB' and token['id'] < comma_position:
                att_verb_position = token['id']
        for token in sent:
            if token['id'] == sconj['head']:
                embedded_verb['id'] = token['id']
            
    if att_verb_position < comma_position and comma_position < sconj['id'] and embedded_verb['id'] in null_prons:
        return 'coreference resolution'
    elif (
        att_verb_position < comma_position and comma_position < sconj['id'] and
        any(i > sconj['id'] and i == sconj['head'] for i in overt_prons)
        ):
        return 'TRUE'
    else:
        return None
    # return None


def subclause_check_attitude(conllu_sents: list, overt_prons: list, null_prons: list):
    ## 'chto_count' decides whether the voter can submit a vote for a given sentence or not
    clauses_count = 0
    chto_count = 0
    comma_position = 0
    sconj = {'id': 0, 'head': 0}
    att_verb_position = 0
    embedded_verb = {'id': 0, 'upos': ''}
    
    for sent in conllu_sents:
        for token in sent:
            if token['form'] == 'что': 
                sconj['id'] = token['id']
                sconj['head'] = token['head']
                chto_count += 1
            if token['deprel'] in CLAUSES_DEPREL:
                clauses_count += 1
        for token in sent:
            if token['id'] == sconj['head']:
                embedded_verb['upos'] = token['upos']

    # if chto_count == clauses_count and embedded_verb['upos'] == 'VERB':
    for sent in conllu_sents:
        for token in sent:
            if token['form'] == ',' and token['id'] < sconj['id']:
                comma_position = token['id']
        for token in sent:
            if token['lemma'] in ATT_VERBS and token['id'] < comma_position:
                att_verb_position = token['id']
        for token in sent:
            if token['id'] == sconj['head']:
                embedded_verb['id'] = token['id']
            
    if att_verb_position < comma_position and comma_position < sconj['id'] and embedded_verb['id'] in null_prons:
        return 'coreference resolution'
    elif (
        att_verb_position < comma_position and comma_position < sconj['id'] and
        any(i > sconj['id'] and i == sconj['head'] for i in overt_prons)
        ):
        return 'TRUE'
    else:
        return None
        # return 'FALSE'
    # return None


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


def wh_question_check(conllu_sents: list, overt_prons: list, null_prons: list):
    wh_nodes = list()

    for sent in conllu_sents:
        for token in sent:
            if token['form'] in WH_QUESTIONS:
                wh_nodes.append(token['head'])
    if wh_nodes:
        if any(item in wh_nodes for item in null_prons):
            return 'coreference resolution'
        elif any(item in wh_nodes for item in overt_prons):
            return 'TRUE'
        else:
            'FALSE'
    return None


def relative_check(conllu_sents: list, overt_prons: list, null_prons: list):
    relative_nodes = list()

    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'acl:relcl':
                relative_nodes.append(token['id'])
    if relative_nodes:
        if any(item in relative_nodes for item in null_prons):
            return 'coreference resolution'
        if any(item in relative_nodes for item in overt_prons):
            return 'TRUE'
        else:
            return 'FALSE'
    return None


def nominal_copular_check(conllu_sents: list, overt_prons: list, null_prons: list):
    nominal_copular_nodes = list()
    copular_aux_count = 0

    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'ccomp' and token['upos'] == 'NOUN':
                nominal_copular_nodes.append(token['id'])
    for sent in conllu_sents:
        for token in sent:
            if token['head'] in nominal_copular_nodes and token['deprel'] == 'cop':
                copular_aux_count += 1
    if nominal_copular_nodes and copular_aux_count == 0:
        if any(item in nominal_copular_nodes for item in null_prons):
            return 'FALSE'
        elif any(item in nominal_copular_nodes for item in overt_prons):
            return 'TRUE'
        else:
            return 'coreference resolution'
    return None


def adj_copular_check(conllu_sents: list, overt_prons: list, null_prons: list):
    short_adj_copular_nodes = list()
    long_adj_copular_nodes = list()
    copular_aux_count = 0

    for sent in conllu_sents:
        for token in sent:
            if (token['deprel'] == 'ccomp' or token['deprel'] == 'amod') and token['upos'] == 'ADJ':
                if token['feats'] and 'Variant' in token['feats'] and token['feats']['Variant'] == 'Short':
                    short_adj_copular_nodes.append(token['id'])
                else:
                    long_adj_copular_nodes.append(token['id'])
    for sent in conllu_sents:
        for token in sent:
            if (
                (token['head'] in short_adj_copular_nodes or
                token['head'] in long_adj_copular_nodes) and token['deprel'] == 'cop'
            ):
                copular_aux_count += 1
            elif token['upos'] == 'VERB' and token['head'] in short_adj_copular_nodes:
                short_adj_copular_nodes.remove(token['head'])
    if short_adj_copular_nodes and copular_aux_count == 0:
        if any(item in short_adj_copular_nodes for item in null_prons):
            return 'coreference resolution'
        elif any(item in short_adj_copular_nodes for item in overt_prons):
            return 'TRUE'
    elif long_adj_copular_nodes and copular_aux_count == 0:
        if any(item in long_adj_copular_nodes for item in null_prons):
            return 'FALSE'
        elif any(item in long_adj_copular_nodes for item in overt_prons):
            return 'TRUE'
    else:
        return None


def overt_compl_check(conllu_sents: list, overt_prons: list, null_prons: list):
    null_compl_nodes = list()

    for sent in conllu_sents:
        for token in sent:
            if (
                token['feats'] and 'VerbForm' in token['feats'] and 
                token['feats']['VerbForm'] == 'Fin' and
                token['upos'] == 'VERB' and token['head'] != 0
            ):
                null_compl_nodes.append(token['id'])
    for sent in conllu_sents:
        for token in sent:
            if (token['upos'] == 'SCONJ' or token['upos'] == 'CCONJ') and token['head'] in null_compl_nodes:
                null_compl_nodes.remove(token['head'])
    if any(item in null_compl_nodes for item in null_prons):
        return 'FALSE'
    elif any(item in null_compl_nodes for item in overt_prons):
        return 'TRUE'
    else:
        return None


def coordinate_clause_check(conllu_sents: list, overt_prons: list, null_prons: list):
    coordinate_nodes = dict()
    main_subj = ''

    for sent in conllu_sents:
        for token in sent:
            if token['head'] == 0:
                root = token['id']
    for sent in conllu_sents:
        for token in sent:
            if token['head'] == root and token['deprel'] in SUBJ_DEPREL:
                main_subj = token['form']
    for sent in conllu_sents:
        for token in sent:
            if token['upos'] == 'CCONJ':
                coordinate_nodes[token['head']] = ''
    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'obl' and token['head'] in coordinate_nodes.keys():
                coordinate_nodes.pop(token['head'], None)
    for sent in conllu_sents:
        for token in sent:
            if token['head'] in coordinate_nodes and token['deprel'] in SUBJ_DEPREL:
                coordinate_nodes[token['head']] = token['form']    
    if any(item in coordinate_nodes.keys() for item in null_prons):
        return 'TRUE'
    elif any(item in coordinate_nodes.keys() for item in overt_prons):
        if any(str(item).lower() == str(main_subj).lower() for item in coordinate_nodes.values()):
            return 'FALSE'
        else:
            return 'TRUE'
    else:
        None

def complex_coordinate_clause_check(conllu_sents: list, overt_prons: list, null_prons: list):
    candidate_nodes = list()
    complex_coordinate_nodes = list()

    for sent in conllu_sents:
        for token in sent:
            if token['upos'] == 'CCONJ':
                candidate_nodes.append(token['head'])
    candidate_nodes = list(set(candidate_nodes))
    for sent in conllu_sents:
        for token in sent:
            if token['deprel'] == 'obl' and token['head'] in candidate_nodes:
                complex_coordinate_nodes.append(token['head'])
    if any(item in complex_coordinate_nodes for item in null_prons):
        return 'FALSE'
    elif any(item in complex_coordinate_nodes for item in overt_prons):
        return 'TRUE'
    else:
        None


def subjunctive_clause_check(conllu_sents: list, overt_prons: list, null_prons: list):
    candidate_nodes = list()
    subj_nodes = list()
    main_verb_constraint = False

    for sent in conllu_sents:
        for token in sent:
            if (
                token['feats'] and 'VerbForm' in token['feats'] and 'Tense' in token['feats'] and
                token['feats']['VerbForm'] == 'Fin' and token['feats']['Tense'] == 'Past'
            ):
                candidate_nodes.append(token['id'])
    for sent in conllu_sents:
        for token in sent:
            if token['upos'] == 'SCONJ' and token['head'] in candidate_nodes:
                subj_nodes.append(token['head'])
    subj_nodes = list(set(subj_nodes))
    for sent in conllu_sents:
        for token in sent:
            if (
                token['feats'] and 'VerbForm' in token['feats'] and token['feats']['VerbForm'] == 'Fin' and
                token['head'] == 0 and token['lemma'] in ATT_VERBS
            ):
                main_verb_constraint = True
    if main_verb_constraint:
        if any(item in subj_nodes for item in null_prons):
            return 'coreference resolution'
        elif any(item in subj_nodes for item in overt_prons):
            return 'TRUE'
        else:
            return None
    else:
        if any(item in subj_nodes for item in null_prons):
            return 'FALSE'
        elif any(item in subj_nodes for item in overt_prons):
            return 'TRUE'
        else:
            return None
    
import my_parsers
import prodrop_check
from abc import ABC, abstractmethod


class Voter(ABC):

    @abstractmethod
    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        pass

class SubjClauseChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.subclause_check(conllu_sents, overt_prons, null_prons)

class SubjClauseCheckerAtt(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.subclause_check_attitude(conllu_sents, overt_prons, null_prons)

class AdjunctChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.adjuncts_check(conllu_sents, overt_prons, null_prons)
        

VOTER2CHECKER = {
    'subjclauses': SubjClauseChecker(),
    'subjclauses_att': SubjClauseCheckerAtt(),
    'adjunctclauses': AdjunctChecker()
}


def decision(text: str):
    votes = {'TRUE' : 0, 'FALSE': 0, 'coreference resolution': 0}

    conllu_sents = my_parsers.udpipe_req(text)
    overt_prons = prodrop_check.detect_overt_pron_heads(conllu_sents)
    null_prons = prodrop_check.detect_null_pron_heads(conllu_sents)
    
    for key in VOTER2CHECKER.keys():
        voter = VOTER2CHECKER[key]
        vote = voter.check_and_vote(conllu_sents, overt_prons, null_prons)
        if vote:
            votes[vote] += 1
        else:
            continue
    
    if any(i > 0 for i in votes.values()):
        # return votes
        return max(votes, key=votes.get)  
    return 'None'
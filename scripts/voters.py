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

class WhQuestionChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.wh_question_check(conllu_sents, overt_prons, null_prons)

class RelativeChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.relative_check(conllu_sents, overt_prons, null_prons)

class NominalCopularChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.nominal_copular_check(conllu_sents, overt_prons, null_prons)

class AdjCopularChecker(Voter):
    
    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.adj_copular_check(conllu_sents, overt_prons, null_prons)

class OvertComplChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.overt_compl_check(conllu_sents, overt_prons, null_prons)

class CClauseChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.coordinate_clause_check(conllu_sents, overt_prons, null_prons)

class ComplexCClauseChecker(Voter):

    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.complex_coordinate_clause_check(conllu_sents, overt_prons, null_prons)

class SubjClauseChecker(Voter):
    
    def check_and_vote(self, conllu_sents, overt_prons, null_prons):
        return prodrop_check.subjunctive_clause_check(conllu_sents, overt_prons, null_prons)
        

VOTER2CHECKER = {
    'subjclauses': SubjClauseChecker(),
    'subjclauses_att': SubjClauseCheckerAtt(),
    'adjunctclauses': AdjunctChecker(),
    'whclauses': WhQuestionChecker(),
    'relativeclauses': RelativeChecker(),
    'nominalcopularclauses': NominalCopularChecker(),
    'adjcopularclauses': AdjCopularChecker(),
    'overtcomplclauses': OvertComplChecker(),
    'cclauses': CClauseChecker(),
    'complexcclauses': ComplexCClauseChecker(),
    'subjclauses': SubjClauseChecker()
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
        if votes['FALSE'] > 0:
            return 'FALSE'
        else:
            return max(votes, key=votes.get)  
    return 'None'
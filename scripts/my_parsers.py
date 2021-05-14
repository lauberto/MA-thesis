import os
import conllu
from ufal.udpipe import Model, Pipeline
import requests
import json


def make_conll_with_udpipe(text):
    model_path = os.path.join(os.getcwd(), 'russian-syntagrus-ud-2.5-191206.udpipe')
    model = Model.load(model_path)
    pipeline = Pipeline(model, 'tokenizer=ranges', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')
    udpipe_output = pipeline.process(text)
    return conllu.parse(udpipe_output)


def udpipe_req(text):
    MODEL = 'russian-syntagrus-ud-2.6-200830'
    url = f'http://lindat.mff.cuni.cz/services/udpipe/api/process?model={MODEL}&tokenizer=ranges&tagger&parser&data={text}'
    res = requests.get(url)
    conllu_sents = conllu.parse(json.loads(res.content)['result'])
    return conllu_sents
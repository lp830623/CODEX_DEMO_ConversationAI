from copy import deepcopy
import pytest
from backend.app.domain import find_promises,analyze_conversation
from backend.app.store import fixture

def conversation(text,speaker='agent'):
 c=deepcopy(fixture()['conversations'][0]);c['segments']=[{'id':'E1','speaker':speaker,'start':0,'end':10,'text':text}];return c
@pytest.mark.parametrize('text,deadline',[('Oddzwonię jutro do godziny 14:00.','jutro do godziny 14:00'),('Prześlę potwierdzenie do końca dnia.','do końca dnia'),('Wyślę instrukcję w ciągu dwóch dni roboczych.','w ciągu dwóch dni roboczych'),('Zgłoszę problem do zespołu.',None)])
def test_deadlines_are_quoted_not_invented(text,deadline):
 p=find_promises(conversation(text))[0]
 assert p['deadline']==deadline and p['status']=='unverified' and p['evidenceId']=='E1'
@pytest.mark.parametrize('text',['Może Pan skontaktować się z działem sprzedaży.','Proszę zadzwonić jutro.','Usługa jest już aktywna.'])
def test_suggestions_are_not_commitments(text):assert find_promises(conversation(text))==[]
def test_customer_statements_do_not_count():assert find_promises(conversation('Oddzwonię jutro.','customer'))==[]
def test_no_cross_conversation_evidence():
 data=fixture();analyze_conversation(data,'CALL-001');c=data['conversations'][0]
 ids={s['id'] for s in c['segments']}
 assert all(p['evidenceId'] in ids for p in c['promises'])
 assert all(r['evidenceId'] in ids for r in c['analysis']['risks'])
 assert c['analysis']['modelVersion']=='deterministic-demo-v1'
 assert c['analysis']['score']==sum(r['points'] for r in c['analysis']['criteria'])
def test_reanalysis_is_idempotent_for_findings():
 data=fixture();analyze_conversation(data,'CALL-001');first=deepcopy(data['conversations'][0]);analyze_conversation(data,'CALL-001')
 assert data['conversations'][0]==first

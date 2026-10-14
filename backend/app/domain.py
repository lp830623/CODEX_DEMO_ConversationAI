import re
MODEL_VERSION = 'deterministic-demo-v1'

def find_promises(conversation):
    """Extract explicit first-person commitments; do not infer deadlines or completion."""
    promises=[]
    pattern=r'\b(oddzwonię|prześlę|wyślę|sprawdzę|zgłoszę|skontaktuję|przekażę)\b'
    deadline=r'(jutro(?: do godziny \d{1,2}:\d{2})?|do końca dnia|w ciągu (?:dwóch|\d+) dni roboczych)'
    for segment in conversation['segments']:
        if segment['speaker']!='agent' or not re.search(pattern, segment['text'], re.I): continue
        match=re.search(deadline,segment['text'],re.I)
        promises.append({'id':f"PROM-{segment['id']}", 'text':segment['text'], 'owner':conversation['agent'], 'deadline':match.group(0) if match else None, 'confidence':0.94 if match else 0.85, 'evidenceId':segment['id'], 'status':'unverified'})
    return promises

def analyze_conversation(data, conversation_id):
    conv=next(c for c in data['conversations'] if c['id']==conversation_id)
    segments=conv['segments']
    agent=[s for s in segments if s['speaker']=='agent']
    customer=[s for s in segments if s['speaker']=='customer']
    greeting=any('dzień dobry' in s['text'].lower() for s in agent)
    empathy=any(re.search(r'rozumiem|przepraszam',s['text'],re.I) for s in agent)
    closing=any('dziękuję' in s['text'].lower() for s in agent)
    promises=find_promises(conv)
    clarity=bool(promises) or any('aktywna' in s['text'].lower() for s in agent)
    criteria=[{'name':'Powitanie','points':20 if greeting else 0,'max':20,'evidenceId':agent[0]['id'] if greeting else None}, {'name':'Empatia','points':25 if empathy else 0,'max':25,'evidenceId':next((s['id'] for s in agent if re.search(r'rozumiem|przepraszam',s['text'],re.I)),None)}, {'name':'Kolejne kroki','points':35 if clarity else 10,'max':35,'evidenceId':promises[0]['evidenceId'] if promises else next((s['id'] for s in agent if 'aktywna' in s['text'].lower()),None)}, {'name':'Zamknięcie','points':20 if closing else 0,'max':20,'evidenceId':agent[-1]['id'] if closing else None}]
    risks=[]
    if conv['sentiment']=='negative': risks.append({'label':'Ryzyko eskalacji','evidenceId':customer[-1]['id'],'text':customer[-1]['text']})
    if any(p['deadline'] is None for p in promises):
        p=next(p for p in promises if p['deadline'] is None)
        risks.append({'label':'Brak terminu działania','evidenceId':p['evidenceId'],'text':p['text']})
    conv['promises']=promises
    conv['analysis']={'modelVersion':MODEL_VERSION,'analyzedAt':data['clock'],'score':sum(c['points'] for c in criteria),'criteria':criteria,'summary':f"Temat: {conv['title']}. Konsultant omówił kolejne kroki. Wynik działań po rozmowie nie jest potwierdzony.", 'risks':risks,'recommendations':['Potwierdź konkretny termin kolejnego kontaktu.' if risks else 'Utrzymaj jasne podsumowanie i potwierdzanie kolejnych kroków.', 'Sprawdź wykonanie deklaracji w zewnętrznym procesie; sama transkrypcja tego nie potwierdza.'], 'sentiment':conv['sentiment'],'evidenceIds':[s['id'] for s in segments]}
    data['audit'].insert(0,{'id':f"AUD-{len(data['audit'])+1}",'at':data['clock'],'action':f'Przeanalizowano {conversation_id} algorytmem {MODEL_VERSION}.','actor':'Analityk DEMO'})

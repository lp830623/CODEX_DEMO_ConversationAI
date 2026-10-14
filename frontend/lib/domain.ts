export type Segment={id:string;speaker:string;start:number;end:number;text:string};
export type PromiseItem={id:string;text:string;owner:string;deadline:string|null;confidence:number;evidenceId:string;status:string};
export type Analysis={modelVersion:string;analyzedAt:string;score:number;criteria:{name:string;points:number;max:number;evidenceId:string|null}[];summary:string;risks:{label:string;evidenceId:string;text:string}[];recommendations:string[];sentiment:string;evidenceIds:string[]};
export type Conversation={id:string;title:string;category:string;agent:string;customer:string;startedAt:string;duration:number;sentiment:string;segments:Segment[];audio:string|null;analysis:Analysis|null;promises:PromiseItem[]};
export type State={schemaVersion:number;mode:string;clock:string;conversations:Conversation[];audit:{id:string;at:string;action:string;actor:string}[]};
export const sentimentLabel:Record<string,string>={negative:'Negatywny',neutral:'Neutralny',positive:'Pozytywny'};
export function findPromises(c:Conversation):PromiseItem[]{
 // TODO: match backend semantics and make the exercise tests pass.
 return [];
}
export function analyze(c:Conversation,clock:string){
 const agent=c.segments.filter(s=>s.speaker==='agent'),customer=c.segments.filter(s=>s.speaker==='customer');
 const greeting=agent.some(s=>s.text.toLowerCase().includes('dzień dobry')),empathy=agent.some(s=>/rozumiem|przepraszam/i.test(s.text)),closing=agent.some(s=>s.text.toLowerCase().includes('dziękuję'));
 const promises=findPromises(c),clarity=promises.length>0||agent.some(s=>s.text.toLowerCase().includes('aktywna'));
 const criteria=[{name:'Powitanie',points:greeting?20:0,max:20,evidenceId:greeting?agent[0].id:null},{name:'Empatia',points:empathy?25:0,max:25,evidenceId:agent.find(s=>/rozumiem|przepraszam/i.test(s.text))?.id||null},{name:'Kolejne kroki',points:clarity?35:10,max:35,evidenceId:promises[0]?.evidenceId||agent.find(s=>s.text.includes('aktywna'))?.id||null},{name:'Zamknięcie',points:closing?20:0,max:20,evidenceId:closing?agent.at(-1)!.id:null}];
 const risks:Analysis['risks']=[];if(c.sentiment==='negative'){const s=customer.at(-1)!;risks.push({label:'Ryzyko eskalacji',evidenceId:s.id,text:s.text});}
 const noDeadline=promises.find(p=>!p.deadline);if(noDeadline)risks.push({label:'Brak terminu działania',evidenceId:noDeadline.evidenceId,text:noDeadline.text});
 c.promises=promises;c.analysis={modelVersion:'deterministic-demo-v1',analyzedAt:clock,score:criteria.reduce((s,c)=>s+c.points,0),criteria,summary:`Temat: ${c.title}. Konsultant omówił kolejne kroki. Wynik działań po rozmowie nie jest potwierdzony.`,risks,recommendations:[risks.length?'Potwierdź konkretny termin kolejnego kontaktu.':'Utrzymaj jasne podsumowanie i potwierdzanie kolejnych kroków.','Sprawdź wykonanie deklaracji w zewnętrznym procesie; sama transkrypcja tego nie potwierdza.'],sentiment:c.sentiment,evidenceIds:c.segments.map(s=>s.id)};
}
export function reduce(s:State,path:string){const id=path.split('/')[3];const c=s.conversations.find(c=>c.id===id);if(!c)throw new Error('Nie znaleziono rozmowy.');analyze(c,s.clock);s.audit.unshift({id:`AUD-${s.audit.length+1}`,at:s.clock,action:`Przeanalizowano ${id} algorytmem deterministic-demo-v1.`,actor:'Analityk DEMO'});}

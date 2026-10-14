import test from 'node:test';import assert from 'node:assert/strict';
import {analyze,findPromises,Conversation,State,reduce} from '../lib/domain';
import seed from '../../datasets/synthetic/seed.json';
const conversation=(text:string,speaker='agent'):Conversation=>({...structuredClone(seed.conversations[0]),segments:[{id:'E1',text,speaker,start:0,end:10}]} as unknown as Conversation);
test('keeps deadline wording and unverified status',()=>{const p=findPromises(conversation('Oddzwonię jutro do godziny 14:00.'))[0];assert.equal(p.deadline,'jutro do godziny 14:00');assert.equal(p.status,'unverified');assert.equal(p.evidenceId,'E1');});
test('does not invent a missing deadline',()=>assert.equal(findPromises(conversation('Zgłoszę problem do zespołu.'))[0].deadline,null));
test('suggestions and customer statements are not agent commitments',()=>{assert.deepEqual(findPromises(conversation('Może Pan skontaktować się z działem sprzedaży.')),[]);assert.deepEqual(findPromises(conversation('Oddzwonię jutro.','customer')),[]);});
test('browser analysis equals seeded Python analysis',()=>{for(const original of seed.conversations.slice(0,20)){const c=structuredClone(original) as unknown as Conversation;analyze(c,seed.clock);assert.deepEqual(c.analysis,original.analysis);assert.deepEqual(c.promises,original.promises);}});
test('analysis is scoped to conversation and evidence',()=>{const s=structuredClone(seed) as unknown as State;reduce(s,'/api/conversations/CALL-021/analyze');const c=s.conversations[20];assert.ok(c.analysis);assert.equal(s.conversations[21].analysis,null);assert.ok(c.analysis.evidenceIds.every(id=>c.segments.some(s=>s.id===id)));});

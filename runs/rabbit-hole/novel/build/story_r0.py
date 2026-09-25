import json, sys
sys.path.insert(0, 'build')
from mm import *

comp = json.load(open('results/compile-story-r0.json'))['model']
m = comp
mm = m['meaning_model']
ev, rels = mm['events'], mm['event_relations']

ev += [
 event('event.world', 'The accepted world of the novel: our real world as documented up to the opening stage\'s cutoff, with invented people and companies in the foreground and real events, technology, prices and laws in the background.'),
 event('event.deep.foragers', 'Homo sapiens as mobile foragers, from about 300,000 to about 12,000 years before the present.',
       'For almost the whole history of the species people lived in bands of a few dozen inside a network of perhaps a hundred and fifty known faces. Trust ran on kinship, reputation and repeated meeting; wealth was what you could carry; a stranger was rare and a threat or a gift. The emotions the protagonist carries (fear of exclusion, hunger for status, the pull of the group, alarm at sudden loss, delight in discovery) were tuned for this world.',
       iv(-298000, -10000)),
 event('event.deep.agriculture', 'Cultivation and its consequences, from about 12,000 years ago.',
       'Farming produced surplus, storage, property, hierarchy, writing, money and debt. Time became the calendar of the harvest: the same work in the same field every season. Institutions grew to manage strangers who had to trust each other: temples, granaries, ledgers, kings, courts, and much later banks with double-entry books.',
       iv(-10000, 2026)),
 event('event.deep.old_institutions', 'The slow institutions inherited from agrarian and early modern states: the bank, the ledger, the court, the nation state, the working week.',
       'These are the medieval institutions of E. O. Wilson\'s phrase: they change on the scale of generations, settle disputes through intermediaries, open at nine and close at five, and remember everything in someone else\'s book.',
       iv(1400, 2026)),
 event('event.deep.global_order', 'The global institutional order built mostly after 1944: a world of international money, treaties, clearing systems and multinational banks.',
       'The global institutions people live inside took shape within roughly the last fifty to eighty years: post-war monetary agreements, the international lenders, card networks, interbank messaging, the floating dollar after 1971. They are younger than many living grandparents, and most people who depend on them have never seen how they work.',
       iv(1944, 2026)),
 event('event.deep.digital', 'The networked and then pocketed computer, from the public internet of the 1990s to the smartphone and its feeds.',
       'Information, then attention, then money began to move at the speed of software. A phone in every pocket connected a forager\'s mind to millions of strangers at once.',
       iv(1991, 2026)),
 event('event.deep.crypto', 'Programmable money: from the 2008 crisis and the first cryptocurrency to smart contracts, decentralized finance and the booms and crashes of 2017 to 2022.',
       'A ledger nobody owns, that never closes, where code replaces the clerk. It promised to route around the old institutions and instead reproduced most of their temptations at machine speed, in public, around the clock.',
       iv(2008.8, 2026)),
]
for e in ['event.deep.foragers','event.deep.agriculture','event.deep.old_institutions','event.deep.global_order','event.deep.digital','event.deep.crypto','event.profile.protagonist.person.protagonist.life']:
    rels.append(rel(f'world.contains.{e.split("event.")[1]}', 'contains', 'event.world', e, 'Accepted-world containment.'))
rels += [
 rel('foragers.precedes.agriculture', 'other', 'event.deep.foragers', 'event.deep.agriculture', 'Precedes: the agricultural transition follows the long forager era and inherits its minds.'),
 rel('agriculture.enables.old_institutions', 'enables', 'event.deep.agriculture', 'event.deep.old_institutions', 'Surplus, property and writing make ledgers, banks and courts possible.'),
 rel('old_institutions.enables.global_order', 'enables', 'event.deep.old_institutions', 'event.deep.global_order', 'The post-war order is built from inherited institutions scaled to the world.'),
 rel('global_order.enables.crypto', 'enables', 'event.deep.global_order', 'event.deep.crypto', 'The 2008 crisis in the global banking order is the stated occasion of the first cryptocurrency.'),
 rel('digital.enables.crypto', 'enables', 'event.deep.digital', 'event.deep.crypto', 'Networked computing is the substrate of programmable money.'),
]
mm['context_roots'] = [{'event_id': 'event.world', 'kind': 'accepted_world', 'provenance': PROV}]
m['revision']['reason'] = comp['revision']['reason']
dump({'requestId': 'register-story-r0', 'model': m}, 'inputs/register-story-r0.json')
print('events', len(ev), 'relations', len(rels))

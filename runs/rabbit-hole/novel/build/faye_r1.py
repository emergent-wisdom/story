import json, sys
sys.path.insert(0, 'build')
import mm as M
from mm import *
P = ["rabbit-hole-run; invented author persona, authored by the calling LLM under delegation"]
M.PROV[:] = P
m = json.load(open('results/compile-faye-r1.json'))['model']
mm = m['meaning_model']; ev = mm['events']; rels = mm['event_relations']
for k in ('concepts','abstract_cuts','abstract_relations','encapsulation_cuts','physical_cuts','realizations','normalized_cuts'): mm.setdefault(k, [])
cuts, concepts, arels, reals = mm['normalized_cuts'], mm['concepts'], mm['abstract_relations'], mm['realizations']
R = 'referent.profile.faye.person.faye'; LIFE = 'event.profile.faye.person.faye.life'
SWI, AVE, UNI, OFF = 'Swindon, Wiltshire, England', 'Avebury and the Marlborough Downs, Wiltshire', 'A university town on the English south coast', 'The building society payments office, west Swindon'
E = {e['id']: e for e in ev}
E[LIFE]['interval'] = iv(1979.2, 2026.75)
E[LIFE]['description'] = 'Invented life of Faye Titcombe from her birth in Swindon in March 1979 to September 2026, when she is finishing this novel. Her life runs between two kinds of time: the deep time of the Wiltshire downs she studied and the batch cycles of the payments office where she worked.'
E[LIFE]['region'] = SWI
arcreg = {'works_closure': SWI, 'leaving_doctorate': UNI, 'collapse_2022': 'Faye\'s kitchen table and phone, north Swindon', 'redundancy_and_stones': AVE}
for e in ev:
    if e['id'].startswith('event.profile.') and '.change_arc' in e['id']:
        e.setdefault('description', e['boundary'])
        e['region'] = arcreg[e['id'].split('.')[2]]
        if e['id'].endswith('.change_arc'):
            rels.append(rel(f'life.contains.{e["id"]}', 'contains', LIFE, e['id'], 'Change arc inside the life.'))
# roots
ev.append(event('ev.faye.world', 'Faye Titcombe\'s reality: our world from 1979 to 2026, the same world the novel is set in.', 'The author lives in the novel\'s world: England, the Wiltshire downs, the payments system, the crypto markets of 2020-2022.', iv(-3800, 2026.75)))
ev.append(event('ev.faye.inner', 'Faye\'s inner perspective root: her wants, beliefs and appraisals are attributed here, never accepted as world fact.', None, None, {'subject': R}))
rels.append(rel('world.contains.life', 'contains', 'ev.faye.world', LIFE, 'The life inside the author\'s reality.'))
rels.append(rel('world.contains.inner', 'contains', 'ev.faye.world', 'ev.faye.inner', 'Inner root nested in the accepted world.'))
mm['context_roots'] = [{'event_id': 'ev.faye.world', 'kind': 'accepted_world', 'provenance': P}, {'event_id': 'ev.faye.inner', 'kind': 'inner', 'provenance': P}]
# long developments enclosing her life
macro = [
 ('ev.macro.works', 'The Great Western railway works at Swindon, from the 1840s to their closure in 1986.', 'For about a hundred and forty years the works made Swindon: the town grew around the sheds, the hooter set the day, and families like the Titcombes had sons there for three generations. Its closure ended the town\'s oldest routine.', iv(1843, 1986.3), SWI),
 ('ev.macro.clearing', 'Automated interbank clearing in Britain from the late 1960s: overnight batch files and a three-working-day cycle.', 'The payments infrastructure Faye worked inside was designed for magnetic tape and still ran on its rhythm: submit on day one, process on day two, settle on day three, nothing at weekends.', iv(1968, 2026.75), 'Britain'),
 ('ev.macro.downs', 'The monument landscape of the Marlborough Downs, from the first Neolithic gathering enclosures to the stone circle and the chalk figures kept by scouring.', 'About 3700 BC herders began meeting at ditched hilltop enclosures such as Windmill Hill; later came the great henge and stone circle at Avebury and the long barrows. The chalk horses of the region fade unless people keep scouring them.', iv(-3700, 2026.75), AVE),
 ('ev.macro.defi', 'Cryptocurrency and decentralized finance, from 2008 to the collapses of 2022.', 'Programmable money that never closes: the markets Faye entered in 2020 ran every hour of every day, at machine speed, in public.', iv(2008.8, 2026.75), 'Online, worldwide'),
]
for eid, b, d, i, reg in macro:
    ev.append(event(eid, b, d, i, region=reg))
    rels.append(rel(f'world.contains.{eid}', 'contains', 'ev.faye.world', eid, 'A long development enclosing the life.'))
# periods
def per(pid, label, a, b, desc, reg):
    ev.append(event(pid, label, desc, iv(a, b), {'subject': R}, region=reg))
    rels.append(rel(f'life.contains.{pid}', 'contains', LIFE, pid, 'Period of the life.'))
per('ev.faye.p1.childhood', 'Childhood in a railway-works family in north Swindon, 1979-1990.', 1979.2, 1990.7,
    'Faye grows up in a terraced house in north Swindon. Her father has worked in the railway works since he was sixteen; the works hooter, the shift and the Friday pay packet are the calendar of the house. Her mother is a school dinner lady. On Sundays they walk on the downs, where her father shows her the chalk horse and says it has been kept white for three thousand years by people scouring it.', SWI)
per('ev.faye.p1b.school', 'Secondary school and the sixth form, 1990-1997.', 1990.7, 1997.7,
    'A clever, watchful teenager who reads archaeology books from the town library and works Saturdays at a supermarket checkout. Her father drinks more; her mother holds the house together. A history teacher takes her class to Avebury and she stays behind in the rain to count the stones.', SWI)
per('ev.faye.p2.study', 'Archaeology, then a doctorate on Neolithic gathering enclosures, 1997-2004.', 1997.7, 2004.4,
    'First in her family at university. She falls for deep time: the forager hundreds of thousands of years, then the first farmers who met at ditched hilltop enclosures to feast, trade and bury. Her doctorate asks why scattered herders began gathering in one place at set seasons: the beginning of institutions.', UNI)
per('ev.faye.p3.ledger', 'Eighteen years in a building society payments operations team, 2004-2022.', 2004.4, 2022.9,
    'She learns the batch: payment files that run overnight, exceptions that must be cleared before the cut-off, a three-day cycle designed in the 1960s. She becomes the person who knows why a payment failed. She meets her partner, a secondary-school geography teacher, in 2008; their daughter is born in 2011.', OFF)
per('ev.faye.p4.rabbit_hole', 'The decentralized-finance rabbit hole, 2020-2022.', 2020.25, 2022.6,
    'Working from home in the 2020 lockdown, she follows a younger colleague into decentralized finance. She understands the mechanisms quickly and loves it: money as open code, a ledger anyone can read. She moves most of the family savings in, grows them, joins a chat server where people talk through the night, and holds through the spring 2022 collapse.', 'Faye\'s spare room in north Swindon, and online')
per('ev.faye.p5.after', 'After: separation, the stones and the novel, 2022-2026.', 2022.6, 2026.75,
    'She confesses the loss in summer 2022; she and her partner separate in 2023 and share the care of their daughter. After redundancy she becomes a seasonal guide at the Avebury stones and writes fiction in the evenings, finishing this novel in 2026 when her daughter is fifteen and has a trading app on her phone.', AVE)
rels += [
 rel('works.enables.childhood', 'enables', 'ev.macro.works', 'ev.faye.p1.childhood', 'The works set the routine of the house.'),
 rel('works.causes.closure_arc', 'causes', 'ev.macro.works', 'event.profile.works_closure.change_arc', 'The end of the works is the end of the development.'),
 rel('downs.enables.study', 'enables', 'ev.macro.downs', 'ev.faye.p2.study', 'The landscape of her childhood walks becomes her subject.'),
 rel('clearing.enables.ledger', 'enables', 'ev.macro.clearing', 'ev.faye.p3.ledger', 'The clearing cycle is the routine of her working life.'),
 rel('defi.enables.rabbit_hole', 'enables', 'ev.macro.defi', 'ev.faye.p4.rabbit_hole', 'The new markets are there to fall into.'),
 rel('closure.enables.ledger_skill', 'enables', 'event.profile.works_closure.change_arc.adaptation', 'ev.faye.p3.ledger', 'The want to know how systems work, learned in 1986, makes her good at the ledger and over-trusting of understanding.'),
 rel('collapse.causes.redundancy_turn', 'other', 'event.profile.collapse_2022.change_arc', 'event.profile.redundancy_and_stones.change_arc', 'Coincides with and colours: she meets redundancy already ashamed, which makes the stones a refuge rather than a defeat.'),
]
# wants as inner Events
wants = [
 ('ev.faye.want.safe', 'Deepest want: to be safe, to have a floor under the house that nobody else can pull away.', 1979.2, 2026.75),
 ('ev.faye.want.known', 'Deepest want: to be known by her people for what she actually sees.', 1979.2, 2026.75),
 ('ev.faye.want.understand', 'Deepest want: to understand how things came to be; for Faye understanding is the form freedom takes.', 1986.3, 2026.75),
 ('ev.faye.want.daughter', 'Deepest want from 2011: that her daughter can trust her and will not be hurt by what hurt her.', 2011.3, 2026.75),
 ('ev.faye.want.mechanism', 'Learned want after 1986: to know the mechanism of any system she depends on, so it cannot close on her without warning. It became a proxy: she came to believe that understanding a mechanism protects her from its pull on her feelings.', 1986.3, 2026.75),
 ('ev.faye.want.useful', 'Learned want after 2004: to be the reliable one who knows why a payment failed, as a way to belong.', 2004.4, 2023.4),
 ('ev.faye.want.band', 'Learned want in 2020-2022: to belong to the band of those who know, the people awake at three in the morning in the chat server.', 2020.4, 2022.6),
]
for wid, d, a, b in wants:
    ev.append(event(wid, d, d, iv(a, b), {'subject': R}))
    rels.append(rel(f'inner.contains.{wid}', 'contains', 'ev.faye.inner', wid, 'Want attributed to Faye.'))
# composition and the open decision
ev.append(event('ev.faye.composition', 'Writing this novel, autumn 2025 to autumn 2026.',
    'Faye writes in the evenings after guiding at the stones, at the kitchen table in north Swindon. She is four years from her own fall and far enough to laugh at parts of it.',
    iv(2025.7, 2026.75), {'subject': R}, region='Faye\'s kitchen table, north Swindon'))
rels.append(rel('p5.contains.composition', 'contains', 'ev.faye.p5.after', 'ev.faye.composition', 'The composition moment inside the last period.'))
rels.append(rel('collapse.causes.composition', 'causes', 'event.profile.collapse_2022.change_arc.adaptation', 'ev.faye.composition', 'The unfinished adaptation to 2022 is one cause of the book.'))
ev.append(event('ev.faye.daughter_app', 'September 2025: Faye finds a trading app on her fifteen-year-old daughter\'s phone.',
    'At the kitchen table her daughter shows her, half proud and half defiant, a small balance in a coin that a video told her about. Faye recognises the feeling in her own chest before she recognises the coin. She has to choose what to do.',
    iv(2025.65, 2025.7), {'subject': R}, region='Faye\'s kitchen table, north Swindon'))
rels.append(rel('p5.contains.daughter_app', 'contains', 'ev.faye.p5.after', 'ev.faye.daughter_app', 'A moment of the last period.'))
rels.append(rel('daughter_app.causes.composition', 'causes', 'ev.faye.daughter_app', 'ev.faye.composition', 'Whatever she chooses, this evening is when the novel starts.'))
# Cuts
def outlook(pid, q, assur, threat):
    cuts.append(cut(f'cut.faye.{pid.split(".")[-2]}.{pid.split(".")[-1]}.outlook', pid, q, 'share of one unit of represented outlook toward fulfilment of her active wants',
        [('assurance', assur), ('threat', threat), ('remainder', round(1-assur-threat, 6))]))
def threatened(pid, q, ans):
    cuts.append(cut(f'cut.faye.{pid.split(".")[-2]}.{pid.split(".")[-1]}.threatened', pid, q, 'share of what she sees as threatened in this period', ans))
outlook('ev.faye.p1.childhood', 'Across her childhood, how does Faye expect what she wants to turn out?', 0.62, 0.28)
threatened('ev.faye.p1.childhood', 'What does Faye see as threatened during her childhood?', [('the_house_and_its_routine', 0.5), ('her_father', 0.3), ('remainder', 0.2)])
outlook('ev.faye.p1b.school', 'In her school years, how does Faye expect what she wants to turn out?', 0.55, 0.35)
threatened('ev.faye.p1b.school', 'What does Faye see as threatened in her school years?', [('her_mother_holding_the_house', 0.4), ('her_chance_to_leave', 0.4), ('remainder', 0.2)])
outlook('ev.faye.p2.study', 'At university, how does Faye expect what she wants to turn out?', 0.7, 0.2)
threatened('ev.faye.p2.study', 'What does Faye see as threatened at university?', [('money_and_debt', 0.45), ('her_mother_at_home', 0.35), ('remainder', 0.2)])
outlook('ev.faye.p3.ledger', 'In the payments years, how does Faye expect what she wants to turn out?', 0.6, 0.25)
threatened('ev.faye.p3.ledger', 'What does Faye see as threatened in the payments years?', [('the_unfinished_life_she_meant_to_have', 0.45), ('the_family_s_security', 0.35), ('remainder', 0.2)])
outlook('ev.faye.p4.rabbit_hole', 'In the rabbit hole, how does Faye expect what she wants to turn out?', 0.66, 0.26)
threatened('ev.faye.p4.rabbit_hole', 'What does Faye see as threatened in the rabbit hole?', [('being_left_behind', 0.4), ('the_family_savings', 0.35), ('remainder', 0.25)])
outlook('ev.faye.p5.after', 'After the fall, how does Faye expect what she wants to turn out?', 0.48, 0.4)
threatened('ev.faye.p5.after', 'What does Faye see as threatened after the fall?', [('her_daughter_falling_the_same_way', 0.5), ('her_self_respect', 0.3), ('remainder', 0.2)])
MA = 'share of motivational attention over her wants'
cuts += [
 cut('cut.faye.1986.safety', 'event.profile.works_closure.change_arc.adaptation', 'After the works close, where does seven-year-old Faye come to locate safety?', 'share of her sense of safety',
     [('in_knowing_how_things_work', 0.45), ('in_her_mother', 0.30), ('in_the_routine', 0.10), ('remainder', 0.15)]),
 cut('cut.faye.2004.reasons', 'event.profile.leaving_doctorate.change_arc.focal_change', 'What moves Faye to leave the doctorate: love or fear?', 'share of the motive',
     [('love_care_for_mother', 0.55), ('fear_debt_and_insecurity', 0.35), ('remainder', 0.10)]),
 cut('cut.faye.2021.pull', 'ev.faye.p4.rabbit_hole', 'Over her wants, where does Faye\'s motivational attention go as she moves deeper into decentralized finance in 2021?', MA,
     [('understand', 0.35), ('band', 0.30), ('safe', 0.10), ('known', 0.10), ('mechanism', 0.10), ('remainder', 0.05)]),
 cut('cut.faye.2022.holding', 'event.profile.collapse_2022.change_arc.focal_change', 'Why does Faye hold as the peg breaks?', 'share of the reason',
     [('trust_in_her_own_understanding', 0.35), ('loyalty_to_the_group', 0.30), ('shame_of_selling_at_a_loss', 0.20), ('remainder', 0.15)]),
 cut('cut.faye.2026.why_write', 'ev.faye.composition', 'Over her wants, where does Faye\'s motivational attention go as she writes this novel?', MA,
     [('understand', 0.35), ('daughter', 0.30), ('known', 0.15), ('safe', 0.05), ('remainder', 0.15)]),
 cut('cut.faye.2025.daughter_app.response', 'ev.faye.daughter_app', 'What does Faye do when her daughter shows her the trading app?', 'proposal weight over mutually exclusive continuations',
     [('forbid_it', 0.20), ('learn_it_beside_her', 0.35), ('say_little_and_write', 0.30), ('remainder', 0.15)], 'authored proposal weights fixed before the draw; seed fixed in advance'),
]
# concepts and their realizations
C = lambda cid, label, boundary, diff: {'id': cid, 'label': label, 'boundary': boundary, 'differentia': [diff], 'provenance': P}
concepts += [
 C('concept.routine_as_safety', 'Routine as safety', 'A life made safe by a repeating schedule owned by an institution.', 'The safety is real but belongs to whoever can end the routine.'),
 C('concept.understanding_as_protection', 'Understanding as protection', 'The belief that knowing how a system works protects you from what it does to you.', 'A proxy strategy: it protects against surprise, not against one\'s own feelings.'),
 C('concept.the_band', 'The band', 'A small group of known faces that shares food, attention and danger and punishes defection.', 'The forager unit of belonging, reproduced by offices, chat servers and crowds.'),
 C('concept.gathering_institution', 'Institution as gathering', 'An institution that begins as people meeting at a place at set times and hardens into rules.', 'Causewayed enclosures, the works hooter, the clearing cycle and the chat server are all gatherings with a clock.'),
 C('concept.deep_time_gap', 'The deep-time gap', 'Paleolithic emotions, medieval institutions and godlike technology running at once in one person.', 'Three clocks: the body\'s, the institution\'s and the machine\'s.'),
]
arels += [
 {'id': 'arel.understanding.specializes.safety', 'source_concept_id': 'concept.understanding_as_protection', 'target_concept_id': 'concept.routine_as_safety', 'kind': 'other', 'label': 'replaces: the child who lost routine as safety put understanding in its place', 'provenance': P},
 {'id': 'arel.band.analogy.gathering', 'source_concept_id': 'concept.the_band', 'target_concept_id': 'concept.gathering_institution', 'kind': 'analogy', 'provenance': P},
 {'id': 'arel.gap.constrains.understanding', 'source_concept_id': 'concept.deep_time_gap', 'target_concept_id': 'concept.understanding_as_protection', 'kind': 'constrains', 'provenance': P},
]
def real(rid, cid, eid, deg):
    reals.append({'id': rid, 'concept_id': cid, 'purpose': 'describe', 'roles': {'instance': eid}, 'degree': deg, 'uncertainty': UNK, 'viewpoint': 'author persona (Faye) as modeled by the recorder', 'authority': None, 'provenance': P})
real('real.works.routine', 'concept.routine_as_safety', 'ev.macro.works', 0.9)
real('real.closure.understanding', 'concept.understanding_as_protection', 'event.profile.works_closure.change_arc.adaptation', 0.8)
real('real.collapse.understanding_fails', 'concept.understanding_as_protection', 'event.profile.collapse_2022.change_arc.focal_change', 0.85)
real('real.rabbit_hole.band', 'concept.the_band', 'ev.faye.p4.rabbit_hole', 0.8)
real('real.ledger.band', 'concept.the_band', 'ev.faye.p3.ledger', 0.6)
real('real.downs.gathering', 'concept.gathering_institution', 'ev.macro.downs', 0.9)
real('real.clearing.gathering', 'concept.gathering_institution', 'ev.macro.clearing', 0.6)
real('real.collapse.gap', 'concept.deep_time_gap', 'event.profile.collapse_2022.change_arc', 0.85)
m['revision'] = {'number': 1, 'previous_model_hash': 'cb24467c43d301aa8d9ab8f83b8c208ef23439f31151785067f591a51c960a6e', 'provenance': P,
                 'reason': 'Revision 1: shocks rebuilt as change arcs (adding the 2023 redundancy), wants as inner Events under an inner root, places, the long developments enclosing the life, a school period, outlook and threat Cuts per period, motivational-attention Cuts, concepts with realizations, and one open decision (the daughter\'s trading app) for a seeded draw.'}
dump({'requestId': 'revise-faye-r1', 'previousModelHash': 'cb24467c43d301aa8d9ab8f83b8c208ef23439f31151785067f591a51c960a6e', 'model': m, 'requireDescribedNumbers': True}, 'inputs/revise-faye-r1.json')
print(len(ev), len(rels), len(cuts), len(concepts), len(reals))

import json, sys
sys.path.insert(0, 'build')
from mm import *
P = ["rabbit-hole-run; invented author persona, authored by the calling LLM under delegation"]
import mm as M; M.PROV[:] = P
m = json.load(open('results/compile-faye.json'))['model']
mm = m['meaning_model']; ev = mm['events']; rels = mm['event_relations']; cuts = mm.setdefault('normalized_cuts', [])
for k in ('concepts','abstract_cuts','abstract_relations','encapsulation_cuts','physical_cuts','realizations'): mm.setdefault(k, [])
ev.append(event('ev.faye.world', 'Faye Titcombe\'s reality: our world from 1979 to 2026, the same world the novel is set in.', 'The author lives in the novel\'s world: England, the Wiltshire downs, the payments system, the crypto markets of 2020-2022.', iv(1979.2, 2026.75)))
rels.append(rel('world.contains.life', 'contains', 'ev.faye.world', 'event.profile.faye.person.faye.life', 'The life inside the author\'s reality.'))
mm['context_roots'] = [{'event_id': 'ev.faye.world', 'kind': 'accepted_world', 'provenance': P}]
R = 'referent.profile.faye.person.faye'; LIFE = 'event.profile.faye.person.faye.life'
for e in ev:
    if e['id'] == LIFE:
        e['interval'] = iv(1979.2, 2026.75)
        e['description'] = 'Invented life of Faye Titcombe from her birth in Swindon in March 1979 to September 2026, when she is finishing this novel. Her life runs between two kinds of time: the deep time of the Wiltshire downs she studied and the batch cycles of the payments office where she worked.'
def per(pid, label, a, b, desc):
    ev.append(event(pid, label, desc, iv(a, b), {'subject': R}))
    rels.append(rel(f'life.contains.{pid}', 'contains', LIFE, pid, 'Period of the life.'))
per('ev.faye.p1.childhood', 'Childhood in a railway-works family on a Swindon estate, 1979-1990.', 1979.2, 1990.7,
    'Faye grows up in a terraced house in north Swindon. Her father has worked in the Great Western railway works since he was sixteen; the works hooter, the shift and the Friday pay packet are the calendar of the house. Her mother is a school dinner lady. Sundays they walk on the downs, where her father shows her the chalk horse and says it has been kept white for three thousand years by people scouring it.')
per('ev.faye.p2.study', 'Archaeology, then a doctorate on Neolithic causewayed enclosures, 1997-2004.', 1997.7, 2004.4,
    'First in her family at university, on the south coast. She falls for deep time: the forager hundreds of thousands of years, then the first farmers who met at ditched hilltop enclosures like Windmill Hill above Avebury to feast, trade and bury. Her doctorate asks why scattered herders began gathering in one place at set seasons: the beginning of institutions.')
per('ev.faye.p3.ledger', 'Eighteen years in a building society payments operations team in Swindon, 2004-2022.', 2004.4, 2022.9,
    'She takes the job to pay her debts and to be near her mother. She learns the batch: payments files that run overnight, exceptions that must be cleared before the cut-off, three-day clearing cycles designed in the 1960s. She is good at it and becomes the person who knows why a payment failed. She meets her partner, a secondary-school geography teacher, in 2008; their daughter is born in 2011.')
per('ev.faye.p4.rabbit_hole', 'The decentralized-finance rabbit hole, 2020-2022.', 2020.25, 2022.6,
    'Working from home in the 2020 lockdown, she follows a younger colleague into decentralized finance. She understands the mechanisms quickly and loves it: money as open code, a ledger you can read. She moves most of the family savings in, grows them, joins a chat server where people talk through the night, and holds through the spring 2022 collapse because she understands the mechanism and because the group holds.')
per('ev.faye.p5.after', 'After: separation, redundancy, the stones and the novel, 2022-2026.', 2022.6, 2026.75,
    'She confesses the loss in summer 2022; she and her partner separate in 2023, sharing the care of their daughter. Her payments team is automated away the same year. She becomes a seasonal guide at the Avebury stones and begins writing fiction in the evenings, finishing this novel in 2026 when her daughter is fifteen and has a trading app on her phone.')
# shocks with anticipation, focal change and adaptation
def arc(key, label, anticip, focal, adapt, parent, desc_a, desc_f, desc_d):
    a, f, d = f'ev.faye.{key}.anticipation', f'ev.faye.{key}.focal', f'ev.faye.{key}.adaptation'
    ev.append(event(a, f'{label}: anticipation', desc_a, iv(*anticip), {'subject': R}))
    ev.append(event(f, f'{label}: focal change', desc_f, iv(*focal), {'subject': R}))
    ev.append(event(d, f'{label}: adaptation', desc_d, iv(*adapt), {'subject': R}))
    for x in (a, f):
        rels.append(rel(f'{parent}.contains.{x}', 'contains', parent, x, 'Change arc inside its period.'))
    dpar = parent if adapt[1] <= {'ev.faye.p1.childhood': 1990.7, 'ev.faye.p2.study': 2004.4, 'ev.faye.p4.rabbit_hole': 2022.6}[parent] else LIFE
    rels.append(rel(f'{dpar}.contains.{d}', 'contains', dpar, d, 'Adaptation inside the period, or inside the life when it outlasts the period.'))
    rels.append(rel(f'{a}.enables.{f}', 'enables', a, f, 'What was expected or feared shapes the response to the change.'))
    rels.append(rel(f'{f}.causes.{d}', 'causes', f, d, 'The change sets off the adaptation.'))
    return a, f, d
arc('works_closure', 'The railway works close', (1985.0, 1986.2), (1986.2, 1986.3), (1986.3, 1990.7), 'ev.faye.p1.childhood',
    'Talk at the kitchen table about the works running down; her father says they will never close a place that big.',
    'The works close in 1986 after about a hundred and forty years. Her father, forty-four, loses the only job he has had. Faye is seven.',
    'Her father drives a taxi, then parcels, and stops walking on the downs. Faye learns that the routine that made the house safe was someone else\'s to end, and she starts wanting to know how things work, so nothing can close on her without warning.')
arc('leaving_doctorate', 'Leaving the doctorate', (2003.5, 2004.2), (2004.2, 2004.4), (2004.4, 2008.0), 'ev.faye.p2.study',
    'Her mother\'s illness worsens and the student debt grows; the funding for the final year is not renewed.',
    'She leaves the doctorate unfinished, moves back to Swindon and takes a job clearing payment exceptions.',
    'She tells herself it is temporary. The ledger becomes her new field site: she watches colleagues as a band, the tea round as food sharing, the appraisal as a status ritual, and keeps notes she never writes up.')
arc('collapse_2022', 'The spring 2022 collapse', (2022.2, 2022.35), (2022.35, 2022.4), (2022.4, 2023.8), 'ev.faye.p4.rabbit_hole',
    'She reads the stablecoin\'s design and knows its weak point in theory; the chat server says the peg has always come back.',
    'In May 2022 an algorithmic stablecoin loses its peg and its sister token collapses within days. Faye loses about two thirds of the family savings she had moved in.',
    'She hides it for two months, then tells her partner. The shame is less about the money than about having known the mechanism and held anyway. The partnership does not survive it; she keeps her daughter\'s trust by telling her the truth when she is old enough.')
# composition moment
ev.append(event('ev.faye.composition', 'Writing this novel, autumn 2025 to autumn 2026.',
    'Faye writes in the evenings after guiding at the stones. Her daughter, fifteen, has started trading on an app. Faye is four years from her own fall and far enough to laugh at parts of it.',
    iv(2025.7, 2026.75), {'subject': R}))
rels.append(rel('p5.contains.composition', 'contains', 'ev.faye.p5.after', 'ev.faye.composition', 'The composition moment inside the last period.'))
rels.append(rel('collapse.causes.composition', 'causes', 'ev.faye.collapse_2022.adaptation', 'ev.faye.composition', 'The unfinished adaptation to 2022 is one cause of the book.'))
rels.append(rel('closure.enables.ledger', 'enables', 'ev.faye.works_closure.adaptation', 'ev.faye.p3.ledger', 'The want to know how systems work, learned in 1986, makes her good at the ledger and over-trusting of understanding.'))
# wants
ev.append(event('ev.faye.wants.deep', 'Faye\'s deepest wants across the life.',
    'To be safe; to be known by her people; to understand, which for her is the form freedom takes; to matter to her daughter.',
    iv(1979.2, 2026.75), {'subject': R}))
ev.append(event('ev.faye.wants.learned', 'The wants her life taught her as ways to get them.',
    'After 1986: knowing how a system works as protection against it. After 2004: being useful and reliable as a way to belong. In 2020-2022: belonging to the band of those who know. The first became a proxy that displaced the aim it served: she began to believe that understanding a mechanism protected her from its pull on her feelings.',
    iv(1986.3, 2026.75), {'subject': R}))
for x in ('ev.faye.wants.deep', 'ev.faye.wants.learned'):
    rels.append(rel(f'life.contains.{x}', 'contains', LIFE, x, 'Wants run through the whole life.'))
# Cuts at the moments that matter
cuts += [
 cut('cut.faye.1986.safety', 'ev.faye.works_closure.adaptation', 'After the works close, where does seven-year-old Faye come to locate safety?', 'share of her sense of safety',
     [('in_knowing_how_things_work', 0.45), ('in_her_mother', 0.30), ('in_the_routine', 0.10), ('remainder', 0.15)]),
 cut('cut.faye.2004.reasons', 'ev.faye.leaving_doctorate.focal', 'What moves Faye to leave the doctorate: love or fear?', 'share of the motive',
     [('love_care_for_mother', 0.55), ('fear_debt_and_insecurity', 0.35), ('remainder', 0.10)]),
 cut('cut.faye.2021.pull', 'ev.faye.p4.rabbit_hole', 'What pulls Faye deeper into decentralized finance during 2021?', 'share of the pull',
     [('curiosity_and_understanding', 0.35), ('belonging_to_those_who_know', 0.30), ('status_and_gain', 0.15), ('fear_of_being_left_behind', 0.15), ('remainder', 0.05)]),
 cut('cut.faye.2022.holding', 'ev.faye.collapse_2022.focal', 'Why does Faye hold as the peg breaks?', 'share of the reason',
     [('trust_in_her_own_understanding', 0.35), ('loyalty_to_the_group', 0.30), ('shame_of_selling_at_a_loss', 0.20), ('remainder', 0.15)]),
 cut('cut.faye.2026.why_write', 'ev.faye.composition', 'Why is Faye writing this novel now?', 'share of her reasons',
     [('to_understand_why_she_fell', 0.35), ('love_for_her_daughter', 0.30), ('to_make_the_shame_useful', 0.15), ('pleasure_of_making', 0.15), ('remainder', 0.05)]),
]
dump({'requestId': 'register-faye-r0', 'model': m}, 'inputs/register-faye-r0.json')
print(len(ev), len(rels), len(cuts))

import json, sys
sys.path.insert(0, 'build')
from mm import *
m = json.load(open('results/compile-story-r1.json'))['model']
r0 = json.load(open('inputs/register-story-r0.json'))['model']
mm = m['meaning_model']; ev = mm['events']; rels = mm['event_relations']; refs = mm['referents']; binds = mm['event_referent_bindings']
for k in ('concepts','abstract_cuts','abstract_relations','encapsulation_cuts','physical_cuts','realizations','normalized_cuts'): mm.setdefault(k, [])
cuts, concepts, acuts, arels, reals = mm['normalized_cuts'], mm['concepts'], mm['abstract_cuts'], mm['abstract_relations'], mm['realizations']
procs = m['processes']
K='referent.profile.protagonist.person.protagonist'; B='referent.profile.barbara.person.barbara'; L='referent.profile.laura.person.laura'
KL='event.profile.protagonist.person.protagonist.life'; BL='event.profile.barbara.person.barbara.life'; LL='event.profile.laura.person.laura.life'
SW='Swindon, Wiltshire'; OLD='Old Swindon: the rented flat above a shop on Wood Street'; HART='White Hart House, the Hart\'s head office in west Swindon'; AVE='Avebury Trusloe and the Ridgeway, Wiltshire'; ONL='Online: the Sharehouse and the chains, every time zone'
# carry over r0 world and deep-time events and relations
for e in r0['meaning_model']['events']:
    if e['id'] == 'event.world' or e['id'].startswith('event.deep.'): ev.append(e)
for r in r0['meaning_model']['event_relations']:
    if not r['id'].startswith('relation.profile') and r['target_event_id'] != KL and r['source_event_id'] != KL: rels.append(r)
E = {e['id']: e for e in ev}
_fix = {'event.profile.kieran_white_rabbit.change_arc.focal_change': (None, 2019.835), 'event.profile.kieran_white_rabbit.change_arc.adaptation': (2019.835, None),
        'event.profile.kieran_collapse.change_arc': (2022.02, None), 'event.profile.kieran_collapse.change_arc.anticipation': (2022.02, None)}
for _id, (_a, _b) in _fix.items():
    if _a is not None: E[_id]['interval']['start'] = _a
    if _b is not None: E[_id]['interval']['end'] = _b
E['event.world']['interval'] = None
def life(eid, a, b, desc, reg):
    E[eid]['interval'] = iv(a, b); E[eid]['description'] = desc; E[eid]['region'] = reg
life(KL, 1990.27, 2023.25, 'Kieran Hale from his birth in Swindon in April 1990 to March 2023, where the story leaves him at thirty-two. Three generations of his family kept the town\'s industrial hours; he keeps the Hart\'s.', SW)
life(BL, 1953.37, 2023.25, 'Barbara Ashby from her birth in Rodbourne, Swindon, in May 1953 to March 2023, at sixty-nine. She has outlived the works, the bureau and her own trust in the clearing system.', SW)
life(LL, 1991.6, 2023.25, 'Laura Russell from her birth in August 1991 to March 2023, at thirty-one: a childhood of rented rooms, then the discipline of intensive care.', 'Highworth and Swindon, Wiltshire')
for x in (KL, BL, LL): rels.append(rel(f'world.contains.{x}', 'contains', 'event.world', x, 'Accepted-world containment.'))
for e in ev:
    if '.change_arc' in e['id']: e.setdefault('description', e['boundary'])
for arcid, owner in [('kieran_quits_game',KL),('kieran_white_rabbit',KL),('kieran_fall',KL),('kieran_father_plant',KL),('kieran_collapse',KL),('barbara_works_closure',BL),('barbara_crisis_2008',BL),('barbara_exit_2019',BL),('laura_last_move',LL),('laura_first_wave',LL),('laura_second_wave',LL)]:
    rels.append(rel(f'life.contains.arc.{arcid}', 'contains', owner, f'event.profile.{arcid}.change_arc', 'Change arc inside the life.'))
regs = {'kieran_quits_game':'Kieran\'s bedroom in Penhill, Swindon','kieran_white_rabbit':HART,'kieran_fall':OLD,'kieran_father_plant':'The car plant at South Marston and his parents\' house in Penhill','kieran_collapse':OLD,'barbara_works_closure':'The railway works, Swindon','barbara_crisis_2008':'The software bureau in Reading','barbara_exit_2019':AVE,'laura_last_move':'Highworth, Wiltshire','laura_first_wave':'The intensive-care unit of the Swindon hospital','laura_second_wave':'The intensive-care unit of the Swindon hospital'}
for e in ev:
    for k2, rg in regs.items():
        if e['id'].startswith(f'event.profile.{k2}.change_arc'): e['region'] = rg
# Things: referents with lifecycles
def thing(key, boundary, cont, a, b, desc, reg):
    lid = f'ev.{key}.life'
    ev.append(event(lid, boundary, desc, iv(a, b), {'subject': f'referent.{key}'}, region=reg))
    refs.append(referent(f'referent.{key}', boundary, cont, lid))
    binds.append(binding(f'binding.{key}.life', f'referent.{key}', lid))
    rels.append(rel(f'world.contains.{key}', 'contains', 'event.world', lid, 'A Thing of the world with its own long life.'))
    return lid
thing('works', 'The Great Western railway works at Swindon', 'Same works site and workforce', 1843, 1986.25, 'For about a hundred and forty years the works made the town: sheds, hooter, shifts, the Friday pay packet, three generations of families. Kieran\'s grandfather and Barbara both worked there. It closed in March 1986.', 'The railway works, Swindon')
thing('car_plant', 'The car plant on the old airfield at South Marston', 'Same plant and workforce', 1985.0, 2021.58, 'Engines from 1989 and cars from 1992; Kieran\'s father worked there from 1992. Its closure was announced in February 2019 and production ended at the end of July 2021.', 'South Marston, Swindon')
thing('hart', 'The White Hart Building Society (invented): a mutual savings and mortgage society', 'Same mutual society and its members', 1868, 2023.25, 'Founded in 1868 by railwaymen pooling savings in a White Hart inn to buy houses; now about 1,100 staff, a head office and payments operations in west Swindon. Its day is set by the clearing cut-offs; in 2021 it decides to block payments to several crypto exchanges.', HART)
thing('clearing', 'The interbank clearing system that the Hart\'s payments run through', 'Same clearing arrangements and their software lineage', 1968, 2023.25, 'Automated clearing designed for magnetic tape in the late 1960s: files submitted on day one, processed on day two, settled on day three, nothing at weekends. Barbara wrote software for it at a Reading bureau from 1988 to 2013, including the part that holds a payment while it waits.', 'Britain')
thing('sharehouse', 'The Sharehouse (invented): an online chat server of a few thousand anonymous yield farmers', 'Same server and its core members', 2020.3, 2023.25, 'Founded in spring 2020 as a yield-farming chat; a few thousand members in every time zone, a dozen who never seem to sleep, a language of memes and food tokens. It shares tips, losses, jokes and a belief that holding together is loyalty.', ONL)
thing('card', 'Barbara\'s card: a white index card with twelve words in her handwriting, and the wallet they open', 'Same card and the same key it records', 2019.83, 2023.25, 'Twelve words written in capitals in blue biro, posted to Kieran at the Hart on 1 November 2019 with a note: there is fifty pounds behind these; it is yours; go and look. The words are a recovery phrase for a wallet holding 0.0071 bitcoin. Kieran keeps the card behind his bus pass.', HART)
thing('stablecoin', 'The stablecoin and its savings protocol (real in the background, unnamed in the story)', 'Same token contract and protocol', 2020.7, 2022.4, 'A dollar token that held its peg not with dollars in a vault but through a mint-and-burn arbitrage with a sister token: one stablecoin could always be swapped for a dollar\'s worth of the sister token. Its savings protocol paid about twenty percent. When confidence broke, redemptions minted more of the sister token, its price fell, and each swap bought less: a spiral that took the peg from a dollar to cents between 9 and 13 May 2022.', ONL)
thing('stones', 'The Avebury henge and stone circles', 'Same monument', -2850, 2023.25, 'Raised by Neolithic farming communities between about 2850 and 2200 BC around a village that now sits inside the circle; the Ridgeway, used for at least five thousand years, runs along the downs above it. People dragged stones of up to forty tons there in order to gather.', 'Avebury, Wiltshire')
thing('flat', 'Kieran and Laura\'s rented flat in Old Swindon', 'Same tenancy and rooms', 2016.3, 2023.25, 'Two rooms and a spare room above a shop on Wood Street: the fridge with Laura\'s rota on it, the spare room where Kieran works the batch and farms at night, the kitchen table where the card is first read and where the truth is eventually told.', OLD)
# long developments connected to the deep-time frame
macro = [
 ('ev.macro.pandemic', 'The COVID-19 pandemic in England, 2020-2022.', 'National lockdowns from 23 March 2020, November 2020 and January 2021; intensive-care units at or beyond capacity in April 2020 and January 2021; offices emptied and work moved to spare rooms.', iv(2020.2, 2022.2), 'England'),
 ('ev.market.regime', 'The crypto market regime from the 2019 recovery to the 2022 collapses.', 'A market that never closes: the March 2020 crash, the yield-farming summer of 2020, the boom to November 2021, the slide through early 2022, the stablecoin collapse in May, the lender freezes in June and the exchange collapse in November 2022.', iv(2019.7, 2023.25), ONL),
 ('ev.market.crash_2020', 'Thursday 12 March 2020: bitcoin loses about half its value within a day.', 'Markets everywhere fall as the pandemic arrives; bitcoin trades near five thousand dollars at the low, down from about eight thousand the day before.', iv(2020.194, 2020.197), ONL),
 ('ev.market.defi_summer', 'The yield-farming summer of 2020.', 'From mid-June 2020 decentralized protocols begin paying their users in new governance tokens; farmers move money between pools chasing yields in the hundreds of percent; many of the new tokens are named after food.', iv(2020.455, 2020.75), ONL),
 ('ev.market.boom_2021', 'The boom from late 2020 to November 2021.', 'Prices of bitcoin and of the decentralized-finance tokens multiply; bitcoin peaks near sixty-nine thousand dollars on 10 November 2021.', iv(2020.85, 2021.86), ONL),
 ('ev.market.slide_2022', 'The slide from November 2021 to May 2022.', 'Prices fall steadily; money moves from volatile tokens into stablecoins and their yields, especially the savings protocol paying about twenty percent.', iv(2021.86, 2022.353), ONL),
 ('ev.market.stablecoin_collapse', '9 to 13 May 2022: the algorithmic stablecoin loses its peg and its sister token collapses.', 'Large withdrawals from the savings protocol and sales of the stablecoin push it below a dollar; the mint-and-burn mechanism floods the market with the sister token, which falls to almost nothing within days. By 13 May the stablecoin trades at ten to twenty cents; by June at one or two.', iv(2022.353, 2022.364), ONL),
 ('ev.market.lender_freeze', 'June 2022: a large crypto lender freezes withdrawals.', 'Contagion from the collapse reaches lenders and funds; customers cannot withdraw.', iv(2022.44, 2022.46), ONL),
 ('ev.market.exchange_collapse', 'November 2022: a large crypto exchange collapses into bankruptcy.', 'Customer funds turn out to have been used by the exchange\'s trading firm; bitcoin falls to about a quarter of its peak.', iv(2022.85, 2022.87), ONL),
 ('ev.macro.scam_rules', 'The British response to payment scams and crypto, 2019-2022.', 'A voluntary code for reimbursing victims of authorised push-payment scams from May 2019, name checks on new payees from 2020, regulator warnings about crypto, a ban on selling crypto derivatives to retail customers from January 2021, and banks blocking or limiting payments to some crypto exchanges from 2021.', iv(2019.4, 2023.25), 'Britain'),
 ('ev.macro.town_week', 'The town\'s week: the shape of ordinary time in Swindon.', 'Shift patterns inherited from the works and the plants, office hours set by the clearing cut-offs, the Thursday quiz, the Saturday town centre, Sunday lunch; the roundabouts and the M4.', iv(1843, 2023.25), SW),
]
for eid, b, d, i, rg in macro:
    ev.append(event(eid, b, d, i, region=rg))
    par = 'ev.market.regime' if eid.startswith('ev.market.') and eid != 'ev.market.regime' else 'event.world'
    rels.append(rel(f'contains.{eid}', 'contains', par, eid, 'Containment of a long development or its episode.'))
rels += [
 rel('crypto.enables.market', 'enables', 'event.deep.crypto', 'ev.market.regime', 'The market regime is an episode of programmable money.'),
 rel('global.enables.clearing', 'enables', 'event.deep.global_order', 'ev.clearing.life', 'The clearing system is part of the post-war financial order.'),
 rel('old.enables.hart', 'enables', 'event.deep.old_institutions', 'ev.hart.life', 'The mutual society is a descendant of the old savings institutions.'),
 rel('agri.enables.stones', 'enables', 'event.deep.agriculture', 'ev.stones.life', 'Only farmers with surplus could raise the circle.'),
 rel('foragers.constrains.town_week', 'constrains', 'event.deep.foragers', 'ev.macro.town_week', 'The minds keeping the town\'s week were built for a band, not a timetable.'),
 rel('works.enables.town_week', 'enables', 'ev.works.life', 'ev.macro.town_week', 'The works set the town\'s hours.'),
 rel('crash.causes.fall', 'causes', 'ev.market.crash_2020', 'event.profile.kieran_fall.change_arc.focal_change', 'The news of the crash reminds Kieran of the card.'),
 rel('pandemic.enables.fall', 'enables', 'ev.macro.pandemic', 'event.profile.kieran_fall.change_arc.adaptation', 'Lockdown empties his days and his flat.'),
 rel('pandemic.causes.first_wave', 'causes', 'ev.macro.pandemic', 'event.profile.laura_first_wave.change_arc', 'The pandemic fills Laura\'s unit.'),
 rel('pandemic.causes.second_wave', 'causes', 'ev.macro.pandemic', 'event.profile.laura_second_wave.change_arc', 'The winter wave of 2021.'),
 rel('defi.enables.fall', 'enables', 'ev.market.defi_summer', 'event.profile.kieran_fall.change_arc.adaptation', 'The yield-farming summer gives the fall its game.'),
 rel('collapse.causes.kieran', 'causes', 'ev.market.stablecoin_collapse', 'event.profile.kieran_collapse.change_arc.focal_change', 'The market event is the focal change of Kieran\'s collapse.'),
 rel('stablecoin.enables.collapse', 'enables', 'ev.stablecoin.life', 'ev.market.stablecoin_collapse', 'The mechanism that held the peg is the mechanism that broke it.'),
 rel('plant.causes.father', 'causes', 'ev.car_plant.life', 'event.profile.kieran_father_plant.change_arc.focal_change', 'The plant\'s end is his father\'s loss.'),
 rel('works.causes.barbara_closure', 'causes', 'ev.works.life', 'event.profile.barbara_works_closure.change_arc.focal_change', 'The works\' end is Barbara\'s loss.'),
 rel('exit.causes.white_rabbit', 'causes', 'event.profile.barbara_exit_2019.change_arc.focal_change', 'event.profile.kieran_white_rabbit.change_arc.focal_change', 'Barbara\'s transfer produces Kieran\'s call.'),
 rel('scam_rules.enables.call', 'enables', 'ev.macro.scam_rules', 'event.profile.kieran_white_rabbit.change_arc.focal_change', 'The scam rules are why the call is made.'),
 rel('card.enables.fall', 'enables', 'ev.card.life', 'event.profile.kieran_fall.change_arc.focal_change', 'The card is the key.'),
 rel('crisis2008.enables.exit', 'enables', 'event.profile.barbara_crisis_2008.change_arc.adaptation', 'event.profile.barbara_exit_2019.change_arc', 'Her purism, formed after 2008, leads to the exit.'),
]
# periods
def per(owner, pid, label, a, b, desc, reg):
    ev.append(event(pid, label, desc, iv(a, b), {'subject': {KL:K, BL:B, LL:L}[owner]}, region=reg))
    rels.append(rel(f'life.contains.{pid}', 'contains', owner, pid, 'Period of the life.'))
per(KL,'ev.kieran.p1.childhood','Childhood in Penhill, 1990-2002.',1990.27,2002.7,'A council-built house in Penhill; his father on shifts at the car plant, his mother a care assistant; his grandfather Ron, a works fitter until 1986, tells stories about the hooter. Kieran is quiet, clever with systems, and happiest drawing maps of invented places.','Penhill, Swindon')
per(KL,'ev.kieran.p2.game','The game years, 2002-2010.',2002.7,2010.35,'From twelve he plays an online role-playing game every night; at sixteen he leads a raiding guild of forty people across Europe who depend on his timetables. Middling GCSEs, a college course dropped, two years in a call centre. The guild is the first band that needs him.','Penhill, Swindon, and online')
per(KL,'ev.kieran.p3.hart','The Hart, 2010-2019.',2010.35,2019.8,'Payments floor from May 2010; exceptions analyst by 2014; meets Laura at a friend\'s thirtieth in 2014; the flat on Wood Street from 2016; saving for a deposit. Reliable, liked, no trouble; the week has one shape.',HART)
per(KL,'ev.kieran.p4.story','The story years, October 2019 to March 2023.',2019.8,2023.25,'The white rabbit, the fall, the harvest, the break and the reckoning.',SW)
per(BL,'ev.barbara.p1.childhood','Childhood in a Rodbourne railway family, 1953-1969.',1953.37,1969.6,'Her father a boilermaker at the works; she mends the family radio at ten and wants to be an electrician, which nobody takes seriously.','Rodbourne, Swindon')
per(BL,'ev.barbara.p2.works','The works, 1969-1986.',1969.6,1986.25,'One of very few women apprentices; the men call her Babs and she answers only to Barbara; a qualified electrical fitter by 1974; unmarried by choice; a long friendship with a woman draughtsman.','The railway works, Swindon')
per(BL,'ev.barbara.p3.bureau','The bureau, 1988-2013.',1988.5,2013.3,'Twenty-five years writing and maintaining clearing software in COBOL at a Reading bureau; the one who knows why the file stopped; never promoted past senior analyst; credited in no document.','Reading, Berkshire')
per(BL,'ev.barbara.p4.retirement','Retirement and bitcoin, 2013-2019.',2013.3,2019.8,'A cottage at Avebury Trusloe; walks on the Ridgeway; bitcoin bought in 2013 at about a hundred dollars and held through every crash; a quiet life with a laptop and a dog.',AVE)
per(BL,'ev.barbara.p5.story','The story years, 2019-2023.',2019.8,2023.25,'The exit from the Hart, the card, the friendship with Kieran, his fall, her guilt.',AVE)
per(LL,'ev.laura.p1.childhood','Childhood of rented rooms, 1991-2009.',1991.6,2009.7,'Her mother works two jobs; they move five times before she is thirteen; she keeps her things in boxes. A steady, practical girl who looks after her younger brother.','Highworth and Swindon')
per(LL,'ev.laura.p2.training','Nurse training, 2009-2013.',2009.7,2013.6,'A nursing degree in Oxford; she finds she is good in emergencies and bad at asking for anything.','Oxford')
per(LL,'ev.laura.p3.nursing','Nursing and Kieran, 2013-2020.',2013.6,2020.19,'Wards, then intensive care from 2017; Kieran from 2014; the flat from 2016; overtime put into the deposit, fifteen thousand pounds of the nineteen by 2019.','The Swindon hospital and Old Swindon')
per(LL,'ev.laura.p4.pandemic','The pandemic, 2020-2021.',2020.19,2021.8,'Two waves on the intensive-care unit; night shifts; sleeping by day; the car outside the flat.','The intensive-care unit of the Swindon hospital')
per(LL,'ev.laura.p5.after','After the waves, 2021-2023.',2021.8,2023.25,'Recovering; looking at houses in Wroughton; wanting to be looked after for once.','Old Swindon')
# inner roots and wants
for who, ref, nm in ((KL,K,'kieran'),(BL,B,'barbara'),(LL,L,'laura')):
    ev.append(event(f'ev.{nm}.inner', f'{nm.title()}\'s inner perspective root: wants, beliefs and appraisals attributed to them, never accepted as world fact.', None, None, {'subject': ref}))
    rels.append(rel(f'world.contains.{nm}.inner', 'contains', 'event.world', f'ev.{nm}.inner', 'Inner root nested in the accepted world.'))
    mm.setdefault('context_roots', [])
mm['context_roots'] = [{'event_id': 'event.world', 'kind': 'accepted_world', 'provenance': PROV}] + [{'event_id': f'ev.{n}.inner', 'kind': 'inner', 'provenance': PROV} for n in ('kieran','barbara','laura')]
def want(nm, ref, wid, text, a, b):
    ev.append(event(wid, text, text, iv(a, b), {'subject': ref}))
    rels.append(rel(f'{nm}.inner.contains.{wid}', 'contains', f'ev.{nm}.inner', wid, 'Want attributed to them.'))
for wid, text, a, b in [
 ('ev.kieran.want.matter','Deepest want: to matter to people he can see, to be the one they needed.',1990.27,2023.25),
 ('ev.kieran.want.map','Deepest want: to see the whole map, past the edges of the part he was given.',1990.27,2023.25),
 ('ev.kieran.want.safe','Deepest want: to be safe, which his family taught him means a job for life and no trouble.',1990.27,2023.25),
 ('ev.kieran.want.laura','Deepest want from 2014: a life with Laura and a front door that is theirs.',2014.4,2023.25),
 ('ev.kieran.want.no_trouble','Learned want from 2010: to be no trouble to anyone, the reliable one, as the way to stay safe and liked.',2010.35,2023.25),
 ('ev.kieran.want.band_loyalty','Learned want from the guild years: loyalty to whichever band needs him; leaving a band while it is losing is the one unforgivable thing.',2004.0,2023.25),
 ('ev.kieran.want.provide','Learned want from 2021: to provide for his family with what he wins, as proof that the game was real.',2021.58,2023.25)]:
    want('kieran', K, wid, text, a, b)
for wid, text, a, b in [
 ('ev.barbara.want.credited','Deepest want: to be believed and credited for what she knows and built.',1960.0,2023.25),
 ('ev.barbara.want.free','Deepest want: to depend on nothing she cannot verify; not to be anyone\'s wife or mother.',1969.6,2023.25),
 ('ev.barbara.want.leave_something','Deepest want, late: to leave something that outlasts her, the way her father left her his tools.',2013.3,2023.25),
 ('ev.barbara.want.verify','Learned want from 1986 and 2008: verify, do not trust; a key nobody can switch off.',1986.3,2023.25)]:
    want('barbara', B, wid, text, a, b)
for wid, text, a, b in [
 ('ev.laura.want.home','Deepest want: a home nobody can take away.',1996.0,2023.25),
 ('ev.laura.want.cared_for','Deepest want: to be the one looked after, for once.',2003.6,2023.25),
 ('ev.laura.want.competent','Deepest want: to be good at the work that keeps people alive.',2009.7,2023.25),
 ('ev.laura.want.hold_silent','Learned want from her mother: hold everything together and say nothing.',2003.6,2023.25)]:
    want('laura', L, wid, text, a, b)
# key moments
ev.append(event('ev.kieran.call_2019','Monday 21 October 2019, 3.40 pm: Kieran\'s scam-check call to Barbara.','He reads the script: has anyone contacted you and asked you to move your money, have you been promised returns. She laughs, answers every question and then asks hers: how old is the system he works in, and who could switch it off? He finds he does not know. She asks his name. The payment is released at 4.55.',iv(2019.804,2019.8045),{'caller':K,'customer':B},region=HART))
ev.append(event('ev.kieran.card_arrives','Friday 1 November 2019: the letter with the card arrives at the exceptions desk.','An envelope addressed in capitals to Mr K. Hale, Payments Exceptions, Third Floor, White Hart House. A white card, twelve words, and a note: there is fifty pounds behind these; it is yours; go and look. He must declare gifts from customers. He puts the card in his wallet behind his bus pass.',iv(2019.833,2019.834),{'recipient':K},region=HART))
ev.append(event('ev.kieran.mirror','Evening of 12 March 2020: Kieran types the twelve words in.','At the kitchen table in the flat, with the news on about the crash, he downloads a wallet app, types the words, and presses his thumb to the glass to confirm. The balance rises: 0.0071 bitcoin, about twenty-eight pounds. Then he finds the public ledger and the transaction that sent it to him, and every transaction before it since 2009.',iv(2020.195,2020.196),{'subject':K},region=OLD))
ev.append(event('ev.kieran.deposit_move','January 2022: the house deposit goes into the stablecoin\'s savings protocol.','Twenty-four thousand pounds, fifteen of it Laura\'s, leaves the Hart through a payments app and becomes stablecoin earning about twenty percent. How Laura is involved is drawn from cut.kieran.2022.deposit_consent.',iv(2022.03,2022.06),{'subject':K,'co_owner':L},region=OLD))
ev.append(event('ev.kieran.depeg_hold','9 to 13 May 2022: Kieran watches the peg break.','Four nights at the spare-room desk. The stablecoin slips below a dollar on 9 May; the Sharehouse says it always comes back; the founder\'s account says he is deploying capital; Kieran reads the mechanism and understands it perfectly. What he does is drawn from cut.kieran.2022.depeg_response.',iv(2022.353,2022.364),{'subject':K},region=OLD))
for x,par in (('ev.kieran.call_2019','event.profile.kieran_white_rabbit.change_arc.focal_change'),('ev.kieran.card_arrives','event.profile.kieran_white_rabbit.change_arc.focal_change'),('ev.kieran.mirror','event.profile.kieran_fall.change_arc.focal_change'),('ev.kieran.deposit_move','event.profile.kieran_collapse.change_arc.anticipation'),('ev.kieran.depeg_hold','event.profile.kieran_collapse.change_arc.focal_change')):
    rels.append(rel(f'contains.{x}', 'contains', par, x, 'A moment inside the change arc.'))
rels.append(rel('call.causes.card','causes','ev.kieran.call_2019','ev.kieran.card_arrives','Barbara remembers his voice and his name.'))
rels.append(rel('card.enables.mirror','enables','ev.kieran.card_arrives','ev.kieran.mirror','The card is the key he types in.'))
rels.append(rel('deposit.enables.depeg','enables','ev.kieran.deposit_move','ev.kieran.depeg_hold','Without the move there is nothing of Laura\'s to lose.'))
json.dump(m, open('build/story_r1_partial.json','w'))
print('events', len(ev), 'rels', len(rels))

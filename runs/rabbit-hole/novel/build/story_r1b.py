import json, sys
sys.path.insert(0, 'build')
from mm import *
m = json.load(open('build/story_r1_partial.json'))
mm = m['meaning_model']; ev = mm['events']; rels = mm['event_relations']
cuts, concepts, acuts, arels, reals = mm['normalized_cuts'], mm['concepts'], mm['abstract_cuts'], mm['abstract_relations'], mm['realizations']
procs = m['processes']
K='referent.profile.protagonist.person.protagonist'; B='referent.profile.barbara.person.barbara'; L='referent.profile.laura.person.laura'
OLD='Old Swindon: the rented flat above a shop on Wood Street'
ev.append(event('ev.kieran.harvest_2021','2021: the harvest year.','Kieran farms through the night, answers newcomers in the Sharehouse at three in the morning, watches six thousand pounds become thirty-eight and then seventy-one thousand on the screen, builds the Hart\'s crypto-payment block by day and pays his parents\' rent after the plant closes.',iv(2021.0,2021.86),{'subject':K},region=OLD))
rels.append(rel('p4.contains.harvest','contains','ev.kieran.p4.story','ev.kieran.harvest_2021','A stretch of the story years.'))
O='share of one unit of represented outlook toward fulfilment of active wants'; T='share of what is seen as threatened'; MA='share of motivational attention over the person\'s wants'; FL='share of the reasons behind the act'
def ol(pid, who, a, t, threats):
    cuts.append(cut(f'cut.{pid[3:]}.outlook', pid, f'Across this stretch, how does {who} expect what they want to turn out?', O, [('assurance',a),('threat',t),('remainder',round(1-a-t,6))]))
    cuts.append(cut(f'cut.{pid[3:]}.threatened', pid, f'What does {who} see as threatened in this stretch?', T, threats))
ol('ev.kieran.p1.childhood','Kieran',0.70,0.18,[('the_family_s_work',0.45),('his_grandfather',0.25),('remainder',0.30)])
ol('ev.kieran.p2.game','Kieran',0.62,0.26,[('the_guild_holding_together',0.40),('a_future_outside_the_game',0.35),('remainder',0.25)])
ol('ev.kieran.p3.hart','Kieran',0.66,0.20,[('the_sameness_of_the_week',0.30),('the_deposit_and_a_house',0.35),('remainder',0.35)])
ol('ev.kieran.p4.story','Kieran',0.55,0.35,[('the_deposit_and_laura',0.40),('his_place_in_the_band',0.30),('his_job',0.15),('remainder',0.15)])
ol('ev.barbara.p1.childhood','Barbara',0.60,0.25,[('being_let_into_a_trade',0.55),('remainder',0.45)])
ol('ev.barbara.p2.works','Barbara',0.55,0.35,[('her_place_in_the_shop',0.45),('the_works_itself',0.35),('remainder',0.20)])
ol('ev.barbara.p3.bureau','Barbara',0.60,0.30,[('the_system_s_integrity',0.45),('being_credited',0.30),('remainder',0.25)])
ol('ev.barbara.p4.retirement','Barbara',0.72,0.18,[('her_savings_in_the_old_system',0.50),('remainder',0.50)])
ol('ev.barbara.p5.story','Barbara',0.50,0.38,[('kieran',0.45),('her_own_judgement',0.30),('remainder',0.25)])
ol('ev.laura.p1.childhood','Laura',0.40,0.48,[('the_house_they_live_in',0.60),('her_mother_s_strength',0.25),('remainder',0.15)])
ol('ev.laura.p2.training','Laura',0.66,0.24,[('money',0.45),('her_mother',0.25),('remainder',0.30)])
ol('ev.laura.p3.nursing','Laura',0.64,0.24,[('the_deposit_growing_too_slowly',0.40),('her_patients',0.35),('remainder',0.25)])
ol('ev.laura.p4.pandemic','Laura',0.35,0.55,[('her_patients',0.45),('herself',0.30),('kieran',0.10),('remainder',0.15)])
ol('ev.laura.p5.after','Laura',0.55,0.33,[('the_house',0.45),('her_health',0.30),('remainder',0.25)])
cuts += [
 cut('cut.kieran.2019.card.attention','ev.kieran.card_arrives','When the card arrives, where does Kieran\'s motivational attention go among his wants?',MA,[('map',0.35),('no_trouble',0.30),('matter',0.15),('safe',0.10),('remainder',0.10)]),
 cut('cut.kieran.2019.card.fear_love','ev.kieran.card_arrives','Is keeping the card an act of love or of fear?',FL,[('love_of_curiosity_and_of_being_trusted',0.45),('fear_of_the_same_week_forever',0.40),('remainder',0.15)]),
 cut('cut.kieran.2020.mirror.attention','ev.kieran.mirror','As he types the words in, where does Kieran\'s motivational attention go?',MA,[('map',0.45),('matter',0.15),('safe',0.10),('no_trouble',0.10),('remainder',0.20)]),
 cut('cut.kieran.2021.harvest.attention','ev.kieran.harvest_2021','Through the harvest year, where does Kieran\'s motivational attention go?',MA,[('matter',0.30),('band_loyalty',0.20),('provide',0.15),('map',0.15),('laura',0.10),('remainder',0.10)]),
 cut('cut.kieran.2022.deposit.fear_love','ev.kieran.deposit_move','Is moving the deposit an act of love or of fear?',FL,[('love_for_laura_and_the_house',0.40),('fear_of_house_prices_leaving_them_behind',0.35),('remainder',0.25)]),
 cut('cut.kieran.2022.depeg.attention','ev.kieran.depeg_hold','As the peg breaks, where does Kieran\'s motivational attention go?',MA,[('band_loyalty',0.30),('safe',0.20),('laura',0.20),('matter',0.10),('map',0.05),('remainder',0.15)]),
 cut('cut.kieran.2022.depeg.fear_love','ev.kieran.depeg_hold','Is holding through the depeg an act of love or of fear?',FL,[('fear_of_exile_and_of_making_the_loss_real',0.60),('love_as_loyalty_to_the_band',0.25),('remainder',0.15)]),
 cut('cut.barbara.2019.card.attention','event.profile.barbara_exit_2019.change_arc.adaptation','When Barbara decides to send the card, where does her motivational attention go?',MA,[('leave_something',0.40),('credited',0.20),('verify',0.15),('free',0.10),('remainder',0.15)]),
 cut('cut.barbara.2019.card.fear_love','event.profile.barbara_exit_2019.change_arc.adaptation','Is sending the card an act of love or of fear?',FL,[('love_giving_as_her_father_gave_her_his_tools',0.55),('fear_of_leaving_nothing_behind',0.30),('remainder',0.15)]),
 cut('cut.laura.2021.attention','event.profile.laura_second_wave.change_arc.focal_change','In the January 2021 wave, where does Laura\'s motivational attention go?',MA,[('competent',0.45),('home',0.20),('cared_for',0.15),('hold_silent',0.10),('remainder',0.10)]),
 cut('cut.kieran.2022.deposit_consent','ev.kieran.deposit_move','How does the house deposit come to be moved into the stablecoin?','proposal weight over mutually exclusive continuations',[('asks_and_she_agrees',0.25),('asks_and_she_leaves_it_to_him',0.35),('moves_it_without_asking',0.30),('remainder',0.10)],'authored proposal weights from the modeled states, fixed before the draw'),
 cut('cut.kieran.2022.depeg_response','ev.kieran.depeg_hold','What does Kieran do as the peg breaks between 9 and 13 May 2022?','proposal weight over mutually exclusive continuations',[('holds_everything',0.55),('sells_part_early',0.25),('sells_all_early',0.10),('remainder',0.10)],'authored proposal weights from the modeled states, fixed before the draw'),
]
# quantities the causality runs through
Q=[('card.wallet_btc',0,1,0.0071,'BTC','balance of the wallet behind Barbara\'s card',['authored-observed-value: 0.0071 BTC at 1 Nov 2019']),
 ('kieran.stake_gbp',0,500000,0,'GBP','sterling value of Kieran\'s own crypto holdings',['authored: 0 before March 2020; 6,000 in July 2020; about 38,000 in Feb 2021; about 71,000 in Nov 2021']),
 ('household.deposit_gbp',0,200000,19000,'GBP','Kieran and Laura\'s shared house deposit',['authored: 19,000 in Oct 2019 (15,000 Laura\'s); 24,000 by Jan 2022']),
 ('stablecoin.price_usd',0,1.5,1.0,'USD','market price of one stablecoin',['documented path: about 1.00 until 7 May 2022; 0.10-0.20 on 13 May; 0.01-0.02 by late June 2022']),
 ('clearing.cycle_days',0,10,3,'working days','working days from file submission to settlement in the clearing cycle',['documented: a three-working-day cycle']),
 ('kieran.sleep_hours',0,12,7.5,'hours per night','Kieran\'s usual sleep',['authored: about 7.5 in 2019; about 5 in 2021; about 3 in May 2022']),
 ('sharehouse.members',0,100000,0,'members','members of the Sharehouse chat server',['authored: founded spring 2020; about 3,000 by 2021']),
 ('kieran.known_faces',0,10000,150,'people','people Kieran knows by face and name',['authored anchor: about 150, the forager band scale'])]
for pid, lo, hi, init, unit, role, sup in Q: procs.append(scalar(pid, lo, hi, init, unit, role, sup))
E={e['id']:e for e in ev}
for eid, pids in [('ev.card.life',['card.wallet_btc']),('ev.kieran.mirror',['card.wallet_btc']),('ev.kieran.harvest_2021',['kieran.stake_gbp','kieran.sleep_hours','sharehouse.members']),('ev.kieran.deposit_move',['household.deposit_gbp']),('ev.market.stablecoin_collapse',['stablecoin.price_usd']),('ev.kieran.depeg_hold',['stablecoin.price_usd','household.deposit_gbp','kieran.sleep_hours']),('ev.clearing.life',['clearing.cycle_days']),('ev.sharehouse.life',['sharehouse.members']),('ev.kieran.p3.hart',['kieran.known_faces','clearing.cycle_days'])]:
    E[eid]['process_ids'] = sorted(set(E[eid]['process_ids'] + pids))
# concepts
def C(cid, label, boundary, diff): concepts.append({'id': cid, 'label': label, 'boundary': boundary, 'differentia': [diff], 'provenance': PROV})
C('concept.deep_time_gap','The deep-time gap','Paleolithic emotions, medieval institutions and godlike technology running at once in one person (E. O. Wilson\'s phrase; the history as told in Harari\'s Sapiens).','Three clocks in one life: the body\'s, the institution\'s and the machine\'s.')
C('concept.paleolithic_emotions','Paleolithic emotions','Fear of exile, hunger for status, loyalty to the band, alarm at sudden loss, delight in discovery: emotions tuned over hundreds of thousands of years of foraging.','They respond to faces, rank and danger, not to percentages.')
C('concept.medieval_institutions','Medieval institutions','Institutions that change over generations and settle through intermediaries: the mutual, the ledger, the court, the working week, the three-day clearing cycle.','Slow, closing at five, remembering everything in someone else\'s book.')
C('concept.godlike_technology','Godlike technology','Machines that act at planetary scale and machine speed: a ledger nobody owns that never closes, a phone that carries every market into bed.','Twelve-second blocks, twenty-four hours a day, in public.')
C('concept.band','The band','A small group of known faces, about the size a forager could hold in mind, that shares food, attention and danger and punishes defection.','Reproduced by guilds, offices, chat servers and crowds.')
C('concept.routine_as_safety','Routine as safety','A life made safe by a repeating schedule owned by an institution.','The safety is real but belongs to whoever can end the routine.')
C('concept.second_agriculture','The second agriculture','Yield farming as a new domestication: the farmer who checks his fields at three in the morning is kept by the crop, as, in Harari\'s account, wheat kept its first farmers.','The vocabulary is agricultural (seed, farm, harvest, stake, pool); the hours are the machine\'s.')
C('concept.playing_field','The playing field','The world understood as a game map of which one knew a single corner; past its edges are other players, rules and prizes.','Kieran\'s teenage skill at games is a way of seeing the world, not only a pastime.')
C('concept.key_without_map','A key without a map','Access handed over without the understanding or company needed to use it safely.','Barbara\'s gift: she verified the key and not the person.')
C('concept.peg','The peg','A promise that holds only while people believe it will hold: a stablecoin\'s dollar, a bank\'s deposit, a routine\'s permanence.','Its failure is sudden because belief is shared.')
acuts.append({'id':'acut.deep_time_gap.wilson','parent_concept_id':'concept.deep_time_gap','child_concept_ids':['concept.paleolithic_emotions','concept.medieval_institutions','concept.godlike_technology'],'lens':'E. O. Wilson\'s triad','query':'Which of the three clocks is driving this moment?','provenance':PROV})
arels += [
 {'id':'arel.band.specializes.paleolithic','source_concept_id':'concept.band','target_concept_id':'concept.paleolithic_emotions','kind':'specialization','provenance':PROV},
 {'id':'arel.routine.specializes.medieval','source_concept_id':'concept.routine_as_safety','target_concept_id':'concept.medieval_institutions','kind':'specialization','provenance':PROV},
 {'id':'arel.second_agriculture.specializes.godlike','source_concept_id':'concept.second_agriculture','target_concept_id':'concept.godlike_technology','kind':'specialization','provenance':PROV},
 {'id':'arel.peg.analogy.routine','source_concept_id':'concept.peg','target_concept_id':'concept.routine_as_safety','kind':'analogy','provenance':PROV},
 {'id':'arel.playing_field.opposition.routine','source_concept_id':'concept.playing_field','target_concept_id':'concept.routine_as_safety','kind':'opposition','provenance':PROV},
 {'id':'arel.key_without_map.constrains.playing_field','source_concept_id':'concept.key_without_map','target_concept_id':'concept.playing_field','kind':'constrains','provenance':PROV}]
def real(rid, cid, eid, deg, vp='narrative authority (the recorder under delegation)'):
    reals.append({'id': rid, 'concept_id': cid, 'purpose': 'describe', 'roles': {'instance': eid}, 'degree': deg, 'uncertainty': UNK, 'viewpoint': vp, 'authority': None, 'provenance': PROV})
for rid, cid, eid, deg in [('real.town_week.routine','concept.routine_as_safety','ev.macro.town_week',0.9),('real.clearing.medieval','concept.medieval_institutions','ev.clearing.life',0.9),('real.hart.medieval','concept.medieval_institutions','ev.hart.life',0.8),
 ('real.sharehouse.band','concept.band','ev.sharehouse.life',0.85),('real.guild.band','concept.band','ev.kieran.p2.game',0.8),('real.defi.second_agriculture','concept.second_agriculture','ev.market.defi_summer',0.85),('real.harvest.second_agriculture','concept.second_agriculture','ev.kieran.harvest_2021',0.8),
 ('real.mirror.playing_field','concept.playing_field','ev.kieran.mirror',0.85),('real.card.key_without_map','concept.key_without_map','ev.card.life',0.8),('real.stablecoin.peg','concept.peg','ev.stablecoin.life',0.95),('real.collapse.peg','concept.peg','ev.market.stablecoin_collapse',0.95),
 ('real.stones.band','concept.band','ev.stones.life',0.6),('real.depeg.gap','concept.deep_time_gap','ev.kieran.depeg_hold',0.9),('real.plant.routine','concept.routine_as_safety','ev.car_plant.life',0.8),('real.works.routine','concept.routine_as_safety','ev.works.life',0.9),('real.market.godlike','concept.godlike_technology','ev.market.regime',0.85)]:
    real(rid, cid, eid, deg)
m['id'] = 'rabbit-hole-world'
m['revision'] = {'number': 1, 'previous_model_hash': '282531cc472c577ff972f6beda3b74626bb4c24987ca6fe41313e31479c28070', 'provenance': PROV,
 'reason': 'Revision 1: what the four opening accounts commit, macro first. Things with their own long lives (the railway works, the car plant, the Hart, the clearing system, the Sharehouse, Barbara\'s card, the stablecoin, the Avebury stones, the flat); the pandemic, the market regime and its dated episodes, the British scam and crypto rules, the town\'s week; the whole lives of Kieran Hale, Barbara Ashby and Laura Russell with periods, eleven change arcs, inner roots and wants; outlook and threat Cuts per period, motivational-attention and fear-or-love Cuts at key moments, two direction Cuts to draw (the deposit consent and the depeg response); quantities; concepts opening the Wilson triad, with realizations.'}
dump({'requestId':'revise-story-r1','previousModelHash':'282531cc472c577ff972f6beda3b74626bb4c24987ca6fe41313e31479c28070','model':m,'requireDescribedNumbers':True}, 'inputs/revise-story-r1.json')
print(len(ev), len(rels), len(cuts), len(concepts), len(reals), len(procs))

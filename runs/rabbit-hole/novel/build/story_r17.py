import json, sys
sys.path.insert(0, 'build')
from mm import *
m = json.load(open('results/inspect-r16.json'))['model']
EV = {e['id']: e for e in m['meaning_model']['events']}
P = []
def sp(pid, lo, hi, init, unit, role, path, frame):
    P.append(scalar(pid, lo, hi, init, unit, role, [f'authored path: {path}'], frame=frame))
# people: authored judgment scales with explicit meanings and anchors
sp('kieran.sharehouse_belonging',0,1,0,'0-1 authored scale','how strongly Kieran feels the Sharehouse is his band (0 a stranger to it, 0.5 a regular, 1 it is the group he would not leave while it is losing)','0 before June 2020; 0.5 by autumn 2020; 0.85 through 2021; 0.9 on 9-13 May 2022; 0.3 by August 2022; 0.1 by March 2023','person:kieran')
sp('kieran.honesty_with_laura',0,1,0.95,'share','share of the money and the fear that Laura knows about (1 she knows all of it)','0.95 in October 2019; 0.85 after he keeps the card; 0.6 through 2021; 0.35 after the January 2022 move; 0.05 from 13 May to mid-June 2022; 0.8 after the June telling; 0.95 from September 2022','person:kieran')
sp('kieran.fear_left_behind',0,1,0.2,'0-1 authored scale','intensity of Kieran\'s fear of being left behind by the others (0 none, 0.5 a steady pressure, 1 panic)','0.2 in 2019; 0.45 in the 2020 summer; 0.6 at the November 2021 peak; 0.75 in January 2022; 0.9 on 9 May 2022; 0.3 by March 2023','person:kieran')
sp('kieran.screen_hours',0,24,1,'hours per day','hours a day Kieran spends in crypto apps and the Sharehouse','1 in 2019 (none on crypto); 5 in summer 2020; 6 in 2021; 9 during 9-13 May 2022; 0.5 from September 2022','person:kieran')
sp('laura.exhaustion',0,10,4,'0-10 authored scale','Laura\'s exhaustion (0 rested, 5 tired after a run of nights, 10 unable to function)','4 in 2019; 8 in April 2020; 9 in January 2021; 6 in January 2022; 7 in June 2022; 4 by March 2023','person:laura')
sp('laura.spoken_share',0,1,0.3,'share','share of her hurt and fear that Laura says aloud to Kieran','0.3 in 2019; 0.1 through the waves; 0.05 from June to August 2022; 0.8 on the evening of Barbara\'s visit; 0.6 from September 2022','person:laura')
sp('laura.trust_in_kieran_money',0,1,0.8,'0-1 authored scale','how far Laura trusts Kieran to handle their money without checking (1 complete, the way she trusts a monitor)','0.8 in 2019; 0.9 in January 2022; 0.1 in June 2022; 0.45 by March 2023 with shared accounts','person:laura')
sp('barbara.purism',0,1,0.9,'0-1 authored scale','Barbara\'s conviction that everything but bitcoin is a casino (1 absolute)','0.9 from 2013 to 2022; 0.8 after the collapse, when she stops caring whether she was right','person:barbara')
sp('barbara.care_for_kieran',0,1,0.1,'0-1 authored scale','how much Barbara\'s concern for Kieran guides what she does (0 none, 1 she acts on it at a cost to herself)','0.1 on the October 2019 call; 0.35 when she sends the card; 0.55 through the 2020-2021 walks; 0.6 in February 2022, not acted on; 0.9 in August 2022 when she goes to Laura','person:barbara')
sp('barbara.guilt',0,1,0,'0-1 authored scale','Barbara\'s guilt at having handed Kieran a key without a map','0 until 2021; 0.2 in February 2022; 0.8 in July 2022; 0.5 after the visit to Laura','person:barbara')
# world
sp('btc.price_gbp',0,100000,6300,'GBP','market price of one bitcoin in pounds','about 6,300 in October 2019; about 3,900 on 12 March 2020; about 49,000 on 10 November 2021; about 24,000 in May 2022; about 14,000 in November 2022; about 20,000 in March 2023 (approximate, from the documented dollar prices)','market')
sp('house_price.wroughton_gbp',0,1000000,265000,'GBP','asking price of the kind of semi-detached house Laura watches in Wroughton (authored)','about 265,000 in 2019; 300,000 by late 2021; 310,000 in mid 2022','market')
sp('hart.crypto_block',0,1,0,'0-1','whether the Hart blocks payments to the crypto exchanges it lists (0 open, 1 blocked)','0 until June 2021; 1 afterwards','institution:hart')
sp('sharehouse.messages_per_day',0,500000,0,'messages per day','messages posted in the Sharehouse in a day','0 before spring 2020; about 20,000 in summer 2020; about 60,000 in 2021; about 140,000 on 11 May 2022; about 3,000 by autumn 2022','sharehouse')
sp('icu.occupancy_share',0,2,0.75,'share of normal capacity','occupancy of the Swindon intensive-care unit as a share of its normal beds','about 0.75 in 2019; about 1.4 in April 2020; about 1.6 in January 2021; about 0.9 in 2022','hospital')
obs = {'ev.kieran.fall.sharehouse':['kieran.sharehouse_belonging','sharehouse.messages_per_day'],'ev.kieran.harvest_2021':['kieran.sharehouse_belonging','kieran.fear_left_behind','kieran.screen_hours','kieran.honesty_with_laura','btc.price_gbp'],
 'ev.kieran.state.2022_01':['kieran.fear_left_behind','kieran.honesty_with_laura','house_price.wroughton_gbp'],'ev.laura.state.2022_01':['laura.exhaustion','laura.trust_in_kieran_money','house_price.wroughton_gbp'],
 'ev.kieran.depeg.holds':['kieran.sharehouse_belonging','kieran.fear_left_behind','kieran.screen_hours','sharehouse.messages_per_day'],'ev.kieran.telling.mortgage':['kieran.honesty_with_laura','laura.trust_in_kieran_money'],
 'ev.laura.response.silence':['laura.spoken_share','laura.exhaustion'],'ev.barbara.after.goes_to_laura':['barbara.guilt','barbara.care_for_kieran','laura.spoken_share'],'ev.barbara.walk.his_choice':['barbara.purism','barbara.care_for_kieran','barbara.guilt'],
 'ev.kieran.call_2019':['barbara.care_for_kieran'],'ev.kieran.mirror':['btc.price_gbp'],'ev.hart.block_decision_2021':['hart.crypto_block'],'event.profile.laura_second_wave.change_arc.focal_change':['icu.occupancy_share','laura.exhaustion'],
 'event.profile.laura_first_wave.change_arc.focal_change':['icu.occupancy_share','laura.exhaustion'],'ev.kieran_laura.rebuild':['kieran.honesty_with_laura','laura.spoken_share','laura.trust_in_kieran_money'],'ev.kieran.end.open_eyes':['kieran.sharehouse_belonging','kieran.screen_hours'],'ev.market.exchange_collapse':['btc.price_gbp'],'ev.market.boom_2021':['btc.price_gbp']}
U=[]
for eid, pids in obs.items():
    e = dict(EV[eid]); e['process_ids'] = sorted(set(e.get('process_ids', []) + pids)); U.append(e)
change={"reason":"Revision 17 (the human asked for more processes): fifteen processes that change over the story, ten of them authored judgment scales for the principals (Kieran's belonging to the Sharehouse, honesty with Laura, fear of being left behind, screen hours; Laura's exhaustion, spoken share of her hurt, trust in Kieran about money; Barbara's purism, care for Kieran, guilt) and five of the world (the bitcoin price in pounds, house prices in Wroughton, the Hart's crypto block, the Sharehouse's messages per day, intensive-care occupancy), each with its meaning, anchors and authored path, observed by the Events where they matter.","provenance":PROV,"upsert":{"processes":P,"events":U}}
dump({'requestId':'revise-story-r17','previousModelHash':'94c0ef70447dbee8cc264945e2e752e6f4f2e25f678859b574e26406074378d7','change':change},'inputs/revise-story-r17.json')
print(len(P), len(U))

"""Fail closed if a restored component has new contact with unrelated surfaces."""
from pathlib import Path
import json,hashlib,collections,math
D=Path(__file__).resolve().parent
i=json.loads((D/'contacts-with-cap.json').read_text()); old=json.loads((D/'contacts.json').read_text());P=json.loads((D/'donor-plan-with-cap.json').read_text())
C=i['components']; assert len(C)==51 and i['paired_edges']==1050 and i['unchanged_triangles']==36586
samebefore=old['components']
s=collections.Counter(); hosts=[set(),set()]
for r in C:
 def contacts(k):return [p for h in r[k].values() for p in h['pairs']]
 if r['family']=='upper_rods':
  floor=(contacts('mid'));assert len(floor)==8 and all(abs(p[2][0][2]-r['bounds'][0][2])<1e-5 for p in floor)
  assert not r['Gls'] and len(r['Win'])==1 and len(contacts('Win')) in (10,12)
  s.update(roof_identical_source_sill_pairs=len(floor),roof_inherited_window_pairs=len(contacts('Win')))
 elif r['family']=='entry_ornament':
  p=r['center']; lower=upper=0
  for h in r['mid'].values():
   h0,h1=h['host_bounds']
   assert h0[0]-.018<p[0]<h1[0]+.018 and h0[1]-.018<p[1]<h1[1]+.018
   if h1[2]<3.025:
    assert max(v[2][1][2] for v in h['pairs'])<=3.025; lower+=1
    s.update(lantern_lower_pairs=len(h['pairs']))
   elif h0[2]>3.478:
    assert min(v[2][0][2] for v in h['pairs'])>=3.478; upper+=1
    s.update(lantern_right_existing_upper_pairs=len(h['pairs']))
   else: raise ValueError((p,h))
  assert lower==1 and upper==int(p[0]>0) and len(r['Gls'])==1 and not r['Win']
  s.update(lantern_inherited_glass_pairs=len(contacts('Gls')))
 else:
  assert not r['mid'] and not r['Win'] and len(r['Gls'])==1
  old_links=[len(h['pairs']) for h in r['near'].values()]
  new_links=list(i['cap_link_count'].values())
  assert sorted(old_links)==sorted(new_links) and sorted(new_links)==[22,24,24,26]
  s.update(left_cap_to_four_posts_pairs=sum(new_links),left_cap_to_inherited_glass_pairs=len(contacts('Gls')))
assert len(samebefore[21]['mid'])==1 and i['cap_link_count']['21']>0
out={**i};del out['components']
out.update({'contact_counts':dict(s),'known_pre_cap_missing_upper_seat_donor':21,'maximum_two_source_donor_error_m':max(r['donor_max_hausdorff_from_archival_m'] for r in P['components']),
 'note':'Contact counts are local BVH triangle pairs. The near/medium window and glass vertices and face order are identical. No claim of global watertightness or in-game validation.'})
(D/'contacts-summary.json').write_text(json.dumps(out,indent=2)+'\n');print(out)

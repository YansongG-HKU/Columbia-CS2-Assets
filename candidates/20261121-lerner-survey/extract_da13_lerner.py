"""Extract one verified OTI 2014 building from a ZIP member range, without bulk XML output."""
import re,zlib,struct,binascii,sys,hashlib,json
from pathlib import Path
src=Path(sys.argv[1]); out=Path(sys.argv[2])
members=[]; rest=b''; ns=None; sep=b'</core:cityObjectMember>'
dec=zlib.decompressobj(-15);n=c=0
with src.open('rb') as f:
 k=struct.unpack('<4s5H3L2H',f.read(30));name=f.read(k[-2]);f.read(k[-1])
 assert k[0]==b'PK\x03\x04' and k[3]==8 and k[6:9]==(329400131,44197658,618444705)
 assert name==b'DA_WISE_GMLs/DA13_3D_Buildings_Merged.gml'
 while b:=f.read(65536):
  while b:
   z=dec.decompress(b,1048576);b=dec.unconsumed_tail;n+=len(z);c=binascii.crc32(z,c)
   rest+=z
   if ns is None:
    j=rest.find(b'<core:CityModel');end=rest.find(b'>',j)
    assert j>=0 and end>j;ns=rest[j:end+1]
   rr=rest.split(sep);rest=rr.pop()
   for t in rr:
    if not re.search(rb'<gen:value>\s*1082166\s*</gen:value>',t):continue
    s=t.find(b'<core:cityObjectMember>'); assert s>=0
    members.append(t[s:]+sep)
 assert dec.eof and not dec.unused_data and c==k[6] and n==k[8]
assert 1<=len(members)<=5
gml=b'<?xml version="1.0" encoding="UTF-8"?>\n'+ns+b'\n'+b'\n'.join(members)+b'\n</core:CityModel>\n'
out.write_bytes(gml)
print(json.dumps({'member':name.decode(),'source_size_b':src.stat().st_size,'uncompressed_size_b':n,'full_entry_crc32':hex(c),'matching_city_members':len(members),'extracted_gml_bytes':len(gml),'gml_sha256':hashlib.sha256(gml).hexdigest()}))


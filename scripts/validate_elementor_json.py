from pathlib import Path
import argparse,json
def walk(items,ids,errors):
 for i,e in enumerate(items):
  if not isinstance(e,dict):errors.append('Element is not object');continue
  x=e.get('id')
  if not isinstance(x,str) or not x:errors.append('Missing id')
  else:ids.append(x)
  if not e.get('elType'):errors.append('Missing elType for '+str(x))
  ch=e.get('elements',[])
  if isinstance(ch,list):walk(ch,ids,errors)
  else:errors.append('Invalid children for '+str(x))
def main():
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);path=p.parse_args().path
 try:d=json.loads(path.read_text(encoding='utf-8'))
 except Exception as ex:print('ERROR:',ex);return 1
 c=d.get('content');errors=[];ids=[]
 if not isinstance(c,list):print('ERROR: content must be list');return 1
 walk(c,ids,errors);dup=sorted({x for x in ids if ids.count(x)>1})
 if dup:errors.append('Duplicate IDs: '+','.join(dup))
 for x in errors:print('ERROR:',x)
 if errors:return 1
 print('OK:',path);return 0
if __name__=='__main__':raise SystemExit(main())

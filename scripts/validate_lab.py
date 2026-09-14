from pathlib import Path
import argparse,re
PATTERNS={'private key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),'AWS key':re.compile(r'\bAKIA[0-9A-Z]{16}\b'),'Windows user path':re.compile(r'[A-Za-z]:\\Users\\[^\\\s]+'),'Unix home path':re.compile(r'/home/[^/\s]+/')}
SOL={'solution.py','solution.sql','answers.md','answer.md','completed.py'}
def main():
 p=argparse.ArgumentParser();p.add_argument('lab_dir',type=Path);lab=p.parse_args().lab_dir;e=[]
 if not lab.is_dir():print('ERROR: missing lab',lab);return 1
 if not (lab/'README.md').is_file():e.append('Missing README.md')
 t=lab/'tests'
 if not t.is_dir() or not any(x.is_file() for x in t.rglob('*')):e.append('No automated tests')
 for f in lab.rglob('*'):
  if not f.is_file():continue
  rel=f.relative_to(lab)
  in_starter=rel.parts[0]=='starter' if rel.parts else False
  if not in_starter and f.name.lower() in SOL:e.append('Possible solution leak: '+str(rel))
  try:s=f.read_text(encoding='utf-8')
  except:continue
  for label,pat in PATTERNS.items():
   if pat.search(s):e.append(label+' found in '+str(f.relative_to(lab)))
 for x in e:print('ERROR:',x)
 if e:return 1
 print('OK:',lab);return 0
if __name__=='__main__':raise SystemExit(main())

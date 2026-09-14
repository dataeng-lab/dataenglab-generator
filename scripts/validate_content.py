from pathlib import Path
import argparse,re

def heading_positions(text):
 return [(m.start(),m.end(),m.group(1).strip()) for m in re.finditer(r'^##[ \t]+(.+)$',text,re.M)]

def sections(text):
 pos=heading_positions(text);out={}
 for i,(s,e,name) in enumerate(pos):
  end=pos[i+1][0] if i+1<len(pos) else len(text)
  out[name]=text[e:end].strip()
 return out

def check_lesson(path,required,errors):
 sec=sections(path.read_text(encoding='utf-8'))
 for h in required:
  if h not in sec:errors.append('Missing heading: '+h+' in '+str(path))
  elif not sec[h]:errors.append('Empty section: '+h+' in '+str(path))

FIELD_RE=re.compile(r'^-\s+([A-Za-z][A-Za-z /]*):\s*(.*)$')
OPTION_RE=re.compile(r'^\s+([A-Za-z])\.\s+(.+)$')
REQUIRED_FIELDS=['Type','Difficulty','Related lesson','Question','Options','Correct answer','Explanation']
NON_OPTION_FIELDS=['Type','Difficulty','Related lesson','Question','Correct answer','Explanation']

def check_quiz(path,errors):
 text=path.read_text(encoding='utf-8')
 for qname,content in sections(text).items():
  if not qname.lower().startswith('question'):continue
  fields={};cur=None;letters=[]
  for line in content.splitlines():
   m=FIELD_RE.match(line)
   if m:cur=m.group(1).strip();fields[cur]=m.group(2).strip();continue
   m=OPTION_RE.match(line)
   if m and cur=='Options':letters.append(m.group(1).upper())
  tag=str(path)+' ('+qname+')'
  for f in REQUIRED_FIELDS:
   if f not in fields:errors.append('Missing field: '+f+' in '+tag)
  for f in NON_OPTION_FIELDS:
   if f in fields and not fields[f]:errors.append('Empty field: '+f+' in '+tag)
  dup=sorted({l for l in letters if letters.count(l)>1})
  if dup:errors.append('Duplicate option letters '+','.join(dup)+' in '+tag)
  if len(set(letters))<2:errors.append('Fewer than 2 options in '+tag)
  ans=fields.get('Correct answer','').strip()
  m=re.match(r'^([A-Za-z])',ans)
  letter=m.group(1).upper() if m else ''
  if letter not in set(letters):errors.append('Correct answer "'+ans+'" does not match any option in '+tag)

def main():
 p=argparse.ArgumentParser();p.add_argument('course_dir',type=Path);course=p.parse_args().course_dir;errors=[]
 tmpl=Path(__file__).resolve().parent.parent/'templates'/'lesson-template.md'
 required=[n for _,_,n in heading_positions(tmpl.read_text(encoding='utf-8'))] if tmpl.is_file() else []
 lessons=course/'tutor-lms'/'lessons'
 if lessons.is_dir():
  for f in sorted(lessons.glob('*.md')):check_lesson(f,required,errors)
 else:errors.append('Missing directory: tutor-lms/lessons')
 quizzes=course/'tutor-lms'/'quizzes'
 if quizzes.is_dir():
  for f in sorted(quizzes.glob('*.md')):check_quiz(f,errors)
 else:errors.append('Missing directory: tutor-lms/quizzes')
 for x in errors:print('ERROR:',x)
 if errors:return 1
 print('OK:',course);return 0
if __name__=='__main__':raise SystemExit(main())

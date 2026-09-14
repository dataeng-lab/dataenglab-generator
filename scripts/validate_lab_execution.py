from pathlib import Path
import argparse,json,shutil,subprocess,tempfile

TIMEOUT=300

def run_cmds(cmds,cwd,errors,label):
 for argv in cmds:
  try:
   r=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=TIMEOUT)
  except FileNotFoundError as ex:
   errors.append(label+' command not found: '+' '.join(argv)+' ('+str(ex)+')');return False
  except subprocess.TimeoutExpired:
   errors.append(label+' command timed out after '+str(TIMEOUT)+'s: '+' '.join(argv));return False
  if r.returncode!=0:
   tail=(r.stdout+r.stderr)[-2000:]
   errors.append(label+' failed (exit '+str(r.returncode)+'): '+' '.join(argv)+'\n'+tail)
   return False
 return True

def overlay_solution(course,tmp_lab,errors):
 solution=course/'instructor'/'solution'
 if not solution.is_dir():
  errors.append('Missing instructor/solution — cannot verify the lab is solvable');return False
 applied=False
 for f in solution.rglob('*'):
  if not f.is_file() or f.suffix=='.pyc':continue
  rel=f.relative_to(solution);target=tmp_lab/'starter'/rel
  if not target.is_file():
   errors.append('instructor/solution file has no matching starter file: '+str(rel));continue
  shutil.copyfile(f,target);applied=True
 if not applied:errors.append('No instructor solution files were applied over the starter')
 return applied

def main():
 p=argparse.ArgumentParser();p.add_argument('course_dir',type=Path);course=p.parse_args().course_dir;errors=[]
 lab=course/'student-lab'
 if not lab.is_dir():print('ERROR: missing student-lab in',course);return 1
 manifest=course/'validate.json'
 if not manifest.is_file():
  print('ERROR: missing validate.json in',course);return 1
 try:d=json.loads(manifest.read_text(encoding='utf-8'))
 except Exception as ex:print('ERROR: invalid validate.json:',ex);return 1
 validate_cmds=d.get('validate') or []
 if not validate_cmds:
  print('ERROR: validate.json has no validate commands');return 1
 ok=False
 with tempfile.TemporaryDirectory() as td:
  tmp_lab=Path(td)/'student-lab'
  shutil.copytree(lab,tmp_lab,ignore=shutil.ignore_patterns('__pycache__'))
  if overlay_solution(course,tmp_lab,errors):
   ok=run_cmds(d.get('setup') or [],tmp_lab,errors,'setup')
   if ok:ok=run_cmds(validate_cmds,tmp_lab,errors,'validate')
 for x in errors:print('ERROR:',x)
 if not ok:return 1
 print('OK: instructor solution passes the lab tests —',course);return 0
if __name__=='__main__':raise SystemExit(main())

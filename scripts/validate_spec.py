from pathlib import Path
import argparse,json

REQUIRED_FIELDS=['title','slug','audience','level','prerequisites','outcomes','technologies','business_scenario','deliverable','validation_criteria','acquired_skills','duration_minutes','curriculum']

def main():
 p=argparse.ArgumentParser();p.add_argument('course_dir',type=Path);course=p.parse_args().course_dir.resolve();errors=[]
 spec=course/'course-spec.json'
 if not spec.is_file():print('ERROR: missing course-spec.json in',course);return 1
 try:d=json.loads(spec.read_text(encoding='utf-8'))
 except Exception as ex:print('ERROR: invalid course-spec.json:',ex);return 1
 for f in REQUIRED_FIELDS:
  if f not in d or d[f] in (None,'',[],{}):errors.append('Missing or empty field: '+f)
 slug=d.get('slug')
 if slug and slug!=course.name:errors.append('slug "'+str(slug)+'" does not match directory name "'+course.name+'"')
 dur=d.get('duration_minutes') or {}
 lecture=dur.get('lecture',0);practical=dur.get('practical',0)
 total=lecture+practical
 if total<=0:errors.append('duration_minutes.lecture + practical must be greater than 0')
 elif practical/total<0.5:errors.append('Practical time is only '+str(round(100*practical/total))+'% of duration_minutes — must be at least 50%')
 curriculum=d.get('curriculum') or []
 if not curriculum:errors.append('curriculum is empty')
 for x in errors:print('ERROR:',x)
 if errors:return 1
 print('OK:',course);return 0
if __name__=='__main__':raise SystemExit(main())

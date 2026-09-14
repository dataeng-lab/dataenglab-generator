from pathlib import Path
import argparse

REQ_FILES=['tutor-lms/course-overview.md','tutor-lms/curriculum.md','student-lab/README.md','instructor/instructor-guide.md','instructor/troubleshooting.md']
REQ_DIRS=['tutor-lms/lessons','tutor-lms/quizzes','student-lab/starter','student-lab/tests','instructor/solution']

def main():
 p=argparse.ArgumentParser(); p.add_argument('course_dir',type=Path); c=p.parse_args().course_dir; e=[]
 if not c.is_dir(): print('ERROR: missing course directory',c); return 1
 for r in REQ_FILES:
  x=c/r
  if not x.is_file() or x.stat().st_size==0: e.append('Missing or empty: '+r)
 for r in REQ_DIRS:
  if not (c/r).is_dir(): e.append('Missing directory: '+r)
 for x in e: print('ERROR:',x)
 if e:return 1
 print('OK:',c); return 0
if __name__=='__main__': raise SystemExit(main())

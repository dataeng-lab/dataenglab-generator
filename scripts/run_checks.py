from pathlib import Path
import argparse,subprocess,sys
def run(c):print('\n$',' '.join(c));return subprocess.run(c,check=False).returncode==0
def main():
 p=argparse.ArgumentParser();p.add_argument('course_dir',type=Path);course=p.parse_args().course_dir;s=Path(__file__).resolve().parent;py=sys.executable
 cmds=[[py,str(s/'validate_spec.py'),str(course)],[py,str(s/'validate_course.py'),str(course)],[py,str(s/'validate_content.py'),str(course)],[py,str(s/'validate_lab.py'),str(course/'student-lab')],[py,str(s/'validate_lab_execution.py'),str(course)]]
 e=course/'elementor/landing-page.json'
 if e.is_file():cmds.append([py,str(s/'validate_elementor_json.py'),str(e)])
 ok=True
 for c in cmds:ok=run(c) and ok
 print('ALL CHECKS PASSED' if ok else 'CHECKS FAILED');return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())

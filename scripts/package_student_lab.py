from pathlib import Path
import argparse,zipfile
def main():
 p=argparse.ArgumentParser();p.add_argument('course_dir',type=Path);c=p.parse_args().course_dir.resolve();s=c/'student-lab'
 if not s.is_dir():print('ERROR: missing student-lab');return 1
 out=c/'packages';out.mkdir(parents=True,exist_ok=True);z=out/f'{c.name}-student-lab.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as a:
  for f in sorted(s.rglob('*')):
   if f.is_file():a.write(f,Path(f'{c.name}-student-lab')/f.relative_to(s))
 print('OK:',z);return 0
if __name__=='__main__':raise SystemExit(main())

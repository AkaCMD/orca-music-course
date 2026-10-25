"""Package a self-contained copy of the course and authoring scripts."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'outputs/orca-music-course-complete.zip'
EXCLUDED={'Orca-Tutorial-Triangle.sf2','terminal-triangle-preview.wav','lesson-preview.png'}

def package():
    with zipfile.ZipFile(TARGET,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name in ['README.md','MISSION.md','RESOURCES.md','NOTES.md']:
            archive.write(ROOT/name,name)
        for folder in ['outputs','scripts','course','learning-records']:
            for file in sorted((ROOT/folder).rglob('*')):
                if not file.is_file() or file==TARGET:continue
                if '__pycache__' in file.parts or file.suffix in ('.zip','.pyc') or file.name in EXCLUDED:continue
                archive.write(file,file.relative_to(ROOT))
    with zipfile.ZipFile(TARGET) as archive:
        assert archive.testzip() is None
        assert 'outputs/index.html' in archive.namelist()
        assert 'outputs/projects/final-cue/preview.html' in archive.namelist()
        count=len(archive.namelist())
    print(f'Complete package: {count} files, {TARGET.stat().st_size/1024/1024:.1f} MiB')
if __name__=='__main__':package()

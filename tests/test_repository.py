import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RepositoryTest(unittest.TestCase):
    def test_verifier(self):
        p=subprocess.run([sys.executable,str(ROOT/'tools/verify.py')],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn('ALIVE:',p.stdout)
    def test_no_generated_source_directory(self):
        self.assertFalse((ROOT/'generated').exists())
if __name__=='__main__': unittest.main()

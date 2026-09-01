import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RepositoryTest(unittest.TestCase):
    def run_ok(self,*args):
        p=subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        return p
    def test_verifier(self):
        p=self.run_ok(ROOT/'tools/verify.py')
        self.assertIn('ALIVE:',p.stdout)
    def test_manufacturing_source_contract(self):
        p=self.run_ok(ROOT/'tools/verify_manufacturing.py','source')
        self.assertIn('PARTIAL_ALIVE:',p.stdout)
    def test_manufacturing_falsifiers(self):
        p=self.run_ok(ROOT/'tools/verify_manufacturing.py','falsify')
        self.assertIn('PARTIAL_ALIVE:',p.stdout)
    def test_no_generated_source_directory(self):
        self.assertFalse((ROOT/'generated').exists())
if __name__=='__main__': unittest.main()

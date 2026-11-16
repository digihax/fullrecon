"""Offline saved-output checks. No scanner or network execution."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'oscp-nmap-summary'
FIXTURE='Nmap scan report for fixture.example (192.0.2.10)\nHost is up.\nPORT STATE SERVICE VERSION\n80/tcp open http ExampleServer\n443/tcp closed https\n53/udp open|filtered domain\n'

class SavedSummary(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.target=self.root/'targets/192.0.2.10'
        self.target.mkdir(parents=True)
        self.env=dict(os.environ,OSCP_ARTIFACTS=str(self.root))
    def run_summary(self,*args):
        return subprocess.run([sys.executable,str(SCRIPT),'192.0.2.10',*args],env=self.env,capture_output=True,text=True,timeout=10)
    def test_saved_report_separates_open_and_closed(self):
        (self.target/'00_fixture.nmap').write_text(FIXTURE)
        result=self.run_summary()
        self.assertEqual(result.returncode,0,result.stderr)
        text=(self.target/'services_summary.txt').read_text()
        self.assertIn('fixture.example',text)
        self.assertIn('80',text)
        self.assertIn('53',text)
        self.assertNotIn('443',text)
        self.assertEqual(list(self.target.glob('.summ-*.tmp')),[])
    def test_filter_and_custom_basename(self):
        (self.target/'00_fixture.nmap').write_text(FIXTURE)
        (self.target/'10_other.nmap').write_text('22/tcp open ssh OtherServer\n')
        result=self.run_summary('--only','00*.nmap','--out','phase1')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('1 open TCP',result.stdout)
        self.assertTrue((self.target/'phase1.txt').exists())
        self.assertFalse((self.target/'services_summary.txt').exists())
    def test_missing_saved_files_fails(self):
        self.assertEqual(self.run_summary().returncode,5)
    def test_empty_saved_report_is_not_fabricated_ports(self):
        (self.target/'empty.nmap').write_text('Nmap done: 1 IP address\n')
        result=self.run_summary()
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('0 open TCP, 0 open UDP',result.stdout)

if __name__=='__main__':unittest.main()

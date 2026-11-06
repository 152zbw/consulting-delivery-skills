"""Run with Python 3, standard library only. All inputs are synthetic."""
import importlib.util,json,tempfile,unittest,zipfile,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('delivery_check',ROOT/'skills/consulting-proposal/scripts/check_delivery.py')
MOD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(MOD)

class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.p=Path(self.tmp.name)
        (self.p/'client.md').write_text('项目范围：两个部门。交付：诊断说明与责任矩阵。',encoding='utf-8')
        self.m={'version':'v2','status':'client-release','files':[{'path':'client.md','opened':True}],'issues':[],
                'approval':{'by':'虚构业务负责人','date':'2026-11-06','version':'v2','evidence':'虚构测试确认记录'},
                **{x:True for x in ('facts_verified','scope_consistent','commercial_terms_verified','requirements_covered','metadata_reviewed')}}
    def run_check(self):
        f=self.p/'manifest.json';f.write_text(json.dumps(self.m),encoding='utf-8');return MOD.check(f)
    def test_complete_record_passes(self):self.assertEqual(self.run_check(),[])
    def test_missing_file_blocks(self):
        self.m['files'][0]['path']='missing.docx';self.assertTrue(self.run_check())
    def test_open_serious_issue_blocks(self):
        self.m['issues']=[{'severity':'P1','state':'open','evidence':''}];self.assertTrue(self.run_check())
    def test_closed_issue_needs_evidence(self):
        self.m['issues']=[{'severity':'P0','state':'closed','evidence':''}];self.assertTrue(self.run_check())
    def test_approval_version_mismatch_blocks(self):
        self.m['approval']['version']='v1';self.assertTrue(self.run_check())
    def test_placeholder_blocks(self):
        (self.p/'client.md').write_text('费用：待确认',encoding='utf-8');self.assertTrue(self.run_check())
    def test_renamed_text_is_not_office(self):
        (self.p/'fake.docx').write_text('plain text');self.m['files']=[{'path':'fake.docx','opened':True}];self.assertTrue(self.run_check())
    def test_office_split_run_placeholder_and_missing_visual_blocks(self):
        with zipfile.ZipFile(self.p/'synthetic.docx','w') as z:
            z.writestr('[Content_Types].xml','<Types/>')
            z.writestr('word/document.xml','<document><t>待</t><t>确认</t></document>')
        self.m['files']=[{'path':'synthetic.docx','opened':True}]
        result=' '.join(self.run_check());self.assertIn('placeholder',result);self.assertIn('rendered',result)
    def test_draft_retains_gap_without_false_release(self):
        self.m['status']='draft';self.m['issues']=[{'severity':'P1','state':'open'}]
        (self.p/'client.md').write_text('待确认',encoding='utf-8');self.assertEqual(self.run_check(),[])
    def test_missing_business_verification_blocks(self):
        self.m['commercial_terms_verified']=False;self.assertTrue(self.run_check())
    def test_all_copies_equal(self):
        copies=[p.read_bytes() for p in (ROOT/'skills').glob('*/scripts/check_delivery.py')]
        self.assertEqual(len(copies),4);self.assertTrue(all(c==copies[0] for c in copies))
if __name__=='__main__':unittest.main()

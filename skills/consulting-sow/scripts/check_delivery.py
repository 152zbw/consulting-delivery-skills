#!/usr/bin/env python3
"""Check recorded release evidence. Does not certify factual or visual quality."""
import json,sys,re,zipfile,xml.etree.ElementTree as ET
from pathlib import Path

def check(manifest):
    errors=[]
    try:
        m=json.loads(manifest.read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:
        return ['Cannot read manifest: '+str(e)]
    if not isinstance(m,dict): return ['Manifest must be an object']
    final=m.get('status')=='client-release'
    if m.get('status') not in ('draft','business-review','client-release'): errors.append('Unknown status')
    if not isinstance(m.get('version'),str) or not m['version'].strip(): errors.append('Missing version')
    files=m.get('files')
    if not isinstance(files,list) or not files: errors.append('No deliverable files');files=[]
    for i,f in enumerate(files):
        if not isinstance(f,dict): errors.append(f'files[{i}] must be an object');continue
        if not isinstance(f.get('path'),str) or not f['path'].strip(): errors.append(f'files[{i}] missing path');continue
        p=manifest.parent/f['path']
        if not p.is_file() or p.stat().st_size==0: errors.append('Missing/empty file: '+f['path']);continue
        suffix=p.suffix.lower();text=''
        try:
            if suffix in ('.docx','.pptx','.xlsx'):
                with zipfile.ZipFile(p) as z:
                    if '[Content_Types].xml' not in z.namelist(): raise ValueError('not an Office package')
                    part={'docx':'word/document.xml','pptx':'ppt/presentation.xml','xlsx':'xl/workbook.xml'}[suffix[1:]]
                    ET.fromstring(z.read(part))
                    names=[n for n in z.namelist() if (suffix=='.docx' and n.startswith('word/')) or (suffix=='.pptx' and n.startswith('ppt/')) or (suffix=='.xlsx' and n.startswith('xl/'))]
                    for n in names:
                        if n.endswith('.xml'):
                            t=ET.fromstring(z.read(n))
                            text+='\n'+''.join(e.text or '' for e in t.iter() if e.tag.split('}')[-1] in ('t','v'))
            elif suffix=='.pdf':
                if p.read_bytes()[:5]!=b'%PDF-': raise ValueError('not a PDF')
                if final and f.get('text_inspected') is not True: errors.append('PDF text inspection not recorded: '+f['path'])
            elif suffix in ('.md','.txt','.csv'): text=p.read_text(encoding='utf-8')
            else:
                if final and f.get('format_checked') is not True: errors.append('Format inspection not recorded: '+f['path'])
            if final and re.search(r'待确认|待补充|TODO|\bTBD\b|\{\{[^}]+\}\}',text,re.I): errors.append('Unresolved placeholder: '+f['path'])
        except (OSError,ValueError,KeyError,zipfile.BadZipFile,ET.ParseError) as e: errors.append('Unreadable/invalid package: '+f['path']+' ('+str(e)+')')
        if final:
            if f.get('opened') is not True: errors.append('Final file reopening not recorded: '+f['path'])
            if suffix in ('.docx','.pptx','.xlsx','.pdf'):
                pages=f.get('rendered_pages')
                if not isinstance(pages,list) or not pages: errors.append('No rendered pages: '+f['path'])
                elif any(not isinstance(x,str) or not (manifest.parent/x).is_file() for x in pages): errors.append('Missing rendered page: '+f['path'])
                if f.get('all_pages_reviewed') is not True: errors.append('Full visual review not recorded: '+f['path'])
    issues=m.get('issues')
    if not isinstance(issues,list): errors.append('issues must be a list');issues=[]
    for i,q in enumerate(issues):
        if not isinstance(q,dict): errors.append(f'issues[{i}] must be an object');continue
        if q.get('severity') not in ('P0','P1','P2'): errors.append(f'issues[{i}] unknown severity')
        if q.get('state') not in ('open','fixed-unverified','closed','not-applicable'): errors.append(f'issues[{i}] unknown state')
        if q.get('state') in ('closed','not-applicable') and not str(q.get('evidence','')).strip(): errors.append(f'issues[{i}] missing closure evidence')
        if final and q.get('state') not in ('closed','not-applicable'): errors.append(f'issues[{i}] unresolved issue')
    checks=m.get('review_checks',[])
    if not isinstance(checks,list): errors.append('review_checks must be a list');checks=[]
    for i,c in enumerate(checks):
        if not isinstance(c,dict): errors.append(f'review_checks[{i}] must be an object');continue
        if c.get('verdict') not in ('pass','fail','not-assessed','not-applicable'): errors.append(f'review_checks[{i}] unknown verdict')
        if not isinstance(c.get('evidence'),str) or not c['evidence'].strip(): errors.append(f'review_checks[{i}] missing evidence or reason')
        if final and c.get('verdict') not in ('pass','not-applicable'): errors.append(f'review_checks[{i}] incomplete review')
        if final and c.get('version')!=m.get('version'): errors.append(f'review_checks[{i}] stale review version')
    if final and not checks: errors.append('No professional review checks recorded')
    if final:
        for field in ('facts_verified','scope_consistent','commercial_terms_verified','requirements_covered','metadata_reviewed'):
            if m.get(field) is not True: errors.append('Release evidence missing: '+field)
        a=m.get('approval')
        if not isinstance(a,dict) or any(not isinstance(a.get(k),str) or not a[k].strip() for k in ('by','date','version','evidence')): errors.append('Missing recorded business approval')
        elif a['version']!=m.get('version'): errors.append('Approval version differs from release version')
    return errors

def main():
    if len(sys.argv)!=2: print('Usage: check_delivery.py manifest.json',file=sys.stderr);return 2
    errors=check(Path(sys.argv[1]).resolve())
    print(json.dumps({'recorded_checks_pass':not errors,'errors':errors,'limit':'Checks recorded evidence and basic files only; does not certify facts, contracts, or visual quality.'},ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__': sys.exit(main())

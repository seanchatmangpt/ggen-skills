#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
REQ_SECTIONS=['## Use when','## Inputs','## Procedure','## Output','## Falsifiers and refusals']
STANDINGS={'UNKNOWN','PARTIAL_ALIVE','ALIVE','BLOCKED','BUILD_BROKEN','UNSUPPORTED','REFUSED'}

def frontmatter(text):
    if not text.startswith('---\n'):
        raise ValueError('missing YAML frontmatter')
    end=text.find('\n---\n',4)
    if end<0: raise ValueError('unterminated YAML frontmatter')
    raw=text[4:end].splitlines(); out={}
    for line in raw:
        if ':' not in line: continue
        k,v=line.split(':',1); out[k.strip()]=v.strip()
    return out

def main():
    errors=[]
    lock=json.loads((ROOT/'SOURCE.lock.json').read_text())
    sha=lock['adaptedFrom']['commit']
    if not re.fullmatch(r'[0-9a-f]{40}',sha): errors.append('source lock commit is not a SHA-1')
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    if set(manifest['standingVocabulary']) != STANDINGS: errors.append('standing vocabulary drift')
    ontology=(ROOT/'ontology/ggen-skills.ttl').read_text()
    names=[]
    for p in sorted((ROOT/'skills').glob('*/SKILL.md')):
        text=p.read_text()
        try: fm=frontmatter(text)
        except ValueError as e: errors.append(f'{p}: {e}'); continue
        name=fm.get('name'); desc=fm.get('description','')
        if not name or name != p.parent.name: errors.append(f'{p}: name must match directory')
        if not desc or len(desc)<40: errors.append(f'{p}: description too weak')
        names.append(name)
        for section in REQ_SECTIONS:
            if section not in text: errors.append(f'{p}: missing {section}')
        banned=['has ambient DO authority','receives ambient DO authority','automatic DO authority is granted']
        if any(x.lower() in text.lower() for x in banned): errors.append(f'{p}: ambient DO authority grant')
        token=(name or '').replace('-','_')
        if token and f'gs:{token} ' not in ontology: errors.append(f'{p}: absent from ontology')
    if len(names)<20: errors.append(f'expected DfCM-maximal skill frontier >=20; got {len(names)}')
    if len(names)!=len(set(names)): errors.append('duplicate skill names')
    for required in ['aps-protocol','dfcm','ggen-first','brce-boundary','skill-creator-dfcm','skill-qualifier']:
        if required not in names: errors.append(f'missing kernel skill {required}')
    agents=(ROOT/'AGENTS.md').read_text().replace('`','')
    for phrase in ['SELECT, CONSTRUCT, and DO','Zero unreceipted actuation','Inspection is not execution']:
        if phrase not in agents: errors.append(f'AGENTS missing law: {phrase}')
    if errors:
        print('BUILD_BROKEN')
        for e in errors: print(' -',e)
        return 1
    print(f'ALIVE: {len(names)} skills structurally and constitutionally conformant')
    print(f'SOURCE: {sha}')
    print('GGEN_MANUFACTURING: PARTIAL_ALIVE (pack execution not yet observed)')
    return 0
if __name__=='__main__': sys.exit(main())

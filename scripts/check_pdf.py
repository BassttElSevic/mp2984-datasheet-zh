import hashlib,json,re
from pathlib import Path
import pypdf
root=Path(__file__).resolve().parents[1]
doc=root/'output/pdf/mp2984-zh.pdf'
r=pypdf.PdfReader(doc)
assert len(r.pages)==43
assert all((root/'pages'/('p%02d.tex'%n)).exists() for n in range(1,44))
assert all(abs(float(p.mediabox.width)-612)<0.1 and abs(float(p.mediabox.height)-792)<0.1 for p in r.pages)
log=(root/'output/pdf/main.log').read_text(encoding='utf8')
assert not any(t in log for t in ['Missing character','Overfull','Undefined control sequence'])
info={'pages':len(r.pages),'page_size_pt':[612,792],'source_sha256':hashlib.sha256((root/'assets/original.pdf').read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),'latex_missing_glyphs':False,'latex_overfull':False,'chinese_characters_per_page':[]}
for p in r.pages:
 count=len(re.findall('[\u4e00-\u9fff]',p.extract_text() or ''))
 assert count>15
 info['chinese_characters_per_page'].append(count)
(root/'output/verification.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in info.items() if k!='chinese_characters_per_page'},ensure_ascii=False,indent=2))

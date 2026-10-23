"""Inspect saved product metadata without loading whole catalogs into model context."""
import argparse
import json
from pathlib import Path
from trafa_client import chronological_year_values, is_year_dimension, year_bounds
from reference_metadata import REFERENCE_WARNING, validate_reference_selection


def expand(encoded):
    if encoded['encoding']=='explicit':return encoded['values']
    if encoded['encoding']=='year_ranges':
        return [{'code':f'{y:04d}','label':f'{y:04d}','description':''}
                for a,b in encoded['ranges_inclusive'] for y in range(a,b+1)]+encoded['special_values']
    raise ValueError('Unknown domain encoding')


def thematic_listing(catalog, themes):
    """Editorial display grouping; never interpret API insertion order as a theme."""
    groups = {}
    for code, product in catalog.items():
        theme = themes.get(code, 'Ej grupperad')
        manual = product.get('manual_enrichment') or {}
        groups.setdefault(theme, []).append({'product': code, 'label': product['label'],
            'label_enriched_proposed': manual.get('label_enriched_proposed')})
    return [{'theme': theme, 'products': sorted(products,
             key=lambda x: ((x['label_enriched_proposed'] or x['label']).casefold(), x['product']))}
            for theme, products in sorted(groups.items())]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent/'references'/'metadata')
    ap.add_argument('--search');ap.add_argument('--product');ap.add_argument('--variables',nargs='*')
    ap.add_argument('--values',action='store_true')
    ap.add_argument('--section', choices=['auto','overview','variables','profile','combinations','all'], default='auto',
                    help='Read only the needed section; auto shows variables when --variables is set, otherwise an overview')
    ap.add_argument('--list', action='store_true', help='Show editorial thematic product groups')
    ap.add_argument('--query', help='Exact query for dated, offline reference validation')
    ap.add_argument('--validate-reference', action='store_true',
                    help='Validate codes, parents, domains and one documented table without HTTP; permitted reference use does not assert current API availability')
    ap.add_argument('--lang', choices=['sv','en'], default='sv', help='Request language recorded in a reference-validation receipt')
    ap.add_argument('--output', type=Path, help='Save the reference-validation receipt as JSON')
    a=ap.parse_args()
    if a.validate_reference or a.query is not None:
        if not a.validate_reference or not a.query:
            ap.error('--query and --validate-reference must be used together')
        if a.list or a.search or a.product or a.variables is not None or a.values or a.section != 'auto':
            ap.error('Reference validation cannot be combined with lookup/section options')
        if a.output and a.output.resolve() in {
                (a.root/name).resolve() for name in
                ['variabelkatalog_kompakt.json','kombinationer.json','vardemangder.json']}:
            ap.error('--output must not overwrite reference metadata')
        try:
            result=validate_reference_selection(a.query,root=a.root,lang=a.lang)
        except ValueError as exc:
            ap.error(str(exc))
        rendered=json.dumps(result,ensure_ascii=False,indent=2)
        if a.output:
            a.output.parent.mkdir(parents=True,exist_ok=True)
            a.output.write_text(rendered+'\n',encoding='utf-8')
        print(rendered);return
    if a.output or a.lang != 'sv':
        ap.error('--output and --lang apply to --validate-reference')
    catalog=json.loads((a.root/'variabelkatalog_kompakt.json').read_text())
    if a.list:
        thematic_file = a.root/'produktgrupper_visning.json'
        themes = json.loads(thematic_file.read_text()) if thematic_file.exists() else {}
        result = {'grouping_status': 'editorial_navigation_not_official_api_taxonomy',
                  'groups': thematic_listing(catalog, themes.get('products', {}))}
    elif a.search:
        query=a.search.casefold().split();result=[]
        for code,p in catalog.items():
            manual=p.get('manual_enrichment') or {}
            words=' '.join([code,p['label'],manual.get('label_enriched_proposed',''),
                manual.get('publication_context',''),manual.get('population_description',''),
                ' '.join(manual.get('search_aliases',[]))]).casefold()
            if all(term in words for term in query):
                result.append({'product':code,'label':p['label'],
                    'label_enriched_proposed':manual.get('label_enriched_proposed'),
                    'metadata_usable':p.get('metadata_usable'),
                    'current_product_status':p.get('current_product_status'),
                    'checked_at_utc':p.get('api_checked_at_utc')})
    elif a.product:
        hits=[code for code in catalog if code.casefold()==a.product.casefold()]
        if len(hits)!=1:raise ValueError('Unknown or ambiguous product')
        code=hits[0];p=catalog[code]
        section = ('variables' if a.variables is not None else 'overview') if a.section=='auto' else a.section
        result={k:p.get(k) for k in ['label','current_product_status','metadata_usable','api_checked_at_utc']}
        result.update(product=code,warning=REFERENCE_WARNING)
        if section=='profile':
            result['manual_enrichment']=p.get('manual_enrichment')
            print(json.dumps(result,ensure_ascii=False,indent=2));return
        if section=='combinations':
            combos=json.loads((a.root/'kombinationer.json').read_text()).get(code,{})
            required=set(a.variables or [])
            result['combinations']=[x for x in combos.get('combinations',[]) if required.issubset(set(x.split('|')))]
            result['combination_source']=combos.get('source')
            result['interpretation']='Candidate tables: multiple listed measures need not all be requested. Validate the minimal required measures with the table dimensions.'
            print(json.dumps(result,ensure_ascii=False,indent=2));return
        if section=='overview':
            manual=p.get('manual_enrichment') or {}
            result.update(label_enriched_proposed=manual.get('label_enriched_proposed'),
                          product_role=manual.get('product_role'),
                          variables=[{k:v.get(k) for k in ['api_name','label','type','parent_name']} for v in p['variables']])
            print(json.dumps(result,ensure_ascii=False,indent=2));return
        domains=json.loads((a.root/'vardemangder.json').read_text())
        vs=[]
        for v in p['variables']:
            if a.variables and v.get('api_name') not in a.variables:continue
            out=dict(v);ref=v.get('value_set_ref')
            if ref:
                values=expand(domains[ref]['definition']);out['value_count']=len(values)
                if v.get('type') == 'D' and is_year_dimension(v.get('api_name'), v.get('label')):
                    values=chronological_year_values(values)
                    out.update(year_bounds(values))
                if a.values:out['values']=values
            vs.append(out)
        result['variables']=vs
        if section=='all':
            result.update(combination_source=p.get('combination_source'),manual_enrichment=p.get('manual_enrichment'))
    else:ap.error('Choose --list, --search or --product')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

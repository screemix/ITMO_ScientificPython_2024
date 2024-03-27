import requests
import json
import re


def get_uniprot(ids: list):
    return requests.get("https://rest.uniprot.org/uniprotkb/accessions", params={'accessions': ids})


def get_ensemble(ids: list):
    headers={ "Content-Type" : "application/json", "Accept" : "application/json"}
    data = {"ids": ids}
    return requests.post("https://rest.ensembl.org/lookup/id", headers=headers, data=json.dumps(data))


def parse_response_uniprot(resp: dict):
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError('Request failed. Status code: {}'.format(resp.status_code))
   
    resp = resp.json()
    resp = resp["results"]
    output = {}

    for val in resp:
        acc = val['primaryAccession']
        species = val['organism']['scientificName']
        gene = val['genes']
        seq = val['sequence']
        output[acc] = {'organism': species, 'gene_info': gene, 'sequence_info': seq, 'type': 'protein'}
        
    return output


def parse_response_ensemble(resp: dict):
    if resp.status_code != 200:
        raise requests.exceptions.HTTPError('Request failed. Status code: {}'.format(resp.status_code))
    
    resp = resp.json()
    output = {}
    for key, val in resp.items():
        species = val['species']
        gene = val['display_name']
        canonical_transcript = val['canonical_transcript']
        biotype = val['biotype']
        type_ = val['object_type']
        output[key] = {'organism': species, 'gene_info': gene, 'canonical_transcript': canonical_transcript, 'type': type_, 'biotype': biotype}
        
    return output


def get_and_parse(ids: list):
    
    if re.fullmatch('ENS([A-Z]{3}|[A-Z]{0})[A-Z]{1,2}[0-9]{11}', ids[0]):
        resp = get_ensemble(ids)
        return parse_response_ensemble(resp)
    
    elif re.fullmatch('[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}', ids[0]):
        resp = get_uniprot(ids)
        return parse_response_uniprot(resp)
    else:
        raise TypeError('Passed ids do not match neither ensemble nor uniprot id pattern') 
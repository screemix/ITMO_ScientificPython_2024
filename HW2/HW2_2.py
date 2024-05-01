import subprocess
from Bio import SeqIO
import requests
import json
import re

files = ["hw_file1.fasta", "hw_file2.fasta", "hw_file3.fasta"]
extension = "fasta"
full_results = {}

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
    # print(resp.items())
    for key, val in resp.items():
        species = val['species']
        gene = val['display_name']
        # if "canonical_transcript" in val:
        #     canonical_transcript = val['canonical_transcript']
        # else:
        #     canonical_transcript = ""
        biotype = val['biotype']
        type_ = val['object_type']
        # output[key] = {'organism': species, 'gene_info': gene, 'canonical_transcript': canonical_transcript, 'type': type_, 'biotype': biotype}
        output[key] = {'organism': species, 'gene_info': gene, 'type': type_, 'biotype': biotype}
        
    return output


def get_and_parse(ids: list):
    
    if re.fullmatch('ENS([A-Z]{3}|[A-Z]{0})[A-Z]{1,2}[0-9]{11}', ids[0]):
        resp = get_ensemble(ids)
        return parse_response_ensemble(resp)
    
    elif re.fullmatch('[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}', ids[0]):
        resp = get_uniprot(ids)
        return parse_response_uniprot(resp)
    else:
        return
        raise TypeError('Passed ids do not match neither ensemble nor uniprot id pattern') 


def seqkit_get_stats(stdout_raw: str):
    stdout_raw = stdout_raw.strip().split('\n')
    keys = stdout_raw[0].split()[1:]
    values = stdout_raw[1].split()[1:]
    seqkit_result = dict(zip(keys, values))

    return seqkit_result

def call_seqkit(filename: str):
    seqkit = subprocess.run(("seqkit", "stats", filename, "-a"),
                            capture_output=True, text=True)
    
    return seqkit

def get_biopy_info(sequences: SeqIO.FastaIO.FastaIterator):
    sequences_list = {}
    for seq in sequences:
        if file_type == "DNA":
            id = seq.id.split(".")[0]
            db = "ENSEBL"
        else:
            id = seq.id.split("|")[1]
            db = "UniProt"

        data = dict(get_and_parse([id]))
        data[id].update({"description": seq.description, "sequence": str(seq.seq), "database": db})
        sequences_list.update(data)
    
    return sequences_list

for file in files:
    full_results[file] = {}
    seqkit_result = call_seqkit(file)
    if seqkit_result.stderr == "":
        seqkit_stats = seqkit_get_stats(seqkit_result.stdout)
        file_type = seqkit_stats["type"]
        full_results[file]["seqkit_stats"] = seqkit_stats

        sequences = SeqIO.parse(file, extension)
        sequences_list  = get_biopy_info(sequences)
        full_results[file]["sequences_info"] = sequences_list
                
    else:
        full_results[file]["status"] = f"Error reading fasta file {file}: {seqkit_result.stderr}"


with open('hw2_2_result.json', 'w') as f:
    json.dump(full_results, f, indent=4)

print(json.dumps(full_results, indent=4))
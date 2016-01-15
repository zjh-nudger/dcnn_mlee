# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:13:49 2016

@author: tanfan.zjh
"""

import glob

def build_candidate_vocab(candidate_dir = 'MLEE_DATA/train-a2'):
    ##T2	Blood_vessel_development 69 81	angiogenesis
    candidate = set()
    for f in glob.glob(candidate_dir+'/*.a2'):
        input = open(f)
        for line in input.readlines():
            if line.startswith('T'):
                toks = line.split('\t')
                candidate.add(toks[2].strip().lower())
        input.close()

    candidate_output = open('candidate.txt','w')
    for word in candidate:
        candidate_output.write(word)
        candidate_output.write('\n')
    candidate_output.close()
    return candidate

candidate = build_candidate_vocab()

def process(file_dir,output_dir):
    for f in glob.glob(file_dir+'/*'):
        input = open(f)
        output = open(output_dir+'/'+f.split('.')[0].split('\\')[1]+'.gdep.ann','w')
        ## 1	Subretinal	Subretinal	B-NP	JJ	O	2	NMOD	0
        for line in input.readlines():
            toks = line.strip().split('\t')
            if len(line)==0 or len(toks)<5:
                output.write(line)
                continue
            if int(toks[8])>0:
                output.write(line.strip()+'\n')
                continue
            word = toks[1]
            if word.lower() in candidate:
                output.write(line.strip())
                output.write('\n')
            else:
                new_line = '\t'.join(toks[:8])+'\t'+'-1'
                output.write(new_line+'\n')
        output.close()

if __name__=='__main__':
    process('MLEE_DATA/train-gdep-trigger','MLEE_DATA/train-gdep-trigger-candidate')
            
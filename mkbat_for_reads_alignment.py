#!/usr/bin/python3
# coding = utf-8
# -*- coding: utf-8 -*-
#@Time  :  2020/3/25 16:29
#@Author: 'Lvmj'

import re, glob
path = '/home/*'
rawpath = path+'/raw' ####
bats = path+"/bats"
Ds_bams = path+"/Ds_bams"
trimmed_gtf_uniq = path+"/trimmed_gtf_uniq"
trimmed_seq = path+"/trimmed_seq"

R2 = glob.glob(rawpath+"/*.R2.fastq.gz")

for file in R2:
    filename = file.split("/")[-1].split(".")[0]

    fot = open("%s/%s.fr.bat" %(bats, filename), 'w')
    cmd1 = "bowtie2 -p 10 --local  -x Ds.index" \
           " -U %s| samtools sort -O bam -@ 10 -o - > %s/%s.sorted.bam\n" %(file, Ds_bams ,filename)
    cmd2 = "samtools view -h %s/%s.sorted.bam > %s/%s.sorted.sam\n" %(Ds_bams, filename, Ds_bams, filename)
    cmd3 = "python3 extract_trimmed_seq_from_sam.3.py " \
           "%s/%s.sorted.sam %s/%s.trimmed3.fa\n" %(Ds_bams, filename, trimmed_seq, filename)
    cmd4 = "python3 extract_trimmed_seq_from_sam.5.py " \
           "%s/%s.sorted.sam %s/%s.trimmed5.fa\n" %(Ds_bams, filename, trimmed_seq, filename)
    cmd5 = "bowtie2 -p 10 --end-to-end -x Zea_mays.AGPv4.37.index  " \
           "-f %s/%s.trimmed3.fa | samtools sort -O bam -@ 10 -o - > %s/%s.trimmed3.sorted.bam\n" %(trimmed_seq, filename, trimmed_seq, filename)
    cmd6 = "bowtie2 -p 10 --end-to-end -x Zea_mays.AGPv4.37.index  " \
           "-f %s/%s.trimmed5.fa | samtools sort -O bam -@ 10 -o - > %s/%s.trimmed5.sorted.bam\n" %(trimmed_seq, filename, trimmed_seq, filename)
    cmd7 = "samtools view -hF4 %s/%s.trimmed3.sorted.bam |grep -v \"XS:i\"|samtools view -Sb -o %s/%s.trimmed3.uniq.sorted.bam -\n" %(trimmed_seq, filename, trimmed_seq, filename)
    cmd8 = "samtools view -hF4 %s/%s.trimmed5.sorted.bam |grep -v \"XS:i\"|samtools view -Sb -o %s/%s.trimmed5.uniq.sorted.bam -\n"  %(trimmed_seq, filename, trimmed_seq, filename)
    cmd11 = "stringtie -p 4 --fr -m 70 -g 100 -s 2 %s/%s.trimmed3.uniq.sorted.bam -o %s/%s.uniq.3.gtf\n" %(trimmed_seq, filename, trimmed_gtf_uniq, filename)
    cmd12 = "stringtie -p 4 --fr -m 70 -g 100 -s 2 %s/%s.trimmed5.uniq.sorted.bam -o %s/%s.uniq.5.gtf\n" %(trimmed_seq, filename, trimmed_gtf_uniq, filename)
    fot.write(cmd1+cmd2+cmd3+cmd4+cmd5+cmd6+cmd7+cmd8+cmd11+cmd12)
    

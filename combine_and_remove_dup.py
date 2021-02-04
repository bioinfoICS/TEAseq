#!/usr/bin/python3
# coding = utf-8
# -*- coding: utf-8 -*-
#@Time  :  2019/12/10 22:28
#@Author: 'Lvmj'

import re, glob, os

# unique mapped reads of each sample
uniq_reads = {}
fin_uniq = open("unique_reads_numbers_information.txt", 'r')
for line in fin_uniq:
    line = line.strip("\n")
    _line = line.split("\t")
    sample = _line[0]
    r3 = int(_line[1])
    r5 = int(_line[2])
    if sample.startswith('B'):
        sample = re.sub(r'^B', '17A', sample)
        uniq_reads[sample] = [r3, r5]
    else:
        uniq_reads[sample] = [r3, r5]

# file size information of each sample
fin1 = open("filesize.information.txt", 'r')
size = {}
for line in fin1:
    line = line.strip("\n")
    _line = line.split("\t")
    sample = _line[0].split('.')[0]
    m = _line[1]
    if sample.startswith('B'):
        sample = re.sub(r'^B', '17A', sample)
        size[sample] = m
    else:
        size[sample] = m
###lpm threshold

p_lpm3 = 100
p_lpm5 = 100


loci = []
news3 = glob.glob('*3.uniq.gtf')
samples = []
for new in news3:
    sample = os.path.basename(new).split('.')[0]
    if float(size[sample]) > 25:
        if sample not in samples:
            # print(sample)
            samples.append(sample)
        fin = open(new, 'r')
        for line in fin:
            _line = line.strip("\n").split("\t")
            Chr = _line[0]
            start = int(_line[3])
            end = int(_line[4])
            strand = _line[6]
            # lpm = int(float(re.match(r'.*?lpm \"(.+?)\".*', _line[8]).group(1)))
            cov = int(float(re.match(r'.*?cov \"(.+?)\".*', _line[8]).group(1)))
            lpm = int(cov*1000000/uniq_reads[sample][0])
            if strand == "+":
                locus = Chr + ":" + str(start)
            else:
                locus = Chr + ":" + str(end)
            if lpm >= p_lpm3:  ####lpm过滤
                if locus not in loci:
                    loci.append(locus)
        fin.close()


news5 = glob.glob('*5.uniq.gtf')
for new in news5:
    sample = os.path.basename(new).split('.')[0]
    if float(size[sample]) > 25:
        if sample not in samples:
            samples.append(sample)
        fin = open(new, 'r')
        for line in fin:
            _line = line.strip("\n").split("\t")
            Chr = _line[0]
            start = int(_line[3])
            end = int(_line[4])
            strand = _line[6]
            cov = int(float(re.match(r'.*?cov \"(.+?)\".*', _line[8]).group(1)))
            lpm = int(cov*1000000/uniq_reads[sample][1])
            if strand == "+":
                locus = Chr + ":" + str(end)
            else:
                locus = Chr + ":" + str(start)
            if lpm >= p_lpm5:  ####lpm过滤
                if locus not in loci:
                    loci.append(locus)
        fin.close()

locus_lpm = {}
locus_ft = {}
locus_pm = {}
news3 = glob.glob('*3.uniq.gtf')
for new in news3:
    sample = os.path.basename(new).split('.')[0]
    # if sample in Over25M:
    if sample in samples:
        if sample not in locus_lpm:
            locus_lpm[sample] = {}
            # print(locus_ft)
            locus_ft[sample] = {}
            locus_pm[sample] = {}

        fin = open(new, 'r')
        for line in fin:
            _line = line.strip("\n").split("\t")
            Chr = _line[0]
            start = int(_line[3])
            end = int(_line[4])
            strand = _line[6]
            if strand == "+":
                locus = Chr + ":" + str(start)
                locus_pm[sample][locus] = '+'

            else:
                locus = Chr + ":" + str(end)
                locus_pm[sample][locus] = '-'

            cov = int(float(re.match(r'.*?cov \"(.+?)\".*', _line[8]).group(1)))
            lpm = int(cov*1000000/uniq_reads[sample][0])
            if lpm >= p_lpm3:  ####lpm过滤
                locus_lpm[sample][locus] = lpm
                locus_ft[sample][locus] = '3'
        fin.close()

news5 = glob.glob('*5.uniq.gtf')
for new in news5:
    sample = os.path.basename(new).split('.')[0]
    if sample in samples:
        if sample not in locus_lpm:
            locus_lpm[sample] = {}
            locus_ft[sample] = {}
            locus_pm[sample] = {}

        fin = open(new, 'r')
        for line in fin:
            _line = line.strip("\n").split("\t")
            Chr = _line[0]
            start = int(_line[3])
            end = int(_line[4])
            strand = _line[6]
            if strand == "+":
                locus = Chr + ":" + str(end)
                locus_pm[sample][locus] = '+'

            else:
                locus = Chr + ":" + str(start)
                locus_pm[sample][locus] = '-'

            cov = int(float(re.match(r'.*?cov \"(.+?)\".*', _line[8]).group(1)))
            lpm = int(cov*1000000/uniq_reads[sample][1])
            if lpm >= p_lpm5:   ####lpm过滤
                locus_lpm[sample][locus] = lpm
                locus_ft[sample][locus] = '5'
        fin.close()


fot = open('final.combined.txt', 'w')

fot.write('Chr\tpos\t3or5\tstrand\t'+'\t'.join(samples)+"\tsample_num\tsample_list\n")

print(len(loci), len(samples))
for locus in loci:
    Chr = locus.split(":")[0]
    pos = locus.split(":")[1]
    # print(locus)
    fot.write(Chr+"\t"+pos)
    for sample in samples:
        if locus in locus_ft[sample]:
            fot.write("\t"+locus_ft[sample][locus]+"\t"+locus_pm[sample][locus])
            break
    # fot.write(locus)
    mut_samples = []
    for sample in samples:
        # print(sample)
        if locus not in locus_lpm[sample]:
            fot.write('\t0')
        else:
            fot.write("\t"+str(locus_lpm[sample][locus]))
            mut_samples.append(sample)

    fot.write("\t" + str(len(mut_samples)) + "\t" + ";".join(mut_samples) + "\n")

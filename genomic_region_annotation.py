#!/usr/bin/python3
# coding = utf-8
# -*- coding: utf-8 -*-
#@Time  :  2020/1/8 10:52
#@Author: 'Lvmj'

import re, glob, os, sys

print("start index genome!")
file_maxiso = open("Zea_mays.AGPv4.37.maxiso.txt", 'r')
maxiso = {}
file_maxiso.readline()
for line in file_maxiso:
    _line = line.strip("\n").split("\t")
    maxiso[_line[0]] = _line[1]
    #

gtf = open("Zea_mays.AGPv4.37.Chr.gtf", 'r')
exon_info = {}
CDS_info = {}
for line in gtf:
    line = line.strip("\n")
    _line = line.split("\t")
    if _line[2] == 'exon':
        tid = re.match(r'.*transcript_id \"(.+?)\";', _line[8]).group(1)
        gid = re.match(r'.*gene_id \"(.+?)\";', _line[8]).group(1)
        if tid == maxiso[gid]:
            # print(tid)
            chr = _line[0]
            start = int(_line[3])
            end = int(_line[4])
            strand = _line[6]
            # info[gid] = chr+'_'+str(location)+'_'+str(end)
            if tid not in exon_info:
                exon_info[tid] = [chr, strand, start, end]
            else:
                exon_info[tid].append(start)
                exon_info[tid].append(end)

    elif _line[2] == 'CDS':
        tid = re.match(r'.*transcript_id \"(.+?)\";', _line[8]).group(1)
        gid = re.match(r'.*gene_id \"(.+?)\";', _line[8]).group(1)
        if tid == maxiso[gid]:
            chr = _line[0]
            start = int(_line[3])
            end = int(_line[4])
            strand = _line[6]
            # info[gid] = chr+'_'+str(location)+'_'+str(end)
            if tid not in CDS_info:
                CDS_info[tid] = [chr, strand, start, end]
            else:
                CDS_info[tid].append(start)
                CDS_info[tid].append(end)

dic = {}
for tid in CDS_info:
    for i in range(int((len(CDS_info[tid])-2)/2)):
        # print(tid,i)
        for j in range(CDS_info[tid][2*i+2], CDS_info[tid][2*i+3]+1):
            dic[CDS_info[tid][0] + "_" + str(j)] = [tid, "CDS"]
    if CDS_info[tid][1] == "-":
        for i in range(exon_info[tid][2], CDS_info[tid][2]):
            dic[CDS_info[tid][0] + "_" + str(i)] = [tid, "3_UTR"]
        for i in range(CDS_info[tid][-1]+1, exon_info[tid][-1]+1):
            dic[CDS_info[tid][0] + "_" + str(i)] = [tid, "5_UTR"]
    else:
        for i in range(exon_info[tid][2], CDS_info[tid][2]):
            dic[CDS_info[tid][0] + "_" + str(i)] = [tid, "5_UTR"]
        for i in range(CDS_info[tid][-1]+1, exon_info[tid][-1]+1):
            dic[CDS_info[tid][0] + "_" + str(i)] = [tid, "3_UTR"]
            
    for i in range(int((len(exon_info[tid])-4)/2)):
        for j in range(exon_info[tid][2*i+3]+1, exon_info[tid][2*i+4]):
            dic[exon_info[tid][0] + "_" + str(j)] = [tid, "intron"]


for tid in exon_info:
    if exon_info[tid][1] == "-":
        for i in range(exon_info[tid][-1]+1, exon_info[tid][-1]+2000):
            if exon_info[tid][0] + "_" + str(i) not in dic:
                dic[exon_info[tid][0] + "_" + str(i)] = [tid, "upstream"]
        for i in range(exon_info[tid][2]-2000, exon_info[tid][2]):
            if exon_info[tid][0] + "_" + str(i) not in dic:
                dic[exon_info[tid][0] + "_" + str(i)] = [tid, "downstream"]
    else:
        for i in range(exon_info[tid][-1]+1, exon_info[tid][-1]+2000):
            if exon_info[tid][0] + "_" + str(i) not in dic:
                dic[exon_info[tid][0] + "_" + str(i)] = [tid, "downstream"]
        for i in range(exon_info[tid][2]-2000, exon_info[tid][2]):
            if exon_info[tid][0] + "_" + str(i) not in dic:
                dic[exon_info[tid][0] + "_" + str(i)] = [tid, "upstream"]
file = sys.argv[1]
fileout = re.sub(r'txt$', 'annotation.txt', file)
fin = open(file, 'r')
fot = open(fileout, 'w')
ti = fin.readline().strip("\n")
fot.write(ti+"\tgeneid\tregion\n")

for line in fin:
    line = line.strip("\n")
    _line = line.split("\t")
    chr = _line[0]
    location = int(_line[1])
    downstream = None
    upstream = None
    key = chr + "_" + str(location)
    if key in dic:
        fot.write(line + "\t" + dic[key][0] + "\t" + dic[key][1] + "\n")
    else:
        fot.write(line + "\tNA\tintergenic\n")

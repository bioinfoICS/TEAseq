#!/usr/bin/python3
# coding = utf-8
# -*- coding: utf-8 -*-
#@Time  :  2020/4/13 15:02
#@Author: 'Lvmj'

import re

fot = open(path+"/TSD.txt", 'w')
filename = "final.combined.LPM500.txt"
fin = open(filename, 'r')
fot1 = open(path+"/"+re.sub(r'txt$', 'rmdup.txt', filename), 'w')
fot1.write(fin.readline())
dic = {}
dic1 = {}
for line in fin:
    line = line.strip("\n")
    _line = line.split("\t")
    chr = _line[0]
    locus = int(_line[1])
    key = chr+'_'+str(locus)
    if chr not in dic:
        dic[chr] = [locus]
    else:
        dic[chr].append(locus)
    dic1[key] = _line

for chr in dic:
    lst = dic[chr]
    lst.sort()
    dic[chr] = lst

for chr in dic:
    # print(chr)
    for i in range(len(dic[chr])-1):
        if abs(dic[chr][i] - dic[chr][i+1]) < 10 and abs(dic[chr][i] - dic[chr][i+1]) > 3:
            print(chr)
            # fot1.write("\t".join(dic1[chr + '_' + str(dic[chr][i])]) + "\n")
            # fot1.write("\t".join(dic1[chr + '_' + str(dic[chr][i])][0:4]))
            fot1.write(dic1[chr + '_' + str(dic[chr][i])][0] + "\t" + dic1[chr + '_' + str(dic[chr][i])][1] +"-" + dic1[chr + '_' + str(dic[chr][i+1])][1] + "\tboth\t"+dic1[chr + '_' + str(dic[chr][i])][3])
            for j in range(4, len(dic1[chr + '_' + str(dic[chr][i])])-5):
                if int(dic1[chr + '_' + str(dic[chr][i])][j]) < int(dic1[chr + '_' + str(dic[chr][i+1])][j]):
                    fot1.write("\t" + dic1[chr + '_' + str(dic[chr][i+1])][j])
                else:
                    fot1.write("\t" + dic1[chr + '_' + str(dic[chr][i])][j])
            fot1.write("\t"+str(len(list(set(
                                                               dic1[chr + '_' + str(dic[chr][i])][-4].split(';') +
                                                               dic1[chr + '_' + str(dic[chr][i + 1])][-4].split(';')))))+"\t"+
                       ';'.join(list(set(dic1[chr+'_'+str(dic[chr][i])][-4].split(';') + dic1[chr+'_'+str(dic[chr][i+1])][-4].split(';'))))+"\t"+
                       "\t".join(dic1[chr + '_' + str(dic[chr][i])][-3:-1]))
            fot1.write("\t.\n")
            # if abs(dic[chr][i] - dic[chr][i+1]) == 7:
            fot.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %(chr, dic[chr][i], dic[chr][i+1],
                                                           len(list(set(
                                                               dic1[chr + '_' + str(dic[chr][i])][-4].split(';') +
                                                               dic1[chr + '_' + str(dic[chr][i + 1])][-4].split(';')))),
                                                  ';'.join(list(set(dic1[chr+'_'+str(dic[chr][i])][-4].split(';') + dic1[chr+'_'+str(dic[chr][i+1])][-4].split(';')))),
                                                  dic1[chr + '_' + str(dic[chr][i])][-3],dic1[chr+'_'+str(dic[chr][i])][-2],dic1[chr+'_'+str(dic[chr][i])][-1]))
            # fot.write("%s\t%s\t%s\t%s\n" %(chr, dic[chr][i], dic[chr][i+1], dic1[chr+'_'+str(dic[chr][i+1])]))
        elif abs(dic[chr][i] - dic[chr][i-1]) < 10 and abs(dic[chr][i] - dic[chr][i-1]) > 3:
            continue
        else:
            if chr in dic_combine:
                for loci in dic_combine[chr]:
                    # print(chr, loci)
                    if abs(dic[chr][i]-int(loci)) < 5:
                        fot_k17.write("\t".join(dic1[chr + '_' + str(dic[chr][i])])+"\n")
                        break
                fot1.write("\t".join(dic1[chr + '_' + str(dic[chr][i])])+"\n")

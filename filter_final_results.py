#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-
# @author lvmin
# @time 2020/11/5 10:42

fin = open("final.combined.txt", 'r')
fot = open("final.combined.LPM500.txt", 'w')
key = 500
_ti = fin.readline().strip("\n").split("\t")
fot.write("\t".join(_ti[:-2])+"\tMax_LPM\tsample_num\tsample_list\n")
for line in fin:
    line = line.strip("\n")
    _line = line.split("\t")
    maxlpm = max(map(int, _line[4:len(_line)-2]))
    # print(maxlpm)
    if int(_line[-2]) == 1:
        if maxlpm >= key:
            fot.write("\t".join(_line[:-2])+"\t"+str(maxlpm)+"\t"+_line[-2]+"\t"+_line[-1]+"\n")
        else:
            # print("yes")
            continue
    else:
        fot.write("\t".join(_line[:-2]) + "\t" + str(maxlpm) + "\t" + _line[-2] + "\t" + _line[-1] + "\n")


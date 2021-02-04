#!/usr/bin/python3
# coding = utf-8
# -*- coding: utf-8 -*-
#@Time  :  2020/3/20 9:11
#@Author: 'Lvmj'

import os, sys

g_file_out = None
def append_sequence_to_output(name, seq):
    global g_file_out
    g_file_out.write(">" + name + "\n")
    g_file_out.write(seq + "\n")
    return

def sam_cigar_split(sam_cigar):

    list_digit = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    list_alphabet = ["M", "I", "D", "N", "S", "H", "P", "=", "X"]

    list_split = []

    number_current = 0

    if (len(sam_cigar) == 0):
        return list_split

    for character in sam_cigar:
        if (character in list_digit):
            digit = int (character)
            number_current = (10 * number_current) + digit
        elif (character in list_alphabet):
            if (number_current > 0):
                list_split.append((number_current, character))
            number_current = 0

    return list_split



def main():
    global g_file_out
    file_in_sam = sys.argv[1]
    file_out_fa = sys.argv[2]
    g_file_out = open(file_out_fa, 'w')
    f = open(file_in_sam, "r")
    for line in f:
        line = line.rstrip("\n\r")
        if (len (line) == 0):
            continue
        if (line.startswith ("@")):
            continue
        list_sam_field = line.split("\t")
        sam_qname = list_sam_field[0]
        sam_flag = int(list_sam_field[1])
        sam_rname = list_sam_field[2]
        sam_pos = int(list_sam_field[3])
        sam_mapq = int(list_sam_field[4])
        sam_cigar = list_sam_field[5]
        sam_rnext = list_sam_field[6]
        sam_pnext = int(list_sam_field[7])
        sam_tlen = int(list_sam_field[8])
        sam_seq = list_sam_field[9]
        sam_qual = list_sam_field[10]
        if sam_flag == 4:
            continue
        else:
           # if sam_cigar == "72M78S":
           #     seq_trim = sam_seq[72:150]
           #     append_sequence_to_output(sam_qname, seq_trim)
            if sam_cigar == "75S75M":
                seq_trim = sam_seq[0:75]
                append_sequence_to_output(sam_qname, seq_trim)
    f.close()


if __name__ == '__main__':
    main()
    sys.exit()

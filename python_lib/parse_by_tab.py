#!/usr/bin/env python3
import sys

file_path = sys.argv[1]


def translate_string_to_hex(str_arr):
    # hex(ord("\t"))
    for splitted in str_arr:
        index = 0
        for part in splitted:
            index += 1
            print('str' + str(index)+':' + "|{0}|".format(part))
            hex_arr = []
            for char in part:
                hex_arr.append(char + '(' + hex(ord(char)) + ')')
            print("-->hex" + str(index) + ':' + ''.join(hex_arr))
        print("=====================")


with open(file_path, 'r') as f:
    input_lines = f.readlines()
    splitted_arr = [line.split('\t') for line in input_lines]
    translate_string_to_hex(splitted_arr)

#!/usr/bin/env python
import multiprocessing as mp
import os
import random
import string
import sys

__nproc = mp.cpu_count()

file_name = "EQY_US_ALL_TRADE_ADMIN_20180202.txt"

def _process_wrapper(input_file_name, chunkStart, chunkSize, process_func):
    with open(input_file_name, 'r') as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            process_func(line)
        return "{start}-{end} processed".format(start = chunkStart, end = chunkStart + chunkSize)

def _chunkify(fname,size=1024*1024):
    import pdb
    pdb.set_trace()
    fileEnd = os.path.getsize(fname)
    with open(fname,'r') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size + chunkStart, 0)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

def process_large_file(input_file_name, process_func, size):
    pool = mp.Pool(__nproc)
    jobs = []

    #create jobs
    for chunkStart,chunkSize in _chunkify(input_file_name, size):
        print(chunkStart,chunkSize)
        jobs.append(pool.apply_async(_process_wrapper,(input_file_name, chunkStart,chunkSize, process_func)) )

    #wait for all jobs to finish
    return_result_array = []
    for job in jobs:
        return_result_array.append(job.get())

    #clean up
    pool.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help = "file full abs path with name", type = str) # type is defaulted to str
    parser.add_argument("size", help = "chunk byte size", type = str) # type is defaulted to str
    args = parser.parse_args()

    def _print_operation(x):
        print('processing {0}'.format(x))
    process_large_file(args.file_name, _print_operation, int(args.size))

#!/usr/bin/env python
import argparse,ROOT,os
parser = argparse.ArgumentParser(add_help=False, description='run histos')
parser.add_argument( '--rescale', dest='rescale',action='store_true',default=False,help='Rescale xsec')
parser.add_argument('input')
args = parser.parse_args()
for line in open(args.input):
    cmd = './makeHistosFromNTUP.py '+line.rstrip()
    if args.rescale:
        cmd+=' --rescale'
    os.system(cmd)

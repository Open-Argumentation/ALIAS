#!/usr/bin/env python3

from os import listdir
import alias
import subprocess
import json

path = '/home/szczocik/Workspaces/Benchmark/B/1/'
#test = {}
#for f in listdir(path):
#    af = alias.read_tgf(path+f)
#    test[f] = {'args': af.get_args_count(), 'attacks': af.get_attacks_count()}
#sorted_dict = sorted(test.items(),key=lambda x: x[1]['args'],reverse=False)

sorted_dict = []

with open('/home/szczocik/Workspaces/bFiles.json', 'r') as file:
    sorted_dict = json.load(file)
    # json.dump(sorted_dict, file)
count = 0
for k, v in sorted_dict:
    count += 1
    print('\n----------------------------\n')
    print('Processing file: ' + str(count) + '/' + str(len(sorted_dict)))
    cmd = '/home/szczocik/Workspaces/alias/stableBenchmark.py ' + path + k
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    out, err = process.communicate()
    print(out)
    print(err)


pref_files = []

path = '/home/szczocik/Workspaces/Benchmark/A/1/'

with open('/home/szczocik/Workspaces/prefFiles.json', 'r') as file:
    pref_files = json.load(file)

count = 0
for k,v in pref_files:
    count += 1
    print('\n----------------------------\n')
    print('Processing file: ' + str(count) + '/' + str(len(pref_files)))
    cmd = '/home/szczocik/Workspaces/alias/prefBenchmark.py ' + path + k
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    out, err = process.communicate()
    print(out)

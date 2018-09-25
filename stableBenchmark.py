#!/usr/bin/env python3

import alias
import sys
import time
import signal

def write_to_file(text):
    with open('/home/szczocik/Workspaces/benchmarkScript/alias/results/20180922_stable_results.csv', 'a') as file:
        file.write(text)

def signal_handler(signum, frame):
    raise Exception("Timed out!")

start_r = time.time()
af = alias.read_tgf(sys.argv[1])
end_r = time.time()

signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(1200)
start = time.time()
try:
    stable = af.get_stable_extension()
    end = time.time()
except Exception as e:
    end = time.time()
    stable = e
    write_to_file(sys.argv[1] + ';' + str(af.get_args_count()) + ';' + str(af.get_attacks_count()) + ';' + str(end_r - start_r) + ';' + str(end - start) + ';' + str(stable) + '\n')

write_to_file(sys.argv[1] + ';' + str(af.get_args_count()) + ';' + str(af.get_attacks_count()) + ';' + str(end_r - start_r) + ';' + str(end - start) + ';' + str(stable) + '\n')

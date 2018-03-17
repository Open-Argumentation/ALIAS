import time

from ArgTest import ArgumentationFramework

filename1 = 'A/1/brookings-or-us.gml.50.tgf' # 12 | 18 | 0.02 seconds
filename2 = 'A/1/rockland-county-department-of-public-transportation_20121220_2018.gml.20.tgf' # 16 | 30 | 0.26 seconds
filename3 = 'A/1/caravan-or-us.gml.80.tgf' # 19 | 37 | 2.35 seconds
# Don't use the files below until you are sure it can handle them
filename4 = 'A/1/BA_40_80_5.tgf' # 41 | 73
filename5 = 'A/1/ferry2.pfile-L2-C1-08.pddl.1.cnf.tgf' # 86 | 136
filename6 = 'A/2/BA_60_60_3.tgf' # 41 | 73
filename7 = 'A/4/admbuster_200000.tgf' # 200000 | 299998
filename8 = 'A/5/BA_80_80_2.tgf' # 81 | 145
filename9 = 'B/1/admbuster_2000.tgf' # 2000 | 2998
filename10 = 'A/1/afinput_exp_acyclic_indvary1_step5_batch_yyy04.tgf' # 26 | 90

f = filename5

print('Reading file ' + f)
start = time.time()
af = ArgumentationFramework.read_tgf('/home/szczocik/Workspaces/Benchmark/' + f)
end = time.time()
print('File read in ' + str(end - start) + ' seconds')
print('Argumentation framework has ' + str(len(af.arguments)) + ' arguments')
print('Argumentation framework has ' + str(len(af.attacks)) + ' attacks')
print(af)

start = time.time()
print(af.get_stable_extension_test_1())
end = time.time()
print('stable extension done in ' + str(end - start) + ' seconds')


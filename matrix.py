import alias
import time
#
# af = alias.ArgumentationFramework('test')
# af.add_argument('0')
# af.add_argument('1')
# af.add_argument('2')
# af.add_argument('3')
# af.add_argument('4')
# af.add_attack(['0', '1'])
# af.add_attack(['1', '2'])
# af.add_attack(['1', '4'])
# af.add_attack(['3', '2'])
# af.add_attack(['4', '3'])
#
# cf = af.admissible_from_matrix()
# # print('Length of conflict free set is ' + str(len(cf)))
# print(cf)

#
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

f = filename1

print('Reading file ' + f)
start = time.time()
af = alias.read_tgf('/home/szczocik/Workspaces/Benchmark/' + f)
end = time.time()
print('File read in ' + str(end - start) + ' seconds')
print('Argumentation framework has ' + str(len(af.get_arguments())) + ' arguments')
print('Argumentation framework has ' + str(len(af.get_attacks())) + ' attacks')
print(af.get_arguments())

print(af.is_admissible(['a1', 'a12', 'a5']))

# start = time.time()
# powerSet = alias.ArgumentationFramework.power_set(af)
# end = time.time()
# print('Conflict Free Set of size ' + str(powerSet) + ' created in ' + str(end - start) + ' seconds')
#
# start = time.time()
# powerSet = alias.ArgumentationFramework.power_set_original(af)
# end = time.time()
# print('Conflict Free Set original of size ' + str(powerSet) + ' created in ' + str(end - start) + ' seconds')
#
# args = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19]
# print('Constructing conflict free sets')
# start = time.time()
# cf = af.conflict_free_from_matrix()
# end = time.time()
# print('Conflict free sets  done in ' + str(end - start) + ' seconds')
# #print(cf)
# print('Length of conflict free set is ' + str(len(cf)))


# test from the paper:
# arguments: a, b, c, d
# attacks: (a,b), (b,a), (b,c), (c,d), (d,c)
# complete extension: empty set, {a}, {d}, {a,c}, {a,d}, {b,d}
# af = alias.ArgumentationFramework('complete')
# af.add_argument('a')
# af.add_argument('b')
# af.add_argument('c')
# af.add_argument('d')
# af.add_attack(['a', 'b'])
# af.add_attack(['b', 'a'])
# af.add_attack(['b', 'c'])
# af.add_attack(['c', 'd'])
# af.add_attack(['d', 'c'])
# # print(alias.ArgumentationFramework.admissible_from_matrix(af))
# print(af.matrix)
# print(alias.extension_complete(af))

# print(alias.ArgumentationFramework.test(af))


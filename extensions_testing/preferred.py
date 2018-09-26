import time

import alias
from alias import ArgumentationFramework
# stable extensions
path = '/home/szczocik/Workspaces/Benchmark/A/'

# filenames                                                                                     # arguments | attacks   | solutions from pyglaf
filename1 = '1/massachusetts_vineyardfastferry_2015-11-13.gml.50.tgf'                           # 3         | 2         |
filename2 = '1/afinput_exp_cycles_indvary3_step8_batch_yyy07.tgf'                               # 15        | 1         |
filename3 = '1/hut-airport-shuttle_20120105_0729.gml.50.tgf'                                    # 7         | 7         |
filename4 = '1/brookings-or-us.gml.50.tgf'                                                      # 12        | 18        |
filename5 = '1/rockland-county-department-of-public-transportation_20121220_2018.gml.20.tgf'    # 16        | 30        |
filename6 = '1/caravan-or-us.gml.80.tgf'                                                        # 19        | 37        |
filename7 = '1/BA_60_70_3.tgf'                                                                  # 61        | 102          |
filename8 = '1/ferry2.pfile-L3-C2-02.pddl.2.cnf.tgf'                                            # 528       | 1012
filename9 = '3/stb_496_268.tgf'

# full pat
file = path + filename3
print('Reading file')
start = time.time()
af = alias.read_tgf(file)
end = time.time()
print('------------------------------------------------------------------')
print('File read in ' + str(end - start) + ' seconds')
print('Number of arguments: ' + str(len(af.arguments)))
print('Number of attacks: ' + str(len(af.attacks)))

print('Creating Preferred Extension')
start = time.time()
gr = af.get_complete_extension()
pr = af.get_preferred_extension()
# gr = af.test_of_parallel_dictionaries()
# gr = af.SatSolver()
end = time.time()
print(gr)
print(pr)
print('Preferred Extension created in ' + str(end - start) + ' seconds')
print('------------------------------------------------------------------')
# af.draw_graph()
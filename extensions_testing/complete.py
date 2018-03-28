import time

import alias
from alias import ArgumentationFramework
# stable extensions
path = '/home/szczocik/Workspaces/Benchmark/A/'

# filenames                                                                                     # arguments | attacks   | solutions from pyglaf
filename1 = '1/massachusetts_vineyardfastferry_2015-11-13.gml.50.tgf'                           # 2         | 1         | [a1]
filename2 = '1/afinput_exp_cycles_indvary3_step8_batch_yyy07.tgf'                               # 15        | 1         | [11,12,13,14,0,1,2,3,4,5,6,7,8,10]
filename3 = '1/hut-airport-shuttle_20120105_0729.gml.50.tgf'                                    # 7         | 7         | [a1,a2,a5,a6]
filename4 = '1/brookings-or-us.gml.50.tgf'                                                      # 12        | 18        | [a10,a5],[a1,a11,a10,a5,a7],[a1,a11,a10,a12,a5,a7],[a1,a11,a10,a5,a6,a7],[a10,a5,a6],[a10,a3,a5,a6,a8,a9]
filename5 = '1/rockland-county-department-of-public-transportation_20121220_2018.gml.20.tgf'    # 16        | 30        | [a12,a16],[a13,a12,a16,a8,a9],[a13,a12,a15,a16,a2,a8,a9],[a13,a12,a16,a1,a4,a8,a9]
filename6 = '1/caravan-or-us.gml.80.tgf'                                                        # 19        | 37        | massive

# full path
file = path + filename6
print('Reading file')
start = time.time()
af = alias.read_tgf(file)
end = time.time()
print('------------------------------------------------------------------')
print('File read in ' + str(end - start) + ' seconds')
print('Number of arguments: ' + str(len(af.arguments)))
print('Number of attacks: ' + str(len(af.attacks)))

print('Creating Complete Extension')
start = time.time()
gr = af.get_complete_extension()
end = time.time()
print(gr)
print('Complete Extension created in ' + str(end - start) + ' seconds')
print('------------------------------------------------------------------')
af.draw_graph()
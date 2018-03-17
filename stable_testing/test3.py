import time

from ArgTest import ArgumentationFramework
# stable extensions
path = '/home/szczocik/Workspaces/Benchmark/C/'

# filenames                                                             # arguments | attacks
filename1 = '1/massachusetts_cuttyhunkferryco_2015-11-13.gml.50.tgf'    # 2         | 2
filename2 = '1/afinput_exp_acyclic_indvary3_step4_batch_yyy05.tgf'      # 15        | 2
filename3 = '1/afinput_exp_acyclic_indvary3_step7_batch_yyy09.tgf'      # 14        | 4
filename4 = '1/afinput_exp_acyclic_indvary1_step5_batch_yyy07.tgf'      # 26        | 27
filename5 = '1/admbuster_1000.tgf'                                      # 1000      | 1498



# full path
file = path + filename1
print('Reading file')
start = time.time()
af = ArgumentationFramework.read_tgf(file)
end = time.time()
print('File read in ' + str(end - start) + ' seconds')

# af.draw_graph()
print('Number of arguments: ' + str(len(af.arguments)))
print('Number of attacks: ' + str(len(af.attacks)))

print('Creating Grounded Extension')
start = time.time()
gr = af.get_grounded_labelling()
end = time.time()
print(gr)
print('Grounded Extension created in ' + str(end - start) + ' seconds')

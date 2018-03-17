import time

import alias
from alias import ArgumentationFramework
# stable extensions
path = '/home/szczocik/Workspaces/Benchmark/B/'

# filenames                                                             # arguments | attacks   | solutions from pyglaf
filename1 = '1/massachusetts_blockislandferry_2015-11-13.gml.80.tgf'    # 2         | 1         | [a2]
filename2 = '1/afinput_exp_cycles_indvary3_step4_batch_yyy03.tgf'       # 15        | 5         | 10 elements - [11,12,13,14,0,1,2,3,8,10]
filename3 = '1/BA_40_80_4.tgf'                                          # 41        | 73        | [a32,a35,a37,a36,a17,a39,a38,a19,a20,a22,a21,a24,a25,a28,a27,a0,a4,a5,a7,a31,a30],[a32,a35,a36,a17,a39,a38,a19,a20,a22,a21,a24,a26,a25,a28,a27,a0,a4,a5,a7,a31,a30],[a32,a35,a36,a17,a39,a38,a19,a18,a20,a22,a21,a26,a25,a28,a27,a29,a0,a4,a5,a7,a31,a30],[a32,a35,a37,a36,a17,a39,a38,a19,a18,a20,a22,a21,a25,a28,a27,a29,a0,a4,a5,a7,a31,a30],[a32,a35,a37,a36,a17,a39,a38,a19,a18,a20,a22,a21,a25,a27,a29,a0,a4,a5,a6,a7,a31,a30],[a32,a35,a37,a36,a17,a39,a38,a19,a20,a22,a21,a24,a25,a27,a0,a4,a5,a6,a7,a31,a30],[a32,a35,a36,a17,a39,a38,a19,a20,a22,a21,a24,a26,a25,a27,a0,a4,a5,a6,a7,a31,a30],[a32,a35,a36,a17,a39,a38,a19,a18,a20,a22,a21,a26,a25,a27,a29,a0,a4,a5,a6,a7,a31,a30],[a32,a35,a12,a15,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a26,a25,a27,a29,a4,a5,a6,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a25,a27,a29,a4,a5,a6,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a25,a28,a27,a29,a4,a5,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a26,a25,a28,a27,a29,a4,a5,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a26,a25,a28,a27,a4,a5,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a26,a25,a27,a4,a5,a6,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a25,a27,a4,a5,a6,a7,a8,a9,a31,a30],[a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a25,a28,a27,a4,a5,a7,a8,a9,a31,a30],[a11,a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a25,a28,a27,a4,a5,a8,a9],[a11,a32,a35,a12,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a26,a25,a28,a27,a4,a5,a8,a9],[a11,a32,a35,a12,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a26,a25,a28,a27,a29,a4,a5,a8,a9],[a11,a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a25,a28,a27,a29,a4,a5,a8,a9],[a11,a32,a35,a37,a36,a17,a39,a38,a20,a22,a21,a25,a28,a27,a29,a0,a4,a5],[a11,a32,a35,a37,a36,a17,a39,a38,a20,a22,a21,a24,a25,a28,a27,a0,a4,a5],[a11,a32,a35,a36,a17,a39,a38,a20,a22,a21,a24,a26,a25,a28,a27,a0,a4,a5],[a11,a32,a35,a36,a17,a39,a38,a20,a22,a21,a26,a25,a28,a27,a29,a0,a4,a5],[a11,a32,a35,a36,a17,a39,a38,a20,a22,a21,a26,a25,a27,a29,a0,a4,a5,a6],[a11,a32,a35,a37,a36,a17,a39,a38,a20,a22,a21,a25,a27,a29,a0,a4,a5,a6],[a11,a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a25,a27,a29,a4,a5,a6,a8,a9],[a11,a32,a35,a12,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a26,a25,a27,a29,a4,a5,a6,a8,a9],[a11,a32,a35,a12,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a26,a25,a27,a4,a5,a6,a8,a9],[a11,a32,a35,a36,a17,a39,a38,a20,a22,a21,a24,a26,a25,a27,a0,a4,a5,a6],[a11,a32,a35,a37,a36,a17,a39,a38,a20,a22,a21,a24,a25,a27,a0,a4,a5,a6],[a11,a32,a35,a12,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a25,a27,a4,a5,a6,a8,a9],[a11,a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a25,a27,a4,a5,a6,a8,a9],[a11,a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a26,a25,a27,a4,a5,a6,a8,a9],[a11,a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a26,a25,a27,a29,a4,a5,a6,a8,a9],[a11,a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a25,a27,a29,a4,a5,a6,a8,a9],[a11,a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a25,a28,a27,a29,a4,a5,a8,a9],[a11,a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a25,a28,a27,a4,a5,a8,a9],[a11,a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a24,a23,a26,a25,a28,a27,a4,a5,a8,a9],[a11,a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a40,a20,a22,a21,a23,a26,a25,a28,a27,a29,a4,a5,a8,a9],[a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a26,a25,a28,a27,a29,a4,a5,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a25,a28,a27,a29,a4,a5,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a25,a27,a29,a4,a5,a6,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a19,a18,a40,a20,a22,a21,a23,a26,a25,a27,a29,a4,a5,a6,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a26,a25,a27,a4,a5,a6,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a26,a25,a28,a27,a4,a5,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a25,a28,a27,a4,a5,a7,a8,a9,a31,a30],[a13,a35,a12,a34,a15,a37,a14,a36,a17,a39,a38,a19,a40,a20,a22,a21,a24,a23,a25,a27,a4,a5,a6,a7,a8,a9,a31,a30],[a13,a35,a34,a37,a36,a17,a39,a38,a19,a20,a22,a21,a24,a25,a27,a0,a4,a5,a6,a7,a31,a30],[a13,a35,a34,a36,a17,a39,a38,a19,a20,a22,a21,a24,a26,a25,a27,a0,a4,a5,a6,a7,a31,a30],[a13,a35,a34,a36,a17,a39,a38,a19,a18,a20,a22,a21,a26,a25,a27,a29,a0,a4,a5,a6,a7,a31,a30],[a13,a35,a34,a37,a36,a17,a39,a38,a19,a18,a20,a22,a21,a25,a27,a29,a0,a4,a5,a6,a7,a31,a30],[a11,a13,a35,a34,a37,a36,a17,a39,a38,a20,a22,a21,a25,a27,a29,a0,a4,a5,a6],[a11,a13,a35,a34,a37,a36,a17,a39,a38,a20,a22,a21,a24,a25,a27,a0,a4,a5,a6],[a11,a13,a35,a34,a36,a17,a39,a38,a20,a22,a21,a24,a26,a25,a27,a0,a4,a5,a6],[a11,a13,a35,a34,a36,a17,a39,a38,a20,a22,a21,a26,a25,a27,a29,a0,a4,a5,a6],[a11,a13,a35,a34,a36,a17,a39,a38,a20,a22,a21,a26,a25,a28,a27,a29,a0,a4,a5],[a11,a13,a35,a34,a37,a36,a17,a39,a38,a20,a22,a21,a25,a28,a27,a29,a0,a4,a5],[a13,a35,a34,a37,a36,a17,a39,a38,a19,a18,a20,a22,a21,a25,a28,a27,a29,a0,a4,a5,a7,a31,a30],[a13,a35,a34,a36,a17,a39,a38,a19,a18,a20,a22,a21,a26,a25,a28,a27,a29,a0,a4,a5,a7,a31,a30],[a13,a35,a34,a36,a17,a39,a38,a19,a20,a22,a21,a24,a26,a25,a28,a27,a0,a4,a5,a7,a31,a30],[a11,a13,a35,a34,a36,a17,a39,a38,a20,a22,a21,a24,a26,a25,a28,a27,a0,a4,a5],[a11,a13,a35,a34,a37,a36,a17,a39,a38,a20,a22,a21,a24,a25,a28,a27,a0,a4,a5],[a13,a35,a34,a37,a36,a17,a39,a38,a19,a20,a22,a21,a24,a25,a28,a27,a0,a4,a5,a7,a31,a30]
filename4 = '1/afinput_exp_cycles_indvary1_step8_batch_yyy08.tgf'       # 41        | 216       | 23 elements - [23,25,27,29,10,32,11,34,35,37,16,38,17,18,19,0,1,2,4,5,40,20,21]
filename5 = '1/sembuster_60.tgf'                                        # 60        | 480       | 20 elements - [b20,c1,c2,c3,c4,c5,c6,c7,c8,c9,c11,c10,c13,c12,c15,c14,c17,c16,c19,c18]
filename6 = '4/thecomet_20131025_1906.gml.20.tgf'                       # 168       | 233
filename7 = '1/grd_156_3_6.tgf'                                         # 156       | 409


# full path
file = path + filename5
print('Reading file')
start = time.time()
af = alias.read_tgf(file)
end = time.time()

print('------------------------------------------------------------------')
print('File read in ' + str(end - start) + ' seconds')
print('Number of arguments: ' + str(len(af.arguments)))
print('Number of attacks: ' + str(len(af.attacks)))
# af.draw_graph()

print(file)
print('Creating Stable Extension')
start = time.time()
gr = af.get_stable_extension()
end = time.time()
print(gr)
for i in gr:
    print(len(i))
print('Stable Extension created in ' + str(end - start) + ' seconds')
print('------------------------------------------------------------------')

"""
Timings as of 17/03/2018
------------------------------------------------------------------
File read in 0.001512289047241211 seconds
Number of arguments: 2
Number of attacks: 1
/home/szczocik/Workspaces/Benchmark/B/1/massachusetts_blockislandferry_2015-11-13.gml.80.tgf
Creating Stable Extension
[frozenset({'a2'})]
Stable Extension created in 0.0011169910430908203 seconds
------------------------------------------------------------------
File read in 0.0023615360260009766 seconds
Number of arguments: 15
Number of attacks: 5
/home/szczocik/Workspaces/Benchmark/B/1/afinput_exp_cycles_indvary3_step4_batch_yyy03.tgf
Creating Stable Extension
[frozenset({'12', '3', '14', '0', '8', '11', '13', '10', '1', '2'})]
Stable Extension created in 0.054082393646240234 seconds
------------------------------------------------------------------
File read in 0.010593891143798828 seconds
Number of arguments: 41
Number of attacks: 73
/home/szczocik/Workspaces/Benchmark/B/1/BA_40_80_4.tgf
Creating Stable Extension
[frozenset({'a38', 'a24', 'a39', 'a20', 'a32', 'a35', 'a15', 'a14', 'a12', 'a40', 'a30', 'a4', 'a21', 'a22', 'a25', 'a28', 'a23', 'a5', 'a27', 'a26', 'a31', 'a36', 'a17', 'a8', 'a19', 'a9', 'a7'}), frozenset({'a38', 'a24', 'a39', 'a20', 'a32', 'a35', 'a15', 'a14', 'a12', 'a40', 'a4', 'a21', 'a22', 'a25', 'a28', 'a23', 'a5', 'a27', 'a26', 'a11', 'a36', 'a17', 'a8', 'a9'}), frozenset({'a38', 'a39', 'a20', 'a32', 'a18', 'a35', 'a15', 'a14', 'a12', 'a40', 'a30', 'a4', 'a21', 'a29', 'a22', 'a25', 'a28', 'a23', 'a5', 'a27', 'a26', 'a31', 'a36', 'a17', 'a8', 'a19', 'a9', 'a7'}), frozenset({'a38', 'a24', 'a39', 'a20', 'a34', 'a35', 'a15', 'a14', 'a12', 'a40', 'a4', 'a21', 'a22', 'a25', 'a28', 'a5', 'a23', 'a27', 'a13', 'a26', 'a11', 'a36', 'a17', 'a8', 'a9'}), frozenset({'a38', 'a24', 'a39', 'a20', 'a32', 'a35', 'a15', 'a14', 'a12', 'a40', 'a37', 'a4', 'a21', 'a22', 'a25', 'a28', 'a23', 'a5', 'a27', 'a11', 'a36', 'a17', 'a8', 'a9'}), frozenset({'a38', 'a24', 'a39', 'a20', 'a34', 'a35', 'a15', 'a14', 'a12', 'a40', 'a30', 'a4', 'a21', 'a22', 'a25', 'a28', 'a5', 'a23', 'a27', 'a13', 'a26', 'a31', 'a36', 'a17', 'a8', 'a19', 'a9', 'a7'}), frozenset({'a25', 'a38', 'a28', 'a0', 'a22', 'a5', 'a35', 'a27', 'a36', 'a24', 'a17', 'a4', 'a39', 'a20', 'a26', 'a11', 'a21', 'a32'}), frozenset({'a25', 'a38', 'a0', 'a22', 'a5', 'a35', 'a27', 'a36', 'a24', 'a17', 'a4', 'a39', 'a20', 'a26', 'a11', 'a21', 'a6', 'a32'}), frozenset({'a25', 'a38', 'a28', 'a0', 'a34', 'a5', 'a35', 'a27', 'a36', 'a24', 'a17', 'a4', 'a39', 'a20', 'a13', 'a26', 'a11', 'a21', 'a22'})]
Stable Extension created in 0.4656977653503418 seconds
------------------------------------------------------------------
File read in 0.024327993392944336 seconds
Number of arguments: 41
Number of attacks: 216
/home/szczocik/Workspaces/Benchmark/B/1/afinput_exp_cycles_indvary1_step8_batch_yyy08.tgf
Creating Stable Extension
[frozenset({'5', '32', '27', '18', '40', '20', '34', '35', '1', '17', '16', '4', '29', '10', '11', '23', '25', '19', '0', '21', '37', '2', '38'})]
Stable Extension created in 0.1760878562927246 seconds
------------------------------------------------------------------
File read in 0.05037093162536621 seconds
Number of arguments: 60
Number of attacks: 460
/home/szczocik/Workspaces/Benchmark/B/1/sembuster_60.tgf
Creating Stable Extension
[frozenset({'c7', 'c17', 'c10', 'c14', 'c8', 'c11', 'c3', 'c19', 'c9', 'c5', 'c2', 'c12', 'b20', 'c13', 'c15', 'c16', 'c18', 'c6', 'c4', 'c1'})]
Stable Extension created in 0.5061049461364746 seconds
------------------------------------------------------------------
File read in 0.05090618133544922 seconds
Number of arguments: 60
Number of attacks: 460
/home/szczocik/Workspaces/Benchmark/B/1/sembuster_60.tgf
Creating Stable Extension
[frozenset({'c19', 'c11', 'c3', 'c14', 'c16', 'c6', 'c13', 'b20', 'c18', 'c10', 'c9', 'c4', 'c2', 'c17', 'c8', 'c15', 'c5', 'c1', 'c12', 'c7'})]
Stable Extension created in 0.5772404670715332 seconds
------------------------------------------------------------------
"""
import alias as al

def read_apx(path):
	"""Generates an alias.ArgumentationFramework from an Aspartix (.apx) file.

	Parameters
	----------
	path : file or string
		File, directory or filename to be read.

	Returns
	-------
	framework : alias ArgumentationFramework

	Examples
	--------

	References
	---------- 
	http://www.dbai.tuwien.ac.at/research/project/argumentation/systempage/docu.htm
	"""


	try:
		from pyparsing import Word, Literal, nums, Keyword, Group, OneOrMore, Suppress
	except ImportError:
		raise ImportError("read_apx requires pyparsing")

	if not isinstance(path, str):
		return

	# Define apx grammar
	LPAR,RPAR,DOT,COMMA = map(Suppress,"().,")
	arg,attack,pref,val,valpref,support = map(Keyword, 
	    "arg att pref val valpref support".split())

	ID = Word(alphas, alphanums)
	id_pair = Group(ID + COMMA + ID)
	integer = Word(nums)
	int_pair = Group(integer + COMMA + integer)

	arg_cmd = (arg + LPAR + ID("arg*") + RPAR)
	attack_cmd = (attack + LPAR + id_pair("attack*") + RPAR)
	pref_cmd = (pref + LPAR + id_pair("pref*") + RPAR)
	val_cmd = (val + LPAR + Group(ID + COMMA + integer)("val*") + RPAR)
	valpref_cmd = (valpref + LPAR + int_pair("valpref*") + RPAR)
	support_cmd = (support + LPAR + id_pair("support*") + RPAR)

	apx = OneOrMore((arg_cmd | attack_cmd | pref_cmd | val_cmd | valpref_cmd | support_cmd) + DOT)
	
	framework = al.ArgumentationFramework()
	f = open(path, 'r')
	f = f.read()

	try:
		parsed = apx.parseString(f)
	except ParseException:
		raise ParseException()

	for arg in parsed['arg']:
		framework.add_argument(arg)

	for att in parsed['attack']:
		framework.add_attack(att[0], att[1])

	return framework

def apx_out(framework, outloc):
	"""Outputs an Aspartix (.apx) file from an alias.ArgumentationFramework.

	Parameters
	----------
	framework :
		alias ArgumentationFramework
	outloc : string
		Directory location for file to be written to.

	Returns
	-------
	framework : alias ArgumentationFramework

	Examples
	--------

	References
	----------
	http://www.dbai.tuwien.ac.at/research/project/argumentation/systempage/docu.htm
	"""

	f = open(outloc, 'w')

	for arg in framework.get_arguments():
		f.write('arg(' + arg + ').\n')
	for att in framework.get_attacks():
		f.write('att(' + att[0] + att[1] + ').\n')

	f.close()
import alias

af = alias.ArgumentationFramework('test')
af.add_attack(('6', '4'))
af.add_attack(('2', '4'))
af.add_attack(('2', '7'))
af.add_attack(('1', '7'))
af.add_attack(('1', '3'))
af.add_attack(('3', '1'))
af.add_attack(('5', '3'))
g = af.get_complete_extension()
print(g)
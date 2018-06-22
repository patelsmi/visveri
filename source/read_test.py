import read as dut

db = dut.database()

print

db.add_module('test_top_module')
db.add_input('test_top_in1')
db.add_input('test_top_in2')
db.add_output('test_top_ou3')
db.add_submodule('test_submodule', 'test_instance')
db.add_input('test_submodule_in1')
db.add_input('test_in3', 'test_top_module')
db.add_input('test_submodule_in2')
db.add_output('test_submodule_ou1')

print db.design

db.print_inputs()
db.print_inputs('test_top_module')
db.print_outputs()
db.print_outputs('test_top_module')
db.print_submodules('test_top_module')

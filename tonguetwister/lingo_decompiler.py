from decompiler.detokenizer import detokenize
from decompiler.name_parser import replace_names
from decompiler.reconstructor import reconstruct_statements
from decompiler.code_generator import generate_code

class Decompiler(object):
  def twist_to_pseudo(self, function, namelist, script):
    operator_list = detokenize(function.bytecode)
    print '-----------------------------------'
    replace_names(operator_list, function, namelist, script)
    print '-----------------------------------'
    reconstruct_statements(operator_list)
    print '-----------------------------------'
    generate_code(operator_list, function, namelist)

  def twist_to_c(object):
    pass

  def twist_to_lingo(object):
    pass

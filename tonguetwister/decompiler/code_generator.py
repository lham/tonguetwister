from data.statements import *
from data.operators import Operator

def generate_code(operators, function, namelist):
  s = '    '
  indent = 1
  switch_case_active = False

  # Function name
  function_name = namelist[function.header['function_id']]
  function_args = ', '.join(map(lambda x: namelist[x], function.args))
  print 'function %s(%s)' % (function_name, function_args)

  # function body
  for i, code in enumerate(operators):
    if isinstance(code, LoopEndStatement):
      indent -= 1
    if isinstance(code, IfEndStatement):
      indent -= 1
    if isinstance(code, SwitchEndStatement):
      indent -= 1
    if isinstance(code, SwitchEndStatement) and switch_case_active:
      switch_case_active = False
      indent -= 1
    if isinstance(code, ElseControlStatement) or isinstance(code, ElseifControlStatement):
      indent -= 1

    if isinstance(code, AssignVariable) and code.var_type == 'LoopCounter' and not isinstance(operators[i-1], EndControlStatement):
      print

    if isinstance(operators[i-1], SwitchCaseStatement) and isinstance(code, SwitchCaseStatement):
      indent -= 1

    print '%s%s' % (s*indent, code.code_gen_string())

    if isinstance(code, EndControlStatement):
      print

    if isinstance(code, SwitchBreakStatement):
      switch_case_active = False
      indent -= 1

    if isinstance(operators[i-1], SwitchCaseStatement) and isinstance(code, SwitchCaseStatement):
      indent += 1
    if isinstance(code, IfControlStatement):
      indent += 1
    if isinstance(code, ElseControlStatement) or isinstance(code, ElseifControlStatement):
      indent += 1
    if isinstance(code, LoopOpenStatement):
      indent += 1
    if isinstance(code, SwitchOpenStatement):
      indent += 1
    if not switch_case_active:
      if isinstance(code, SwitchCaseStatement):
        switch_case_active = True
        indent += 1

  # function end
  print 'endfunction'

  # Print warning
  if any(map(lambda x: isinstance(x, Operator), operators)):
    print '-----------------------------------------'
    print 'WARNING: Got unknown operator in function'
    print '-----------------------------------------'

class PropertyReference(object):
  def __init__(self, var_name, property_name):
    self.var_name = var_name
    self.property_name = property_name

  def __str__(self):
    return '%s.%s' % (self.var_name, self.property_name)

  def code_gen_string(self):
    return str(self)

class FunctionCallArgument(object):
  def __init__(self, arg_type, value):
    self.arg_type = arg_type
    self.value = value

  def __str__(self):
    return '%s: %s' % (self.arg_type, self.value)

  def code_gen_string(self):
    if isinstance(self.value, str) or isinstance(self.value, int) or isinstance(self.value, float):
      return str(self.value)

    return self.value.code_gen_string()

class FunctionCall(object):
  def __init__(self, name, args, result):
    self.name = name
    self.args = args
    self.result = result

  def __str__(self):
    return_str = ''
    args = ', '.join(map(str, self.args))
    return '%s%s(%s)' % (return_str, self.name, args)

  def code_gen_string(self):
    args = ', '.join(map(lambda x: x.code_gen_string(), self.args))
    return '%s(%s)' % (self.name, args)

class AssignVariable(object):
  def __init__(self, var_name, var_type, value):
    self.var_name = var_name
    self.var_type = var_type
    self.value = value

  def __str__(self):
    val = self.value
    if isinstance(val, list):
      val = ', '.join(map(str, self.value))
    return '%s: %s = %s' % (self.var_type, self.var_name, val)

  def code_gen_string(self):
    val = None
    if isinstance(self.value, list):
      val = '[' + ', '.join(map(lambda x: x.code_gen_string(), self.value)) + ']'
    elif isinstance(self.value, str):
      val = self.value
    else:
      val = self.value.code_gen_string()
    return '%s = %s' % (self.var_name, val)

class ModifyString(object):
  def __init__(self, insert_mode, int_val, str_val, obj):
    self.insert_mode = insert_mode
    self.int_val = int_val
    self.str_val = str_val
    self.obj = obj

  def __str__(self):
    args = (self.insert_mode, self.int_val, self.str_val, self.obj)
    return 'modify_string_59(%s, %s, %s, %s)' % args

  def code_gen_string(self):
    return str(self)

class BinaryIntermediate(object):
  def __init__(self, op, left, right):
    self.op = op
    self.left = left
    self.right = right

  def __str__(self):
    return '%s %s %s' % (self.left, self.op, self.right)

  def code_gen_string(self):
    return '%s %s %s' % (self.left.code_gen_string(), self.op, self.right.code_gen_string())

class UnaryIntermediate(object):
  def __init__(self, operator, operand):
    self.operator = operator
    self.operand = operand

  def __str__(self):
    return '%s %s' % (self.operator, self.operand)

  def code_gen_string(self):
    return '%s %s' % (self.operator, self.operand.code_gen_string())



class EndControlStatement(object):
  def __init__(self, control_statement):
    self.control_statement = control_statement

  def __str__(self):
    return 'end%s' % self.control_statement
  
  def code_gen_string(self):
    return str(self)

class BreakStatement(object):
  def __str__(self):
    return 'break'

  def code_gen_string(self):
    return str(self)

class LoopOpenStatement(object):
  def __init__(self, cond):
    self.cond = cond

  def __str__(self):
    return 'loop while( %s )' % self.cond
  
  def code_gen_string(self):
    return 'repeat while (%s)' % self.cond.code_gen_string()

class LoopEndStatement(EndControlStatement):
  def __init__(self):
    super(LoopEndStatement, self).__init__('repeat')

class LoopCounterIncrement(object):
  def __init__(self, var):
    self.var = var

  def __str__(self):
    return 'increment( %s )' % self.var.name

  def code_gen_string(self):
    return '%s++' % self.var.name

class IfEndStatement(EndControlStatement):
  def __init__(self):
    super(IfEndStatement, self).__init__('if')

class IfControlStatement(object):
  def __init__(self, expr):
    self.expr = expr

  def __str__(self):
    return 'if( %s )' % self.expr
  
  def code_gen_string(self):
    return 'if (%s)' % self.expr.code_gen_string()

class ElseifControlStatement(object):
  def __init__(self, expr):
    self.expr = expr

  def __str__(self):
    return 'elseif( %s )' % self.expr
  
  def code_gen_string(self):
    return 'elseif (%s)' % self.expr.code_gen_string()

class ElseControlStatement(object):
  def __str__(self):
    return 'else'

  def code_gen_string(self):
    return str(self)

class SwitchOpenStatement(object):
  def __init__(self, cond):
    self.cond = cond

  def __str__(self):
    return 'switch ( %s ):' % self.cond

  def code_gen_string(self):
    val = None
    if isinstance(self.cond, str):
      val = self.cond
    else:
      val = self.cond.code_gen_string()
    return 'switch (%s)' % val

class SwitchCaseStatement(object):
  def __init__(self, case_opt):
    self.case_opt = case_opt

  def __str__(self):
    return 'case %s:' % self.case_opt.code_gen_string()

  def code_gen_string(self):
    return str(self)

class SwitchEndStatement(EndControlStatement):
  def __init__(self):
    super(SwitchEndStatement, self).__init__('switch')

class SwitchBreakStatement(BreakStatement):
  pass

class ReturnStatement(object):
  def __str__(self):
    return 'return'
      
  def code_gen_string(self):
    return str(self)

class GotoStatement(object):
  def __init__(self, label):
    self.label = label

  def __str__(self):
    return 'goto %s' % self.label

  def code_gen_string(self):
    return str(self)

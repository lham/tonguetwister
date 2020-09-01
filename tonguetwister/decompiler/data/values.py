class HookMethodValueNode__str__(type):
  def __init__(cls, name, bases, cls_dict):
    if '__str__' in cls_dict:
      def prefixed_str(self):
        return self.__class__.__name__ + ':' + cls_dict['__str__'](self)
      setattr(cls, '__str__', prefixed_str)

class Value(object):
  __metaclass__ = HookMethodValueNode__str__

  def class_name(self):
    return self.__class__.__name__

  def __str__(self):
    return 'IMPLEMENT __STR__()'

""" Literal values """
class Literal(Value):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

  def code_gen_string(self):
    return str(self.value)

class String(Literal):
  def __str__(self):
    return '"' + self.value.replace('\r', '\\r') + '"'

class Integer(Literal):
  pass
 
class Float(Literal):
  pass

class Symbol(Literal):
  pass

class Object(Literal):
  pass

class List(Literal):
  def __init__(self, *literals):
    super(List, self).__init__(literals)

  def __str__(self):
    return '[' + ', '.join(map(str, self.value)) + ']'

class ArgumentList(List):
  pass

class GotoLabel(Literal):
  it = 0

  def __init__(self):
    self.value = 'GOTO_label_%d' % GotoLabel.it
    GotoLabel.it += 1

""" Variable values """
class Variable(Value):
  def __init__(self, name, value=None):
    self.name = name
    self.value = value

  def __str__(self):
    return '%s=%s' % (self.name, self.value)

  def code_gen_string(self):
    if self.value:
      return '%s = %s' % (self.name, self.value)
    else:
      return str(self.name)

class GlobalVar(Variable):
  pass

class LocalVar(Variable):
  pass

class Property(Variable):
  pass

class FunctionArgument(Variable):
  pass

class LoopCounter(Variable):
  it = 0

  def __init__(self):
    var_names = ['i_', 'j_', 'k_', 'm_', 'n_', 'o_']
    var_name = var_names[LoopCounter.it]
    LoopCounter.it += 1
    super(LoopCounter, self).__init__(var_name, None)


""" Function values """
class Function(Value):
  def __init__(self, script_id, name, arg):
    self.script = script_id  # TODO
    self.name = name
    self.arg = arg
    
    if type(arg) == ArgumentList:
      self.do_return = False
    else:
      self.do_return = True
    
  def __str__(self):
    return '%s.%s(%s)' % (self.script, self.name, self.arg)

class LocalFunction(Function):
  def __init__(self, name, arg):
    super(LocalFunction, self).__init__('this', name, arg)

class ExternalFunction(Function):
  def __init__(self, name, arg):
    super(ExternalFunction, self).__init__('', name, arg)

""" Other values """
class FunctionResult(Value):
  def __init__(self, function):
    self.function = function
    self.do_push = function.do_return
  
  def __str__(self):
    return self.function.name

class BinaryResult(Value):
  def __init__(self, op, left, right):
    self.left = left
    self.right = right
    self.operand = op
  
  def __str__(self):
    return '%s[%s, %s]' % (self.operand, self.left, self.right)

class UnaryResult(Value):
  def __init__(self, operator, operand):
    self.operator = operator
    self.operand = operand

  def __str__(self):
    return '%s[%s]' % (self.operator, self.operand)

class ObjectProperty(Value):
  def __init__(self, obj, property_name):
    self.obj = obj
    self.property_name = property_name

  def __str__(self):
    return '(%s).%s' % (self.obj, self.property_name)

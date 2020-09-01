from opcode import OPCode
from values import *

class HookMethodOperatorNode__str__(type):
  def __init__(cls, name, bases, cls_dict):
    if 'get_opcode_addr' not in cls_dict:
      def get_opcode_addr(self):
        return self.opcode.addr
      cls_dict['get_opcode_addr'] = get_opcode_addr

    if 'get_opcode_name' not in cls_dict:
      def get_opcode_name(self):
        return self.opcode.name
      cls_dict['get_opcode_name'] = get_opcode_name

    if '__str__' in cls_dict:
      def prefixed_str(self):
        return '%#04x %-25s: %-30s --> %s' % (cls_dict['get_opcode_addr'](self), cls_dict['get_opcode_name'](self), self.__class__.__name__, cls_dict['__str__'](self))
      setattr(cls, '__str__', prefixed_str)

class Operator(object):
  __metaclass__ = HookMethodOperatorNode__str__

  def __init__(self, opcode, arg1=None, arg2=None):
    self.opcode = opcode
    self.arg1 = arg1
    self.arg2 = arg2

  def __str__(self):
    return 'NOT IMPLMENTED(%s)' % self.opcode.name

  def raw_detokenize_string(self):
    msg = '[%#06x]: %#04x|%-25s(%4s, %4s)'
    args = (self.opcode.addr, self.opcode.value, self.opcode.name, self.arg1, self.arg2)
    return msg % args

  def parse_names(self, stack, var_dict, data):
    pass

  def code_gen_string(self):
    return '___NOT IMPLEMENTED(%s)___' % (self.opcode.name)

class BinaryOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    right_operand = stack.pop()
    left_operand = stack.pop()
    operator = self.opcode.lingo_name

    self.push_value = BinaryResult(operator, left_operand, right_operand)
    stack.append(self.push_value)

  def __str__(self):
    return 'push( %s )' % self.push_value
    
class UnaryOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    operand = stack.pop()
    operator = self.opcode.lingo_name

    self.push_value = UnaryResult(operator, operand)
    stack.append(self.push_value)

  def __str__(self):
    return 'push( %s )' % self.push_value

class PushOperator(Operator):
  def __init__(self, opcode, arg1=None, arg2=None):
    self.operand = arg1
    super(PushOperator, self).__init__(opcode, arg1, arg2)

  def parse_names(self, stack, var_dict, data):
    op_name = self.opcode.name
    arg = self.operand

    if op_name == OPCode.PUSH_ZERO:
      push_value = Integer(0)
    elif op_name == OPCode.PUSH_INTEGER:
      push_value = Integer(arg)
    elif op_name == OPCode.PUSH_CONST:  # constant = literal
      lit = data.get_constant(arg)
      if lit.type == lit.TYPE_STRING:
        push_value = String(lit.value)
      elif lit.type == lit.TYPE_INT:
        push_value = Integer(lit.value)
      elif lit.type == lit.TYPE_DOUBLE:
        push_value = Float(lit.value)
      else:
        raise Exception()
    elif op_name == OPCode.PUSH_SYMBOL:
      push_value = Symbol(data.get_symbol(arg))
    elif op_name == OPCode.PUSH_OBJECT:
      push_value = Object(data.get_object(arg))
    elif op_name == OPCode.PUSH_GLOBAL_VAR:
      push_value = GlobalVar(data.get_global_var(arg))
    elif op_name == OPCode.PUSH_PROPERTY:
      push_value = Property(data.get_property(arg))
    elif op_name == OPCode.PUSH_FUNCTION_ARGUMENT:
      push_value = FunctionArgument(data.get_function_argument(arg))
    elif op_name == OPCode.PUSH_LOCAL_VAR:
      var = LocalVar(data.get_local_var(arg))
      push_value = var_dict[var.name]
    else:
      raise Exception()
    
    stack.append(push_value)
    self.push_value = push_value

  def update_operand(self, new_operand):
    self.operand = new_operand

  def __str__(self):
    return 'push( %s )' % (self.push_value)

class LargePushOperator(PushOperator):
  def parse_names(self, stack, var_dict, data):
    self.update_operand((self.arg1 * 0x100) + self.arg2)
    super(LargePushOperator, self).parse_names(stack, var_dict, data)

class CallFunctionOperator(Operator):
  def __init__(self, opcode, arg1=None, arg2=None, name_id=None):
    if name_id:
      self.name_id = name_id
    else:
      self.name_id = arg1
    super(CallFunctionOperator, self).__init__(opcode, arg1, arg2)

  def pushable(self):
    return self.function_result.do_push

  @property
  def function(self):
    return self._function

  @function.setter
  def function(self, func):
    self._function = func
    self._function_result = FunctionResult(func)

  @property
  def function_result(self):
    return self._function_result

  def __str__(self):
    msg = 'call( %s )' % (self.function)
    if self.pushable():
      msg += '\n%62s --> ' % ''
      msg += 'push( %s )' % self.function_result
    return msg

  def parse_names(self, stack, var_dict, data):
    argument = stack.pop()

    if self.opcode.name == OPCode.CALL_EXT:
      name = data.get_external_function_name(self.name_id)
      self.function = ExternalFunction(name, argument) 
    elif self.opcode.name == OPCode.CALL_LOCAL:
      name = data.get_local_function_name(self.name_id)
      self.function = LocalFunction(name, argument) 
    else:
      raise Exception()

    if self.pushable():
      stack.append(self.function_result)

class LargeCallFunctionOperator(CallFunctionOperator):
  def parse_names(self, stack, var_dict, data):
    self.name_id = (self.arg1 * 0x100) + self.arg2
    super(LargeCallFunctionOperator, self).parse_names(stack, var_dict, data)

class AssignmentOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    arg = self.arg1
    value = stack.pop()
    op_name = self.opcode.name

    if op_name == OPCode.SET_GLOBAL_VAR:
      var = GlobalVar(data.get_global_var(arg), value)
    elif op_name == OPCode.SET_PROPERTY:
      var = Property(data.get_property(arg), value)
    elif op_name == OPCode.SET_FUNCTION_ARGUMENT:
      var = FunctionArgument(data.get_function_argument(arg), value)
    elif op_name == OPCode.SET_LOCAL_VAR:
      var = LocalVar(data.get_local_var(arg), value)
    else:
      raise Exception()

    var_dict[var.name] = var
    self.variable = var

  def __str__(self):
    return 'assign( %s )' % self.variable

class ReturnOperator(Operator):
  def __str__(self):
    return 'return'

class ListOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    n_args = self.arg1
    args = []
    for i in xrange(0, n_args):
      args.append(stack.pop())

    lst = List(*args)
    if self.opcode.name == OPCode.MAKE_ARG_LIST:
      lst = ArgumentList(*args)

    stack.append(lst)
    self.lst = lst

  def __str__(self):
    return 'push( %s )' % self.lst

class TransformListOperator(ListOperator):
  def parse_names(self, stack, var_dict, data):
    self.lst = stack.pop()
    stack.append(self.lst)

  def __str__(self):
    return 'push_unknown_transform_list_1e( %s )' % self.lst 

class IfTrueOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    self.comparison = stack.pop()
    self.jmp_addr = self.opcode.addr + (self.arg1 * 0x100) + self.arg2

  def __str__(self):
    return 'if-not-true ( %s ) then jump to %#0x' % (self.comparison, self.jmp_addr)

class ElseOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    self.jmp_addr = self.opcode.addr + (self.arg1 * 0x100) + self.arg2

  def __str__(self):
    return 'Else-case. When not entering, jump to %#0x' % (self.jmp_addr)

class EndRepeatOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    self.jmp_addr = self.opcode.addr - self.arg1

  def __str__(self):
    return 'End-repeat. Jump to %#0x' % (self.jmp_addr)

class IteratorOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    self.push_value = stack[-(self.arg1+1)]  # look from stack top = end of list
    stack.append(self.push_value)

  def __str__(self):
    return 'push( %s )' % self.push_value

class CleanupIteratorOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    self.pop_count = self.arg1
    for i in xrange(0, self.pop_count):
      stack.pop()

  def __str__(self):
    return 'popped %d items from the stack' % self.pop_count

class PushObjectPropertyOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    property_owning_object = stack.pop()
    property_name = data.get_object_property(self.arg1)

    self.push_value = ObjectProperty(property_owning_object, property_name)
    stack.append(self.push_value)

  def __str__(self):
    return 'push( %s )' % self.push_value

class ModifyStringOperator(Operator):
  def parse_names(self, stack, var_dict, data):

    insert_modes = ('', 'replace', 'after', 'before')
    object_types = ('', '', 'object', '', 'parameter', 'local_var', 'global_var')

    self.int_val = stack.pop() # int 0
    self.string_val = stack.pop() # string playerSilver
    self.target = stack.pop() # gvar gPlayerSilver

    insert_mode = None
    object_arg = self.arg1
    if self.arg1 < 0x10:
      raise Exception('unknown')
    elif self.arg1 < 0x20:
      insert_mode = insert_modes[1]
      object_arg -= 0x10
    elif self.arg1 < 0x30:
      insert_mode = insert_modes[2]
      object_arg -= 0x20
    elif self.arg1 < 0x40:
      insert_mode = insert_modes[3]
      object_arg -= 0x30
    else:
      raise Exception('unknown')

    self.insert_mode = insert_mode
    self.object_type = object_types[object_arg]

  def __str__(self):
    args = (self.arg1, self.insert_mode, self.object_type, self.int_val, self.string_val, self.target)
    return 'modify_string_59( %#04x --> %s, %s on %s, %s, %s)' % args

class GotoOperator(Operator):
  def parse_names(self, stack, var_dict, data):
    self.jmp_addr = self.opcode.addr - ((self.arg1 * 0x100) + self.arg2)

  def __str__(self):
    return 'goto( %#x )' % self.jmp_addr

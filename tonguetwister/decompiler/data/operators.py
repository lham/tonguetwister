from tonguetwister.decompiler.data.opcode import OPCode
from tonguetwister.decompiler.data.values import *


def get_opcode_addr(self):
    return self.opcode.addr


def get_opcode_name(self):
    return self.opcode.name


def format_opcode_str(opcode_addr, opcode_name, cls_name, string):
    return f'{opcode_addr:#04x} {opcode_name:25s}: {cls_name:30s} --> {string}'


class OperatorStrOverride(type):
    def __init__(cls, name, bases, cls_dict):
        super().__init__(name, bases, cls_dict)

        if 'get_opcode_addr' not in cls_dict:
            cls_dict['get_opcode_addr'] = get_opcode_addr

        if 'get_opcode_name' not in cls_dict:
            cls_dict['get_opcode_name'] = get_opcode_name

        if '__str__' in cls_dict:
            def prefixed_str(self):
                return format_opcode_str(
                    cls_dict['get_opcode_addr'](self),
                    cls_dict['get_opcode_name'](self),
                    self.__class__.__name__,
                    cls_dict['__str__'](self)
                )

            setattr(cls, '__str__', prefixed_str)


class Operator(metaclass=OperatorStrOverride):
    def __init__(self, opcode, arg1=None, arg2=None):
        self.opcode = opcode
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return f'NOT IMPLEMENTED ({self.opcode.name})'

    def raw_detokenization_string(self):
        return (
            f'[{self.opcode.addr:#06x}]: '
            f'{self.opcode.value:#04x}|{self.opcode.name:25s}({str(self.arg1):4s}, {str(self.arg2):4s})'
        )

    def parse_names(self, stack, var_dict, data):
        pass

    def code_gen_string(self):
        return f'___NOT IMPLEMENTED ({self.opcode.name})___'


class BinaryOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push_value = None

    def parse_names(self, stack, var_dict, data):
        right_operand = stack.pop()
        left_operand = stack.pop()
        operator = self.opcode.lingo_name

        self.push_value = BinaryResult(operator, left_operand, right_operand)
        stack.append(self.push_value)

    def __str__(self):
        return f'push( {self.push_value} )'


class UnaryOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push_value = None

    def parse_names(self, stack, var_dict, data):
        operand = stack.pop()
        operator = self.opcode.lingo_name

        self.push_value = UnaryResult(operator, operand)
        stack.append(self.push_value)

    def __str__(self):
        return f'push( {self.push_value} )'


class PushOperator(Operator):
    def __init__(self, opcode, arg1=None, arg2=None):
        super().__init__(opcode, arg1, arg2)
        self.operand = arg1
        self.push_value = None

    def parse_names(self, stack, var_dict, data):
        op_name = self.opcode.name
        arg = self.operand

        if op_name == OPCode.PUSH_ZERO:
            push_value = Integer(0)
        elif op_name == OPCode.PUSH_INTEGER:
            push_value = Integer(arg)
        elif op_name == OPCode.PUSH_CONST:  # constant = literal
            literal = data.get_constant(arg)

            if literal.type == literal.TYPE_STRING:
                push_value = String(literal.value)
            elif literal.type == literal.TYPE_INT:
                push_value = Integer(literal.value)
            elif literal.type == literal.TYPE_DOUBLE:
                push_value = Float(literal.value)
            else:
                raise RuntimeError()

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
            raise RuntimeError()

        stack.append(push_value)
        self.push_value = push_value

    def update_operand(self, new_operand):
        self.operand = new_operand

    def __str__(self):
        return f'push( {self.push_value} )'


class LargePushOperator(PushOperator):
    def parse_names(self, stack, var_dict, data):
        self.update_operand((self.arg1 * 0x100) + self.arg2)
        super().parse_names(stack, var_dict, data)


class CallFunctionOperator(Operator):
    def __init__(self, opcode, arg1=None, arg2=None, name_id=None):
        super().__init__(opcode, arg1, arg2)
        self.name_id = name_id if name_id else arg1
        self._function = None
        self._function_result = None

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
        msg = f'call( {self.function} )'
        if self.pushable():
            msg += f"\n{' ' * 62} --> push( {self.function_result} )"

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
            raise RuntimeError()

        if self.pushable():
            stack.append(self.function_result)


class LargeCallFunctionOperator(CallFunctionOperator):
    def parse_names(self, stack, var_dict, data):
        self.name_id = (self.arg1 * 0x100) + self.arg2
        super().parse_names(stack, var_dict, data)


class AssignmentOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = None

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
            raise RuntimeError()

        var_dict[var.name] = var
        self.variable = var

    def __str__(self):
        return f'assign( {self.variable} )'


class ReturnOperator(Operator):
    def __str__(self):
        return 'return'


class ListOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = None

    def parse_names(self, stack, var_dict, data):
        n_args = self.arg1
        args = []

        for i in range(n_args):
            args.append(stack.pop())

        lst = List(*args)
        if self.opcode.name == OPCode.MAKE_ARG_LIST:
            lst = ArgumentList(*args)

        stack.append(lst)
        self.lst = lst

    def __str__(self):
        return f'push( {self.lst} )'


class TransformListOperator(ListOperator):
    def parse_names(self, stack, var_dict, data):
        self.lst = stack.pop()
        stack.append(self.lst)

    def __str__(self):
        return f'push_unknown_transform_list_1e( {self.lst} )'


class IfTrueOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.comparison = None
        self.jmp_addr = None

    def parse_names(self, stack, var_dict, data):
        self.comparison = stack.pop()
        self.jmp_addr = self.opcode.addr + (self.arg1 * 0x100) + self.arg2

    def __str__(self):
        return f'if-not-true ( {self.comparison} ) then jump to {self.jmp_addr:#0x}'


class ElseOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jmp_addr = None

    def parse_names(self, stack, var_dict, data):
        self.jmp_addr = self.opcode.addr + (self.arg1 * 0x100) + self.arg2

    def __str__(self):
        return f'Else-case. When not entering, jump to {self.jmp_addr:#0x}'


class EndRepeatOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jmp_addr = None

    def parse_names(self, stack, var_dict, data):
        self.jmp_addr = self.opcode.addr - self.arg1

    def __str__(self):
        return f'End-repeat. Jump to {self.jmp_addr:#0x}'


class IteratorOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push_value = None

    def parse_names(self, stack, var_dict, data):
        self.push_value = stack[-(self.arg1 + 1)]  # look from stack top = end of list
        stack.append(self.push_value)

    def __str__(self):
        return f'push( {self.push_value} )'


class CleanupIteratorOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pop_count = None

    def parse_names(self, stack, var_dict, data):
        self.pop_count = self.arg1
        for i in range(self.pop_count):
            stack.pop()

    def __str__(self):
        return f'popped {self.pop_count} items from the stack'


class PushObjectPropertyOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.push_value = None

    def parse_names(self, stack, var_dict, data):
        property_owning_object = stack.pop()
        property_name = data.get_object_property(self.arg1)

        self.push_value = ObjectProperty(property_owning_object, property_name)
        stack.append(self.push_value)

    def __str__(self):
        return f'push( {self.push_value} )'


class ModifyStringOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_mode = None
        self.object_type = None
        self.int_val = None
        self.string_val = None
        self.target = None

    def parse_names(self, stack, var_dict, data):
        insert_modes = ('', 'replace', 'after', 'before')
        object_types = ('', '', 'object', '', 'parameter', 'local_var', 'global_var')

        self.int_val = stack.pop()  # int, i.e. 0
        self.string_val = stack.pop()  # string, i.e. playerSilver
        self.target = stack.pop()  # gvar, i.e. gPlayerSilver

        object_arg = self.arg1
        if self.arg1 < 0x10:
            raise RuntimeError('Unknown')
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
            raise RuntimeError('Unknown')

        self.insert_mode = insert_mode
        self.object_type = object_types[object_arg]

    def __str__(self):
        return (f'modify_string_59( {self.arg1:#04x} --> {self.insert_mode}, '
                f'{self.object_type} on {self.int_val}, '
                f'{self.string_val}, '
                f'{self.target})')


class GotoOperator(Operator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jmp_addr = None

    def parse_names(self, stack, var_dict, data):
        self.jmp_addr = self.opcode.addr - ((self.arg1 * 0x100) + self.arg2)

    def __str__(self):
        return f'goto( {self.jmp_addr:#x} )'

class ValueStrOverride(type):
    def __init__(cls, name, bases, cls_dict):
        super().__init__(name, bases, cls_dict)

        if '__str__' in cls_dict:
            def prefixed_str(self):
                return f"{self.__class__.__name__}:{cls_dict['__str__'](self)}"

            setattr(cls, '__str__', prefixed_str)


class Value(metaclass=ValueStrOverride):
    def class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return 'IMPLEMENT __STR__()'


class Literal(Value):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def code_gen_string(self):
        return str(self.value)


class String(Literal):
    def __str__(self):
        val = self.value.replace("\r", "\\r")
        return f'"{val}"'


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
        super().__init__(literals)

    def __str__(self):
        return f"[{', '.join(map(str, self.value))}]"


class ArgumentList(List):
    pass


class GotoLabel(Literal):
    it = 0

    def __init__(self):
        super().__init__(f'GOTO_label_{GotoLabel.it}')
        GotoLabel.it += 1


class Variable(Value):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        return f'{self.name}={self.value}'

    def code_gen_string(self):
        if self.value:
            return f'{self.name} = {self.value}'
        else:
            return f'{self.name}'


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
        var_names = ['_i', '_j', '_k', '_l', '_m', '_n']
        var_name = var_names[LoopCounter.it]
        LoopCounter.it += 1
        super().__init__(var_name, None)


class Function(Value):
    def __init__(self, script_id, name, arg):
        self.script = script_id  # TODO
        self.name = name
        self.arg = arg
        self.do_return = type(arg) != ArgumentList

    def __str__(self):
        return f'{self.script}.{self.name}({self.arg})'


class LocalFunction(Function):
    def __init__(self, name, arg):
        super().__init__('this', name, arg)


class ExternalFunction(Function):
    def __init__(self, name, arg):
        super().__init__('', name, arg)


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
        return f'{self.operand}[{self.left}, {self.right}]'


class UnaryResult(Value):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f'{self.operator}[{self.operand}]'


class ObjectProperty(Value):
    def __init__(self, obj, property_name):
        self.obj = obj
        self.property_name = property_name

    def __str__(self):
        return f'({self.obj}).{self.property_name}'

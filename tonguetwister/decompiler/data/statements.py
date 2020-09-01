class PropertyReference:
    def __init__(self, var_name, property_name):
        self.var_name = var_name
        self.property_name = property_name

    def __str__(self):
        return f'{self.var_name}.{self.property_name}'

    def code_gen_string(self):
        return str(self)


class FunctionCallArgument:
    def __init__(self, arg_type, value):
        self.arg_type = arg_type
        self.value = value

    def __str__(self):
        return f'{self.arg_type}: {self.value}'

    def code_gen_string(self):
        if isinstance(self.value, str) or isinstance(self.value, int) or isinstance(self.value, float):
            return f'{self.value}'

        return self.value.code_gen_string()


class FunctionCall:
    def __init__(self, name, args, result):
        self.name = name
        self.args = args
        self.result = result

    def __str__(self):
        return_str = ''
        args = ', '.join(map(str, self.args))
        return f'{return_str}{self.name}({args})'

    def code_gen_string(self):
        args = ', '.join(map(lambda x: x.code_gen_string(), self.args))
        return f'{self.name}({args})'


class AssignVariable:
    def __init__(self, var_name, var_type, value):
        self.var_name = var_name
        self.var_type = var_type
        self.value = value

    def __str__(self):
        val = self.value
        if isinstance(val, list):
            val = ', '.join(map(str, self.value))
        return f'{self.var_type}: {self.var_name} = {val}'

    def code_gen_string(self):
        if isinstance(self.value, list):
            val = f"[{', '.join(map(lambda x: x.code_gen_string(), self.value))}]"
        elif isinstance(self.value, str):
            val = self.value
        else:
            val = self.value.code_gen_string()

        return f'{self.var_name} = {val}'


class ModifyString:
    def __init__(self, insert_mode, int_val, str_val, obj):
        self.insert_mode = insert_mode
        self.int_val = int_val
        self.str_val = str_val
        self.obj = obj

    def __str__(self):
        return f'modify_string_59({self.insert_mode}, {self.int_val}, {self.str_val}, {self.obj})'

    def code_gen_string(self):
        return str(self)


class BinaryIntermediate:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.left} {self.op} {self.right}'

    def code_gen_string(self):
        return f'{self.left.code_gen_string()} {self.op} {self.right.code_gen_string()}'


class UnaryIntermediate:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f'{self.operator} {self.operand}'

    def code_gen_string(self):
        return f'{self.operator} {self.operand.code_gen_string()}'


class EndControlStatement:
    def __init__(self, control_statement):
        self.control_statement = control_statement

    def __str__(self):
        return f'end{self.control_statement}'

    def code_gen_string(self):
        return str(self)


class BreakStatement:
    def __str__(self):
        return 'break'

    def code_gen_string(self):
        return str(self)


class LoopOpenStatement:
    def __init__(self, cond):
        self.cond = cond

    def __str__(self):
        return f'loop while( {self.cond} )'

    def code_gen_string(self):
        return f'repeat while ( {self.cond.code_gen_string()} )'


class LoopEndStatement(EndControlStatement):
    def __init__(self):
        super().__init__('repeat')


class LoopCounterIncrement:
    def __init__(self, var):
        self.var = var

    def __str__(self):
        return f'increment( {self.var.name} )'

    def code_gen_string(self):
        return f'{self.var.name}++'


class IfEndStatement(EndControlStatement):
    def __init__(self):
        super().__init__('if')


class IfControlStatement:
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f'if( {self.expr} )'

    def code_gen_string(self):
        return f'if ({self.expr.code_gen_string()})'


class ElseifControlStatement:
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f'elseif( {self.expr} )'

    def code_gen_string(self):
        return f'elseif ({self.expr.code_gen_string()})'


class ElseControlStatement:
    def __str__(self):
        return 'else'

    def code_gen_string(self):
        return str(self)


class SwitchOpenStatement:
    def __init__(self, cond):
        self.cond = cond

    def __str__(self):
        return f'switch ( {self.cond} ):'

    def code_gen_string(self):
        if isinstance(self.cond, str):
            val = self.cond
        else:
            val = self.cond.code_gen_string()

        return f'switch ({val})'


class SwitchCaseStatement:
    def __init__(self, case_opt):
        self.case_opt = case_opt

    def __str__(self):
        return f'case {self.case_opt.code_gen_string()}:'

    def code_gen_string(self):
        return str(self)


class SwitchEndStatement(EndControlStatement):
    def __init__(self):
        super().__init__('switch')


class SwitchBreakStatement(BreakStatement):
    pass


class ReturnStatement:
    def __str__(self):
        return 'return'

    def code_gen_string(self):
        return str(self)


class GotoStatement:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f'goto {self.label}'

    def code_gen_string(self):
        return str(self)

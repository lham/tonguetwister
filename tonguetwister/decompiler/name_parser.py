def replace_names(operators, function, namelist, script):
    data = NameData(function, namelist, script)
    stack = []
    var_dict = {}

    for op in operators:
        op.parse_names(stack, var_dict, data)
        print(op)


class NameData:
    def __init__(self, function, namelist, script):
        self.function_arguments = function.args
        self.local_vars = function.locals
        self.global_vars = script.globals
        self.properties = script.properties
        self.literals = script.literals
        self.namelist = namelist
        self.functions = script.functions

    def get_constant(self, arg):
        return self.literals[int(arg / 8)]

    def get_symbol(self, arg):
        return '#' + self.namelist[arg]  # TODO?

    def get_object(self, arg):
        return self.namelist[arg]  # TODO?

    def get_property(self, arg):
        return self.namelist[self.properties[arg]]  # TODO?

    def get_object_property(self, arg):
        return self.namelist[arg]

    def get_global_var(self, arg):
        return self.namelist[arg]

    def get_local_var(self, arg):
        return self.namelist[self.local_vars[int(arg / 8)]]

    def get_function_argument(self, arg):
        return self.namelist[self.function_arguments[int(arg / 8)]]

    def get_external_function_name(self, arg):
        return self.namelist[arg]

    def get_local_function_name(self, arg):
        try:
            return self.namelist[self.functions[arg].name_id]
        except IndexError:
            print('WARNING: Using weird local function name')
            return self.namelist[arg]

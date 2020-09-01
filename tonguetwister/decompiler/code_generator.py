from tonguetwister.decompiler.data.statements import *
from tonguetwister.decompiler.data.operators import Operator


def generate_code(operators, function, namelist):
    indent_str = '    '
    indent = 1
    switch_case_active = False

    # Function name
    function_name = namelist[function.header['function_id']]
    function_args = ', '.join(map(lambda x: namelist[x], function.args))
    print(f'function {function_name}({function_args})')

    # function body
    for i, code in enumerate(operators):
        prev_code = operators[i - 1]

        if should_decrease_indent_prior_to_line(code, prev_code, switch_case_active):
            indent -= 1
        if should_deactivate_switch_case_prior_to_line(code, prev_code, switch_case_active):
            switch_case_active = False
            indent -= 1
        if should_print_blank_line_prior_to_line(code, prev_code, switch_case_active):
            print()

        print(f'{indent_str * indent}{code.code_gen_string()}')

        if should_print_blank_line_after_line(code, prev_code, switch_case_active):
            print()
        if should_deactivate_switch_case_after_line(code, prev_code, switch_case_active):
            switch_case_active = False
            indent -= 1
        if should_increase_indent_after_line(code, prev_code, switch_case_active):
            indent += 1

        if should_activate_switch_case(code, prev_code, switch_case_active):
            switch_case_active = True
            indent += 1

    # function end
    print('endfunction')

    # Print warning
    if any(map(lambda x: isinstance(x, Operator), operators)):
        print('-----------------------------------------')
        print('WARNING: Got unknown operator in function')
        print('-----------------------------------------')


def should_decrease_indent_prior_to_line(line, prev_line, switch_case_active):
    return (
            isinstance(line, LoopEndStatement)
            or isinstance(line, IfEndStatement)
            or isinstance(line, SwitchEndStatement)
            or (isinstance(line, SwitchEndStatement) and switch_case_active)
            or isinstance(line, ElseControlStatement)
            or isinstance(line, ElseifControlStatement)
            or (isinstance(prev_line, SwitchCaseStatement) and isinstance(line, SwitchCaseStatement))
    )


def should_deactivate_switch_case_prior_to_line(line, prev_line, switch_case_active):
    return isinstance(line, SwitchEndStatement) and switch_case_active


def should_print_blank_line_prior_to_line(line, prev_line, switch_case_active):
    return (isinstance(line, AssignVariable) and line.var_type == 'LoopCounter'
            and not isinstance(prev_line, EndControlStatement))


def should_print_blank_line_after_line(line, prev_line, switch_case_active):
    return isinstance(line, EndControlStatement)


def should_decrease_indent_after_line(line, prev_line, switch_case_active):
    return isinstance(line, SwitchBreakStatement)


def should_deactivate_switch_case_after_line(line, prev_line, switch_case_active):
    return isinstance(line, SwitchBreakStatement)


def should_increase_indent_after_line(line, prev_line, switch_case_active):
    return (
            (isinstance(prev_line, SwitchCaseStatement) and isinstance(line, SwitchCaseStatement))
            or isinstance(line, IfControlStatement)
            or isinstance(line, ElseControlStatement)
            or isinstance(line, ElseifControlStatement)
            or isinstance(line, LoopOpenStatement)
            or isinstance(line, SwitchOpenStatement)
    )


def should_activate_switch_case(line, prev_line, switch_case_active):
    return not switch_case_active and isinstance(line, SwitchCaseStatement)


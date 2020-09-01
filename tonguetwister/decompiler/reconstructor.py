from tonguetwister.decompiler.data.statements import *
from tonguetwister.decompiler.data.operators import *


def reconstruct_statements(operator_list):
    opseq = OperatorSequence(operator_list)

    # Basic reconstructors
    parse_goto_statements(opseq)
    parse_conditional_statements(opseq)
    parse_assignments(opseq)
    parse_function_calls(opseq)
    parse_string_modifiers(opseq)
    parse_return_operators(opseq)
    parse_iterator_cleanups(opseq)

    # Syntax sugar
    # TODO: for-in loops
    # TODO: else-if
    # TODO: if-not operator

    print('... Finished reconstruction ...')
    opseq.print_all()


def ensure(var, cls, msg=''):
    if isinstance(cls, list):
        if not any(map(lambda k: isinstance(var, k), cls)):
            msg = (f"Expected: {', '.join(map(lambda k: k.__name__, cls))}\n"
                   f'Actual:   {var.__class__.__name__}\n'
                   f'{msg}\n')
            raise UnexpectedOperatorException(var, msg)
    else:
        if not isinstance(var, cls):
            msg = (f'Expected: {cls.__name__}\n'
                   f'Actual:   {var.__class__.__name__}\n'
                   f'{msg}\n')
            raise UnexpectedOperatorException(var, msg)


class UnexpectedOperatorException(Exception):
    def __init__(self, op, msg=None):
        super().__init__('\n' + (str(msg) if msg else str(op)))


class OperatorNotFoundException(Exception):
    pass


class OperatorSequence:
    def __init__(self, operator_list):
        self.operators = operator_list

    def print_all(self, start=0, end=None):
        """
        Outputs the operator sequence to stdout.

        Args:
          start: Position from which the operator sequence will be printed.
          end: Position to which the operator sequence will be printed.
        """
        if not end:
            end = len(self.operators)

        print('-------------------------------')
        for i, op in enumerate(self.operators[start:end], start):
            print(f'{i:3d}: {op}')
        print('-------------------------------')

    def find(self, cls, start=0):
        """
        Find the first occurrence of an operator of a specified class.

        Args:
          cls: Class of the operator to be found.
          start: Offset from which the search will be performed.
        Returns:
          The position of the first operator with class `op_klass`, if no such operator is found
          `None` is returned.
        """
        for pos, op in enumerate(self.operators[start:], start):
            if isinstance(op, cls):
                return pos

    def find_all(self, cls, start=0):
        """
        Find all the occurrences of an operator of a specified class.

        Args:
          cls: Class of the operators to be found.
          start: Offset from which the search will be performed.
        Returns:
          An iterable of all the operators with class `op_klass`, if no such operator is found
          `None` is returned.
        """
        while True:
            pos = self.find(cls, start)
            if not pos:
                break
            yield pos

    def find_by_address(self, addr):
        """
        Find an operator with a specific address.

        Args:
          addr: The (integer) address of an operator to be found.
        Returns:
          The position of the operator with the address `addr`, if no such operator is found
          `None` is returned.
        """
        for pos, op in enumerate(self.operators):
            if isinstance(op, Operator) and op.opcode.addr == addr:
                return pos

    def extract(self, pos):
        """
        Remove and return the operator at position `pos`.

        Args:
          pos: The position of the operator to be extracted.
        Returns:
          The operator extracted from the list.
        """
        return self.operators.pop(pos)

    def peek(self, pos):
        """
        Get the operator at position `pos`without removing it from the list.

        Args:
          pos: The position of the operator.
        Returns:
          The operator.
        """
        return self.operators[pos]

    def insert(self, pos, op):
        """
        Insert an operator at position `pos`.

        Args:
          pos: The position at which the operator is to be inserted.
          op: The operator to be inserted.
        """
        self.operators.insert(pos, op)


def parse_goto_statements(opseq):
    for pos in opseq.find_all(GotoOperator):
        op = opseq.extract(pos)

        label_op = GotoLabel()
        goto_op = GotoStatement(label_op.value)
        opseq.insert(pos, goto_op)
        opseq.insert(opseq.find_by_address(op.jmp_addr), label_op)


def parse_assignments(opseq):
    for pos in opseq.find_all(AssignmentOperator):
        op = opseq.extract(pos)
        var = op.variable

        if isinstance(var.value, FunctionResult):
            pos, expr = extract_function(opseq, pos - 1)
        elif isinstance(var.value, BinaryResult):
            pos, expr = extract_binary_result(opseq, pos - 1)
        elif isinstance(var.value, UnaryResult):
            pos, expr = extract_unary_result(opseq, pos - 1)
        elif isinstance(var.value, List):
            pos, expr = extract_argument_list(opseq, pos - 1)
        elif isinstance(var.value, Literal):
            pos, expr = extract_literal(opseq, pos - 1)
        elif isinstance(var.value, Variable):
            pos, expr = extract_variable(opseq, pos - 1)
        else:
            raise UnexpectedOperatorException(var.value)

        assign_stmt = AssignVariable(var.name, var.__class__.__name__, expr)
        opseq.insert(pos, assign_stmt)


def parse_function_calls(opseq):
    for pos in opseq.find_all(CallFunctionOperator):
        pos, func_call_op = extract_function(opseq, pos)
        opseq.insert(pos, func_call_op)


def parse_string_modifiers(opseq):
    for pos in opseq.find_all(ModifyStringOperator):
        pos -= 1
        push_int_op = opseq.extract(pos)
        ensure(push_int_op.push_value, Integer, 'In stack before string modifier operator.')
        arg1 = push_int_op.push_value

        pos -= 1
        push_str_op = opseq.extract(pos)
        ensure(push_str_op.push_value, String, 'In stack before string modifier operator.')
        arg2 = push_str_op.push_value

        pos -= 1
        op = opseq.extract(pos)
        if isinstance(op, PushOperator):
            ensure(op.push_value, Variable)
            arg3 = op.push_value
        elif isinstance(op, BinaryOperator):
            pos, arg3 = extract_binary_result(opseq, pos, op.push_value.operand)
        else:
            raise UnexpectedOperatorException(op)

        op = opseq.extract(pos)
        mod_stmt = ModifyString(op.insert_mode, arg1, arg2, arg3)
        opseq.insert(pos, mod_stmt)


def parse_return_operators(opseq):
    for pos in opseq.find_all(ReturnOperator):
        opseq.extract(pos)
        opseq.insert(pos, ReturnStatement())


def parse_iterator_cleanups(opseq):
    for pos in opseq.find_all(CleanupIteratorOperator):
        n_to_be_cleaned = opseq.extract(pos).pop_count

        cleaned = 0
        iterations = 0
        while iterations < n_to_be_cleaned:
            for i in range(pos, 0, -1):
                op = opseq.peek(i - 1)
                if isinstance(op, PushOperator):
                    opseq.extract(i - 1)
                    cleaned += 1
                    break
            iterations += 1

        if cleaned != iterations:
            raise RuntimeError('Could not clean as many push values as stated.')


def parse_conditional_statements(opseq):
    for if_pos in opseq.find_all(IfTrueOperator):
        # Find the if operator
        if_op = opseq.peek(if_pos)

        # Try to find the position of the jump target
        addr = if_op.jmp_addr
        jmp_pos = opseq.find_by_address(addr)

        # We might have extracted the target address already, thus we need to do some lookup tricks
        add_one = False
        while not jmp_pos:
            addr -= 1
            jmp_pos = opseq.find_by_address(addr)
            add_one = True

        if add_one:
            jmp_pos += 1

        # Extract the jump target
        jmp_target_op = opseq.peek(jmp_pos)
        jmp_target_prev_op = opseq.peek(jmp_pos - 1)

        if isinstance(jmp_target_prev_op, EndRepeatOperator):
            # This is a loop
            parse_single_loop_conditional(opseq, if_pos)
        elif isinstance(jmp_target_prev_op, ElseOperator):
            jmp_pos = opseq.find_by_address(jmp_target_prev_op.jmp_addr)
            jmp_target_op = opseq.peek(jmp_pos)
            jmp_target_prev_op = opseq.peek(jmp_pos - 1)

            if isinstance(jmp_target_prev_op, LoopEndStatement):
                # This a break from  a loop
                parse_break_statement(opseq, if_pos)
            elif isinstance(jmp_target_op, CleanupIteratorOperator):
                # This is a switch-statement
                parse_single_switch_conditional(opseq, if_pos)
            else:
                # This is an if/else/end-statement
                parse_single_if_conditional(opseq, if_pos)
        elif (isinstance(jmp_target_prev_op, IfTrueOperator) and
              isinstance(opseq.peek(opseq.find_by_address(jmp_target_prev_op.jmp_addr)), IteratorOperator)):
            # This is a switch-statement
            parse_single_switch_conditional(opseq, if_pos)
        elif isinstance(jmp_target_prev_op, SwitchEndStatement):
            # If-statement in the last case of a switch-statement
            parse_single_if_conditional(opseq, if_pos)
        elif isinstance(jmp_target_op, CleanupIteratorOperator):
            # This is a switch-statement
            parse_single_switch_conditional(opseq, if_pos)
        else:
            # This is an if/end-statement
            parse_single_if_conditional(opseq, if_pos)


def parse_break_statement(opseq, pos):
    # Extract IfTrueOperator
    if_op = opseq.extract(pos)
    pos, cond = extract_condition(opseq, pos - 1, if_op.comparison)

    # Extract the ElseOperator
    jmp_pos = opseq.find_by_address(if_op.jmp_addr)
    jmp_target_prev_op = opseq.extract(jmp_pos - 1)
    ensure(jmp_target_prev_op, ElseOperator)

    # Insert a break statement
    ending_op = IfEndStatement()
    opseq.insert(pos, ending_op)

    break_op = BreakStatement()
    opseq.insert(pos, break_op)

    opening_op = IfControlStatement(cond)
    opseq.insert(pos, opening_op)


def parse_single_loop_conditional(opseq, pos):
    # Extract loop start
    if_op = opseq.extract(pos)
    pos, if_cond = extract_condition(opseq, pos - 1, if_op.comparison)
    ensure(if_cond, BinaryIntermediate, 'Loop conditional needs to start with a binary comparison.')

    # Insert loop counter
    if_cond.left = LoopCounter()
    assign_loop_counter_op = AssignVariable(if_cond.left.name, 'LoopCounter', Integer(0))
    opseq.insert(pos, assign_loop_counter_op)
    pos += 1

    # Insert loop opening statement
    loop_stmt = LoopOpenStatement(if_cond)
    opseq.insert(pos, loop_stmt)
    pos += 1

    # Find and extract loop end
    end_repeat_pos = opseq.find_by_address(if_op.jmp_addr) - 1
    opseq.extract(end_repeat_pos)

    # Extract loop counter increase
    end_repeat_pos -= 1
    bin_incr_op = opseq.extract(end_repeat_pos)
    ensure(bin_incr_op, BinaryOperator)

    # Insert loop counter increment
    loop_counter_op = LoopCounterIncrement(if_cond.left)
    opseq.insert(end_repeat_pos, loop_counter_op)
    end_repeat_pos += 1

    # Insert loop ending statement
    end_repeat_stmt = LoopEndStatement()
    opseq.insert(end_repeat_pos, end_repeat_stmt)


def parse_single_if_conditional(opseq, if_pos):
    if_op = opseq.extract(if_pos)

    # Parse the condition
    if isinstance(if_op.comparison, Variable):
        if_pos, expr = extract_variable(opseq, if_pos - 1)
        cond = FunctionCallArgument(expr.__class__.__name__, expr)
    elif isinstance(if_op.comparison, BinaryResult):
        if_pos, cond = extract_binary_result(opseq, if_pos - 1)
    elif isinstance(if_op.comparison, UnaryResult):
        if_pos, cond = extract_unary_result(opseq, if_pos - 1)
    elif isinstance(if_op.comparison, FunctionResult):
        if_pos, cond = extract_function(opseq, if_pos - 1)
    elif isinstance(if_op.comparison, ObjectProperty):
        if_pos, cond = extract_object_property(opseq, if_pos - 1)
    else:
        raise UnexpectedOperatorException(if_op.comparison)

    # Try to find an else-statement
    addr = if_op.jmp_addr
    end_op_pos = opseq.find_by_address(addr)

    # We might have extracted the target address, thus we need to do some lookup tricks
    add_one_due_to_missing_end_op = False
    while not end_op_pos:
        addr -= 1
        end_op_pos = opseq.find_by_address(addr)
        add_one_due_to_missing_end_op = True

    if add_one_due_to_missing_end_op:
        end_op_pos += 1

    end_op = opseq.peek(end_op_pos - 1)

    if isinstance(end_op, SwitchEndStatement):
        end_op_pos -= 1
        end_op = opseq.peek(end_op_pos - 1)

    if isinstance(end_op, ElseOperator):  # if-statement has else-clause
        else_op_pos = end_op_pos - 1
        else_op = opseq.extract(else_op_pos)
        else_op_target_addr = else_op.jmp_addr

        end_op_pos = opseq.find_by_address(else_op_target_addr)

        ending_op = IfEndStatement()
        opseq.insert(end_op_pos, ending_op)

        elsing_op = ElseControlStatement()
        opseq.insert(else_op_pos, elsing_op)

        opening_op = IfControlStatement(cond)
        opseq.insert(if_pos, opening_op)
    else:
        ending_op = IfEndStatement()
        opseq.insert(end_op_pos, ending_op)

        opening_op = IfControlStatement(cond)
        opseq.insert(if_pos, opening_op)


def parse_single_switch_conditional(opseq, pos):
    ensure(opseq.peek(pos), IfTrueOperator)

    op = opseq.peek(pos)
    cond = op.comparison.left
    if isinstance(cond, Variable):
        cond = cond.name
    else:
        cond = cond.value

    pos = extract_switch_case(opseq, pos, cond)
    opseq.insert(pos - 1, SwitchOpenStatement(cond))


def extract_switch_case(opseq, pos, switch_cond_val):
    pos = opseq.find(IfTrueOperator, start=pos)
    op = opseq.extract(pos)
    pos, cond = extract_condition(opseq, pos - 1, op.comparison)

    if cond.left.value != switch_cond_val:
        raise UnexpectedOperatorException(cond.left, switch_cond_val.__class__)

    opseq.insert(pos, SwitchCaseStatement(cond.right))
    pos += 1

    if cond.op == '!=':
        # -- Fall through case --
        extract_switch_case(opseq, pos, switch_cond_val)
    elif cond.op == '==':
        # -- Case with statements --
        # Find the next case and insert a break if it's an else-operator
        jmp_target_pos = opseq.find_by_address(op.jmp_addr)
        jmp_target_op = opseq.peek(jmp_target_pos)
        jmp_target_prev_pos = jmp_target_pos - 1
        jmp_target_prev_op = opseq.peek(jmp_target_prev_pos)

        if isinstance(jmp_target_op, CleanupIteratorOperator):
            # TODO: default case?
            opseq.insert(jmp_target_pos, SwitchEndStatement())
        elif isinstance(jmp_target_prev_op, ElseOperator):
            opseq.extract(jmp_target_prev_pos)
            opseq.insert(jmp_target_prev_pos, SwitchBreakStatement())
            jmp_target_pos += 1
            jmp_target_prev_pos += 1
            extract_switch_case(opseq, jmp_target_pos, switch_cond_val)
        else:
            raise UnexpectedOperatorException('Unknown op')

    else:
        raise RuntimeError('Wrong condition in switch statement')

    return pos


def extract_condition(opseq, pos, comparison):
    if isinstance(comparison, Variable):
        pos, expr = extract_variable(opseq, pos)
        cond = FunctionCallArgument(expr.__class__.__name__, expr)
        return pos, cond
    elif isinstance(comparison, BinaryResult):
        return extract_binary_result(opseq, pos)
    elif isinstance(comparison, FunctionResult):
        return extract_function(opseq, pos)
    elif isinstance(comparison, ObjectProperty):
        return extract_object_property(opseq, pos)
    else:
        raise UnexpectedOperatorException(comparison)


def extract_function(opseq, pos, func_op=None):
    ensure(opseq.peek(pos), CallFunctionOperator)

    # Extract the argument list
    pos, extracted_args = extract_argument_list(opseq, pos - 1)

    # Replace the old operator with a new one
    if not func_op:
        func_op = opseq.extract(pos)
    call_func_stmt = FunctionCall(func_op.function.name, extracted_args, func_op.function_result)

    return pos, call_func_stmt


def extract_argument_list(opseq, pos):
    ensure(opseq.peek(pos), ListOperator)
    arg_list_op = opseq.extract(pos)

    # If it's a transform list operator, we have to extract the previous list first
    if isinstance(arg_list_op, TransformListOperator):
        pos -= 1
        ensure(opseq.peek(pos), ListOperator)
        arg_list_op = opseq.extract(pos)

    # Extract each argument in the argument list
    args_to_process = list(arg_list_op.lst.value)
    extracted_args = []
    i = 0
    while i < len(args_to_process):
        arg = args_to_process[i]
        i += 1

        # Each argument will be pushed
        pos -= 1
        push_op = opseq.extract(pos)

        # If it's a transform list operator, extend the args we have to process
        if isinstance(push_op, TransformListOperator):
            pos -= 1
            ensure(opseq.peek(pos), ListOperator)
            lst = opseq.extract(pos).lst.value
            args_to_process.extend(lst)
            continue

        ensure(push_op, [
            PushOperator,
            IteratorOperator,
            BinaryOperator,
            PushObjectPropertyOperator,
            FunctionCall,
            CallFunctionOperator
        ])

        if isinstance(push_op, IteratorOperator):
            if isinstance(arg, Integer):
                pos, arg_value = extract_loop_counter_from_iterator_operator(opseq, pos)
            elif isinstance(arg, FunctionResult):
                pos, arg_value = extract_function_result_from_iterator_operator(opseq, pos, arg)
                opseq.insert(pos, arg_value)
                pos += 1
            elif isinstance(arg, Variable):
                arg_value = arg.name
            else:
                raise UnexpectedOperatorException(arg)
        elif isinstance(push_op, FunctionCall):
            arg_value = push_op
        elif isinstance(arg, Literal):
            arg_value = arg.value
        elif isinstance(arg, Variable):
            arg_value = arg.name
        elif isinstance(arg, FunctionResult):
            pos, arg_value = extract_function(opseq, pos, push_op)
        elif isinstance(arg, BinaryResult):
            pos, arg_value = extract_binary_result(opseq, pos, arg.operand)
        elif isinstance(arg, ObjectProperty):
            pos, arg_value = extract_object_property(opseq, pos, arg)
        else:
            raise UnexpectedOperatorException(arg)

        extracted_arg = FunctionCallArgument(arg.__class__.__name__, arg_value)
        extracted_args.append(extracted_arg)

    return pos, extracted_args


def extract_object_property(opseq, pos, obj_prop=None):
    if not obj_prop:
        ensure(opseq.peek(pos), PushObjectPropertyOperator)
    ensure(opseq.peek(pos - 1), PushOperator)
    ensure(opseq.peek(pos - 1).push_value, Variable)

    pos -= 1
    op = opseq.extract(pos)

    var = op.push_value
    ensure(var, Variable)
    obj_var_name = var.name

    if not obj_prop:
        obj_prop = opseq.extract(pos).push_value
    obj_property_name = obj_prop.property_name
    property_ref_op = PropertyReference(obj_var_name, obj_property_name)

    return pos, property_ref_op


def extract_binary_result(opseq, pos, binary_instruction=None):
    """
    Extract a binary result from the OpSeq located at a specified position.

    Args:
      opseq: The OpSeq.
      pos: Position of the binary result.
      binary_instruction: The instruction of the binary result if the operator has already been extracted.
    Returns:
      1: The position from where the binary result was extracted.
      2: A binary intermediate operator
    """
    if not binary_instruction:
        ensure(opseq.peek(pos), BinaryOperator)

    # Find first operand
    pos, right = extract_binary_operand(opseq, pos - 1)

    # Find second operand
    pos, left = extract_binary_operand(opseq, pos - 1)

    # Construct a binary intermediate
    if not binary_instruction:
        op = opseq.extract(pos)
        ensure(op, BinaryOperator)
        binary_instruction = op.push_value.operand  # TODO: Yes, it's misspelled.

    binary_intermediate = BinaryIntermediate(binary_instruction, left, right)

    return pos, binary_intermediate


def extract_unary_result(opseq, pos):
    ensure(opseq.peek(pos), UnaryOperator)

    # Find operand
    pos, operand = extract_binary_operand(opseq, pos - 1)

    # Construct a unary intermediate
    op = opseq.extract(pos)
    ensure(op, UnaryOperator)
    unary_instruction = op.push_value.operator

    unary_intermediate = UnaryIntermediate(unary_instruction, operand)

    return pos, unary_intermediate


def extract_literal(opseq, pos):
    ensure(opseq.peek(pos), PushOperator)
    ensure(opseq.peek(pos).push_value, Literal)
    return pos, opseq.extract(pos).push_value


def extract_variable(opseq, pos):
    ensure(opseq.peek(pos), PushOperator)
    ensure(opseq.peek(pos).push_value, Variable)
    var = opseq.extract(pos).push_value
    return pos, var.name


def extract_binary_operand(opseq, pos):
    # TODO: why is it now a function argument?
    op = opseq.peek(pos)

    if isinstance(op, IteratorOperator):
        # The iterator operator is not the original source of the operator. Find the real one.
        res = opseq.extract(pos).push_value

        if isinstance(res, FunctionResult):
            pos, operand_op = extract_function_result_from_iterator_operator(opseq, pos, res)
        elif isinstance(res, Literal):
            operand_op = FunctionCallArgument(res.__class__.__name__, res.value)
        elif isinstance(res, Variable):
            operand_op = FunctionCallArgument(res.__class__.__name__, res.name)
        else:
            raise UnexpectedOperatorException(res)
    elif isinstance(op, FunctionCall):
        operand_op = opseq.extract(pos)
    elif isinstance(op, PushOperator):
        pos, operand_op = extract_push_operator_as_function_argument(opseq, pos)
    elif isinstance(op, PushObjectPropertyOperator):
        pos, operand_op = extract_object_property(opseq, pos)
    elif isinstance(op, CallFunctionOperator):
        pos, operand_op = extract_function(opseq, pos)
    elif isinstance(op, BinaryOperator):
        pos, operand_op = extract_binary_result(opseq, pos)
    elif isinstance(op, UnaryOperator):
        pos, operand_op = extract_unary_result(opseq, pos)
    else:
        raise UnexpectedOperatorException(op)

    return pos, operand_op


def extract_push_operator_as_function_argument(opseq, pos):
    push_op = opseq.extract(pos)
    ensure(push_op, PushOperator)

    res = push_op.push_value
    val_type = res.__class__.__name__
    val_value = res.value
    if isinstance(res, Variable):
        val_value = res.name

    operand_op = FunctionCallArgument(val_type, val_value)
    return pos, operand_op


def extract_function_result_from_iterator_operator(opseq, pos, res):
    # Traverse backwards from the current function to find the previously parsed operator
    for i, op in enumerate(opseq.operators[pos - 1: 0: -1]):
        if isinstance(op, FunctionCall) and op.name == res.function.name:
            return pos, op

        if isinstance(op, CallFunctionOperator) and op.function.name == res.function.name:
            # However, if it happens to be uncomputed, compute it
            pos, func_op = extract_function(opseq, pos - i - 1)
            return pos + 2, func_op


def extract_loop_counter_from_iterator_operator(opseq, pos):
    for op in opseq.operators[pos - 1: 0: -1]:
        if isinstance(op, AssignVariable) and op.var_type == 'LoopCounter':
            return pos, op.var_name

    raise OperatorNotFoundException()

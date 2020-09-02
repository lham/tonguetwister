# noinspection PyTypeChecker
class OPCode:
    UNK = 'unknown_op'
    RET = 'ret'
    MUL = 'mul'
    ADD = 'add'
    SUB = 'sub'
    DIV = 'div'
    MOD = 'mod'
    NEG = 'neg'
    CONCAT = 'concat'
    CONCAT_S = 'concat_with_space'
    EQ = 'eq'
    NEQ = 'neq'
    LT = 'lt'
    GT = 'gt'
    LEQ = 'leq'
    GEQ = 'geq'
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    CONTAINS = 'contains'
    BEGINS = 'begins'
    STARTS = 'starts'
    SPLIT = 'split'
    HL = 'highlight'
    S_INTERSECT = 'sprite_intersect'
    S_CONTAINS = 'sprite_contains'
    PUSH_CM = 'push_cast_member'
    EXEC_O = 'execute_object_sequence'
    RET_O = 'return_object_sequence'
    T_LIST = 'transform_list'
    MAKE_DICT = 'make_dict'
    MAKE_ARG_LIST = 'create_arg_list'
    MAKE_LIST = 'create_list'
    PUSH_ZERO = 'push_zero'
    PUSH_INTEGER = 'push_int'
    PUSH_CONST = 'push_const'
    PUSH_SYMBOL = 'push_symbol'
    PUSH_OBJECT = 'push_object'
    PUSH_GLOBAL_VAR = 'push_global'
    PUSH_PROPERTY = 'push_property_value'
    PUSH_FUNCTION_ARGUMENT = 'push_function_argument'
    PUSH_LOCAL_VAR = 'push_local'
    SET_GLOBAL_VAR = 'pop_and_set_global'
    SET_PROPERTY = 'pop_and_set_property_value'
    SET_FUNCTION_ARGUMENT = 'pop_and_set_function_argument'
    SET_LOCAL_VAR = 'pop_and_set_local'
    REP_END = 'end_repeat'
    CALL_EXT = 'call_external_function'
    CALL_LOCAL = 'call_local_function'
    CALL_OBJ = 'call_object_function'
    GET = 'get'
    SET = 'set'
    GET_P = 'get_property'
    SET_P = 'set_property'
    SET_OP = 'set_object_property'
    GET_OP = 'get_object_property'
    IF_TRUE = 'if_true'
    ELSE = 'else'
    IT_INCR = 'iterator_var_incrementor'
    IT_CLEAN = 'iterator_cleanup'
    GOTO = 'goto'

    # Bytecode instructions init
    TOKENS = [None] * 0xFF

    # One byte instructions
    TOKENS[0x00] = (0x00, UNK, '', '')
    TOKENS[0x01] = (0x01, RET, 'ReturnOperator', 'return')
    TOKENS[0x02] = (0x02, UNK, '', '')
    TOKENS[0x03] = (0x03, PUSH_ZERO, 'PushOperator', '')
    TOKENS[0x04] = (0x04, MUL, 'BinaryOperator', '*')
    TOKENS[0x05] = (0x05, ADD, 'BinaryOperator', '+')
    TOKENS[0x06] = (0x06, SUB, 'BinaryOperator', '-')
    TOKENS[0x07] = (0x07, DIV, 'BinaryOperator', '/')
    TOKENS[0x08] = (0x08, MOD, 'BinaryOperator', '%')
    TOKENS[0x09] = (0x09, NEG, 'UnaryOperator', '-')
    TOKENS[0x0A] = (0x0A, CONCAT, 'BinaryOperator', '&')
    TOKENS[0x0B] = (0x0B, CONCAT_S, 'BinaryOperator', '&&')
    TOKENS[0x0C] = (0x0C, LT, 'BinaryOperator', '<')
    TOKENS[0x0D] = (0x0D, LEQ, 'BinaryOperator', '<=')
    TOKENS[0x0E] = (0x0E, NEQ, 'BinaryOperator', '!=')
    TOKENS[0x0F] = (0x0F, EQ, 'BinaryOperator', '==')
    TOKENS[0x10] = (0x10, GT, 'BinaryOperator', '>')
    TOKENS[0x11] = (0x11, GEQ, 'BinaryOperator', '>')
    TOKENS[0x12] = (0x12, AND, 'BinaryOperator', 'and')
    TOKENS[0x13] = (0x13, OR, 'BinaryOperator', 'or')
    TOKENS[0x14] = (0x14, NOT, 'UnaryOperator', 'not')
    TOKENS[0x15] = (0x15, CONTAINS, 'BinaryOperator', 'contains')
    TOKENS[0x16] = (0x16, BEGINS, 'BinaryOperator', 'starts')
    TOKENS[0x17] = (0x17, STARTS, 'SubstringOperator', '<chunker>')
    TOKENS[0x18] = (0x18, HL, 'SubstringOperator', '???')
    TOKENS[0x19] = (0x19, S_INTERSECT, 'BinaryOperator', '???')
    TOKENS[0x1A] = (0x1A, S_CONTAINS, 'BinaryOperator', '???')
    TOKENS[0x1B] = (0x1B, PUSH_CM, 'UnaryOperator', '???')
    TOKENS[0x1C] = (0x1C, EXEC_O, 'Operator', '')
    TOKENS[0x1D] = (0x1D, RET_O, 'Operator', '')
    TOKENS[0x1E] = (0x1E, T_LIST, 'TransformListOperator', '')
    TOKENS[0x1F] = (0x1F, MAKE_DICT, 'Operator', '')

    # Two byte instructions
    TOKENS[0x41] = (0x41, PUSH_INTEGER, 'PushOperator', '')
    TOKENS[0x42] = (0x42, MAKE_ARG_LIST, 'ListOperator', '')
    TOKENS[0x43] = (0x43, MAKE_LIST, 'ListOperator', '')
    TOKENS[0x44] = (0x44, PUSH_CONST, 'PushOperator', '')
    TOKENS[0x45] = (0x45, PUSH_SYMBOL, 'PushOperator', '')
    TOKENS[0x46] = (0x46, PUSH_OBJECT, 'PushOperator', '')
    TOKENS[0x47] = (0x47, UNK, 'Operator', '')
    TOKENS[0x48] = (0x48, UNK, 'Operator', '')
    TOKENS[0x49] = (0x49, PUSH_GLOBAL_VAR, 'PushOperator', '')
    TOKENS[0x4A] = (0x4A, PUSH_PROPERTY, 'PushOperator', '')
    TOKENS[0x4B] = (0x4B, PUSH_FUNCTION_ARGUMENT, 'PushOperator', '')
    TOKENS[0x4C] = (0x4C, PUSH_LOCAL_VAR, 'PushOperator', '')
    TOKENS[0x4D] = (0x4D, UNK, 'Operator', '')
    TOKENS[0x4E] = (0x4E, UNK, 'Operator', '')
    TOKENS[0x4F] = (0x4F, SET_GLOBAL_VAR, 'AssignmentOperator', '')
    TOKENS[0x50] = (0x50, SET_PROPERTY, 'AssignmentOperator', '')
    TOKENS[0x51] = (0x51, SET_FUNCTION_ARGUMENT, 'AssignmentOperator', '')
    TOKENS[0x52] = (0x52, SET_LOCAL_VAR, 'AssignmentOperator', '')
    TOKENS[0x53] = (0x53, UNK, 'Operator', '')  # jump?
    TOKENS[0x54] = (0x54, REP_END, 'EndRepeatOperator', '')
    TOKENS[0x55] = (0x55, UNK, 'Operator', '')  # if true?
    TOKENS[0x56] = (0x56, CALL_LOCAL, 'CallFunctionOperator', '')
    TOKENS[0x57] = (0x57, CALL_EXT, 'CallFunctionOperator', '')
    TOKENS[0x58] = (0x58, CALL_OBJ, 'Operator', '')
    TOKENS[0x59] = (0x59, UNK, 'ModifyStringOperator', '')  # insert_into_text_var?
    TOKENS[0x5A] = (0x5A, UNK, 'Operator', '')  # put_value?
    TOKENS[0x5B] = (0x5B, UNK, 'Operator', '')  # delete?
    TOKENS[0x5C] = (0x5C, SET, 'Operator', '')
    TOKENS[0x5D] = (0x5D, GET, 'Operator', '')
    TOKENS[0x5E] = (0x5E, UNK, 'Operator', '')
    TOKENS[0x5F] = (0x5F, GET_P, 'Operator', '')
    TOKENS[0x60] = (0x60, SET_P, 'Operator', '')
    TOKENS[0x61] = (0x61, GET_OP, 'PushObjectPropertyOperator', '')
    TOKENS[0x62] = (0x62, SET_OP, 'Operator', '')
    TOKENS[0x63] = (0x63, UNK, 'Operator', '')
    TOKENS[0x64] = (0x64, IT_INCR, 'IteratorOperator', '')
    TOKENS[0x65] = (0x65, IT_CLEAN, 'CleanupIteratorOperator', '')

    # Three byte instructions
    TOKENS[0x80] = (0x80, UNK, 'Operator', '')
    TOKENS[0x81] = (0x81, PUSH_INTEGER, 'LargePushOperator', '')
    # 0x82 = Large 0x42 but with more than 255 list elements? (mk arg list)
    # 0x83 = Large 0x43 but with more than 255 list elements? (mk list)
    # 0x84 = Large 0x44 but with bigger index? (const)
    TOKENS[0x85] = (0x85, PUSH_SYMBOL, 'LargePushOperator', '')  # large-push something (symbol)
    TOKENS[0x86] = (0x86, PUSH_OBJECT, 'LargePushOperator', '')  # First param of 0x58 call (object)
    # 0x87 = ?
    # 0x88 = ?
    TOKENS[0x89] = (0x89, PUSH_GLOBAL_VAR, 'LargePushOperator', '')  # correct?

    # 0x8F = Large 0x4F but with bigger index?
    # 0x90 = Large 0x50 but with bigger index?

    TOKENS[0x93] = (0x93, ELSE, 'ElseOperator', '')
    TOKENS[0x94] = (0x94, GOTO, 'GotoOperator',
                    '')  # I think this is a GOTO with jmp_addr = self.opcode.addr - (self.arg1 * 0x100) + self.arg2
    TOKENS[0x95] = (0x95, IF_TRUE, 'IfTrueOperator', '')
    TOKENS[0x96] = (0x96, UNK, 'Operator', '')
    TOKENS[0x97] = (0x97, CALL_EXT, 'LargeCallFunctionOperator', '')

    TOKENS[0xA6] = (0xA6, CALL_LOCAL, 'LargeCallFunctionOperator', '')  # TODO: Not entirely sure if correct

    def __init__(self, addr, byte):
        token = self.TOKENS[byte]

        if token is None:
            raise RuntimeError(f'The OPCode {byte:#2x} is not reverse engineered yet')

        self.value = byte
        self.name = token[1]
        self.class_name = token[2]
        self.lingo_name = token[3]
        self.addr = addr

    def is_single_byte_instruction(self):
        return 0x00 <= self.value < 0x40

    def is_two_byte_instruction(self):
        return 0x40 <= self.value < 0x80

    def is_three_byte_instruction(self):
        return 0x80 <= self.value

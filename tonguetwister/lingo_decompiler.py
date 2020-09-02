from tonguetwister.decompiler.code_generator import generate_code
from tonguetwister.decompiler.detokenizer import detokenize
from tonguetwister.decompiler.name_parser import replace_names
from tonguetwister.decompiler.reconstructor import reconstruct_statements


class Decompiler:
    @staticmethod
    def to_pseudo_code(function, namelist, script):
        operator_list = detokenize(function.bytecode)
        print('-------------------------------')
        replace_names(operator_list, function, namelist, script)
        print('-------------------------------')
        reconstruct_statements(operator_list)
        print('-------------------------------')

        return generate_code(operator_list, function, namelist)

    @staticmethod
    def to_c_code(function, namelist, script):
        pass

    @staticmethod
    def to_lingo_code(function, namelist, script):
        pass

from tonguetwister.decompiler.code_generator import generate_code
from tonguetwister.decompiler.detokenizer import detokenize
from tonguetwister.decompiler.name_parser import replace_names
from tonguetwister.decompiler.reconstructor import reconstruct_statements


class Decompiler:
    def __init__(self, catch_exceptions=False):
        self._catch_exceptions = catch_exceptions

        self.detokenized_operators = []
        self.named_operators = []
        self.reconstructed_operators = []
        self.generated_code = []
        self.exception = None

    def has_exception(self):
        return self.exception is not None

    def to_pseudo_code(self, function, namelist, script):
        try:
            self._unsafe_to_pseudo_code(function, namelist, script)
        except Exception as ex:
            self.exception = ex
            if not self._catch_exceptions:
                raise ex

    def _unsafe_to_pseudo_code(self, function, namelist, script):
        operator_list = self._get_operator_list(function, namelist, script)
        self.generated_code = generate_code(operator_list, function, namelist)

    def _get_operator_list(self, function, namelist, script):
        operator_list = detokenize(function.bytecode)
        self.detokenized_operators = [op.raw_detokenization_string() for op in operator_list]

        operator_list = replace_names(operator_list, function, namelist, script)
        self.named_operators = [str(op) for op in operator_list]

        operator_list = reconstruct_statements(operator_list)
        self.reconstructed_operators = [str(op) for op in operator_list]

        return operator_list

    def to_c_code(self, function, namelist, script):
        pass

    def to_lingo_code(self, function, namelist, script):
        pass

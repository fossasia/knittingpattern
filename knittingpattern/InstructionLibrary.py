from knittingpattern.Instruction import Instruction

TYPE = "type"

class InstructionLibrary(object):

    from .Loader import Loader
    
    @property
    def load(self):
        return self.Loader(self._process_loaded_object)
        
    def _process_loaded_object(self, obj):
        self.library = obj
        self._create_type_to_index_dict()
        return self
    
    def _create_type_to_index_dict(self):
        temp_dict = {}
        index = 0
        for instruction_def in self.library:
            instruction_type = instruction_def[TYPE]
            temp_dict[instruction_type] = index
            index += 1
        self.type_to_index_dict = temp_dict
        
    def find_instruction_def(self, instruction_type):
        index = self.type_to_index_dict[instruction_type]
        return self.library[index]
        
    def as_instruction(self, stitch_def):
        instruction_type = stitch_def[TYPE]
        instruction_def = self.find_instruction_def(instruction_type)
        instruction_def.update(stitch_def)
        return Instruction(instruction_def)
        
from pprint import pprint
import json
from collections import OrderedDict

from chunks.lingo_script import LingoScript
from chunks.lingo_namelist import LingoNamelist
from chunks.styled_text import StyledText
from chunks.font_map import FontMap
from chunks.memory_map import MemoryMap
from chunks.cast_library_info import CastLibraryInfo
from chunks.cast_key_map import CastKeyMap
from chunks.cast_member import CastMember
from chunks.idealized_map import IdealizedMap
from chunks.drcf import DRCF
from chunks.cast_association_map import CastAssociationMap
from chunks.lingo_context import LingoContext
from lib.byte_block_io import ByteBlockIO
from lib.helper import grouper

class RifxParser(object):
  FOUR_CC_FUNCTION_MAP = {
    'CASt': 'parse_cast',
    'STXT': 'parse_STXT', 
    'Cinf': 'parse_Cinf', 
    'Fmap': 'parse_fmap', 
    'free': 'parse_undefined', 
    'Lctx': 'parse_lctx',
    'Lnam': 'parse_Lnam', 
    'Lscr': 'parse_Lscr', 
    'CAS*': 'parse_cas_star', 
    'imap': 'parse_imap', 
    'DRCF': 'parse_drcf', 
    'ccl ': 'parse_undefined',
    'RIFX': 'parse_RIFX', 
    'mmap': 'parse_mmap', 
    'KEY*': 'parse_key_star',
    'RTE0': 'parse_undefined',
    'RTE1': 'parse_undefined',
    'RTE2': 'parse_undefined',
    'FXmp': 'parse_undefined',
    'MCsL': 'parse_undefined',
    'Sord': 'parse_undefined'
  }

  def __init__(self, filename, silent=False):
    self.stack_depth = 0
    self.silent = silent

    with open(filename, 'rb') as f:
      stream = ByteBlockIO(f.read())
      four_cc, addr, chunk = self.__parse_command(stream)
      
      if four_cc == 'RIFX':
        self.version = chunk.uint32()
        self.stream = ByteBlockIO(chunk.read_bytes())
      else:
        raise Exception('Input file not a RIFX file.')

  def unpack(self):
    while not self.stream.is_depleted():
      four_cc, address, chunk_stream = self.__parse_command(self.stream)
      self.current_four_cc = four_cc
      self.current_address = address + 12  # Add 12 bytes for the RIFX chunk
      
      function_name = self.FOUR_CC_FUNCTION_MAP[four_cc]
      func = getattr(self, function_name, self.__undefined_function)
      func(chunk_stream)

      if not chunk_stream.is_depleted():
        print chunk_stream.n_processed_bytes_string()
        print chunk_stream.unprocessed_bytes()
        raise Exception('[%s]: Unprocessed data remains.' % four_cc)

  def __parse_command(self, stream):
    address = stream.tell()
    four_cc = stream.string(4)

    chunk_length = stream.uint32()
    chunk = ByteBlockIO(stream.read_bytes(chunk_length))

    # Remove padding for uneven blocks
    if chunk_length % 2 != 0:
      pad = stream.uint8()
      if pad != 0:
        raise Exception('Pad is non-zero')

    return four_cc, address, chunk

  def __undefined_function(self, stream):
    print self.__chunk_info('FOUR_CC PARSER FUNCTION NOT IMPLEMENTED')
    stream.read_bytes()

  def __chunk_info(self, message=''):
    args = (
        self.__indent_string(),
        self.current_address,
        self.current_address,
        self.current_four_cc,
        message)

    return '%s[%5d / %#6x] :: %s --> %s' % args if self.silent else ''

  def __indent_string(self, offset=0):
    return '    '*(self.stack_depth+offset)

  def __parse_pad(self, stream, n):
    stream.read_bytes(n)

  def parse_STXT(self, stream):
    if not hasattr(self, 'styled_texts'):
      self.styled_texts = OrderedDict()

    self.styled_texts[self.current_address] = StyledText(stream)
    print self.__chunk_info()
    #print repr(self.styled_texts[self.current_address])

  def parse_cast(self, stream):
    if not hasattr(self, 'cast_members'):
      self.cast_members = OrderedDict()

    self.cast_members[self.current_address] = CastMember(stream)
    print self.__chunk_info()
    #print repr(self.cast_members[self.current_address])

  def parse_fmap(self, stream):
    self.font_map = FontMap(stream)
    print self.__chunk_info()
    #print repr(self.font_map)

  def parse_Lnam(self, stream):
    self.namelist = LingoNamelist(stream)
    print self.__chunk_info() 
    #print repr(self.namelist)

  def parse_Cinf(self, stream):
    self.cast_library_info = CastLibraryInfo(stream)
    print self.__chunk_info()
    #print repr(self.cast_library_info)

  def parse_Lscr(self, stream):
    if not hasattr(self, 'lingo_scripts'):
      self.lingo_scripts = OrderedDict()

    self.lingo_scripts[self.current_address] = LingoScript(stream)
    print self.__chunk_info()
    #print repr(self.lingo_scripts[self.current_address])
       
  def parse_imap(self, stream):
    self._imap = IdealizedMap(stream)
    print self.__chunk_info()
    #print repr(self._imap)

  def parse_drcf(self, stream):
    self._imap = DRCF(stream)
    print self.__chunk_info()
    #print repr(self._imap)

  def parse_cas_star(self, stream):
    self.cast_assoc_map = CastAssociationMap(stream)
    print self.__chunk_info()
    #print repr(self.cast_assoc_map)

  def parse_key_star(self, stream):
    self.cast_key_map = CastKeyMap(stream)
    print self.__chunk_info()
    #print repr(self.cast_key_map)

  def parse_mmap(self, stream):
    self.memory_map = MemoryMap(stream)
    print self.__chunk_info()
  #  print repr(self.memory_map)

  def parse_lctx(self, stream):
    self.lingo_context = LingoContext(stream)
    print self.__chunk_info()
    #print repr(self.lingo_context)

  def __create_cast_lib(self):
    self.cast_lib = []

    """
    Iterate the CAS*:
      Add CASt to cast library AS entry:
        i = mmap-index of CASt in mmap
        Lookup mmap[i], add CASt data to entry

        k = mmap-index of key*(cast_mmap_idx=i)
        Lookup mmap[k] and add media type data to entry
    """

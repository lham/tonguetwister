from itertools import izip_longest

def grouper(ws, size, newline=False, indent=1):
  hex_str =  ''.join('{:02x}'.format(ord(b)) for b in ws)
  return ('%s%s' % ('\n' if newline else '', ' '*indent)).join([hex_str[i:i+size] for i in range(0, len(hex_str), size)])

def splat_ordered_dict(odict):
  return ', '.join('%s: %s' % (k, v) for k, v in odict.iteritems())

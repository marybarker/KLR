import re
import string

class single_braid(): 
  def __init__(self, word, colors, cartan): 
    # make sure notation is in standard form 
    word = str(word).replace('Y','y').replace('S', 's')
    # extract all dots and crossings with associated strand numbers 
    y_and_s = re.sub('\d+', ' ', word).split(' ')[:-1]
    nums = re.sub('[ys]', ' ', word).split(' ')[1:]

    self.c = colors
    self.cartan = cartan
    self.string_char = y_and_s
    self.string_nums = nums
    self.num_dots = y_and_s.count('y')
    self.num_crossings = y_and_s.count('s')

class braid():
  def __init__(self, word, colors, cartan): 
    b = single_braid(word, colors, cartan)
    self.terms = [b]
    self.coefs = [1]


def s(n, strand):
  """ 
  Gives the new value of 
  strand after the switch Sn 
  """
  if strand == n: 
    return strand + 1
  elif strand == (n + 1): 
    return n
  else: 
    return strand

def color_find(strand_no, braid_level, braid): 
  """ 
  Find the color of strand number strand_no 
  at the braid_level level in the braid
  """ 
  nums = braid.nums[braid_level:-1]
  n = strand_no
  for i_num in nums: 
    n = s(i_num, n)
  return braid.c[n]

def slide_dots(braid_list): 
  error_terms = list()
  error_coefs = list()

  i_b = 0
  # for each braid term in the list... (has to be a while loop, bc terms get added on inside)
  while(i_b < len(braid_list.terms)):
    b = braid_list.terms[i_b]

    # now for each instance of a dot in that particular braid, go through and move completely over
    for k in range(0, b.num_dots):
      for i in range(0, len(b.string_char)): 
        s_1 = b.string_char[i]
        n_1 = b.string_nums[i]

        if(s_1 == 'y'): 
          for j in range(i+1, len(b.string_char)): 
            s_2 = b.string_char[j]
            n_2 = b.string_nums[j]

            if(s_2 == 's'): 
              if (n_2 == n_1):
                b.string_char = b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]
                b.string_nums = b.string_nums[0:i]+b.string_nums[i+1:j+1]+[n_1]+b.string_nums[j+1:]

                new_word = b.string_char[0:j-1]+b.string_char[j+1:]
                new_nums = b.string_nums[0:j-1]+b.string_nums[j+1:]
                new_braid_word = zip(new_word, new_nums)
                new_braid_word = ''.join([''.join(a) for a in new_braid_word])
                newbraid = single_braid(new_braid_word, b.c, b.cartan)

                error_terms.append(newbraid)
                error_coefs.append(-1*braid_list.coefs[i_b])

              elif (int(n_1) == (int(n_2) + 1)):
                b.string_char = b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]
                b.string_nums = b.string_nums[0:i]+b.string_nums[i+1:j+1]+[n_1]+b.string_nums[j+1:]

                new_word = b.string_char[0:j-1]+b.string_char[j+1:]
                new_nums = b.string_nums[0:j-1]+b.string_nums[j+1:]
                new_braid_word = zip(new_word, new_nums)
                new_braid_word = ''.join([''.join(a) for a in new_braid_word])
                newbraid = single_braid(new_braid_word, b.c, b.cartan)

                error_terms.append(newbraid)
                error_coefs.append(braid_list.coefs[i_b])

              else: 
                b.string_char = b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]
                b.string_nums = b.string_nums[0:i]+b.string_nums[i+1:j+1]+[n_1]+b.string_nums[j+1:]

              i = j 
              j = j + 1

    braid_list.terms[i_b] = b
    if(len(error_terms) > 0):
      braid_list.terms = braid_list.terms + error_terms
      braid_list.coefs = braid_list.coefs + error_coefs
      error_terms = list()
      error_coefs = list()
    i_b = i_b + 1

  return braid_list

def remove_doubles(mybraid):
  # only loop through the crossings, bc dots don't matter for this
  for i in range(0, mybraid.num_crossings):
    num_i = mybraid.string_nums[i]

    for j in range(i+1, mybraid.num_crossings):
      num_j = mybraid.string_nums[j]

      if num_j == num_i: 
        can_delete = True

        for k in range(i+1, j):
          if mybraid.string_char[k] != 'd': 
            num_k = int(mybraid.string_nums[k])
            if( abs(num_k - i) < 2 ): 
              can_delete = False

        if can_delete:
          mybraid.string_char[i] = 'd'
          mybraid.string_char[j] = 'd'

  i = 0
  while i < mybraid.num_crossings: 
    if mybraid.string_char[i] == 'd': 
      mybraid.num_crossings = mybraid.num_crossings - 1
      mybraid.string_char.pop(i)
      mybraid.string_nums.pop(i)
      i = i - 1

    i = i + 1
  return mybraid,[]

def order_descending(mybraid): 
  for i in reversed(range(0, mybraid.num_crossings)):
    for j in range(0, i):
      n1 = mybraid.string_nums[j]
      n2 = mybraid.string_nums[j+1]
      if (int(n2) - int(n1)) > 1 : 
        mybraid.string_nums[j] = n2
        mybraid.string_nums[j+1] = n1
  return mybraid,[]

def flip(mybraid):
  for i in range(0, mybraid.num_crossings-2):
    n1 = int(mybraid.string_nums[i  ])
    n2 = int(mybraid.string_nums[i+1])
    n3 = int(mybraid.string_nums[i+2])

    if( (n1 == n3) & ((n1 - n2) == -1) ):
      mybraid.string_nums[i  ] = n2
      mybraid.string_nums[i+1] = n1
      mybraid.string_nums[i+2] = n2
  return mybraid,[]

def canonical_form(braid_list):
  error_terms = list()

  i_b = 0
  while(i_b < len(braid_list.terms)): 
    error_terms = list()

    b = braid_list.terms[i_b]
    in_canonical_form = True

    while in_canonical_form:
      in_canonical_form = False

      b, new_terms = order_descending(b)
      b, new_terms = remove_doubles(b)
      if( len(new_terms) > 0 ): 
        in_canonical_form = True
        error_terms = error_terms + new_terms

      b, new_terms = flip(b)
      if( len(new_terms) > 0 ):
        in_canonical_form = True
        error_terms = error_terms + new_terms

    if( len(error_terms) > 0): 
      braid_list.terms = braid_list.terms + error_terms
      braid_list.terms = braid_list.terms + [braid_list.coefs[i_b] for i in range(0, len(error_terms))]

    braid_list.terms[i_b] = b

    i_b = i_b + 1
  return braid_list

thing = braid('s1y3s2s6s2', '123456', 1)
print 80*'*'
print zip(thing.terms[0].string_char, thing.terms[0].string_nums)
print 80*'*'
print

g = slide_dots(thing)
print
print 80*'*'
print [zip(i.string_char, i.string_nums) for i in g.terms]
print 80*'*'

other = braid('s1s4s3y4s3y2s5s6y3y2s4', '123', 1)
print
print
print
print 80*'*'
print [zip(i.string_char, i.string_nums) for i in other.terms]

other = slide_dots(other)

h = canonical_form(other)
print 80*'*'
print [zip(i.string_char, i.string_nums) for i in h.terms]
print 80*'*'



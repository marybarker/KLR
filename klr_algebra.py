import re
import string
run_tests = False

def plusminus(a):
    if a < 0:
        return ' - '+str(abs(a))
    else: 
        return ' + '+str(abs(a))

class braid():

    cartan = 1

    def __init__(self, word, colors, num=-1, coef=1.0):
        # make sure notation is in standard form
        word = str(word).replace('Y','y').replace('S', 's')
        # extract all dots and crossings with associated strand numbers 
        y_and_s = re.sub('\d+', ' ', word).split(' ')[:-1]
        nums = re.sub('[ys]', ' ', word).split(' ')[1:]

        y_ns = [int(nums[i]) for i in range(len(nums)) if y_and_s[i] == 'y']
        s_ns = [int(nums[i]) for i in range(len(nums)) if y_and_s[i] == 's']
        y_max = max(y_ns) if y_ns else 0
        s_max = max(s_ns) if s_ns else 0

        self.max_strands = max(num, max(s_max + 1, y_max))

        if( len(colors) < self.max_strands): 
            colors = self.max_strands*'i'

        self.c = colors
        self.word = word
        self.string_char = y_and_s
        self.string_nums = nums
        self.num_dots = y_and_s.count('y')
        self.num_crossings = y_and_s.count('s')
        self.coef = coef
        self.dots_at_top = False

    def __mul__(self, other):
        if isinstance(other, braid):
            c1 = other.c
            c2 = ''
            return_val = braid('', '', self.max_strands)

            for col in range(self.max_strands): 
                c2 = c2 + self.color_find(col+1, 0)
            if str(c1) == str(c2): 
                word = self.word + other.word
                return_val = braid(word, c1, self.max_strands)
        else:
            return_val = braid(self.word, self.c, self.max_strands)
            return_val.coef = other.coef * self.coef
        return return_val

    def __add__(self, other):
        if isinstance(other, braid): 
            if( (other.c == self.c) and (other.word == self.word) ): 
                return_val = braid(other.word, other.c, other.max_strands, other.coef + self.coef)
                return_val = [return_val]
        return_val = [self, other]
        return return_val

    def color_find(self, strand_no, braid_level): 
        """ 
        Return the color of strand in position strand_no 
        at the braid_level level in the braid (counting from 
        the bottom of the braid up)
        """ 
        n = strand_no 
        for ii in range(braid_level, len(self.string_nums)): 
            if(self.string_char[ii] == 's'): 
                i_num = int(self.string_nums[ii])
                n = self.s(i_num, n)
        return self.c[n - 1]

    def are_same(self, level, n1, n2): 
        c1 = self.color_find(n1, level)
        c2 = self.color_find(n2, level)
        return c1 == c2

    def s(self, n, strand):
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

    def draw(self): 

        if( len(self.word) > 0): 
            outstr = ''
            for i in range(self.max_strands):
                outstr = outstr+str(self.c[i])+'  '
            print outstr

            outstr = self.max_strands * '|  '

            for i in reversed(range(len(self.string_char))):
                char = self.string_char[i]
                num = int(self.string_nums[i])

                if char == 'y': 
                    old_char = outstr[3*(num-1)]
                    if old_char == 'o': 
                        print outstr
                        outstr = self.max_strands * '|  '
                    outstr = outstr[0:3*(num-1)]+'o  '+outstr[3*num:-1]
                else: 
                    print outstr
                    outstr = self.max_strands*'|  '
                    a = 3*(num-1) + 4
                    b = 3*(num-1) + 0
                    outstr = outstr[0:b]+' \\'+'/ '+outstr[a:-1]
                    print outstr
                    outstr = outstr[0:b]+' /'+'\\ '+outstr[a:-1]
                    print outstr
                    outstr = self.max_strands * '|  '
            print outstr
            colors = '' 
            for col in range(self.max_strands): 
                colors = colors + self.color_find(col+1, 0) + '  '
            print colors
            """
            outstr = ''
            for i in range(self.max_strands):
                outstr = outstr+str(self.c[i])+' '
            print outstr

            outstr = self.max_strands * '| '
            for i in reversed(range(len(self.string_char))):
                char = self.string_char[i]
                num  = int(self.string_nums[i])
                if char == 'y': 
                    print outstr
                    outstr=self.max_strands * '| '
                    outstr=outstr[0:2*(num-1)]+'o '+outstr[2*(num-1)+2:-1]
                else: 
                    print outstr
                    outstr=self.max_strands * '| '
                    a = 2*num
                    b = 2*num-1
                    c = 2*num-2
                    outstr=outstr[0:c]+' X '+outstr[c+3:-1]
                    print outstr
                    outstr = self.max_strands * '| '
            print outstr
            colors = '' 
            for col in range(self.max_strands): 
                colors = colors + self.color_find(col+1, 0) + ' '
            print colors
            """
        else: 
            print

def print_braid(input_braid):
    mystring = ''
    if isinstance(input_braid, braid): 
        if len(input_braid.word) > 0: 
            mystring = str(input_braid.coef) + input_braid.word
    else: 
        for b in range(len(input_braid)):
            if len(input_braid[b].word) > 0: 
                if len(mystring) > 0:
                    mystring = mystring + plusminus(input_braid[b].coef) + input_braid[b].word
                else: 
                    mystring = str(input_braid[b].coef) + input_braid[b].word
    print
    print mystring
    print

""" " " " " " TEST Braid class arithmetic " " " " " """
if(run_tests):
  print 'Beginning testing basic braid class'
  braid1 = braid('s1s2s7y2s3y4s4', '12')
  braid2 = braid('s1s2s3', '1234')
  braid3 = braid('s1s3s2', '4123')
  print [i.word for i in braid1 + braid2]
  print (braid1*braid2).word
  print (braid2*braid3).word
  print braid2.max_strands

  for i in braid1+braid2: 
       print_braid(i)
       i.draw()
  print '... Finished testing basic braid class'

""" " " " " " " "  " " " " " " " " " " " " " " " " " """

def slide_dots(input_braid): 
    error_terms = list()
    if isinstance(input_braid, braid):
        braid_list = [input_braid]
    else: 
        braid_list = input_braid
    i_b = 0
    # for each braid term in the list... (has to be a while loop, bc terms get added on inside)
    while(i_b < len(braid_list)):
        b = braid(braid_list[i_b].word, braid_list[i_b].c, braid_list[i_b].max_strands, braid_list[i_b].coef)
        if((braid_list[i_b].dots_at_top == False) and (braid_list[i_b].num_dots > 0)): 
      
            # now for each instance of a dot in that particular braid, move to farthest side
            for k in range(len(b.string_char)):
                no_change_i = True
                for i in range(len(b.string_char)): 
                    if(no_change_i): 
                        s_1 = b.string_char[i]
                        n_1 = b.string_nums[i]
                    
                        if(s_1 == 'y'): 
                            no_change_j = True
                            for j in range(i+1, len(b.string_char)): 
                                if(no_change_j):
                                    s_2 = b.string_char[j]
                                    n_2 = b.string_nums[j]
                                  
                                    if(s_2 == 's'): 
                                        if( (n_1 == n_2) or (int(n_1) == (int(n_2) + 1)) ):
                                            no_change_i = False
                                            no_change_j = False
                                            y_n = str(b.s(int(n_2), int(n_1))) # new string index for y after strand switch
                                            b.string_char=b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]
                                            b.string_nums=b.string_nums[0:i]+b.string_nums[i+1:j+1]+[y_n]+b.string_nums[j+1:]
                                            b.word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])
                                            b.num_dots = b.word.count('y')
                                            b.num_crossings = b.word.count('s')
                                
                                            # check if the two strands are the same 'color'
                                            if(n_2 == n_1): 
                                                same = b.are_same(j, int(n_1), int(n_1)+1)
                                            else: 
                                                same = b.are_same(j, int(n_1), int(n_1)-1)
                                          
                                            # error terms are introduced only when the strands are the same color. 
                                            if(same): 
                                                new_word = b.string_char[0:j-1]+b.string_char[j+1:]
                                                new_nums = b.string_nums[0:j-1]+b.string_nums[j+1:]
                                                new_braid_word = zip(new_word, new_nums)
                                                new_braid_word = ''.join([''.join(a) for a in new_braid_word])
                                                newbraid = braid(new_braid_word, b.c, b.max_strands, b.coef)
                                
                                                if(n_2 == n_1): 
                                                    newbraid.coef = -1*b.coef
                                                else:
                                                    newbraid.coef = b.coef
                                                error_terms= error_terms + [newbraid]
                                        else: 
                                            b.string_char=b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]
                                            b.string_nums=b.string_nums[0:i]+b.string_nums[i+1:j+1]+[n_1]+b.string_nums[j+1:]
                                            b.word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])
                                            b.num_dots = b.word.count('y')
                                            b.num_crossings = b.word.count('s')
                                        i = j 
                                        j = j + 1
          
            braid_list[i_b] = b
            if(len(error_terms) > 0):
                braid_list = braid_list + error_terms
                error_terms = list()
            i_b = i_b + 1
        else: 
            i_b = i_b + 1

    for b in braid_list: 
        b.dots_at_top = True

    return braid_list

""" " " " " " " " " " " TEST sliding dots " " " " " " " " " " " """
if(run_tests):
  print
  print "testing slide_dots routine..."

  braid4 = braid('y1s3s2y3s3s1', 'iiii')
  #s3s2y3s3y1s1 -> s3s2s3y1s1y4 - s3s2y1s1 
  #             -> s3s2s3s1y2y4 - s3s2s3y4 - s3s2y1s1 
  #             -> s3s2s3s1y2y4 - s3s2s3y4 - s3s2s1y2 + s3s2
  print braid4.word
  braid4 = slide_dots(braid4)
  print [i.word for i in braid4]
  for i in braid4: 
      print_braid(i)
      i.draw()
  print '...finished testing slide_dots'
  print

""" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " """

def remove_doubles(mybraid):
    nothing_changed = True
    if isinstance(mybraid, braid):
        # only loop through the crossings, bc dots don't matter for this
        if(mybraid.dots_at_top):
            bcopy = braid(mybraid.word, mybraid.c, mybraid.max_strands, mybraid.coef)
            bcopy.coef = mybraid.coef

            for i in range(bcopy.num_crossings):
                num_i = bcopy.string_nums[i]
                if bcopy.string_char[i] != 'd':

                    for j in range(i+1, bcopy.num_crossings):
                        num_j = bcopy.string_nums[j]

                        if num_j == num_i: 
                            can_delete = True

                            for k in range(i+1, j):
                                if bcopy.string_char[k] != 'd': 
                                    num_k = int(bcopy.string_nums[k])
                                    if( abs(num_k - int(num_i)) < 2 ): 
                                        can_delete = False

                            if can_delete:
                                bcopy.string_char[i] = 'd'
                                bcopy.string_char[j] = 'd'
                                nothing_changed = False
            i = 0
            while i < bcopy.num_crossings: 
                if bcopy.string_char[i] == 'd': 
                    n1 = bcopy.string_nums[i]
                    n2 = bcopy.string_nums[i+1]
                    if(bcopy.are_same(int(n1),int(n2),i)): 
                        bcopy = braid('','', num=0)
                    else: 
                        bcopy.num_crossings = bcopy.num_crossings - 1
                        bcopy.string_char.pop(i)
                        bcopy.string_nums.pop(i)
                        i = i - 1
                    nothing_changed = False
                i = i + 1
            return [bcopy], nothing_changed
        else: 
            print "Not all dots moved to top of braid. Calling slide_dots first"
            total_braid = slide_dots(mybraid)
            to_return, nothing_changed = remove_doubles(total_braid)
            return to_return, nothing_changed
    else: 
        total_return = list()
        for b in mybraid: 
            bcopy = braid(b.word, b.c, b.max_strands, b.coef)
            bcopy.coef = b.coef
            if(bcopy.dots_at_top == False): 
                newlist = slide_dots(bcopy)
            else: 
                newlist = [bcopy]
            for thing in newlist: 
                tmp, anything_change = remove_doubles(thing)
                total_return = total_return + tmp
                if anything_change == False: 
                    nothing_change = False
        return total_return, nothing_changed

""" " " " " " " " " " " TEST remove_doubles " " " " " " " " " " """
if(run_tests):
  print
  print"Beginning testing remove_doubles..."

  braid5 = braid("s1s3s1y2s3y1y4", "iijj")
  print braid5.word
  print [i.word for i in slide_dots(braid5)]
  print braid5.word
  braid5.draw()
  result,a = remove_doubles(braid5)
  for i in result: 
      i.draw()

  braid6 = braid('s1y1s1', 'iii')
  print
  braid6.draw()
  print
  braid6 = slide_dots(braid6)
  for b in braid6: 
      print_braid(b)
      b.draw()
  print
  braid7,a = remove_doubles(braid6)
  print"...Finished testing remove doubles"

""" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " """

def order_descending(input_braid): 
    nothing_changed = True
    if isinstance(input_braid, braid):
        mybraid = braid(input_braid.word, input_braid.c, input_braid.max_strands, input_braid.coef)
        mybraid.coef = input_braid.coef
        for i in reversed(range(mybraid.num_crossings)):
            for j in range(i):
                n1 = mybraid.string_nums[j]
                n2 = mybraid.string_nums[j+1]
                if (int(n2) - int(n1)) > 1 : 
                    mybraid.string_nums[j] = n2
                    mybraid.string_nums[j+1] = n1
                    nothing_changed = False
        for i in reversed(range(mybraid.num_crossings, len(mybraid.string_nums))):
            for j in range(mybraid.num_crossings, i):
                n1 = mybraid.string_nums[j]
                n2 = mybraid.string_nums[j+1]
                if int(n2) > int(n1): 
                    mybraid.string_nums[j] = n2
                    mybraid.string_nums[j+1] = n1
        mybraid.word = ''.join([''.join(a) for a in zip(mybraid.string_char, mybraid.string_nums)])
        return [mybraid], nothing_changed
    else: 
        ret_braid = list()
        for b in input_braid: 
            out_b, none_changed = order_descending(b)
            if(none_changed == False): 
                nothing_changed = False
            out_b[0].coef = b.coef
            ret_braid = ret_braid + out_b
        return ret_braid, nothing_changed

""" " " " " " " " " " TEST order_descending " " " " " " " " " " """
if(run_tests):
  print
  print"Beginning testing order_descending..."
  braid8 = braid('s1s2y1s1s3s2s7s5s3s6', 'iiii')
  braid8 = slide_dots(braid8)
  braid8,a = order_descending(braid8)
  for b in braid8: 
      print_braid(b)
      b.draw()
  print"...Finished testing order_descending"

""" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " """

def flip_triples(input_braid):
    nothing_changed = True

    if isinstance(input_braid, braid):
        mybraid = braid(input_braid.word, input_braid.c, input_braid.max_strands, input_braid.coef)

        for i in range(0, mybraid.num_crossings-2):
            n1 = int(mybraid.string_nums[i  ])
            n2 = int(mybraid.string_nums[i+1])
            n3 = int(mybraid.string_nums[i+2])

            if( (n1 == n3) and ((n1 - n2) == 1) ):
                mybraid.string_nums[i  ] = str(n2)
                mybraid.string_nums[i+1] = str(n1)
                mybraid.string_nums[i+2] = str(n2)
                nothing_changed = False
        mybraid.word = ''.join([''.join(a) for a in zip(mybraid.string_char, mybraid.string_nums)]) 
        return [mybraid], nothing_changed
    else: 
        output_braid = list()
        for b in input_braid: 
            none_changed = True
            mybraid, none_changed = flip_triples(b)
            if none_changed == False: 
                nothing_changed = False
            output_braid = output_braid + mybraid
        return output_braid, nothing_changed


""" " " " " " " " " " " " TEST flip_triples " " " " " " " " " " """
if(run_tests): 
  print
  print'Beginning testing flip_triples...'
  braid10 = braid('s2s1y1s2s3s4s3s6', 'iiii')
  braid10 = slide_dots(braid10)
  braid10,a = order_descending(braid10)
  print_braid(braid10)
  braid10,a = flip_triples(braid10)
  for b in braid10: 
      print_braid(b)
      b.draw()
  print"...Finished testing flip_triples"

""" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " """



def canonical_form(input_braid):
    stuff_to_change = True
    input_braid = slide_dots(input_braid)
    max_braid_len = 0
    if isinstance(input_braid, braid):
        max_braid_len = len(input_braid.string_char)
    else: 
        for b in input_braid: 
            max_braid_len = max(max_braid_len, len(b.string_char))

    count = 0
    while(stuff_to_change and count < max_braid_len):
        stuff_to_change = False
        count = count + 1

        input_braid, anything_happen = remove_doubles(input_braid)
        if anything_happen: 
            stuff_to_change = True

        input_braid, anything_happen = order_descending(input_braid)
        if anything_happen: 
            stuff_to_change = True

        input_braid, anything_happen = flip_triples(input_braid)
        if anything_happen: 
            stuff_to_change = True
    return input_braid

braid4 = braid('y1s3s2y3s3s1', 'iiii')
braid4.draw()
braid4 = canonical_form(braid4)
for i in braid4: 
   print 
   print i.word
   i.draw()
   print

print_braid(braid4)

#braid7 = braid1+braid2
#for i in braid7:
#    i.c = '123123123'
#braid7 = canonical_form(braid7)
#print_braid(braid7)
#for i in braid7:
#   print 
#   print i.word
#   i.draw()
#   print


other = braid('s1s4y4s3y2s5s6y3y2s4', '123123123')

"""
s1s4s3y4s3y2s5s6y3y2s4 -> s1s4s3y3y2s5s6y3y2s4
                       -> s1s4s3s5s6y3y2y3y2s4
                       -> s1s4s3s5s6y3y3s4y2y2
                       -> s1s4s3s5s6s4y3y3y2y2
                       -> s4s5s6s3s4s1y3y3y2y2
"""

"""
other.draw()
print_braid(other)

print
other = canonical_form(other)
for i in other: 
    print i.word
    i.draw()
print_braid(other)

"""

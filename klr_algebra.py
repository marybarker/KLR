import re
import string
run_tests = False
are_same = 2
forward_directed = -1
backward_directed = -1

# for pretty printouts
def plusminus(a):
    if a < 0:
        return ' - '+str(abs(a))
    else: 
        return ' + '+str(abs(a))

class braid():
    def __init__(self, word, colors, num=-1, coef=1.0, cartan = 0):
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

        #        self.cartan = {}
        #	if isinstance(cartan, list):
        #            for pair in cartan: 
        #                self.cartan
        #            # stuff
        #        elif isinstance(cartan, int):
        #            pass

        self.c = colors
        self.word = word
        self.string_char = y_and_s
        self.string_nums = nums
        self.num_dots = y_and_s.count('y')
        self.num_crossings = y_and_s.count('s')
        self.coef = coef
        self.dots_at_top = False
        self.cart = cartan

    def cartan(self, col1, col2):
        if isinstance(self.cart, dict): 
            return self.cart[(col1, col2)]
        elif isinstance(self.cart, int): 
            if col1 == col2: 
                return are_same
            else: 
                return 0
        #elif isinstance(self.cart, CartanMatrix): 
        #    return self.cart[col1, col2]

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
            if(self.string_char[ii] != 'y'): 
                i_num = int(self.string_nums[ii])
                n = self.s(i_num, n)
        return self.c[n - 1]

    def are_connected(self, level, n1, n2): 
        c1 = self.color_find(n1, level)
        c2 = self.color_find(n2, level)
        if c1 == c2: 
             return True
        elif self.cartan(c1, c2) != 0: 
             return True
        else: 
             return False
            

    def get_connectivity(self, level, n1, n2):
        c1 = self.color_find(n1, level)
        c2 = self.color_find(n2, level)
        return self.cartan(c1, c2)

    def s(self, n, strand):
        """ 
        Gives the new value of 
        strand after the switch Sn 
        """
        if int(strand) == n: 
            return int(strand) + 1
        elif int(strand) == (n + 1): 
            return n
        else: 
            return int(strand)

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
    print mystring

def slide_dots(input_braid): 
    nothing_changed = True
    if isinstance(input_braid, braid): 
        return_val = [input_braid]
    else: 
        return_val = input_braid
    i_b = 0
    while(i_b < len(return_val)): 
        bc = return_val[i_b]
        b = braid(bc.word, bc.c, bc.max_strands, bc.coef, bc.cart)

        i = 0
        while i < len(b.string_char): 

            no_change_i = True
            s_1 = b.string_char[i]
            n_1 = b.string_nums[i]

            if( s_1 == 'y' ):
                for j in range(i+1,len(b.string_char)): 
                    if no_change_i: 
                        s_2 = b.string_char[j]
                        n_2 = b.string_nums[j]

                        if s_2 == 's' and ( (n_1 == n_2) or (int(n_1) == (int(n_2) + 1)) ): 

                            no_change_i = False
                            nothing_changed = False
                            y_n = str(b.s(int(n_2), int(n_1)))

                            new_word = ''
                            connection = b.get_connectivity(j, n_2, str(int(n_2) + 1))

                            if connection == are_same: 
                                new_nums = b.string_nums[0:i]+b.string_nums[i+1:j]+b.string_nums[j+1:]
                                new_char = b.string_char[0:i]+b.string_char[i+1:j]+b.string_char[j+1:]
                                new_word = ''.join([''.join(a) for a in zip(new_char, new_nums)])

                                if n_1 == n_2: 
                                    coef = -1
                                else: 
                                    coef = 1

                                b.string_nums = b.string_nums[0:i]+b.string_nums[i+1:j+1]+[y_n]+b.string_nums[j+1:]
                                b.string_char = b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]
                            else: 
                                b.string_nums = b.string_nums[0:i]+b.string_nums[i+1:j+1]+[y_n]+b.string_nums[j+1:]
                                b.string_char = b.string_char[0:i]+b.string_char[i+1:j+1]+[s_1]+b.string_char[j+1:]

                            b_word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])

                            b = braid(b_word, b.c, b.max_strands, b.coef, b.cart)
                            if new_word != '': 
                                new_braid = braid(new_word, b.c, b.max_strands, coef * b.coef, b.cart)
                                return_val = return_val + [new_braid]
                if no_change_i:
                    b.string_char.pop(i)
                    b.string_nums.pop(i)
                    b.string_char = b.string_char + [s_1]
                    b.string_nums = b.string_nums + [n_1]
                    b_word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])
                    b = braid(b_word, b.c, b.max_strands, b.coef, b.cart)
                else:
                    i = i - 1
            i = i + 1
        return_val[i_b] = b
        i_b = i_b + 1
    return return_val, nothing_changed

def remove_doubles(mybraid):
    nothing_changed = True
    if isinstance(mybraid, braid): 
        return_val, nothing_changed =  remove_doubles([mybraid])
    else: 
        return_val = mybraid

        i_b = 0
        while(i_b < len(return_val)): 
            b = return_val[i_b]
            b = braid(b.word, b.c, b.max_strands, b.coef, b.cart)

            # loop through all crossings
            for i in range(b.num_crossings + b.num_dots - 1): 
                num_i = b.string_nums[i]
                if ( b.string_char[i] == 's' and b.string_char[i+1] == 's'): 
                    num_j = b.string_nums[i+1]
                    if num_j == num_i: 
                        b.string_char[i  ] = 'd'
                        b.string_char[i+1] = 'd'
                        nothing_changed = False
            i = 0
            while i < (b.num_crossings + b.num_dots): 
                if (b.string_char[i] == 'd' and b.string_char[i+1] == 'd'): 
                    n1 = b.string_nums[i]
                    n2 = b.string_nums[i+1]

                    if b.are_connected(i, int(n1), int(n1)+1): 
                        connection = b.get_connectivity(i, int(n1), int(n1)+1)
                        if connection == are_same: 
                            b = braid('','',num=0)
                        else: 
                            if connection == forward_directed: 
                                first_dot = n1
                                second_dot = str(int(n1) + 1)

                            elif connection == backward_directed: 
                                first_dot = str(int(n1) + 1)
                                second_dot = n1

                            #b.num_crossings = b.num_crossings - 2
                            #b.num_dots = b.num_dots + 1
                            b.string_char[i] = 'y'
                            b.string_nums[i] = first_dot
                            b.string_char.pop(i+1)
                            b.string_nums.pop(i+1)
                            b.word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])
                            b = braid(b.word, b.c, b.max_strands, b.coef, b.cart)

                            new_string_char = b.string_char
                            new_string_nums = b.string_nums
                            new_string_nums[i] = second_dot

                            newword = ''.join([''.join(a) for a in zip(new_string_char, new_string_nums)])
                            newbraid = braid(newword, b.c, b.max_strands, -1 * b.coef, b.cart)

                            return_val = return_val + [newbraid]
                    else: 
                        b.num_crossings = b.num_crossings - 2
                        b.string_char.pop(i+1)
                        b.string_nums.pop(i+1)
                        b.string_char.pop(i)
                        b.string_nums.pop(i)
                i = i + 1

            return_val[i_b] = b
            i_b = i_b + 1

    return return_val, nothing_changed

def order_descending(input_braid): 
    nothing_changed = True
    if isinstance(input_braid, braid):
        mybraid = braid(input_braid.word, input_braid.c, input_braid.max_strands, input_braid.coef, input_braid.cart)
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

def flip_triples(input_braid):
    if isinstance(input_braid, braid): 
        return flip_triples([input_braid])
    else: 
        nothing_changed = True
        i_b = 0
        while i_b < len(input_braid): 
            b = braid(input_braid[i_b].word, input_braid[i_b].c, input_braid[i_b].max_strands, input_braid[i_b].coef, input_braid[i_b].cart)
            for i in range(b.num_crossings + b.num_dots - 2): 
                n1 = int(b.string_nums[i  ])
                n2 = int(b.string_nums[i+1])
                n3 = int(b.string_nums[i+2])
                c1 = b.string_char[i  ]
                c2 = b.string_char[i+1]
                c3 = b.string_char[i+2]
                if (c1 == 's'  and  c2 == 's' and  c3 == 's'): 
                    if (n1 == n3 and (n1 - n2) == 1 ): 
                        col1 = b.color_find(n2  , i)
                        col2 = b.color_find(n2+1, i)
                        col3 = b.color_find(n2+2, i)

                        nothing_changed = False
                        if col1 == col3: 
                            connection = b.cartan(col1,col2)
                            new_word = ''
                            if connection == are_same: 
                                b.string_nums[i  ] = str(n2)
                                b.string_nums[i+1] = str(n1)
                                b.string_nums[i+2] = str(n2)
                                b.word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])

                            elif connection == forward_directed: 
                                coef = 1
                                new_nums = b.string_nums[0:i]+b.string_nums[i+3:]
                                new_char = b.string_char[0:i]+b.string_char[i+3:]
                                new_word = ''.join([''.join(a) for a in zip(new_char, new_nums)])

                            elif connection == backward_directed: 
                                coef = -1

                                new_nums = b.string_nums[0:i]+b.string_nums[i+3:]
                                new_char = b.string_char[0:i]+b.string_char[i+3:]
                                new_word = ''.join([''.join(a) for a in zip(new_char, new_nums)])

                            else: 
                                coef = 0
                            b.string_nums[i  ] = str(n2)
                            b.string_nums[i+1] = str(n1)
                            b.string_nums[i+2] = str(n2)
                            b.word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])

                            if new_word != '': 
                                new_braid = braid(new_word, b.c, b.max_strands, coef * b.coef, b.cart)
                                input_braid = input_braid + [new_braid]
                        else: 
                            b.string_nums[i  ] = str(n2)
                            b.string_nums[i+1] = str(n1)
                            b.string_nums[i+2] = str(n2)
                            b.word = ''.join([''.join(a) for a in zip(b.string_char, b.string_nums)])

            input_braid[i_b] = b
            i_b = i_b + 1
        return input_braid, nothing_changed

def canonical_form(input_braid):
    stuff_to_change = True
    max_braid_len = 0
    if isinstance(input_braid, braid): 
        return canonical_form([input_braid])
    for b in input_braid: 
        max_braid_len = max(max_braid_len, len(b.string_char))

    a = False
    count = 0
    while (a == False and count < max_braid_len): 
        input_braid, a = slide_dots(input_braid)
        count = count + 1

    count = 0
    while(stuff_to_change and count < (max_braid_len*max_braid_len)):
        stuff_to_change = False
        count = count + 1

        input_braid, anything_happen = remove_doubles(input_braid)
        if anything_happen: 
            input_braid, a = slide_dots(input_braid)
            stuff_to_change = True

        input_braid, anything_happen = order_descending(input_braid)
        if anything_happen: 
            input_braid, a = slide_dots(input_braid)
            stuff_to_change = True

        input_braid, anything_happen = flip_triples(input_braid)
        if anything_happen: 
            input_braid, a = slide_dots(input_braid)
            stuff_to_change = True

    return input_braid


test = braid('s3y3s2y2s1s1s3', '1222', cartan={('1','1'):2, ('2','2'):2, ('1','2'):-1, ('2','1'):0, ('2','3'):-1, ('3','2'):0, ('3','3'):2, ('2','2'):2})
i = 0
a = False
while (i < 20 and a==False): 
    test, a = slide_dots(test)
    i = i + 1
print 80*'-'
print 'after sliding dots...'
print 80*'-'
for i in test: 
    print i.word
    i.draw()
print_braid(test)


i = 0
a = False
while (i < 20 and a==False): 
    test, a  = remove_doubles(test)
    test, b = slide_dots(test)
    i = i + 1
print
print 80*'-'
print 'after removing doubles...'
print 80*'-'
for i in test: 
    print i.word
    i.draw()
print_braid(test)


i = 0
a = False
while (i < 20 and a==False): 
    test, a  = order_descending(test)
    test, b = slide_dots(test)
    i = i + 1
test, a  = order_descending(test)
print
print 80*'-'
print 'after reordering ...'
print 80*'-'
for i in test: 
    print i.word
    i.draw()
print_braid(test)

print 80*'='
#test = braid('s5s4s5s3y3s2y2s1s1s3', '1222322', cartan={('1','1'):2, ('2','2'):2, ('1','2'):-1, ('2','1'):0, ('2','3'):-1, ('4','3'):0})
test = braid('s5s4s5s3y3s2y2s1s1s3', '1222322', cartan={('1','1'):2, ('2','2'):2, ('1','2'):-1, ('2','1'):0, ('2','3'):-1, ('3','2'):0, ('3','3'):2, ('2','2'):2})
test.draw()
print 80*'='
print
print 'in Canonical Form ...'
test = canonical_form(test)

for i in test: 
    print i.word
    i.draw()
print_braid(test)

print 80*'='


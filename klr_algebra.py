import re

cartan = {('1','1'):2, ('2','2'):2, ('3','3'):2, ('1','2'):1, ('1','3'):0, ('2','1'):1, ('3','1'):1, ('3','2'):1, ('2','3'):1}
colors = '1'*20

dot = 'x'
swap = 's'
eps = 'e'
x = 'X'
theta = 'theta'
d = 'd'
special_characters = [dot,swap,eps,x,theta,d]
forward_directed = 1
backward_directed = 1

def ASWORD(mylist): 
    if isinstance(mylist, list): 
        return ''.join(mylist)
    else: 
        return str(mylist)

def S(n1,n2): 
    if n1 == n2: 
        return str(n1 + 1)
    elif (int(n1) + 1) == int(n2): 
        return str(n1)
    else: 
        return str(n2)
       
def relation(thing1, thing2, thing3 = 1, c1 = '1', c2='1'): 
    all_that_stuff = list()
    n1 = int(thing1[1])
    n2 = int(thing2[1])

    if thing1[0] == dot: 
       if thing2[0] == swap: 
           thing = [[1, swap+str(n2),dot+S(n2,n1)]]
           if cartan[(c1,c2)] == 2: 
               if n1 == n2:
                   thing = thing + [[-1,'']]
               elif (n2 + 1) == n1:
                   thing = thing + [[ 1,'']]
           return thing

    elif thing1[0] == swap: 
       if thing2[0] == swap: 
           thing = [[1, swap+str(n2),dot+S(n2,n1)]]

    return all_that_stuff

class braid(): 
    def update_from_words(self, string = 0): 
        if string != 0: 
            self.words = [string]

        self.terms = list()
        words = '['+''.join([a for a in special_characters])+']'
        for string in self.words: 
            no_nums = re.sub('\d+', ' ', string).split(' ')[:-1]
            nums = [a for a in re.sub(words, ' ', string).split(' ')[1:] if a]
            terms = [''.join([no_nums[a],nums[a]]) for a in range(len(nums))]
            self.terms.append(terms)

        self.numwords = len(self.words)

        self.numstrands = 0
        strandlist = [self.numstrands]
        for term in self.terms: 
            if len(term) > 0: 
                for t in term: 
                    if len(str(t)) > 0: 
                        if str(t)[0] == swap:
                            strandlist.append(int(str(t)[1])+1)
                        else:
                            strandlist.append(int(str(t)[1]))
        self.numstrands = max(strandlist)

    # update braid after changing/adding to braid.terms
    def update_from_terms(self, termslist = 0):
        if termslist != 0: 
            self.terms = [termslist]
        self.words = list()
        coefs = list()
        for index in range(len(self.terms)):
            coef = self.coefs[index]
            word = ASWORD(self.terms[index])
            if word in self.words: 
                i = self.words.index(word)
                coefs[i] = coefs[i] + self.coefs[index]
            else: 
                self.words.append(word)
                coefs.append(coef)
        self.coefs = coefs
        self.numwords = len(self.words)
        self.numstrands = 0
        strandlist = [self.numstrands]
        for term in self.terms: 
            if len(term) > 0: 
                for t in term: 
                    if len(str(t)) > 0: 
                        if str(t)[0] == swap:
                            strandlist.append(int(str(t)[1])+1)
                        else:
                            strandlist.append(int(str(t)[1]))
        self.numstrands = max(strandlist)


    # initializing an braid
    def __init__(self, string=0, coef = ''): 
        self.coefs = list()
        self.words = list()
        self.terms = list()
        self.numwords = 0
        self.numstrands = 0

        if string != 0: 
            if coef == '': 
                self.coefs.append(1)
            else: 
                self.coefs.append(coef)
            if isinstance(string, list): 
                self.update_from_terms(string)
            elif isinstance(string, str): 
                self.update_from_words(string)
            elif isinstance(string, braid): 
                self.coefs = [a for a in string.coefs]
                self.words = [a for a in string.words]
                self.update_from_words()

    def __rmul__(self, other): 
        if isinstance(other, braid): 
            new = braid('',0)
            for oi in range(other.numwords):
                b1 = braid(other.words[oi], other.coefs[oi])

                for bi in range(self.numwords):
                    b2 = braid(self.words[bi], self.coefs[bi])
                    c1 = ASWORD([b1.col(0,i+1) for i in range(b1.numstrands)])
                    c2 = colors[:b2.numstrands]

                    if c1 == c2:
                        new.coefs.append(b1.coefs[0]*b2.coefs[0])
                        new.words.append(ASWORD(b1.words[0]+b2.words[0]))
                        new.update_from_words()
            return new
        else: 
            self.coefs = [other * int(x) for x in self.coefs]
            return self

    def __mul__(self, other): 
        if isinstance(other, braid): 
            new = braid('',0)
            for oi in range(self.numwords):
                b1 = braid(self.words[oi], self.coefs[oi])

                for bi in range(other.numwords):
                    b2 = braid(other.words[bi], other.coefs[bi])
                    c1 = ASWORD([b1.col(0,i+1) for i in range(b1.numstrands)])
                    c2 = colors[:b2.numstrands]

                    if c1 == c2:
                        new.coefs.append(b1.coefs[0]*b2.coefs[0])
                        new.words.append(ASWORD(b1.words[0]+b2.words[0]))
                        new.update_from_words()
            return new
        else: 
            self.coefs = [other * int(x) for x in self.coefs]
            return self

    def __add__(self, other_braid): 
        if self.numwords > 0:
            newself = braid(self)
        else: 
            newself = braid('',0)

        if isinstance(other_braid, braid): 
            for termindex in range(other_braid.numwords): 
                word1 = other_braid.words[termindex]
                coef1 = other_braid.coefs[termindex]
                if word1 in newself.words: 
                    i = newself.words.index(word1)
                    newself.coefs[i] = newself.coefs[i] + coef1
                else: 
                    newself.words.append(word1)
                    newself.coefs.append(coef1)
                    newself.update_from_words()
        else:
            if isinstance(other_braid, int) | isinstance(other_braid, float): 
                other_braid = braid('', other_braid)
            else: 
                if len(other_braid) < 1: 
                    other_braid = braid('',0)
            newself = newself + braid(other_braid)

        # get rid of any words that are 0
        zero_coef = [newself.words[a] for a in range(newself.numwords) if newself.coefs[a] == 0]
        for z in zero_coef: 
            newself.words.remove(z)
        newself.coefs = [a for a in newself.coefs if a != 0]
        newself.update_from_words()

        return newself

    def __sub__(self, other_braid): 
        if self.numwords > 0:
            newself = braid(self)
        else: 
            newself = braid('',0)
        return newself + -1 * other_braid

    def word(self): 
        print ' + '.join([''.join([str(self.coefs[a]),'.',self.words[a]]) for a in range(self.numwords) if self.coefs[a] != 0])
        print 


    def col(self, braid_level, num): 
        whereami = int(num)
        terms = self.terms[0]
        for t in terms[braid_level:]: 
             if t[0] == swap: 
                 ow = whereami
                 whereami = int(S(int(t[1]), whereami))
        return colors[whereami-1]

    def draw(self): 
        for i in range(self.numwords): 
            word = self.words[i]
            term = self.terms[i]
            sub = braid(self.words[i],self.coefs[i])

            if len(word) > 0: 
                outstr = ASWORD([str(c)+'  ' for c in colors[:self.numstrands]])
                print outstr
                outstr = '|  '*self.numstrands

                for t in term[::-1]: 
                    n = int(t[1]) - 1

                    if t[0] == dot: 
                        if outstr[3*n] == 'o': 
                            print outstr
                            outstr = '|  '*self.numstrands
                        outstr = outstr[0:3*n]+'o  '+outstr[3*n+3:]

                    elif t[0] == swap: 
                        print outstr
                        outstr = '|  '*self.numstrands
                        #print outstr
                        a = 3*n+4
                        b = 3*n+0
                        outstr = outstr[0:b]+' \\'+'/ '+outstr[a:]
                        print outstr
                        outstr = outstr[0:b]+' /'+'\ '+outstr[a:]
                        print outstr
                        outstr = '|  '*self.numstrands

                    elif t[0] == eps: 
                        a = 3*n+4
                        b = 3*n+0
                        print outstr
                        outstr = '|  '*self.numstrands
                        outstr=outstr[:b]+'\__/'+outstr[a:]
                        print outstr
                        outstr=outstr[:b]+' __ '+outstr[a:]
                        print outstr
                        outstr=outstr[:b]+'/  \\'+outstr[a:]
                        print outstr
                        outstr = '|  '*self.numstrands
                print outstr
                outstr = ASWORD([sub.col(0,i+1)+'  ' for i in range(self.numstrands)])
                print outstr
                print 
            else: 
                print ' '

    def word_slide_dots(self, b): 
        i = 1
        terms = b.terms[0]
        nothing_happened = True
        while i < len(terms): 
            if nothing_happened: 
                t1 = terms[i-1]
                t2 = terms[i+0]
                if (t1[0] == dot) & (t2[0] != dot): 
                    col1 = b.col(i-1,int(t1[1]))
                    col2 = b.col(i-1,S(int(t2[1]),int(t1[1])))
                    result = relation(t1,t2,c1=col1, c2=col2)
                    stringlist = [terms[:i-1]+r[1:]+terms[i+1:] for r in result]
                    coef = [int(r[0])*b.coefs[0]  for r in result]
                    nothing_happened = False
            else: 
                break
            i = i + 1
        if nothing_happened:
            return b
        else: 
            extra_error_stuff = [braid(stringlist[i]) for i in range(len(stringlist))]
            stuff = coef[0]*extra_error_stuff[0]
            for i in range(1,len(extra_error_stuff)): 
                stuff = stuff + coef[i]*extra_error_stuff[i]
            return stuff

    def slide_dots(self): 
        nothing_changed = True
        return_val = braid('')
        i_b = 0
        while i_b < self.numwords: 
            b = braid(self.words[i_b], self.coefs[i_b])
            newb = self.word_slide_dots(b)
            return_val = return_val + newb
            i_b = i_b + 1

            if newb != b: 
                nothing_changed = False
        if nothing_changed: 
            return self
        else: 
            return_val = return_val - braid('')
            return return_val.slide_dots()


    def remove_doubles(self):
        nothing_changed = True

        if self.numwords > 0:
            new = braid(self)
        else: 
            new = braid('')

        i_b = 0
        while i_b < self.numwords: 

            terms = self.terms[i_b]
            thisone = braid(self.words[i_b],self.coefs[i_b])

            for t in range(len(terms)-1): 
                if nothing_changed: 
                    t1 = terms[t+0]
                    t2 = terms[t+1]

                    if t1 == t2: 
                        if t1[0] == swap: 
                            n1 = int(t1[1])
                            n2 = int(t2[1])

                            nothing_changed = False
                            new = new - thisone
                            c1, c2 = thisone.col(t, n1), thisone.col(t, n1+1)

                            if c1 == c2: 
                                pass
                            elif cartan[(c1, c2)] == forward_directed: 
                                thisone.terms = [terms[:t]+[dot+str(n1)]+terms[t+2:]]
                                thisone.update_from_terms()
                                thisone = thisone + braid(terms[:t]+[dot+str(n1+1)]+terms[t+2:], -1)
                                new = new + thisone
                            elif cartan[(c1, c2)] == backward_directed: 
                                thisone.terms = [terms[:t]+[dot+str(n1)]+terms[t+2:]]
                                thisone.update_from_terms()
                                thisone = thisone + braid(terms[:t]+[dot+str(n1+1)]+terms[t+2:], -1)
                                new = new + thisone
                            else: 
                                thisone.terms = [terms[:t]+terms[t+2:]]
                                thisone.update_from_terms()
                                new = new + thisone
                else: 
                    break
            i_b = i_b + 1

        if nothing_changed: 
            return new
        else: 
            return new.remove_doubles()

    def order_descending(self): 
        nothing_changed = True

        for i in range(self.numwords): 
            thisone = braid(self.words[i], self.coefs[i])

            if nothing_changed: 
                for t in range(len(thisone.terms[0])-1): 
                    t1 = thisone.terms[0][t+0]
                    t2 = thisone.terms[0][t+1]
                    if (int(t2[1]) > (int(t1[1]) + 1) ) & (t2[0] != dot) : 
                        self = self - thisone

                        nothing_changed = False
                        thisone.words = [ASWORD(thisone.terms[0][:t]+[t2,t1]+thisone.terms[0][t+2:])]
                        thisone.update_from_words()
                        self = self + thisone
            else: 
                break

        if nothing_changed: 
            return self
        else: 
            return self.order_descending()

    def flip_triples(self): 
        to_return = braid('', 0)
        for i in range(self.numwords):
            tmp = braid(self.words[i], self.coefs[i])
            t = tmp.terms[0]
            c = tmp.coefs[0]
            l = len(t)
            no_changes = True
            tempterm = braid('',0)

            to_return = to_return + tmp

            for it in range(len(t)-2): 
                if no_changes: 
                    t1 = t[it+0]
                    t2 = t[it+1]
                    t3 = t[it+2]
                    n1 = int(t1[1])
                    n2 = int(t2[1])
                    n3 = int(t3[1])
                    if (t1[0] == swap) & (t2[0] == swap) & (t3[0] == swap): 
                        if (n1 == n3) & ( (n2 + 1) == n1 ): 
                            c1 = tmp.col(it, n1)
                            c2 = tmp.col(it, n1+1)
                            c3 = tmp.col(it, n1)

                            no_changes = False
                            if c1 == c3: 
                                tempterm = t[:it]+[t2,t1,t2]+t[it+3:]
                                tempterm = braid(tempterm, c)

                                if cartan[(c1,c2)] == forward_directed: 
                                    tempterm = tempterm + braid(t[:it]+t[it+3:], c)

                                if cartan[(c1,c2)] == backward_directed: 
                                    tempterm = tempterm + braid(t[:it]+t[it+3:],-c)
                            else: 
                                tempterm = braid('',0)
                else: 
                   pass
            if no_changes == False: 
                to_return = to_return + tempterm
                to_return = to_return - tmp

        return to_return

    def standard_form(self): 
        for l in range(2*self.numwords): 
            self = self.slide_dots()
            self = self.remove_doubles()
            self = self.order_descending()
            self = self.flip_triples()
        return self
""" end braid relations """

"""
testbraid = braid("s1x1s1")
testbraid.draw()
testbraid.word()
testbraid = testbraid.standard_form()
testbraid.draw()
testbraid.word()

testbraid = braid("s2s1s2")
testbraid = testbraid.standard_form()
testbraid.draw()
testbraid.word()

"""












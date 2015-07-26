#!/usr/bin/env python
#coding: gbk

########################################################################
#Author: Feng Ruohang
#Create: 2014/10/06 11:38
#Digest: Provide a common data struct: Red Black Tree
########################################################################

class RBT(object):
    class Node(object):
        '''
        Node used in RBTree
        '''
        def __init__(self,key,value=None,color=False,N=1):
            self.key = key
            self.val = value
            self.color = color   #False for Black, True for Red
            self.N = N           #Total numbers of nodes in this subtree
            self.left = None
            self.right = None

        def __cmp__(l,r):
            return cmp(l.key,r.key)

        def __eq__(l,r):
            return True if l.key == r.key else False

        def __add__(l,r):
            l.value + r.value

        def reduce(self,new_val):
            self.val.extend(new_val)

    def __init__(self):
        self.root = None

    #====================APIs====================#
    #=====Basic API

    def get(self,key):
        return  self.__get(self.root,key)

    def put(self,key,val):
        self.root = self.__put(self.root,key,val)
        self.root.color = False 

    def append(self,key,val):
        self.root = self.__append(self.root,key,val)
        self.root.color = False

    def delete(self,key):
        if not self.contains(key):
            raise LookupError('No such keys in rbtree. Fail to Delete')
        if self.__is_black(self.root.left) and self.__is_black(self.root.right):
            self.root.color = True
        self.root = self.__delete(self.root,key)
        if not self.is_empty(): 
            self.root.color = False

    def del_min(self):
        if self.is_empty(): 
            raise LookupError('Empty Red-Black Tree. Can\'t delete min')
        if self.__is_black(self.root.left) and self.__is_black(self.root.right):
            self.root.color = True
        self.root = self.__del_min(self.root)
        if not self.is_empty(): self.root.color = False

    def del_max(self):
        if self.is_empty():
            raise LookupError('Empty Red-Black Tree. Can\'t delete max')
        if self.__is_black(self.root.left) and self.__is_black(self.root.right):
            self.root.color = True
        self.root = self.__del_max(self.root)
        if not self.is_empty(): self.root.color = False 

    def size(self):
        return self.__size(self.root)

    def is_empty(self):
        return not self.root

    def contains(self,key):
        return bool(self.get(key))

    #=====Advance API
    def min(self):
        if self.is_empty():
            return None
        return self.__min(self.root).key

    def max(self):
        if self.is_empty():
            return None
        return self.__max(self.root).key

    def floor(self,key):
        x = self.__floor(self.root,key)
        if x:
            return x.key,x.val
        else:
            return None,None

    def ceil(self,key):
        x = self.__ceil(self.root,key)
        if x:
            return x.key,x.val
        else:
            return None,None

    def below(self,key):
        index = self.index(key)
        if not 0 <= index - 1 < self.size():
            return None,None    #Return None if out of range
        x = self.__select(self.root,index - 1)
        return x.key,x.val

    def above(self,key):
        index = self.index(key)
        if self.contains(key):
            if not 0 <= index + 1 < self.size():
                return None,None    #Return None if out of range
            else:
                x = self.__select(self.root,index+1)
                return x.key,x.val
        else:#if key is not in tree. then select(i) is what we need
            if not 0 <= index < self.size():
                return None,None    #Return None if out of range
            else:
                x = self.__select(self.root,index)
                return x.key,x.val

    def index(self,key):
        return self.__index(self.root,key) 

    def keys(self):
        '''Return All Keys in the tree '''
        return self.range(self.min(),self.max())

    def range(self,lo,hi):
        '''Take two keys. return keys between them'''
        q = []
        self.__range(self.root,q,lo,hi)
        return q

    def select(self,index):
        '''Given Index Return Corresponding key '''
        if not 0 <= index < self.size():
            return None
        return self.__select(self.root,index).key

    def width(self,lo,hi):
        '''Return the numbers of keys between lo and hi '''
        if lo > hi: 
            return 0
        if self.contains(hi):
            return self.index(hi) - self.index(lo) + 1
        else:
            return self.index(hi) - self.index(lo)


    #===============Private Method===============#
    #=====Basic
    def __get(self,x,key):
        while x:
            tag = cmp(key,x.key)
            if tag < 0 : x = x.left
            elif tag > 0 :x = x.right
            else: return x.val

    def __put(self,h,key,val):
        if not h: 
            return self.Node(key,val,True,1)
        tag = cmp(key,h.key)
        if tag < 0: 
            h.left = self.__put(h.left,key,val)
        elif tag > 0: 
            h.right = self.__put(h.right,key,val)
        else: 
            h.val = val   #Update

        if self.__is_black(h.left) and self.__is_red(h.right):
            h = self.__rotate_left(h)
        if self.__is_red(h.left) and self.__is_red(h.left.left):
            h = self.__rotate_right(h)
        if self.__is_red(h.left) and self.__is_red(h.right):
            self.__flip_colors(h)
        h.N = self.__size(h.left) + self.__size(h.right) + 1
        return h

    def __append(self,h,key,val):
        if not h: 
            return self.Node(key,val,True,1)
        tag = cmp(key,h.key)
        if tag < 0: 
            h.left = self.__append(h.left,key,val)
        elif tag > 0: 
            h.right = self.__append(h.right,key,val)
        else: 
            h.reduce(val)   #append.

        if self.__is_black(h.left) and self.__is_red(h.right):
            h = self.__rotate_left(h)
        if self.__is_red(h.left) and self.__is_red(h.left.left):
            h = self.__rotate_right(h)
        if self.__is_red(h.left) and self.__is_red(h.right):
            self.__flip_colors(h)
        h.N = self.__size(h.left) + self.__size(h.right) + 1
        return h

    def __del_min(self,h):
        if not h.left: #if h is empty:return None
            return None

        if self.__is_black(h.left) and self.__is_black(h.left.left):
            self.__move_red_left(h)
        h.left = self.__del_min(h.left) #Del recursive
        return self.__balance(h)

    def __del_max(self,h):
        if self.__is_red(h.left): 
            h = self.__rotate_right(h)
        if not h.right: 
            return None
        if self.__is_black(h.right) and self.__is_black(h.right.left):
            h = self.__move_red_right(h)
        h.right = self.__del_max(h.right)
        return self.__balance(h)

    def __delete(self,h,key):
        if key < h.key:
            if self.__is_black(h.left) and self.__is_black(h.left.left):
                h = self.__move_red_left(h)
            h.left = self.__delete(h.left,key)
        else:
            if self.__is_red(h.left):
                h = self.__rotate_right(h)
            if key == h.key and not h.right:
                return None
            if self.__is_black(h.right) and self.__is_black(h.right.left):
                h = self.__move_red_right(h)
            if key == h.key:#replace h with min of right subtree
                x = self.__min(h.right)
                h.key = x.key
                h.val = x.val
                h.right = self.__del_min(h.right)
            else:
                h.right = self.__delete(h.right,key)
        h = self.__balance(h)
        return h
    
    #=====Advance
    def __min(self,h):
        #Assume h is not null
        if not h.left:
            return h
        else:
            return self.__min(h.left)

    def __max(self,h):
        #Assume h is not null
        if not h.right:
            return h
        else:
            return self.__max(h.right)

    def __floor(self,h,key):
        '''Find the NODE with key <= given key in the tree rooted at h '''
        if not h:
            return None
        tag = cmp(key,h.key)
        if tag == 0:
            return h
        if tag < 0:
            return self.__floor(h.left,key)
        t = self.__floor(h.right,key)
        if t:#if find in right tree
            return t
        else:#else return itself
            return h

    def __ceil(self,h,key):
        '''Find the NODE with key >= given key in the tree rooted at h '''
        if not h:
            return None
        tag = cmp(key,h.key)
        if tag == 0:
            return h
        if tag > 0: # key is bigger
            return self.__ceil(h.right,key)
        t = self.__ceil(h.left,key)#key is lower.Try to find ceil left
        if t:#if find in left tree
            return t
        else:#else return itself
            return h

    def __index(self,h,key):
        if not h:
            return 0
        tag = cmp(key,h.key)
        if tag < 0:
            return self.__index(h.left,key)
        elif tag > 0:   #Key is bigger
            return self.__index(h.right,key) + 1 + self.__size(h.left)
        else:   #Eq
            return self.__size(h.left)

    def __select(self,h,index):
        '''assert h. assert 0 <= index < size(tree) '''
        l_size = self.__size(h.left)
        if l_size > index:
            return self.__select(h.left,index)
        elif l_size < index:
            return self.__select(h.right,index - l_size - 1)
        else:
            return h

    def __range(self,h,q,lo,hi):
        if not h: 
            return
        tag_lo = cmp(lo,h.key)
        tag_hi = cmp(hi,h.key)
        if tag_lo < 0:#lo key is lower than h.key
            self.__range(h.left,q,lo,hi)
        if tag_lo <= 0 and tag_hi >= 0:
            q.append(h.key)
        if tag_hi > 0 :# hi key is bigger than h.key
            self.__range(h.right,q,lo,hi)


    #===============Adjust Functions=============#
    def __rotate_right(self,h):
        x = h.left
        h.left,x.right = x.right,h
        x.color,x.N = h.color,h.N
        h.color,h.N = True,self.__size(h.left) + self.__size(h.right) + 1
        return x

    def __rotate_left(self,h):
        x = h.right
        h.right,x.left = x.left,h
        x.color,x.N = h.color,h.N
        h.color,h.N = True,self.__size(h.left) + self.__size(h.right) + 1
        return x

    def __flip_colors(self,h):
        h.color = not h.color
        h.left.color = not h.left.color
        h.right.color = not h.right.color

    def __move_red_left(self,h):
        self.__flip_colors(h)
        if self.__is_red(h.right.left):
            h = self.__rotate_left(h)
        return h

    def __move_red_right(self,h):
        self.__flip_colors(h)
        if self.__is_red(h.left.left):
            h = self.__rotate_right(h)
        return h

    def __balance(self,h):
        if self.__is_red(h.right): 
            h = self.__rotate_left(h)
        if self.__is_red(h.left) and self.__is_red(h.left.left): 
            h = self.__rotate_right(h)
        if self.__is_red(h.left) and self.__is_red(h.right):
            self.__flip_colors(h)
        h.N = self.__size(h.left) + self.__size(h.right) + 1
        return h
    
    #Class Method
    @staticmethod
    def __is_red(x):
        return False if not x else x.color

    @staticmethod
    def __is_black(x):
        return True  if not x else not x.color

    @staticmethod
    def __size(x):
        return 0 if not x else x.N


def RBT_testing():
    '''API Examples '''
    t = RBT()
    test_data = "SEARCHXMPL"

    print '=====testing is_empty()\nBefore Insertion'
    print t.is_empty()

    for letter in test_data:
        t.put(letter,[ord(letter)])
        print "Test Inserting:%s, tree size is %d" % (letter,t.size())
    print "After insertion it return:"
    print t.is_empty()
    print  "====test is_empty complete\n"


    print "=====Tesing Get method:"
    print "get 's' is "
    print t.get('S')
    print "get 'H' is "
    print t.get('H')

    print '==Trying get null key: get "F" is'
    print t.get('F')
    print "=====Testing Get method end\n\n"

    print "=====Testing ceil and floor"
    print "Ceil('L')"
    print t.ceil('L')
    print "Ceil('F') *F is not in tree"
    print t.ceil('F')

    print "Floor('L')"
    print t.ceil('L')
    print "Floor('F')"
    print t.ceil('F')

    print '======test append method'
    print 'Orient key e is correspond with'
    print t.get('E')
    t.append('E',[4])
    print '==After append'
    print t.get('E')
    print "=====Testing Append method end\n\n" 

    print "=====Testing index()"
    print "index(E)" 
    print t.index('E')
    print "index(L),select(4)"
    print t.index('L'),t.select(4)
    print "index('M'),select(5)"
    print t.index('M'),t.select(5)
    print "index a key not in tree:\n index('N'),select(6)"
    print t.index('N'),t.select(6)
    print "index('P')"
    print t.index('P')
    
    
    print "=====Testing select"
    print "select(3) = "
    print t.select(3)
    print "select and index end...\n\n"

    print "====Tesing Min and Max"
    print "min key is:"
    print t.min()
    print "max key is"
    print t.max()

    print "==How much between min and max:"
    print t.width(t.min(),t.max())
    print "keys between min and max:"
    print t.keys()
    print "keys in 'E' and 'M' "
    print t.range('E','M')


    print "try to delete min_key:"
    print "But we could try contains('A') first"
    print t.contains('A')
    t.del_min()
    print "After deletion t.contains('A') is "
    print t.contains('A')

    print t.min()
    print "try to kill one more min key:"
    t.del_min()
    print t.min()
    print "try to delete max_key,New Max key is :"
    t.del_max()
    print t.max()
    print "=====Tesing Min and Max complete\n\n"



    print '=====Deleting Test'
    print t.size()
    t.delete('H')
    print t.size()

    print 'Delete a non-exists key:'
    try:    
        t.delete('F')
    except:
        print "*Look up error occur*"

    print "=====Testing Delete method complete"

def test_basic_api():
    print "==========Testing Basic API=========="
    t = RBT()
    print "Test Data: FENGDIJKABCLM"
    test_data = "FENGDIJKABCLM" #from A-N,without H

    #=====put()
    print "==========put() test begin!=========="
    for letter in test_data:
        t.put(letter,[ord(letter)]) #Value is [ascii order of letter]
        print "put(%s); Now tree size is %d"%(letter,t.size())
    print 'Final tree size is %d'%t.size()
    print "==========put() test complete!==========\n"

    #=====get()
    print "==========get() test begin!=========="
    print "get('F'):\t%s"%repr(t.get('F'))
    print "get('A'):\t%s"%repr(t.get('A'))
    print "get a non-exist key Z: get('Z'):\t%s"%repr(t.get('Z'))
    print "==========get() test complete!==========\n"

    #=====append()
    print "=====append() test begin!=========="
    print "First append to a exist key:[F]"
    print "Before Append:get('F'):\t%s"%repr(t.get('F'))
    print "append('F',[3,'haha']):\t%s"%repr(t.append('F',[3,'haha']))
    print "After Append:get('F'):\t%s\n"%repr(t.get('F'))
    print "Second append to a non-exist key:[O]"
    print "Before Append:get('O'):\t%s"%repr(t.get('O'))
    print "append a non-exist key O: append('O',['value of O']):\t%s"%repr(t.append('O',['value of O']))
    print "After Append:get('O'):\t%s\n"%repr(t.get('O'))
    print "==========append() test complete!==========\n"

    #=====delete()
    print "==========delete() test begin!=========="
    test_data2 = [x for x in test_data]
    test_data2.reverse()
    for letter in test_data2:
        t.delete(letter)
        print "delete(%s); Now tree size is %d"%(letter,t.size())
    print 'Final tree size is %d'%t.size()
    print "==========delete() test complete!==========\n"

    print "==========Basic API Test Complete==========\n\n"

def test_advance_api():
    print "==========Testing min max floor ceil above below =========="
    t = RBT()
    print "Test Data: FENGDIJKABCLM"
    test_data = "FENGDIJKABCLM" #from A-N,without H
    for letter in test_data:
        t.put(letter,[ord(letter)]) #Value is [ascii order of letter]

    #=====min() and del_min()
    print "==========min() and del_min() test begin!=========="
    print "Original min():\t%s"%repr(t.min())
    print "run del_min()"
    t.del_min()
    print "After del_min:min()\t%s"%repr(t.min())

    print "run del_min() again"
    t.del_min()
    print "After del_min run again:min()\t%s"%repr(t.min())

    print "=====max() and del_max() test begin!"
    print "Original max():\t%s"%repr(t.max())
    print "run del_max()"
    t.del_max()
    print "After del_max:max()\t%s"%repr(t.max())

    print "run del_max() again"
    t.del_max()
    print "After del_max run again:max()\t%s"%repr(t.max())
    print "==========min() max() del_min() del_max() test complete!==========\n"

def test_int_api():
    #======ceil floor above below
    print "==========Testing ceil floor above below =========="
    t = RBT()
    print "Test Data: FENGDIJKABCLM - [AHN] = FEGDIJKBCLM"
    test_data = "FEGDIJKBCLM" #from A-N, Del A H N

    for letter in test_data:
        t.put(letter,[ord(letter)]) #Value is [ascii order of letter]
    print "Node\tceil\t\tfloor\t\tabove\t\tbelow"
    for P in ['A','B','C','G','H','I','L','M','N']:
        print "%s\t%s\t%s\t%s\t%s"%(P,t.ceil(P),t.floor(P),t.above(P),t.below(P))

if __name__ == '__main__':
    test_basic_api()
    test_advance_api()
    test_int_api()
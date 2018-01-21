"""
Sorting Algorithm
"""
import random


def insertion_sort(sort_list):
	"""insertion sortO(n^2)"""
	iter_len = len(sort_list)

	if iter_len < 2:
		return sort_list

	for i in range(1, iter_len):
		key = sort_list[i]
		j = i - 1
		while j>=0 and sort_list[j]>key:
		    sort_list[j+1] = sort_list[j]
		    j -= 1
		sort_list[j+1] = key

	return sort_list

def shellSort(seq):  
	"""Shell sortO(n^2)"""
	length=len(seq)  
	inc=0  
	while inc<=length/3:  
		inc=inc*3+1  
	
	while inc>=1:  
		for i in range(inc,length):  
			tmp=seq[i]  
			for j in range(i,0,-inc):  
				if tmp<seq[j-inc]:  
					seq[j]=seq[j-inc]  
				else:  
					j+=inc  
					break  
			seq[j-inc]=tmp  
		inc//=3
	return seq

def bubble_sort(sort_list):
    """bubble sortO(n^2)"""
    iter_len = len(sort_list)

    if iter_len < 2:
        return sort_list

    for i in range(iter_len-1):
        for j in range(iter_len-i-1):
            if sort_list[j] > sort_list[j+1]:
                sort_list[j], sort_list[j+1] = sort_list[j+1], sort_list[j]

    return sort_list

def selection_sort(sort_list):
	"""selection sortO(n^2)"""
	iter_len = len(sort_list)
	
	if iter_len < 2:
		return sort_list

	for i in range(iter_len-1):
		smallest = sort_list[i]
		location = i
		
		for j in range(i, iter_len):
			if sort_list[j] < smallest:
				smallest = sort_list[j]
				location = j
				
		if i != location:
			sort_list[i], sort_list[location] = sort_list[location], sort_list[i]

	return sort_list

class merge_sort(object):
	"""Merge sort O(nlogn)"""
	def _merge(self, alist, p, q, r):
		left = alist[p:q+1]
		right = alist[q+1:r+1]
		
		for i in range(p, r+1):
			if len(left)>0 and len(right)>0:
				if left[0]<=right[0]:
					alist[i] = left.pop(0)
				else:
					alist[i] = right.pop(0)
			elif len(right)==0:
				alist[i] = left.pop(0)
			elif len(left)==0:
				alist[i] = right.pop(0)

	def _merge_sort(self, alist, p, r):
		if p<r:
			q = int((p+r)/2)
			self._merge_sort(alist, p, q)
			self._merge_sort(alist, q+1, r)
			self._merge(alist, p, q, r)


	def __call__(self, sort_list):
		self._merge_sort(sort_list, 0, len(sort_list)-1)
		return sort_list

class heap_sort(object):
	"""heap sort O(nlogn)"""
	def _left(self, i):
		return 2*i+1

	def _right(self, i):
		return 2*i+2

	def _parent(self, i):
		if i%2==1:
			return int(i/2)
		else:
			return i/2-1

	def _max_heapify(self, alist, i, heap_size=None):
		length = len(alist)

		if heap_size is None:
			heap_size = length

		l = self._left(i)
		r = self._right(i)

		if l < length and alist[l] > alist[i]:
			largest = l
		else:
			largest = i

		if r < length and alist[r] > alist[largest]:
			largest = r

		if largest!=i:
			alist[i], alist[largest] = alist[largest], alist[i]
			self._max_heapify(alist, largest, heap_size)

	def _build_max_heap(self, alist):
		roop_end = int(len(alist)/2)
		for i in range(0, roop_end)[::-1]:
			self._max_heapify(alist, i)

	def __call__(self, sort_list):
		self._build_max_heap(sort_list)
		heap_size = len(sort_list)
		
		for i in range(1, len(sort_list))[::-1]:
			sort_list[0], sort_list[i] = sort_list[i], sort_list[0]
			heap_size -= 1
			self._max_heapify(sort_list, 0, heap_size)

		return sort_list

class quick_sort(object):
    #quick sort
	def quicksort(self,low, high, array):
		limit = 10 
		if low < 0 or high >= len(array):
			return

		if (high-low)<limit:
			self.insertsort(low,high,array)
			return
		#radomization
		radomi = random.randint(low, high)
		alist[radomi], alist[high] = alist[high], alist[radomi]

		middle = (low+high)/2

		if array[low] > array[middle]:
			self.exchange(low,middle,array)
	
		if array[middle]>array[high]:
			self.exchange(middle,high,array)

		if array[low]>array[high]:
			self.exchange(low,high,array)

		pivot = array[middle]

		self.exchange(middle,high-1,array)

		low_ind = low + 1

		high_ind = high - 2
	
		while low_ind <= high_ind:
			while array[low_ind] < pivot:
				low_ind+=1

			while array[high_ind] > pivot:
				high_ind-=1

			if low_ind < high_ind:
				self.exchange(low_ind,high_ind,array)

				low_ind+=1
				high_ind-=1
			else:
				break

		self.exchange(low_ind,high-1,array)

		self.quicksort(low,low_ind-1,array)
		self.quicksort(low_ind+1,high,array)

	#exchange two element
	def exchange(self,index1, index2, array):
		temp = array[index1]
		array[index1] = array[index2]
		array[index2] = temp

	#insertion sort
	def insertsort(self,low,high,array):
		if low < 0 or high >= len(array):
			return

		outer = low + 1

		while (outer<=high):
			inner = low
			while (inner<outer):
				if array[outer]<array[inner]:
					array.insert(inner,array[outer])
					del array[outer+1]
					break
				inner+=1
			outer+=1

	def __call__(self, sort_list):
		self.quicksort(0, len(sort_list)-1,sort_list)
		return sort_list

def q_sort(l):
	return l if len(l)<=1 else q_sort([x for x in l[1:] if x<l[0]])+[l[0]]+q_sort([x for x in l[1:] if x>=l[0]])

class counting_sort(object):

	def _counting_sort(self, alist, k):
		alist3 = [0 for i in range(k)]
		alist2 = [0 for i in range(len(alist))]
		
		for j in alist:
			alist3[j] += 1

		for i in range(1, k):
			alist3[i] = alist3[i-1] + alist3[i]

		for l in alist[::-1]:
			alist2[alist3[l]-1] = l
			alist3[l] -= 1

		return alist2

	def __call__(self, sort_list, k=None):
	
		if k is None:
			import heapq
			k = heapq.nlargest(1, sort_list)[0] + 1

		return self._counting_sort(sort_list, k)

def sortTest():
    csort=counting_sort()
    print(csort([1,3,5,6,2,0,10,12]))



if __name__=='Sorting':
    print('Sorting is running')
    sortTest()
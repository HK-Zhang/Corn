#不可变序列-----元组 tuple
		
#元组和列表十分相似,元组和字符串一样都是不可变的。
		
#元组由不同的元素组成，每个元素可以存储不同类型的数据，例如
#字符串、数字和元组
		
#元组通常代表一行数据，而元组中的元素则代表不同的数据项
		
#创建元组，不定长，但一旦创建后则不能修改长度
		
#空元组
tuple_name = ()
print tuple_name

#如果创建的元组只有一个元素，那么该元素后面的逗号是不可忽略的
print (4),(4,)

user = ('01','02','03','04')
#添加元组
user = (user,'05')
print user

#去重
a=set((2,2,2,4,4))
print a

#访问元组
print user[0]

#不可修改元素
user=(1,2,3)
#user[0]=2
		
		
#解包
user = (1,2,3)
a,b,c = user
print a,b,c

##访问二元元组
user1 = (1,2,3)
user2 = (4,5,6)
user = (user1,user2)
print user[0][0]
			
#元组的遍历
#range([start],stop,[,step]) 返回一个递增后者递减的 数字 列表
		
for item in range(len(user)):
	print user[item]
		    
#二元元组的访问
for i in range(len(user)):
	for j in range(len(user[i])):
		print 'user['+str(i)+']['+str(j)+']=',user[i][j]
		   
#使用map()实现遍历	
#map(function_name,sequence[,sequence...])
		
#返回 function处理后的列表
#sequence 元组或列表
		
for item in map(None,user):
	for i in item:
		print i

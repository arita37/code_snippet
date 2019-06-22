# -*- coding: utf-8 -*-
#####################################################################################
def solution(A)



import os







def int_tobinary(x) : 
 aa= "{0:b}".format(x)
 return [  int(a) for a in aa]




int_tobinary(5)


  5 bitxor 6 bitxor 7 bitxor 8 =
      3      bitxor     15     =
               12
               

def bitxor(m, n):
  return int(m) ^ int(n)
  
  
  
  
  mb= int_tobinary(m)
  nb= int_tobinary(n)

  
a= 12
b= 21
int(a) ^ int(b)


25

xor_result = int(a, 16) ^ int(b, 16)



m= 5
n= 8

               
aa= m
for xx in xrange(m+1, n+1) :
  aa= bitxor(aa, xx)


aa

###########################################################
def bitxor(m, n):
  return int(m) ^ int(n)

def solution(m, n) :
 if m > n : print "error"
 
 aa= m
 for xx in xrange(m+1, n+1) :
   aa= bitxor(aa, xx)

 return aa


5  6   7  8


a=5
b= 8



def xorbit(m, n): 
 if n== m   : return n  
 if n== m+1 : return bitxor(m, n)
 if n== m+2 : return bitxor(m, bitxor(m+1,n))

 ll= [ x for x in xrange(m, n+1)]
 
 ilo=0
 iup= len(ll) 
# print ilo, iup
 while True :
   imid = max(0, (ilo + iup-1) //2  )
   #print ll
   #print ilo, imid, iup
   if ilo== imid :  
     #print ll[0]
     return ll[0]
   else :  
     #print ll[ilo], ll[imid]
     a= xorbit( ll[ilo], ll[imid] )
     b= xorbit( ll[imid+1], ll[iup-1] ) 
     return bitxor(a, b)    #BitXor
     
  

xorbit(5, 6) 
3

xorbit(7, 8) 
15



xorbit(5, 25000) 

solution(5, 25000)



################################################################################
def bitxor(m, n):
  return int(m) ^ int(n)

def solution_lin(m, n) :
 aa= m
 for xx in xrange(m+1, n+1) :
   aa= bitxor(aa, xx)

 return aa
 
 

def xorbit(m, n) :
   if n== m   : return n  
   if n== m+1 : return bitxor(m, n)
   if n== m+2 : return bitxor(m, bitxor(m+1,n))
   if n== m+3 : 
     a= bitxor(m, m+1)
     b= bitxor(m+2, m+3)
     return bitxor(a, b)
     
   while True :
     mid= min(n, max(m, int( (m + n) // 2 )))
     if m == n : return m    
     else :      
       a=   xorbit(m, mid)
       b=   xorbit(mid+1, n)
       return bitxor(  a , b    )
     
     
def solution_log(m,n):
   return  xorbit(m, n)
  
  
  
  
solution_lin(5,  8)


solution_log(5,  1000000000)
  
  
  
  
  
  
  
  
  
xorbit(  5, 2500000) 
 





5 6 7 8

5 6
       5
                15
7 8    7







Method 1 (Naive Approach):
1- Initialize result as 0.
1- Traverse all numbers from 1 to n.
2- Do XOR of numbers one by one with result.
3- At the end, return result.

Method 2 (Efficient method) :
1- Find the remainder of n by moduling it with 4.
2- If rem = 0, then xor will be same as n.
3- If rem = 1, then xor will be 1.
4- If rem = 2, then xor will be n+1.
5- If rem = 3 ,then xor will be 0.





5, 6 , 7, 8






5  8   ---> 12





 

 print m,  mid, n
  a= xorbit(m, mid) 
  b= xorbit(mid, n)
 
 return xorbit(a,b)



(5+8)//2


(5+6)//2


bitxor(5,5)


def binary_search(seq, t):
    min = 0
    max = len(seq) - 1
    while True:
        if max < min:
            return -1
        m = (min + max) // 2
        if seq[m] < t:
            min = m + 1
        elif seq[m] > t:
            max = m - 1
        else:
            return m
            
            

xorbit(6, 8 )





(7+8)//2


 while lbound < ubound :
   
   
   
 
 aa= m
 for xx in xrange(m+1, n+1) :
   aa= bitxor(aa, xx)

 return aa




    # Binary search the result
    while resultLowerBound <= resultUpperBound:
        resultMaxMid =  (resultLowerBound + resultUpperBound) / 2
        blocksNeeded =  blocksNo(A, resultMaxMid)
        
        if blocksNeeded <= K:
            #Less than K blocks, so decrease the Boundary up.

        
            resultUpperBound = resultMaxMid - 1
            result = resultMaxMid
        else:

            # Need more than K blocks ---> increase lower bound
            # With large sum being resultMaxMid or resultMaxMid-,
            # we need to use more than K blocks. So resultMaxMid
            # is impossible to be our answer.

            resultLowerBound = resultMaxMid + 1
 



def exists_element(element, array):
    if not array:
        yield False

    mid = len(array) // 2
    if element == array[mid]:
        yield True
    elif element < array[mid]:
        yield from exists_element(element, array[:mid])
    else:
        yield from exists_element(element, array[mid + 1:])
        
        
        

binary



#####################################################################################
def cumsum(A):
  cumsum= [0] * len(A)
  cumsum[0]= A[0]
  for k in xrange(1 , len(A)) :
    cumsum[k]= cumsum[k-1] + A[k] 
  return cumsum
  


def solution(A):
    # write your code in Python 2.7
 n= len(A)
 if n==0 : return -1
 if n==1 : 
     if A[0]==0 : return 0
     else :       return -1
 if n==2 : 
     if (0==A[1] ) : return 0
     if (A[0]==0 ) : return 1
     else :          return -1

  
     
 for p in xrange(0, n) :
   print  sum(A[0:p-1+1]) , sum(A[p+1:]) 
   if cumsum[p] ==  (  cumsum[n-1] - cumsum[p] )   :   
      return p
  
 return -1


position 0 of A = [500, 1, -2, -1, 2]



aa= [-1,3,-4,5,1,-6,2,1 ]

solution(aa)


solution( [500, -1,-2,1,2])




solution( [-1,-1])



#### most frequent
def solutton(A) :

  dd= dict()
  
  for i in xrange(0,n) :
    try :    
      dd[ A[i] ] +=1
    except :
      dd[ A[i]]= 1
      
   maxval = -1   
   kval=-1
   for k, item in dd.items():
     if item > maxval :
       maxval= item
       kval= k
       
   if maxval > round(n/2,0) :  return kval
   else :                      return -1




sum(aa[2:])





  A[0] = -1
  A[1] =  3
  A[2] = -4
  A[3] =  5
  A[4] =  1
  A[5] = -6
  A[6] =  2
  A[7] =  1
############################################################################


















#### most frequent
def findequi(A):
  A.sort()
  n= len(A)
    
  c0= A[ n//2 ]
  count= 0
  for k in xrange(0, n) :
    if A[k]== c0 :
      count+=1

  if count > n/2:  return c0
  else :           return -0.5
    
    

def solution(A) :
  n= len(A)

  count= 0  
  for k in xrange(0, n-1) :
     a1= findequi(A[0:k+1])
     a2= findequi(A[k+1:])
     
     if a1==a2 : 
       print k, a1, a2
       count+= 1
       
  return count
  
  

aa= [ 4, 3, 4, 4, 4, 2    ]


solution(aa)






   A[0] = 4
    A[1] = 3
    A[2] = 4
    A[3] = 4
    A[4] = 4
    A[5] = 2


############################################################################







entry= [ 1, 2, 10, 5, 5 ]
exit1 = [ 4, 5, 12, 9, 12 ]

entry= [13, 28, 29, 14, 40, 17, 3 ] 
exit1= [107, 95, 111, 105, 70, 127, 74 ]

###  merge(a, b)




#####################################################################################
a=  [13, 28, 29, 14, 40, 17, 3 ] 
b=  [107, 95, 111, 105, 70, 127, 74 ]

a.sort()
b.sort()

ntot= len(a) + len(b)

c= []
i2=0
i1=0



while (i1 +i2) < ntot :  
  if (i1 < n1 ) & ( i2 < n2) :    
    if a[i1] < b[i2] :
      c.append( a[i1 ])
      i1= i1 +1
    elif a[i1] == b[i2] :
      c.append(  a[i]  )
      c.append(  b[i2]  )
      i2= i2 +1
      i1= i1 +1
    else :
     c.append(  b[i2] )
     i2= i2 +1
     
     
     
[1, 0.23]
[2, 0.39]
[4, 0.31]
[5, 0.27]
     
 sorted(li,key=lambda l:l[1], reverse=True)






 
 


'''
Maintaint current list
and transform time into same metric to add up +1 / -1 

'''

n= len(entry)
m= len(exit1)


maxt=  max(  max(entry), max(exit1))

seq= [0] * ( maxt +1)


for ti in entry :
   seq[ti] += 1
   

for ti in exit1 :
   seq[ti] -= 1


cumsum= [0] * ( maxt +1)   
for i in xrange(0, maxt) :
  cumsum[i]= cumsum[i-1] + seq[i]   
   
   
maxp= max(cumsum)   



for i in xrange(0, maxt) :
  if cumsum[i] == maxp :
     imax= i
     break;     


 maxp, imax

     
     
     
   
   
   
   
   





















############################################################################
#---------------------             --------------------




############################################################################











#####################################################################################
a= [2, 6, 8 ,9 ]
a2= [0]*n

n=4
k=3
for ii in xrange(0, 4) :
  ik= (ii+k) if ii+k < n else (ii+k-n)
  
  a2[ik]=  a[ii]

a2







#####################################################################################
#---------------------             --------------------
import numpy as np
import scipy as sci
from scipy import fftpack



n= 200
x=0.05
xn = x * np.arange(n)


y=  np.cos(3*xn) + np.cos(2*xn)



y=  np.cos(3*xn) + np.cos(2*xn*xn)
#### Fourier Transform 
k=50
y_fft= sci.fftpack.fft(y)
y_fft[k+1:]= 0   # Filter out higher frequency
y2= sci.fftpack.ifft(y_fft).real







import matplotlib.pylab as plt

plt.plot(y2)



####################################################################










































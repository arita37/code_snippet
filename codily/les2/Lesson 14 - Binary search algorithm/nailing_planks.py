"""
You are given two non-empty zero-indexed As A and B consisting of N integers.
These As represent N planks.
More precisely, A[K] is the start and B[K] the end of the K−th plank.

Next, you are given a non-empty zero-indexed A C consisting of M integers.
This A represents M nails.
More precisely, C[I] is the position where you can hammer in the I−th nail.

We say that a plank (A[K], B[K]) is nailed if there exists a nail C[I]
 such that A[K] ≤ C[I] ≤ B[K].

The goal is to find the minimum number of nails that must be used until all
 the planks are nailed.

In other words, you should find a value J such that all planks will be nailed
 after using only the first J nails. More precisely,
 for every plank (A[K], B[K]) such that 0 ≤ K < N,
 there should exist a nail C[I] such that I < J and A[K] ≤ C[I] ≤ B[K].

For example, given As A, B such that:

    A[0] = 1    B[0] = 4
    A[1] = 4    B[1] = 5
    A[2] = 5    B[2] = 9
    A[3] = 8    B[3] = 10
four planks are represented: [1, 4], [4, 5], [5, 9] and [8, 10].

Given A C such that:

    C[0] = 4
    C[1] = 6
    C[2] = 7
    C[3] = 10
    C[4] = 2
if we use the following nails:

    0, then planks [1, 4] and [4, 5] will both be nailed.
    0, 1, then planks [1, 4], [4, 5] and [5, 9] will be nailed.
    0, 1, 2, then planks [1, 4], [4, 5] and [5, 9] will be nailed.
    0, 1, 2, 3, then all the planks will be nailed.
Thus, four is the minimum number of nails that, used sequentially, 
allow all the planks to be nailed.

Write a function:

def solution(A, B, C)

that, given two non-empty zero-indexed As A and B consisting of N integers
and a non-empty zero-indexed A C consisting of M integers,
returns the minimum number of nails that, used sequentially,
allow all the planks to be nailed.

If it is not possible to nail all the planks, the function should return −1.

For example, given As A, B, C such that:

    A[0] = 1    B[0] = 4
    A[1] = 4    B[1] = 5
    A[2] = 5    B[2] = 9
    A[3] = 8    B[3] = 10

    C[0] = 4
    C[1] = 6
    C[2] = 7
    C[3] = 10
    C[4] = 2
the function should return 4, as explained above.

Assume that:

N and M are integers within the range [1..30,000];
each element of As A, B, C is an integer within the range [1..2*M];
A[K] ≤ B[K].

Complexity:
    expected worst-case time complexity is O((N+M)*log(M));
    expected worst-case space complexity is O(M),
     beyond input storage (not counting the storage required for input arguments).
Elements of input As can be modified.
"""

A = [   1, 4, 5, 8 ]
B = [   4, 5, 9, 10 ]
C = [ 4, 6, 7, 10, 2  ]




#################################################################
(1) The simplest solution
The problem suggests the O((N+M)*log(M)) time complexity for this problem, and log(M) suggests the binary search is done for M (for the number of nails).
The simplest strategy is to perform the binary search for the required number of nails, and check if all the planks are nailed.
The below is the simple implementation for this strategy, however while it gets the 100% score for the correctness, it gives the 0% performance score; this is a matter of course. This is not a O((N+M)*log(M)) solution. 

Bound values : Binary compute



def solution(A, B, C ) :
    N = len(A)
    M = len(C)
 
    # Boundaris of search
    beg = 1
    end = M    
    
    answer = -1
    while (beg <= end) :
        mid = (beg + end) // 2  

        success = check2(A,B,C,N, M, mid) # if this range has nailed
        if success :
            end = mid - 1   # Decrease right side : can reduce nail
            answer = mid 
        else :
            beg = mid + 1   # Increase left side : Need more nails
            
    return answer



######## N*M complexity  !!   ##########################################
def check(A, B, C,N,  M, kmax ) :
    ### Quadratic cost
    nailed =  [0] * N
    # If A,B  are all nailed
    for  i in range(kmax) :  #  up to nailed kmax
        for j in range(N) : # each plank
            if (A[j] <= C[i]  and C[i] <= B[j]) :
                nailed[j] = 1
                
    ### Check if Nailed at each plank
    success = True 
    for i in range(N) :    # Find No nailed plank
        cond = nailed[i] == 0
        if cond  :
            success = False
    return success


solution(A, B, C) 



http://pythontutor.com/live.html#code=%23%23%23%23%0A%0Aprint%28%22start%22%29%0A%0A%0A%0A%0A%0A%0Adef%20solution%28A,%20B,%20C%20%29%20%3A%0A%20%20%20%20N%20%3D%20len%28A%29%0A%20%20%20%20M%20%3D%20len%28C%29%0A%20%0A%20%20%20%20%23%20Boundaris%20of%20search%0A%20%20%20%20beg%20%3D%201%0A%20%20%20%20end%20%3D%20M%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20answer%20%3D%20-1%0A%20%20%20%20while%20%28beg%20%3C%3D%20end%29%20%3A%0A%20%20%20%20%20%20%20%20mid%20%3D%20%28beg%20%2B%20end%29%20//%202%20%20%0A%0A%20%20%20%20%20%20%20%20success%20%3D%20check2%28A,B,C,N,%20M,%20mid%29%20%23%20if%20this%20range%20has%20nailed%0A%20%20%20%20%20%20%20%20if%20success%20%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20end%20%3D%20mid%20-%201%20%20%20%23%20Decrease%20right%20side%20%3A%20can%20reduce%20nail%0A%20%20%20%20%20%20%20%20%20%20%20%20answer%20%3D%20mid%20%0A%20%20%20%20%20%20%20%20else%20%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20beg%20%3D%20mid%20%2B%201%20%20%20%23%20Increase%20left%20side%20%3A%20Need%20more%20nails%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20return%20answer%0A%0A%0A%0A%0Adef%20check2%28A,B,C,N,%20M,%20kmax%29%20%3A%0A%20%20%20%20%20%20%20%20%23%23%20Linear%20cost%0A%20%20%20%20%20%20%20%20%23%23%20Each%20element%20of%20As%20A,%20B,%20C%20is%20an%20integer%20within%20the%20range%20%5B1..2*M%5D%3B%0A%20%20%20%20%20%20%20%20%23%23%23%23Storage%20for%20check%20%20%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%0A%20%20%20%20%20%20%20%20max_pos%20%3D%202%20*%20M%20%2B%201%0A%20%20%20%20%20%20%20%20cum_sum%20%3D%20%5B0%5D%20*%20%28max_pos%29%20%20%23%23%20storage%20of%20info%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20for%20i%20in%20range%28kmax%29%20%3A%20%20%20%20%20%20%20%20%20%20%23%23%23%23%20For%20each%20nail,%20specify%20position%20%0A%20%20%20%20%20%20%20%20%20%20%20%20cum_sum%5BC%5Bi%5D%5D%20%2B%3D%201%20%20%0A%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20for%20i%20in%20range%281,%20max_pos,1%29%20%3A%20%20%23%23%23%20Cumulative%20Nb%20of%20nails%20%3A%20left%20to%20right%0A%20%20%20%20%20%20%20%20%20%20%20%20cum_sum%5Bi%5D%20%3D%20cum_sum%5Bi%5D%20%2B%20cum_sum%5Bi%20-%201%5D%0A%0A%0A%20%20%20%20%20%20%20%20%23%23%23%20Check%20if%20all%20has%20nailed%0A%20%20%20%20%20%20%20%20success%20%3D%20True%0A%20%20%20%20%20%20%20%20for%20i%20in%20range%280,%20N,%201%29%20%3A%20%0A%20%20%20%20%20%20%20%20%20%20%20%20cond%20%3D%20%28cum_sum%5BB%5Bi%5D%5D%20%3D%3D%20cum_sum%5BA%5Bi%5D%20-%201%5D%29%20%20%23%20nb%20of%20Nails%20in%20B%20%20%3D%3D%20Nb%20Nails%20on%20A%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20cond%20%3A%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20success%20%3D%20False%0A%20%20%20%20%20%20%20%20%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%23%0A%20%20%20%20%20%20%20%20return%20success%0A%20%20%20%20%0A%0A%0A%0A%0A%0AA%20%3D%20%5B%20%20%201,%204,%205,%208%20%5D%0AB%20%3D%20%5B%20%20%204,%205,%209,%2010%20%5D%0AC%20%3D%20%5B%204,%206,%207,%2010,%202%20%20%5D%0A%0A%0A%0Asolution%28A,%20B,%20C%29%20%0A%0A%0A%0Aprint%28%22end%22%29&cumulative=false&curInstr=4&heapPrimitives=nevernest&mode=display&origin=opt-live.js&py=3&rawInputLstJSON=%5B%5D&textReferences=false


#######################################################################
(2) The O((M+N) * log(M)) solution

is the time complexity of the 'check' function, and need some more improvement if the given nails can nail all the planks.

First, we clear the A, prefix_sum[] with 0, and then add 1 to prefix_sum[i] 
if there is any new nail found at the position 'i'.

Then we compute the prefix_sum for the total number of nails found so far 
until the position from head to tail.
* Cumulative Nails 

if there is no nail between A[i] and B[i] (within the plank 'i'), 
prefix_sum[B[i]] == prefix_sum[A[i] - 1].


####Projection of all nails, plank into Same Space
each element of As A, B, C is an integer within the range [1..2*M];

 1 < A[i] < 2*M


def check2(A,B,C,N, M, kmax) :
        ## Linear cost
        ## Each element of As A, B, C is an integer within the range [1..2*M];
        ####Storage for check  #######################################
        max_pos = 2 * M + 1
        cum_sum = [0] * (max_pos)  ## storage of info
        
        for i in range(kmax) :          #### For each nail, specify position 
            cum_sum[C[i]] += 1  
      
        for i in range(1, max_pos,1) :  ### Cumulative Nb of nails : left to right
            cum_sum[i] = cum_sum[i] + cum_sum[i - 1]


        ### Check if all has nailed
        success = True
        for i in range(0, N, 1) : 
            cond = (cum_sum[B[i]] == cum_sum[A[i] - 1])  # nb of Nails in B  == Nb Nails on A
            if cond :  
                success = False
        ############################################################
        return success
    
solution(A, B, C )





#### Binary Search using Recursion
We implement the algorithm of binary search using python as shown below.
 We use an ordered list of items and design a recursive function to
 take in the list alogn with starting and ending index as input. Then the binary search function calls itself till find the the searched item or concludes about its absence in the list.


def bsearch(ll, idx0, idxn, val):
    # Initial condition 
    if (idxn < idx0):
        return None
    
    midval = idx0 + ((idxn - idx0) // 2)
    # Compare the search item with middle most value

    if ll[midval] > val:
            return bsearch(ll, idx0, midval-1,val)
    
    elif ll[midval] < val:
            return bsearch(ll, midval+1, idxn, val)
    
    else:
            return midval

ll = [8,11,24,56,88,131]
print(bsearch(ll, 0, 5, 24))
print(bsearch(ll, 0, 5, 51))




################ Visualize Code
http://pythontutor.com/visualize.html#mode=edit



def merge(left, right) :
        # Merge of ordered list
        i=j=k=0    
        A = [0] * (len(left) + len(right))
        
        #### Merge based on condition
        while i < len(left) and j < len(right):
            cond =  left[i] < right[j]
            if cond :
                A[k]=left[i]
                i=i+1
            else:
                A[k]=right[j]
                j=j+1
            k=k+1

        #### Remaining when one table is full:  left < right
        while i < len(left):
            A[k]=left[i]
            i=i+1
            k=k+1

        while j < len(right):
            A[k]=right[j]
            j=j+1
            k=k+1

        return A

   
def mergeSort(nlist):
    print("Splitting ",nlist)
    if len(nlist) == 1 :
        rerurn nlist
    
    # Split part
    mid = len(nlist)//2
    left = nlist[:mid]
    right = nlist[mid:]

    # Sub process
    left = mergeSort(left)
    right = mergeSort(right)
    
    # Merge
    nlist = merge(left, right)
    return nlist

print("Merging ",nlist)

nlist = [14,46,43,27,57,41,45,21,70]
nlist = mergeSort(nlist)
print(nlist)


#############################################################################
#### Merge Compute  Process #################################################
def merge(left, right) :
     return -left * right

def merge_compute(A):
    print("Splitting ",A)
    if len(A) == 1 :  return A[0]
    if len(A) == 2 :  return -A[0] * A[1]
    
    # Split part
    mid = len(A)//2
    left = A[:mid]
    right = A[mid:]

    # Sub process
    left = merge_compute(left)
    right = merge_compute(right)
    
    # Merge
    val = merge(left , right)
    return val

A = [1, 4, 5, 8, 9]
merge_compute(A)
  
def bitxor(m, n):
  return int(m) ^ int(n)

bitxor( 11 , 9)





min= 0
def solution(A):

    
def solution(A) :    
  A.sort()
  min= 1
  for t in A :
    if t > min :
      return min
    elif t == min :
        min = min + 1
  return min        


solution(A)


A = [10, 3, 7,1, 4,6, 2]






##################################################################################
##################################################################################
def sol(A,B,C) :
    na = len(A)
    nc = len(C)

    ### Initilaize
    min0 = 1
    min1 = len(C)

    ## Bin search between [min, max] values
    answer = -1
    while min0 < max0 :
      mid = (min0 + max0) // 2 
      success = check_linear(A,B, mid)
      if success :
           mid = max0 -1
           answer = max0
      else :
           mid = min0 + 1
  
    return answer


def check_linear(A, B, C, mid) :
    flag = True
    for i in range(0, len(C),1) :
        
      flag = has_nailed(A[k], B[k], C[i], mid )           
      if flag is False :
          return False
    return flag        
           
def has_nailed(Ak, Bk, C ) :
    for i in range(0, mid, 1) :
         if ak <= C[i] and C[i]  <= bk :        
             flag = True
             break







#####################################################################################
    ### ok
def solution(A, B, C):
    M = len(C)  # Mac number of nails
    N = len(A)

    ELEMENT_MAX_VALUE = 2 * M + 1

    def recursive(begin, end):
        
        # Terminal condition
        if begin > end:
            return -1
        
        
        mid = (begin + end + 1) // 2

        nails = ELEMENT_MAX_VALUE * [0]
        for i in range(mid):
            nails[C[i]] += 1

        partial_sum = ELEMENT_MAX_VALUE * [0]
        partial_sum[0] = nails[0]
        for i in range(1, 2 * M + 1):
            partial_sum[i] = partial_sum[i - 1] + nails[i]
 
    
        ### linear check
        for a, b in zip(A, B):
            if partial_sum[b] - partial_sum[a - 1] == 0:
                break
        else:
            ret = recursive(begin, mid - 1)
            
            return mid if ret == -1 else ret

   
        return recursive(mid + 1, end)

    # Check min, max values
    return recursive(0, M)



solution(A, B, C)



for item in container:
    if search_something(item):
        # Found it!
        process(item)
        break
else:
    # Didn't find anything..
    not_found_in_container()



















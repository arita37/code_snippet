"""
You are given integers K, M and a non-empty zero-indexed array A consisting of N integers.
Every element of the array is not greater than M.

You should divide this array into K blocks of consecutive elements.
The size of the block is any integer between 0 and N.
Every element of the array should belong to some block.

The sum of the block from X to Y equals A[X] + A[X + 1] + ... + A[Y].
The sum of empty block equals 0.

The large sum is the maximal sum of any block.

For example, you are given integers K = 3, M = 5 and array A such that:

  A[0] = 2
  A[1] = 1
  A[2] = 5
  A[3] = 1
  A[4] = 2
  A[5] = 2
  A[6] = 2
The array can be divided, for example, into the following blocks:

[2, 1, 5, 1, 2, 2, 2], [], [] with a large sum of 15;
[2], [1, 5, 1, 2], [2, 2] with a large sum of 9;
[2, 1, 5], [], [1, 2, 2, 2] with a large sum of 8;
[2, 1], [5, 1], [2, 2, 2] with a large sum of 6.
The goal is to minimize the large sum. In the above example,
 6 is the minimal large sum.

Write a function:

def solution(K, M, A)

that, given integers K, M and a non-empty zero-indexed
 array A consisting of N integers, returns the minimal large sum.

For example, given K = 3, M = 5 and array A such that:

  A[0] = 2
  A[1] = 1
  A[2] = 5
  A[3] = 1
  A[4] = 2
  A[5] = 2
  A[6] = 2
the function should return 6, as explained above.

Assume that:
    N and K are integers within the range [1..100,000];
    M is an integer within the range [0..10,000];
    each element of array A is an integer within the range [0..M].

Complexity:
    expected worst-case time complexity is O(N*log(N+M));
    expected worst-case space complexity is O(1),
     beyond input storage (not counting the storage required for input arguments).

Elements of input arrays can be modified.
"""




A= [ 2,1,5,1,2,2,2 ]
K = 3
M = 5


sum([])

def ff(A, N,K,M) :
    if len(A) == 0 : return 0
    if K > N : return 0
    if K == N : return min(A)
    if K == 1 : return sum(A)
    if K == 0 : return 0
    
    for n0 in range(N,-1,-1) :
      s0 = sum( A[:n0])
      s1 = ff(A[n0:], N-n0, K-1, M)
      smax = max(s0, s1)
    return smax




 ff(A, N,K,M) 


Initial case :
    
    
    
Log(N) Loop :

while start < end :
   mid =  ( start + end ) / 2
   if check(A, mid, K) :
       end = mid-1
       res = mid
   else :
       start = mid+1







Binary Search on potential Min values
  max(A) <  Min largesum < sum(A)
   K=1                      k=N
   O(N*log(N+M));  :  iterate All Val, Binary on (value + block size)



### Binary search  : min,max values and linear costraints
def sol(K, M, A) :
    N = len(A)

    # Search and boundary values for min_sum
    min0 = max(A)
    max0= sum(A)

    ### Initial condition on K
    if K == 1: return max0
    if K == len(A): return min0

    # Binary Search
    while min0 <= max0 :
      mid  = int( (min0 + max0 ) /2 )
       
      if check_linear(A, mid, K) :
            max0 = mid - 1  # Decrease Max reaching values, min search
            res = mid
      else :
            ### Impossible to have mid sum.
            min0 = mid + 1
          
    return res


def check_linear(A, target_val, Kmax) :
    """"
       Calculate sequential sum of sub-bloack an
       Check if mid is reaches by sub-block of A : 
             return True of Block_Sum <= mid else False
    """
    block_sum = 0
    block_k  = 1
    for x in A :
        block_sum = block_sum + x
        
        # Reset Block into new one
        if block_sum >  target_val :
           block_sum = x
           block_k   = block_k + 1

        if block_k > Kmax :  # Total block are used
            break
    
    if block_k <= Kmax:   # nb of block is below than K      
       return True
    else :
       return False 








sol(K, M, A)
# 6




#########################################################################
def solution(K, M, A):
    N = len(A)

    min_largest_sum = max(A)
    max_largest_sum = sum(A)

    if K == 1:
        return max_largest_sum

    if K == len(A):
        return min_largest_sum

    #### Iterate on all possible values of Min_MaxBlock_Sum
    while min_largest_sum <= max_largest_sum:
        largest_sum = int( (min_largest_sum + max_largest_sum) / 2 )

        #### Linear Search
        acumulator = 0
        k_counter = 1
        for val in A:
            acumulator += val

            if acumulator > largest_sum:
                # Reset Block, Increment Block ID
                acumulator = val
                k_counter += 1
                if k_counter > K:
                    break

        # Reduce the search Interval.
        if k_counter <= K:
            max_largest_sum = largest_sum - 1
            result = largest_sum
        else:  #over K , increase value
            min_largest_sum = largest_sum + 1

    return result



solution(K, M, A)



O(N*log(N+M))
expand allExample tests
▶ example 

expand allCorrectness tests
▶ extreme_single 

▶ extreme_double 

▶ extreme_min_max 

▶ simple1 

▶ simple2 

▶ tiny_random_ones 

expand allPerformance tests
▶ small_random_ones 

▶ medium_zeros 

▶ medium_random 

▶ large_random 

▶ large_random_ones 

▶ all_the_same 







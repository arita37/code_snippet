A company has employed N developers (numbered from 0 to N−1) and 



wants to divide them into two teams. The first is a front-end team with F developers. 

The second is a back-end team with N−F developers.

 If the K-th developer is assigned to the front-end team then their contribution is A[K],


 and if they are assigned to the back-end team then their contribution is B[K]. What is the maximum sum of contributions the company can achieve?

Write a function:

def solution(A, B, F)
  that, given two arrays A, B (consisting of N integers each) and the integer F, 
  returns the maximum sum of contributions the company can achieve.

Examples:

1. Given A = [4, 2, 1], B = [2, 5, 3] and F = 2, the function should return 10.
 There should be two front-end developers and one back-end developer. 
 The 0th and 2nd developers should be assigned to the front-end team (with contributions 4 and 1) 
 and the 1st developer should be assigned to the back-end team (with contribution 5).

2. Given A = [7, 1, 4, 4], B = [5, 3, 4, 3] and F = 2, the function should return 18. The 0th and 3rd developers should be assigned to the front-end team and the 1st and 2nd developers should be assigned to the back-end team.

3. Given A = [5, 5, 5], B = [5, 5, 5] and F = 1, the function should return 15. The 0th developer can be assigned to the front-end team and the 1st and 2nd developers can be assigned to the back-end team.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..200,000];
arrays A and B have equal lengths;
each element of array A is an integer within the range [0..1,000];
F is an integer within the range [0..N].
Copyright 2009–2019 by Codility Limited. All Rights Reserved. Unauth


A[K] : front end
B[K] :back end


F * nb of front end:
  Max    A[ sublist ]  + B[  all - sublist ] 
      
  all sublist possible.
  
  
  All permutation of N(,2)
  
  
  
import itertools
list(itertools.permutations([1, 2, 3]))




# Function which returns subset or r length from n 
from itertools import combinations 
  
def subset(arr, r): 
    # return list of all subsets of length r 
    # to deal with duplicate subsets use  
    # set(list(combinations(arr, r))) 
    return list(combinations(arr, r)) 
  

arr = [1, 2, 3, 4] 
r = 3
subset(arr, r) 

A =  [4, 2, 1]
B =  [2, 5, 3] 
F =  2

def solution(A,B, F) :
    n = len(A)
    ll = list(itertools.permutations( [t for t in range(n)] ))
    # ll = subset([t for t in range(n)], n) 
    smax = 0
    for v in ll :
      s1 = 0
      for x in v[:F] :
          s1 = s1 + A[x]

      s2 = 0
      for x in v[F:] :
          s2 = s2 + B[x]
          
      if s1 + s2 > smax :
        smax = s1 + s2
        vmax = v
    
    return smax, vmax



A =  [4, 2, 1]
B =  [2, 5, 3] 
F =  2


list(v)

A[[2,3 ]]




#### Binary Search base Algo :  #######################################
Binary Search on potential Min values
  max(A) <  Min largesum < sum(A)
   K=1                      k=N
   O(N*log(N+M));  :  iterate All Val, Binary on (value + block size)



### Binary search  : min,max values and linear costraints
### Condition on mathatmical part
 
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
            max0 = mid - 1  # Decrease Max reaching values
            res = mid
      else :
            ### Impossible to have mid sum.
            min0 = mid + 1
          
    return res


def check_linear(A, target_val, Kmax) :
    """"
       Calculate sequential sum of sub-bloack an
       Check if mid is reaches by sub-block of A : 
             return True of Block_Sum <= mid
             else False
    """
    block_sum = 0
    block_k  = 1
    for x in A :
        block_sum = block_sum + x
        
        # Reset Block into new one
        if block_sum >  target_val :
           block_sum = x
           block_k =  block_k + 1

        if block_k > Kmax :
            break
    
    if block_k <= Kmax:   # nb of block is below than K      
       return True
    else :
       return False 



sol(K, M, A)
# 6




#########################################################################




def ok(A,mid,K):
  i=0
  for _ in range(K-1):
    s=0
    while i<len(A) and s+A[i] <= mid:
      s+=A[i]
      i+=1
  return sum(A[i:])<=mid


def solution(K, M, A):
  # write your code in Python 3.6
  su = sum(A)
  mi = su//K if su%K==0 else su//K+1
  mi = max(mi, max(A))

  i=ma=0
  for _ in range(K-1):
    s=0
    while i<len(A) and s+A[i]<=mi:
      s+ = A[i]
      i+ = 1
      ma = max(ma,s)
      ma = max(ma, sum(A[i:]))

   res=sum(A)

  #Binary search
  while mi<=ma:
    mid = (mi+ma)//2
    if ok(A,mid,K):
       res = min(res,mid)
       ma = mid-1
    else:
      mi = mid+1
 return res












#####################################################################################   
#####################################################################################   
Arithmetic sequence :
  Difference are same, 

A zero-indexed array A consisting of N numbers is given. A slice of that array is any pair of integers (P, Q) such that 0 <= P < Q < N.
A slice (P, Q) of array A is called arithmetic if the sequence:
A[P], A[p + 1], ..., A[Q - 1], A[Q] is arithmetic. In particular, this means that P + 1 < Q.
The function should return the number of arithmetic slices in the array A.    


def numberOfArithmeticSlices(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        size = len(A)
        if size < 3: return 0
        ans = cnt = 0
        delta = A[1] - A[0]
        for x in range(2, size):
            if A[x] - A[x - 1] == delta:
                cnt += 1
                ans += cnt
            else:
                delta = A[x] - A[x - 1]
                cnt = 0
        return ans
#####################################################################################   
    


#####################################################################################   
Count of AP (Arithmetic Progression) Subsequences in an array
Given an array of n positive integers. The task is to count the number of Arithmetic Progression
subsequence in the array. Note: Empty sequence or single element sequence 
is Arithmetic Progression. 1 <= arr[i] <= 1000000.



Input : arr[] = { 1, 2, 3 }
Output : 8
Arithmetic Progression subsequence from the 
given array are: {}, { 1 }, { 2 }, { 3 }, { 1, 2 },
{ 2, 3 }, { 1, 3 }, { 1, 2, 3 }.

Input : arr[] = { 10, 20, 30, 45 }
Output : 12

Input : arr[] = { 1, 2, 3, 4, 5 }
Output : 23



Since empty sequence and single element sequence is also arithmetic progression, 
so we initialize the answer with n(number of element in the array) + 1.
Now, we need to find the arithmetic progression subsequence of length greater than or equal to 2.
Let minimum and maximum of the array be minarr and maxarr respectively. 
Observe, in all the arithmetic progression subsequences,
the range of common difference will be from (minarr – maxarr) to (maxarr – minarr).
Now, for each common difference, say d, calculate the subsequence of length greater than or equal to 2 using dynamic programming.
Let dp[i] be the number of subsequence that end with arr[i] and have common difference of d. So,



// C++ program to find number of AP
// subsequences in the given array
using namespace std;
 
int numofAP(int a[], int n)
{
    // initializing the minimum value and
    // maximum value of the array.
    int minarr = INT_MAX, maxarr = INT_MIN;
 
    // Finding the minimum and maximum
    // value of the array.
    for (int i = 0; i < n; i++)
    {
        minarr = min(minarr, a[i]);
        maxarr = max(maxarr, a[i]);
    }
 
    // dp[i] is going to store count of APs ending
    // with arr[i].
    // sum[j] is going to store sun of all dp[]'s
    // with j as an AP element.
    int dp[n], sum[MAX];
 
    // Initialize answer with n + 1 as single elements
    // and empty array are also DP.
    int ans = n + 1;
 
    // Traversing with all common difference.
    for (int d=(minarr-maxarr); d<=(maxarr-minarr); d++)
    {
        memset(sum, 0, sizeof sum);
 
        // Traversing all the element of the array :
        for (int i = 0; i < n; i++)
        {
            // Initialize dp[i] = 1.
            dp[i] = 1;
 
            // Adding counts of APs with given differences
            // and a[i] is last element.  
            // We consider all APs where an array element is previous element of AP with a particular 
            // difference
            if (a[i] - d >= 1 && a[i] - d <= 1000000)
                dp[i] += sum[a[i] - d];
 
            ans += dp[i] - 1;
            sum[a[i]] += dp[i];
        }
    }
 
    return ans;
}
 
// Driver code
int main()
{
    int arr[] = { 1, 2, 3 };
    int n = sizeof(arr)/sizeof(arr[0]);
    cout << numofAP(arr, n) << endl;
    return 0;
}







#####################################################################################   

class bintree:
    x = 0
    l = None
    r = None

    def __init__(self,x,l,r):
        self.x = x
        self.l = l
        self.r = r



tree = bintree(5,
               bintree(8,
                       bintree(12,
                               bintree(1,
                                       None,
                                       None),
                               None),
                       bintree(6,
                               None,
                               None),
                       ),
               bintree(9,
                       bintree(7,
                               bintree(2,
                                       None,
                                       None),
                               None),
                       bintree(4,
                               None,
                               bintree(3,
                                       None,
                                       None)

                       )
               )
            )


def maxdiff(maxN,minN, node):

    if node == None:
        return (maxN, minN)

    maxN1 = maxN if maxN != None and maxN >= node.x  else node.x # node.x is max if maxN is less than it
    minN1 = minN if minN != None and minN <= node.x  else node.x # node.x is min if minN is > than it
    
    maxN2 = maxN1
    minN2 = minN1
    # split paths here
    (maxN1,minN1) = maxdiff(maxN1,minN1,node.l)

    (maxN2,minN2) = maxdiff(maxN2,minN2,node.r)

    if abs(maxN1-minN1) > abs(maxN2 - minN2):
        return (maxN1,minN1)

    return (maxN2,minN2)


if __name__=="__main__":
    
    max,min = maxdiff(None,None,tree)
    print("max,min (%d,%d)" % (max,min) )
    print("Solution is %d" % abs(max-min) )
    
    
    
    
    
    
    
    
    
    
#####################################################################################   
    
    
    


def blocksNo(A, maxBlock):
    # Initially set the A[0] being an individual block
 
    blocksNumber = 1    # The number of blocks, that A could
                        # be divided to with the restriction
                        # that, the sum of each block is less
                        # than or equal to maxBlock
    preBlockSum = A[0]
 
    for element in A[1:]:
        # Try to extend the previous block
        if preBlockSum + element > maxBlock:
            # Reset Block count:  because of the sum limitation maxBlock
            preBlockSum = element
            blocksNumber += 1
        else:
            preBlockSum += element
 
    return blocksNumber
    
    
    
def solution(K, A):
    blocksNeeded = 0    # Given the restriction on the sum of
                        # each block, how many blocks could
                        # the original A be divided to?
    resultLowerBound = max(A)    # 1 block
    resultUpperBound = sum(A)    # n block 
    result = 0          # Minimal large sum
 
    # Handle two special cases
    if K == 1:      return resultUpperBound
    if K >= len(A): return resultLowerBound
 
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
 
    return result
    
    
    
    
              # With large sum being resultMaxMid or resultMaxMid-,
            # we need blocksNeeded/blocksNeeded- blocks. While we
            # have some unused blocks (K - blocksNeeded), We could
            # try to use them to decrease the large sum.  
    
    
    
    



##################
#### Equilibrium point   
int equi(int arr[], int n) {
    if (n==0) return -1; 
    long long sum = 0;
    int i; 
    for(i=0;i<n;i++) sum+=(long long) arr[i]; 

    long long sum_left = 0;    
    for(i=0;i<n;i++) {
        long long sum_right = sum - sum_left - (long long) arr[i];
        if (sum_left == sum_right) return i;
        sum_left += (long long) arr[i];
    } 
    return -1; 
} 




##### Find Leader :  Sorting the table  in N*long_N
def solution(A): 
    n = len(A)
    L = [-1] + A
    L.sort()
    count = 0
    pos = (n + 1) // 2
    candidate = L[pos]
    for i in xrange(1, n + 1):
        if (L[i] == candidate):
            count = count + 1
    if (2*count > n):
        return candidate
    return -1







#########################################################################################################################
#########################################################################################################################
https://codility.com/programmers/lessons/3-time_complexity/frog_jmp/


Codility ‘Tape Equilibrium’ Solution
Posted on July 22, 2014 by Martin
Short Problem Definition:
Minimize the value |(A[0] + … + A[P-1]) – (A[P] + … + A[N-1])|.

Link
TapeEquilibrium

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
In the first run I compute the left part up to the point i and the overall sum last. Then I compute the minimal difference between 0..i and i+1..n.

Solution:
import sys
 
def solution(A):
    #1st pass
    parts = [0] * len(A)
    parts[0] = A[0]
  
    for idx in xrange(1, len(A)):
        parts[idx] = A[idx] + parts[idx-1]
  
    #2nd pass
    solution = sys.maxint
    for idx in xrange(0, len(parts)-1):
        solution = min(solution,abs(parts[-1] - 2 * parts[idx]));  
  
    return solution



#########################################################################################################################
Short Problem Definition:
Count minimal number of jumps from position X to Y.

Link
FrogJmp

Complexity:
expected worst-case time complexity is O(1);

expected worst-case space complexity is O(1).

Execution:
Do not use float division if possible!

Solution:
def solution(X, Y, D):
    if Y < X or D <= 0:
        raise Exception("Invalid arguments")
         
    if (Y- X) % D == 0:
        return (Y- X) // D
    else:
        return ((Y- X) // D) + 1




######################################################################################################
Short Problem Definition:
Find the missing element in a given permutation.

Link
PermMissingElem

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(1)

Execution:
Sum all elements that should be in the list and sum all elements that actually are in the list. The sum is 0 based, so +1 is required. The first solution using the + operator can cause int overflow in not-python languages. Therefore the use of a binary XOR is adequate.

Solution:
def solution(A):
    should_be = len(A) # you never see N+1 in the iteration
    sum_is = 0
 
    for idx in xrange(len(A)):
        sum_is += A[idx]
        should_be += idx+1
 
    return should_be - sum_is +1




###################################################################################################
Short Problem Definition:
Check whether array N is a permutation.

Link
PermCheck

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
Mark elements as seen in a boolean array. Elements seen twice or out of bounds of the size indicate that the list is no permutation. The check if the boolean array only contains true elements is not required. This solution only works with permutations starting from 1.

Solution:

def solution(A):
    seen = [False] * len(A)
 
    for value in A:
        if 0 <= value > len(A):
            return 0
        if seen[value-1] == True:
            return 0
        seen[value-1] = True
 
    return 1




###################################################################################################
Short Problem Definition:
Find the earliest time when a frog can jump to the other side of a river.

Link
FrogRiverOne

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(X)

Execution:
Mark seen elements as such in a boolean array. I do not like the idea of returning the first second as 0. But specifications are specifications 🙂

Solution:
def solution(X, A):
    passable = [False] * X
    uncovered = X
 
    for idx in xrange(len(A)):
        if A[idx] <= 0 or A[idx] > X:
            raise Exception("Invalid value", A[idx])
        if passable[A[idx]-1] == False:
            passable[A[idx]-1] = True
            uncovered -= 1
            if uncovered == 0:
                return idx
 
    return -1



###################################################################################################
Short Problem Definition:
Calculate the values of counters after applying all alternating operations: increase counter by 1; set value of all counters to current maximum.

Link
MaxCounters

Complexity:
expected worst-case time complexity is O(N+M);

expected worst-case space complexity is O(N)

Execution:
The idea is to perform the specified operation as stated. It is not required to iterate over the whole array if a new value is set for all the values. Just save the value and check it when an increase on that position is performed.

Solution:
#include <algorithm>
 
vector<int> solution(int N, vector<int> &A) {
    vector<int> sol;
    int current_max = 0;
    int last_increase = 0;
 
    for(int i=0; i<N;i++){
        sol.push_back(0);
    }
 
    for(unsigned int i=0; i<A.size();i++){
        if (A[i] > N) {
            last_increase = current_max;
        } else {
            sol[A[i]-1] = max(sol[A[i]-1], last_increase);
            sol[A[i]-1]++;
            current_max = max(current_max, sol[A[i]-1]);
        }
    }
 
    for(int i=0; i<N;i++){
        sol[i] = max(sol[i], last_increase);
    }
 
    return sol;
}



###################################################################################################
Short Problem Definition:
Find the minimal positive integer not occurring in a given sequence.

Link
MissingInteger

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
You only need to consider the first (N) positive integers. In this specification 0 does not count as a valid candidate! Any value that is below 1 or above N can be ignored.

Solution:
def solution(A):
    seen = [False] * len(A)
    for value in A:
        if 0 < value <= len(A):
            seen[value-1] = True
 
    for idx in xrange(len(seen)):
        if seen[idx] == False:
            return idx + 1
 
    return len(A)+1







###################################################################################################
Short Problem Definition:
Count the number of passing cars on the road.

Link
PassingCars

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(1)

Execution:
Count all cars heading in one direction (west). Each car heading the other direction (east) passes all cars that went west so far. Note that east cars at the beginning of the list pass no cars! Also do not forget the upper limit!

Solution:
def solution(A):
    west_cars = 0
    cnt_passings = 0
 
    for idx in xrange(len(A)-1, -1, -1):
        if A[idx] == 0:
            cnt_passings += west_cars
            if cnt_passings > 1000000000:
                return -1
        else:
            west_cars += 1
 
    return cnt_passings




######################################################################################################
Short Problem Definition:
Find the minimal nucleotide from a range of sequence DNA.

Link
GenomicRangeQuery

Complexity:
expected worst-case time complexity is O(N+M);

expected worst-case space complexity is O(N)

Execution:
Remember the last position on which was the genome (A, C, G, T) was seen. If the distance between Q and P is lower than the distance to the last seen genome, we have found the right candidate.

Solution:
def writeCharToList(S, last_seen, c, idx):
    if S[idx] == c:
        last_seen[idx] = idx
    elif idx > 0:
        last_seen[idx] = last_seen[idx -1]
 
def solution(S, P, Q):
     
    if len(P) != len(Q):
        raise Exception("Invalid input")
     
    last_seen_A = [-1] * len(S)
    last_seen_C = [-1] * len(S)
    last_seen_G = [-1] * len(S)
    last_seen_T = [-1] * len(S)
         
    for idx in xrange(len(S)):
        writeCharToList(S, last_seen_A, 'A', idx)
        writeCharToList(S, last_seen_C, 'C', idx)
        writeCharToList(S, last_seen_G, 'G', idx)
        writeCharToList(S, last_seen_T, 'T', idx)
     
     
    solution = [0] * len(Q)
     
    for idx in xrange(len(Q)):
        if last_seen_A[Q[idx]] >= P[idx]:
            solution[idx] = 1
        elif last_seen_C[Q[idx]] >= P[idx]:
            solution[idx] = 2
        elif last_seen_G[Q[idx]] >= P[idx]:
            solution[idx] = 3
        elif last_seen_T[Q[idx]] >= P[idx]:
            solution[idx] = 4
        else:    
            raise Exception("Should never happen")
         
    return solution



######################################################################################################
Short Problem Definition:
Compute number of integers divisible by k in range [a..b].

Link
CountDiv

Complexity:
expected worst-case time complexity is O(1);

expected worst-case space complexity is O(1)

Execution:
This little check required a bit of experimentation. One needs to start from the first valid value that is bigger than A and a multiply of K.

Solution:
def solution(A, B, K):
    if B < A or K <= 0:
        raise Exception("Invalid Input")
 
    min_value =  ((A + K -1) // K) * K
 
    if min_value > B:
      return 0
 
    return ((B - min_value) // K) + 1









######################################################################################################
Short Problem Definition:
Determine whether a given string of parentheses is properly nested.

Link
Brackets

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
Put every opening bracket on a stack. If a closing bracket is not the same as the top stack bracket, the string is not properly nested.

Solution:
def isValidPair(left, right):
    if left == '(' and right == ')':
        return True
    if left == '[' and right == ']':
        return True 
    if left == '{' and right == '}':
        return True   
    return False
 
def solution(S):
    stack = []
     
    for symbol in S:
        if symbol == '[' or symbol == '{' or symbol == '(':
            stack.append(symbol)
        else:
            if len(stack) == 0:
                return 0
            last = stack.pop()
            if not isValidPair(last, symbol):
                return 0
     
    if len(stack) != 0:
        return 0
             
    return 1


######################################################################################################




######################################################################################################
Codility ‘MaxSliceSum’ Solution
Posted on January 6, 2015 by Martin
Short Problem Definition:
Find a maximum sum of a compact subsequence of array elements.

Link
MaxSliceSum

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
The only difference to the example given by Codility is the minimal slice length, which is 1.


Solution:
def solution(A):
    max_ending = max_slice = -1000000
    for a in A:
        max_ending = max(a, max_ending +a)
        max_slice = max(max_slice, max_ending)
         
    return max_slice



######################################################################################################
Codility ‘MaxDoubleSliceSum’ Solution
Posted on December 30, 2014 by Martin
Short Problem Definition:
Find the maximal sum of any double slice.
A non-empty zero-indexed array A consisting of N integers is given.

A triplet (X, Y, Z), such that 0 ≤ X < Y < Z < N, is called a double slice.
The sum of double slice (X, Y, Z) is the total of A[X + 1] + A[X + 2] + ... + A[Y − 1] + A[Y + 1] + A[Y + 2] + ... + A[Z − 1].
For example, array A such that:

    A[0] = 3
    A[1] = 2
    A[2] = 6
    A[3] = -1
    A[4] = 4
    A[5] = 5
    A[6] = -1
    A[7] = 2
contains the following example double slices:

double slice (0, 3, 6), sum is 2 + 6 + 4 + 5 = 17,
double slice (0, 3, 7), sum is 2 + 6 + 4 + 5 − 1 = 16,
double slice (3, 4, 5), sum is 0.



Link
MaxDoubleSliceSum

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
To solve this task, you need to keep track of two slice arrays. The optimal double slice can be found at an index that has the maximal sum of those two arrays. It can not be the 0th or the last index.

### Solution:
def solution(A):
    ending_here = [0] * len(A)
    starting_here = [0] * len(A)
     
    for idx in xrange(1, len(A)):
        ending_here[idx] = max(0, ending_here[idx-1] + A[idx])
     
    for idx in reversed(xrange(len(A)-1)):
        starting_here[idx] = max(0, starting_here[idx+1] + A[idx])
     
    max_double_slice = 0
     
    for idx in xrange(1, len(A)-1):
        max_double_slice = max(max_double_slice, starting_here[idx+1] + ending_here[idx-1])
         
         
    return max_double_slice




######################################################################################################
def sieve(N):
    semi = set()
    sieve = [True]* (N+1)
    sieve[0] = sieve[1] = False
 
    i = 2
    while (i*i <= N):
        if sieve[i] == True:
            for j in xrange(i*i, N+1, i):
                sieve[j] = False
        i += 1
 
    i = 2
    while (i*i <= N):
        if sieve[i] == True:
            for j in xrange(i*i, N+1, i):
                if (j % i == 0 and sieve[j/i] == True):
                    semi.add(j)
        i += 1
 
    return semi
 
def solution(N, P, Q):
 
    semi_set = sieve(N)
 
    prefix = []
 
    prefix.append(0) # 0
    prefix.append(0) # 1
    prefix.append(0) # 2
    prefix.append(0) # 3
    prefix.append(1) # 4
 
    for idx in xrange(5, max(Q)+1):
        if idx in semi_set:
            prefix.append(prefix[-1]+1)
        else:
            prefix.append(prefix[-1])
 
    solution = []
 
    for idx in xrange(len(Q)):
        solution.append(prefix[Q[idx]] - prefix[P[idx]-1])
 
    return solution




######################################################################################################
Codility ‘FibFrog’ Solution
Posted on December 28, 2014 by Martin
Short Problem Definition:
Count the minimum number of jumps required for a frog to get to the other side of a river.

The Fibonacci sequence is defined using the following recursive formula:

    F(0) = 0
    F(1) = 1
    F(M) = F(M - 1) + F(M - 2) if M >= 2
A small frog wants to get to the other side of a river. The frog is initially located at one bank of the river (position −1) and wants to get to the other bank (position N). The frog can jump over any distance F(K), where F(K) is the K-th Fibonacci number. Luckily, there are many leaves on the river, and the frog can jump between the leaves, but only in the direction of the bank at position N.

The leaves on the river are represented in a zero-indexed array A consisting of N integers. Consecutive elements of array A represent consecutive positions from 0 to N − 1 on the river. Array A contains only 0s and/or 1s:

0 represents a position without a leaf;
1 represents a position containing a leaf.
The goal is to count the minimum number of jumps in which the frog can get to the other side of the river (from position −1 to position N). The frog can jump between positions −1 and N (the banks of the river) and every position containing a leaf.

For example, consider array A such that:

    A[0] = 0
    A[1] = 0
    A[2] = 0
    A[3] = 1
    A[4] = 1
    A[5] = 0
    A[6] = 1
    A[7] = 0
    A[8] = 0
    A[9] = 0
    A[10] = 0
The frog can make three jumps of length F(5) = 5, F(3) = 2 and F(5) = 5.



Link
FibFrog

Complexity:
expected worst-case time complexity is O(N*log(N))

expected worst-case space complexity is O(N)

Execution:
This problem can be solved by in a Dynamic Programming way. You need to know the optimal count of jumps that can reach a given leaf. You get those by either reaching the leaf from the first shore or by reaching it from another leaf.

The N*log(N) time complexity is given by the fact, that there are approximately log(N) Fibonacci numbers up to N and you visit each position once.

As for the sequence hack: there are 26 Fibonacci numbers smaller than 100k, so I just preallocate an array of this size.

Solution:
def get_fib_seq_up_to_n(N):
    # there are 26 numbers smaller than 100k
    fib = [0] * (27)
    fib[1] = 1
    for i in xrange(2, 27):
        fib[i] = fib[i - 1] + fib[i - 2]
        if fib[i] > N:
            return fib[2:i]
        else:
            last_valid = i
     
     
     
def solution(A):
    # you can always step on the other shore, this simplifies the algorithm
    A.append(1)
 
    fib_set = get_fib_seq_up_to_n(len(A))
     
    # this array will hold the optimal jump count that reaches this index
    reachable = [-1] * (len(A))
     
    # get the leafs that can be reached from the starting shore
    for jump in fib_set:
        if A[jump-1] == 1:
            reachable[jump-1] = 1
     
    # iterate all the positions until you reach the other shore
    for idx in xrange(len(A)):
        # ignore non-leafs and already found paths
        if A[idx] == 0 or reachable[idx] > 0:
            continue
 
        # get the optimal jump count to reach this leaf
        min_idx = -1
        min_value = 100000
        for jump in fib_set:
            previous_idx = idx - jump
            if previous_idx < 0:
                break
            if reachable[previous_idx] > 0 and min_value > reachable[previous_idx]:
                min_value = reachable[previous_idx]
                min_idx = previous_idx
        if min_idx != -1:
            reachable[idx] = min_value +1
 
    return reachable[len(A)-1]




######################################################################################################
Codility ‘AbsDistinct’ Solution
Posted on August 14, 2014 by Martin
Short Problem Definition:
Compute number of distinct absolute values of sorted array elements.

Link
AbsDistinct

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
Additional storage is allowed. Therefore a simple python solution will suffice.

Solution:
def solution(A):
    return len(set([abs(x) for x in A]))




######################################################################################################
Codility ‘TieRopes’ Solution
Posted on August 25, 2014 by Martin
Short Problem Definition:
Tie adjacent ropes to achieve the maximum number of ropes of length >= K.

There are N ropes numbered from 0 to N − 1, whose lengths are given in a zero-indexed array A, lying on the floor in a line. For each I (0 ≤ I < N), the length of rope I on the line is A[I].

We say that two ropes I and I + 1 are adjacent. Two adjacent ropes can be tied together with a knot, and the length of the tied rope is the sum of lengths of both ropes. The resulting new rope can then be tied again.

For a given integer K, the goal is to tie the ropes in such a way that the number of ropes whose length is greater than or equal to K is maximal.

For example, consider K = 4 and array A such that:

    A[0] = 1
    A[1] = 2
    A[2] = 3
    A[3] = 4
    A[4] = 1
    A[5] = 1
    A[6] = 3

We can tie:

rope 1 with rope 2 to produce a rope of length A[1] + A[2] = 5;
rope 4 with rope 5 with rope 6 to produce a rope of length A[4] + A[5] + A[6] = 5.
After that, there will be three ropes whose lengths are greater than or equal to K = 4. It is not possible to produce four such ropes.
For example, given K = 4 and array A such that:

    A[0] = 1
    A[1] = 2
    A[2] = 3
    A[3] = 4
    A[4] = 1
    A[5] = 1
    A[6] = 3
the function should return 3, as explained above.


Link
TieRopes

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
I am a bit skeptical about the correctness of my solution. It gets 100/100 through…

Solution:
def solution(K, A):
    cnt = 0
    current = 0
    for part in A:
        current += part
        if current >= K:
            cnt +=1
            current = 0
 
    return cnt
######################################################################################################



######################################################################################################
Codility ‘Max Nonoverlapping Segments’ Solution
Short Problem Definition:
Find a maximal set of non((-))overlapping segments.


Located on a line are N segments, numbered from 0 to N − 1, whose positions are given in zero-indexed arrays A and B. For each I (0 ≤ I < N) the position of segment I is from A[I] to B[I] (inclusive). The segments are sorted by their ends, which means that B[K] ≤ B[K + 1] for K such that 0 ≤ K < N − 1.

Two segments I and J, such that I ≠ J, are overlapping if they share at least one common point. In other words, A[I] ≤ A[J] ≤ B[I] or A[J] ≤ A[I] ≤ B[J].

We say that the set of segments is non-overlapping if it contains no two overlapping segments. The goal is to find the size of a non-overlapping set containing the maximal number of segments.

For example, consider arrays A, B such that:

    A[0] = 1    B[0] = 5
    A[1] = 3    B[1] = 6
    A[2] = 7    B[2] = 8
    A[3] = 9    B[3] = 9
    A[4] = 9    B[4] = 10
The segments are shown in the figure below.



The size of a non-overlapping set containing a maximal number of segments is 3. For example, possible sets are {0, 2, 3}, {0, 2, 4}, {1, 2, 3} or {1, 2, 4}. There is no non-overlapping set with four segments.

Write a function:

def solution(A, B)

that, given two zero-indexed arrays A and B consisting of N integers, returns the size of a non-overlapping set containing a maximal number of segments.

For example, given arrays A, B shown above, the function should return 3, as explained above.

Assume that:

N is an integer within the range [0..30,000];
each element of arrays A, B is an integer within the range [0..1,000,000,000];
A[I] ≤ B[I], for each I (0 ≤ I < N);
B[K] ≤ B[K + 1], for each K (0 ≤ K < N − 1).
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.


Link
MaxNonoverlappingSegments

Complexity:
expected worst-case time complexity is O(N)

expected worst-case space complexity is O(N)

Execution:
This can be solved by using greedy search. The beginning of the next segment must come strictly after its predecessor.

Solution:
def solution(A, B):
    if len(A) < 1:
        return 0
     
    cnt = 1
    prev_end = B[0]
     
    for idx in xrange(1, len(A)):
        if A[idx] > prev_end:
            cnt += 1
            prev_end = B[idx]
     
    return cnt




######################################################################################################
Codility ‘BinaryGap’ Solution
Posted on August 2, 2014 by Martin
Short Problem Definition:
Find longest sequence of zeros in binary representation of an integer.

Link
BinaryGap

Complexity:
expected worst-case time complexity is O(log(N));

expected worst-case space complexity is O(1)

Execution:
The solution is straight-forward! Use of binary shift.

Solution:
def solution(N):
    cnt = 0
    result = 0
    found_one = False
 
    i = N    
         
    while i:
        if i & 1 == 1:
            if (found_one == False):
                found_one = True
            else:
                result = max(result,cnt)
            cnt = 0
        else:
            cnt += 1
        i >>= 1
    
    return result



######################################################################################################
Short Problem Definition:
Find a symmetry point of a string, if any.

Link
StrSymmetryPoint

Complexity:
expected worst-case time complexity is O(length(S));

expected worst-case space complexity is O(1) (not counting the storage required for input arguments).

Execution:
This problem gave me a lot of headache. It is so trivial I that over-complicated it. I thought that you should find a symmetry point at any possible position, ignoring the residual characters. You would obviously try to maximize the length of this symmetrical sub-array. I was not able to come with any O(S) algorithm for this problem derivation. So just to remind you, this problem is a simple palindrome check. Additionally, you drop all evenly sized strings as their symmetry point is between the indexes.

Solution:
def solution(S):
    l = len(S)
 
    if l % 2 == 0:
        return -1
 
    mid_point = l // 2
 
    for idx in xrange(0, mid_point):
        if S[idx] != S[l - idx - 1]:
            return -1
 
    return mid_point





######################################################################################################
Codility ‘OddOccurrencesInArray’ Solution
Find value that occurs in odd number of elements.

Link
OddOccurrencesInArray

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(1)

Execution:
This problem can be found in many algorithm books. A xor A cancels itself and B xor 0 is B. Therefore A xor A xor B xor C xor C is B.

Solution:
def solution(A):
    missing_int = 0
    for value in A:
        missing_int ^= value
    return missing_int





######################################################################################################
Codility ‘TreeHeight’ Solution
Short Problem Definition:
Compute the height of a binary link-tree.

Link
TreeHeight

Complexity:
expected worst-case time complexity is O(N);

expected worst-case space complexity is O(N)

Execution:
The height of a tree is the maximal height +1 of its subtrees. In this specification a tree with just the root node has a height of 0.

Solution:
'''
class Tree(object):
  x = 0
  l = None
  r = None
'''
 
def getHeight(sub_T):
    if sub_T == None:
        return 0
    return max(getHeight(sub_T.l), getHeight(sub_T.r))+1
 
def solution(T):
    return max(getHeight(T.l), getHeight(T.r))





######################################################################################################
Codility ‘CyclicRotation’ Solution
Posted on January 19, 2016 by Martin
Short Problem Definition:
Rotate an array to the right by a given number of steps.

Link
Cyclic Rotation

Complexity:
expected worst-case time complexity is O(N)

Execution:
There are multiple solutions to this problem. I picked the one that does not create a copy of the array.

Solution:
def reverse(arr, i, j):
    for idx in xrange((j - i + 1) / 2):
        arr[i+idx], arr[j-idx] = arr[j-idx], arr[i+idx]
 
def solution(A, K):
    l = len(A)
    if l == 0:
        return []
         
    K = K%l
     
    reverse(A, l - K, l -1)
    reverse(A, 0, l - K -1)
    reverse(A, 0, l - 1)
 
    return A




######################################################################
def solution(A) :
  n= len(A)
  
  def isequi(k) :
    if k==0  : 
      if 0==sum(A[k+1:]) : return 1
   
    if k== n-1 :
      if sum(A[0:k-1])==0 : return 1
      
    
    if sum(A[:k-1+1]) ==  sum(A[k+1:]) : return 1
    else : return 0

  l1= []
  for k in xrange(0, n) :
     if isequi(k) : 
         l1.append(k)

  if len(l1) ==0 : return -1
  else : return l1[0]
  
  

For example, consider the following array A consisting of N = 8 elements:

  A[0] = -1
  A[1] =  3
  A[2] = -4
  A[3] =  5
  A[4] =  1
  A[5] = -6
  A[6] =  2
  A[7] =  1
P = 1 is an equilibrium index of this array, because:

A[0] = −1 = A[2] + A[3] + A[4] + A[5] + A[6] + A[7]
P = 3 is an equilibrium index of this array, because:

A[0] + A[1] + A[2] = −2 = A[4] + A[5] + A[6] + A[7]
P = 7 is also an equilibrium index, because:

A[0] + A[1] + A[2] + A[3] + A[4] + A[5] + A[6] = 0



Write a function:

def solution(A)

that, given a zero-indexed array A consisting of N integers, returns any of its equilibrium indices. 
The function should return −1 if no equilibrium index exists.


##########################################################################################################





console.log('// PERM MISSING ELEMENT //');

/*
    https://app.codility.com/programmers/lessons/3-time_complexity/perm_missing_elem/

    Find the missing element in a given permutation.

*/

function solution(A) {

    let len = A.length;

    if (len <= 1) return 1;

    let max = len + 1;
    let total = A.reduce((x, y) => x + y);
    let missTotal = total - max;
    let actTotal = (len * (len + 1)) / 2;
    let o = actTotal - missTotal;

    return o;

}

test([2, 3, 1, 5]);
// 4

test([1]);
// 1


function test(...params) {
    console.log('\n(', ...params, ')\n');
    console.log('\n=>', solution(...params), '\n\n');
}
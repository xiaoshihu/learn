// Function is exported so that the test can import it
export function isObject(x) {
  // Use the following patterns (instead of `true`):
  // x === null
  // x !== undefined
  // typeof x === 'number'
  // typeof x !== 'object'
  // x === 3 || x === 4  // logical OR
  // x !== 3 && x !== 4  // logical AND
  // 判断一个东西还是有点麻烦的
  if ((typeof x !== 'object' && typeof x !== 'function') || !x) {
    // console.log(false);
    return false;
  }

  // if (!x){
  //   return false;
  // }

  return true;
}

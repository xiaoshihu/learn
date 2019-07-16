/* npm t exercises/values/instanceof_exrc.mjs
Instructions:
- Run this test (it fails).
- Change the second parameters of assert.equal() so that the test passes
*/

import test from 'ava';
import {strict as assert} from 'assert';

test('instanceof', t => {
  assert.equal('abc' instanceof String,false);
  // 这个鬼东西在使用 typeof 的时候，显示的类型是 object，但是其实这个鬼东西是一个基本类型。
  assert.equal(null instanceof Object, false);
  assert.equal(undefined instanceof Object, false);
  
  assert.equal([true, false] instanceof Array, true);
  assert.equal([true, false] instanceof Object, true);
  assert.equal({} instanceof Object, true);
});

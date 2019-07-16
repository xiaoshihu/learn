/* npm t exercises/values/typeof_exrc.mjs
Instructions:
- Run this test (it fails).
- Change the second parameter of each assert.equal() so that the test passes
*/

import test from 'ava';
import { strict as assert } from 'assert';

test('typeof', t => {
  // 怎么判断是不是 null?
  assert.equal(typeof null, 'object');// object
  assert.equal(typeof undefined, 'undefined');

  assert.equal(typeof 123, 'number');
  assert.equal(typeof 'a', 'string');
  assert.equal(typeof "abc", 'string');

  assert.equal(typeof {}, 'object');
  // 这个 function 本来就是 object 的下面的分类，出来这个东西有点疑惑
  assert.equal(typeof function () { }, 'function');
  // 那怎么判断一个变量是数组？
  assert.equal(typeof [], 'object');
});

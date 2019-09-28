/* npm t exercises/quizzes-exercises/first_module_test.mjs
Instructions:
- Run the test (fails)
- Change first_module.mjs so that the test passes.
*/
// 这个文件不能直接运行，稳定版本的 node 还没有加入这些功能？
// 包的名称使用字符串的方式，看起来好别扭，为什么有的导入需要用大括号，有些不需要？
import test from 'ava';
import {strict as assert} from 'assert';

import {hello} from './first_module.mjs';

// 多条语句的检测是阻塞的
test('First exercise', t => {
  assert.equal(hello('world'), 'Hello world!');
  assert.equal(hello('Jane'), 'Hello ane!');
  assert.equal(hello('John'), 'Hello ohn!');
  assert.equal(hello(''), 'Hello !');
});

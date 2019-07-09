// var a = [];
// // 循环自己是一个父作用域，而循环里面的语句又是一个子作用域，如果在子作用域里面再次定义一个
// // 同名的变量，就会使外面的同名变量不可见 
// for (let i = 0; i < 10; i++) {
//     // 这种嵌套的函数看起来真的是有点不习惯
//   a[i] = function () {
//       i;
//       return 'huge';
//   };
// }
// // a[6](); // 6
// console.log(a[9]());

// let tmp = new Date();

// function f() {
//     let tmp = 'huge';
//     // 好像是变量提升的问题
//     // 我最不喜欢了 any 了。
//     console.error('error information');
// //   if (false) {
// //       var tmp = 'hello world';
// //       console.log('hello world');
// //   }
// }
// // console.log(tmp);
// f(); // undefined

import {strict as assert} from 'assert';
assert.equal(3 + 5, 8);
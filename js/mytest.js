// if (true) { // entering scope of `myVar`, TDZ starts
// // 这个作用域的效果还是和其他的语言不一样，其他的语言是不可能写出这种东西来的，很容易出错，逻辑上就是有问题的
// // 最后的效果应该是这样的，就是需要在执行到这句的时候，这个变量被定义了，但是需要这个代码块里面使用了 let 之类的，使用 var 是不行的
//     const func = () => {
//         console.log(myVar); // executed later
//     };

//     // We are within the TDZ:
//     // Accessing `myVar` causes `ReferenceError`

//     let myVar; // TDZ ends
//     func(); // OK, called outside TDZ
// }
// import test from 'ava';
// import {strict as assert} from 'assert';
// 看起来能在声明调用，是因为，在执行 f() 的时候，g 已经被声明了。

// const f = () => g();


// // We call f() after g() was declared:
// console.log(f());
// const g = () => 123;

// funcDecl();

// const MY_STR = 'abc';
// function funcDecl() {
//     assert.throws(
//         () => MY_STR,
//         ReferenceError);
// }

// 外层函数的变量被内层函数使用，
// 是变量生命周期的问题
// function funcFactory(value) {
//     // 一个局部变量的生命周期延长到了内层函数
//     // 为什么都喜欢搞匿名函数？
//     return () => {
//         return value;
//     };
// }

// // 在这句话运行完毕之后，这个函数应该已经被清理了，但是，后面调用的时候，之前传递的值确传递到了内层函数
// // 变量的生命周期和作用域都变大了，这个才叫做闭包
// const func = funcFactory('abc');
// console.log(func());

// function createInc(startValue) {
//     // 将外层函数的参数记录下来了，在内层函数里面一直在使用，确实有点巧妙，
//     // 并且这个值会在内层函数里面一直被改变，记录之前运算的值，这样就实现了
//     // 自己定义的加法一样
//     // 居然实现了函数里面保存状态，跟无状态函数想比有点意思
//     return (step) => { // (A)
//         startValue += step;
//         return startValue;
//     };
// }
// const inc = createInc(0);
// console.log(inc(3));
// console.log(inc(1));

// const foo = 'a';
// function func() {
//     // 内层函数的定义必须在外层函数的声明块里面
//   return (foo) => {};
// }
// function returnFunc(foo) {
//     return () => { return foo; };
// }
// const result = returnFunc('a')();

// console.log(result);

// function returnFunc(foo) {
//     function func() {
//       return foo;
//     }
//     return func;
//   }
// const result = returnFunc('a')();
// console.log(result);
// let x = 3;
// // x = 4;
// let y = x;
// x = 4;
// // y = 4;
// // 赋值操作是引用吗？
// // y = x;
// // y = 3;
// console.log(y);

// let a = {};

// // 还是有点不习惯这种写法,还是需要好好理解这种表达式的写法
// const fun = (obj)=>{obj.add = 'huge'};

// fun(a);
// console.log(a.add);
// 这种标签函数就是一个特殊的用法，不能用一般的函数去考虑
// function cookedRaw(templateStrings) {
//     return {
//         cooked: [...templateStrings], // copy just the Array elements
//         raw: templateStrings.raw,
//         // ？？？？这个又是什么语法？你不能总搞些和一般情况不一样的语法吧。
//         // sub: substitutions,
//     };
// }
// assert.deepEqual(
//     ,
//     {
//         cooked: ['\tab', '\newline\\'],
//         raw: ['\\tab', '\\newline\\\\'],
//         substitutions: ['subst'],
//     });
// console.log(cookedRaw`\tab${'subst'}\newline\\`);
// class MyError extends Error {
// }
// function func() {
//     throw new MyError('Problem!');
// }

// x = () => func();
// try {
//     x();
// }
// catch (err) {
//     console.log('wrong is ',err)
// }
// function add(x, y) {
//     console.log(x + y);
//     return x + y;
//   }

// const inst = new add(2,3);
// inst();
// import {strict as assert} from 'assert';

// const person = {
//     name: 'Jill',
//     someMethod() {
//         const ordinaryFunc = function () {
//             // 正常函数里面的 this 指的是当前的函数,当前函数又没有 name 这个属性，所以结果是 undefined
//             console.log(this.name);
//         };
//         const arrowFunc = () => {
//             // 箭头函数里面的 this 指的是对象
//             console.log(this.name);
//         };

//         ordinaryFunc();
//         arrowFunc();
//     },
// }

// // person.someMethod();

// function myfunc() {
//     console.log(this.name);
// }

// // myfunc();
// function f({x = 3, y =4}) {
//     return [x, y];
// }

// // 这传递过去根本就是一个对象呀
// // 好多点需要注意，首先是，函数定义的时候，参数列表需要用对象的形式标识，默认值使用 = 指定
// // 在传参的时候，也需要注意，不管怎么样，都需要传递一个对象过去
// const obj = {
//     y:20,
//     method(x) {
//         // assert.equal(this, obj); // implicit parameter
//         // assert.equal(x, 'a');
//         // 这里有点莫名奇妙，使用 this 指向自己是可以理解的，为什么这里能直接使用变量名称来表示自己？
//         console.log(obj === this);
//         console.log(this.y);
//     },
// };

// obj.method('a');

// class Person {
//     constructor(name) {
//         this.name = name;
//     }
//     describe() {
//         return `Person named ${this.name}`;
//     }
//     // 这个是啥东西？
//     static logNames(persons) {
//         for (const person of persons) {
//             console.log(person.name);
//         }
//     }
// }

// class Employee extends Person {
//     constructor(name, title) {
//         super(name);
//         this.title = title;
//     }
//     describe() {
//         return super.describe() +
//             ` (${this.title})`;
//     }
// }

// const jane = new Employee('Jane', 'CTO');
// console.log(jane.describe());
// // jane.logNames;

const arr = [];
arr[3] = 123;
console.log(arr[1]);


#ifndef HEAD_H
#define HEAD_H

#include <iostream>

// 类能够被声明两次？
class MyClass
{
    std::string name;
    int age;

public:
    // 也可以在头文件中定义函数，但是，那样定义的函数是内联函数，总是感觉有点奇怪
    // 声明函数原型
    // 也需要
    MyClass(std::string name,int age);
    void showinf();

    void getinf(std::string hname, int hage);

    // void testfunc();
};
// 要在头文件里面定义成员函数吗，这个可以这样做吗？我觉得是可以的，后面可以试一下

// 还有一点是，类的声明一定要放在头文件，其实就是说，类和函数一样，是一定要声明的吗？而且，这种分开的方式，使类的结构很分散啊，
// 这个应该是构造函数
// MyClass::MyClass()
// {
// }

// // 下面是析构函数
// MyClass::~MyClass()
// {
// }
#endif // !1
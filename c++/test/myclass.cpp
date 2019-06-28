#include "myhead.h"

MyClass::MyClass(std::string name,int age)
{
    (*this).name = name;
    (*this).age = age;
}

// 然后在源文件中定义成员函数
void MyClass::showinf()
{
    std::cout << "name is " << name << ",age is " << age << std::endl;
}

void MyClass::getinf(std::string hname, int hage)
{
    name = hname;
    age = hage;
}

// 不能定义没有声明的函数
// void MyClass::testfunc(){
//     std::cout << "in testfunc" << std::endl;
// }
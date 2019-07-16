// 不导入这样东西，你准备用 std 干啥？本来就是因为需要库里面的东西，我的想法有点奇怪
// 后面内容还是去看另外一本书吧，我不喜欢仅仅只在这里介绍类的一些语法之类的，我喜欢听听为什么这么做
#include <cstring>
#include <iostream>

// 声明类
class StringBad
{
    // 使用指针和长度，就能动态分配内存了
    // 由于可以新声明指针，然后再为指针复制和动态分配内存，所以就实现了动态

    char *str;
    // 这个长度怎么获取？
    int len;
    // 这个静态变量会导致所有的类都公用这个变量，也就是说，会导致在任何类里面的改变，在其他的类里面都是可以见到的
    // 怎么突然之间想到了其他的东西，python 里面的非绑定函数和变量？
    // 写在声明里面要不要紧？
    static int num_strings;

public:
    // 只有静态不可变变量才能在声明里面进行初始化，之前的规律不就说不清楚了吗
    static const int huge = 10;
    StringBad(const char *s);
    // 显示实现复制构造函数
    StringBad(const StringBad &s);
    StringBad();
    ~StringBad();
    // 友元重载运算符函数
    friend std::ostream &operator<<(std::ostream &os, const StringBad &st);
    StringBad &operator=(const StringBad &s);
};

// 需要自己这样来赋值吗？必须自己初始化值
// 需要注意的是，声明的时候并没有使用 static 关键字，并且，还需要使用 命名空间解析符
int StringBad::num_strings = 0;
// 确实，在c++ 里面需要考虑所有的细节

StringBad &StringBad::operator=(const StringBad &s)
{
    // check if is itself
    if (this == &s)
    {
        // const var can't return pointer
        // don't return const var
        return *this;
    }
    else
    {
        // free old new room,because this is inted
        delete[] str;
        // deepcopy
        len = std::strlen(s.str);
        str = new char[len + 1];
        std::strcpy(str, s.str);
        return *this;
    }
}

StringBad::StringBad(const StringBad &s)
{
    // 手动进行深拷贝
    len = std::strlen(s.str);
    str = new char[len + 1];
    std::strcpy(str, s.str);

    num_strings++;
    // 这里会直接打印内容吗
    std::cout << "num is " << num_strings << " ,content is " << str << " creat by copy" << std::endl;
}

StringBad::StringBad(const char *s)
{
    // 获取字符串的长度，注意不会将最后一个 \0 计算进去
    len = std::strlen(s);
    // 这里就实现了动态创建，但是，这个变量需要手动释放
    // 总觉得这样的动态并不是我想象的动态，这样的操作还是有点繁琐的
    // 我好像有点理解动态的含义，动态是将变量储存到动态内存里面，也就是堆里面？
    str = new char[len + 1];
    // 复制两个字符串
    std::strcpy(str, s);
    num_strings++;
    // 这里会直接打印内容吗
    std::cout << "num is " << num_strings << " ,content is " << str << std::endl;
}

StringBad::StringBad()
{
    len = 4;
    // 这种写法还是有点不习惯
    str = new char[len + 1];
    // 下面这个函数的声明式在 cstring 头文件里面声明的
    std::strcpy(str, "C++");
    num_strings++;
    // 这里会直接打印内容吗
    std::cout << "num is " << num_strings << " ,content is " << str << " ,creat by gouzao" << std::endl;
}

// 好像是在程序运行完毕之后才调用析构函数
StringBad::~StringBad()
{
    std::cout << "delete num " << num_strings << ",content is " << str << std::endl;
    --num_strings;
    // 还是第一次使用，根据 new 的时候的类型来释放
    delete[] str;
}

// 将 cout 返回，确实很巧妙，就可以连续使用这个重载的运算符了
std::ostream &operator<<(std::ostream &os, const StringBad &st)
{
    os << st.str;
    return os;
}

void pri(StringBad s);
// void pri(StringBad & s);
// 说实话，代码看起来有点分散,但是，目前还没有看到哪里有什么不妥呀，就是这个计数确实没什么作用

int main(int argc, const char **argv)
{
    // // 在代码块里面运行完毕之后就会调用析构函数
    // {
    //     // 匹配不到构造函数
    //     StringBad mystring;
    // }
    // 调用正常的构造函数
    StringBad mystring("huge");
    pri(mystring);
    // {
    //     // 首先这里进行了默认的构造函数，声明一个类，会自动进行初始化，这个和基本类型的做法是不一样的
    //     StringBad test;
    //     // 首先看这里会不会调用我自己定义的复制构造函数
    //     // 这样调用的时候，并没有调用我定义的复制构造函数，但是，确实进行了浅拷贝
    //     test = mystring;
    //     std::cout << test << std::endl;
    //     // 在代码块运行完毕之后，调用了析构函数，将动态内存释放掉了

    //     /*
    //     应该说这两种做法的构造方式就是不一样的，如果是在初始化的时候，运行复制运算，会调用复制构造函数生成对象
    //     而在已经初始化的情况下，再使用复制运算，应该仅仅是对成员变量（非静态）进行浅拷贝，所以才会出现这个问题

    //     使用在初始化时候的赋值运算符与使用在一般情况下的赋值运算符是不一样的，在这个语言里面的每一行语句里面的每一个符号都是值得考虑的

    //     现在解决的方法就是，自己重载赋值运算符，我的天呀，这设计一个类是真的好累呀。让普通的赋值运算符进行深拷贝，在 python 里面是系统提供了方法
    //     还有一点就是，在 python 里面并没有给你自己操作内存的接口，像指针之类的，所以，不需要自己去释放内存，所以才不会知道这种问题，并且，python
    //     里面的 垃圾回收 机制和这个里面有点不同，主要是计算当前引用的数量，如果引用为0了，就会导致被回收。
    //     */
    // }
    // 调用复制构造函数
    // pri(mystring);
    std::cout << mystring << std::endl;
    // // StringBad mystring2("yuner");
    // // std::cout << mystring2.huge << std::endl;
    // return 0;
    // 调用析构函数
}

// 问题来了，如果现在我传递一个对象，调用哪个函数？我之前还没有考虑到,我是说这个肯定会出问题
// 在传递参数的时候，会自动调用复制构造函数
// void pri(StringBad & s)
// {
//     std::cout << "use quote" << std::endl;
//     // 在这个函数执行完毕之后，会调用这个类的析构函数，导致动态内存被释放掉,好像没有出现这个问题呀？
//     // 只有使用复制操作的时候，才会出现这个问题
//     std::cout << s << std::endl;
//     // 调用析构函数
// }

void pri(StringBad s)
{
    std::cout << "use copy" << std::endl;
    // 在这个函数执行完毕之后，会调用这个类的析构函数，导致动态内存被释放掉,好像没有出现这个问题呀？
    // 只有使用复制操作的时候，才会出现这个问题
    std::cout << s << std::endl;
    // 调用析构函数
}
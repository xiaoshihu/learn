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
    StringBad();
    ~StringBad();
    // 友元重载运算符函数
    friend std::ostream &operator<<(std::ostream &os, const StringBad &st);
};

// 需要自己这样来赋值吗？必须自己初始化值
// 需要注意的是，声明的时候并没有使用 static 关键字，并且，还需要使用 命名空间解析符
int StringBad::num_strings = 0;

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

// 说实话，代码看起来有点分散,但是，目前还没有看到哪里有什么不妥呀，就是这个计数确实没什么作用

int main(int argc, const char **argv)
{
    // 在代码块里面运行完毕之后就会调用析构函数
    {
        // 匹配不到构造函数
        StringBad mystring;
    }
    StringBad mystring("huge");
    std::cout << mystring << std::endl;
    StringBad mystring2("yuner");
    std::cout << mystring2.huge << std::endl;
    return 0;
}
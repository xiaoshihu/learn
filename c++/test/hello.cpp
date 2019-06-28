#include "myhead.h"
#include <cmath>
#include <iostream>

using namespace std;

class Time
{

    int hours;
    int minutes;

public:
    // 构造函数是没有返回值的
    Time(int h = 0, int m = 0);
    void addhr(int h);
    void addmin(int m);
    // 这里不要返回引用，应该生成一个新的对象，就像普通的加法一样
    // 这个加号与名称之间能不能用空格隔开
    Time operator+(const Time &t);
    void show();
    // 声明友元函数
    friend ostream & operator<<(ostream &os, Time &t);
    // 不知道 endl 是个什么东西额
    // friend void operator<<(Time &t, endl &os);
};

// 需要好好的考虑运算的结果，这样才能连续运算
ostream & operator<<(ostream &os, Time &t)
{
    os << t.hours << " and " << t.minutes;
    return os;
}

Time::Time(int h, int m)
{
    hours = h;
    minutes = m;
}

// 这些都是改变了当前对象的数据
void Time::addhr(int h)
{
    hours += h;
}

void Time::addmin(int m)
{
    minutes += m;
}

// 这里是不能返回引用的，因为，sum 是在函数里面定义的局部变量，在函数运行完毕之后会被清除掉
// 需要注意声明原型和实际定义需要一样，理解之后用起来还是差不多的
// 也就是说要改变一个成员函数，需要在两个位置做修改，真的麻烦。
// 这个指针和引用的标志和右边的东西放在一起很容易误解，我不喜欢
// 重载加号，看起来感觉要比 python 里面的内建函数要好理解一些呀
Time Time::operator+(const Time &t)
{
    // 初始化一个对象，有一个疑问，this 指针怎么调用成员函数
    // 在类的范围里面是剋范文私有变量的，这个我之前说实话，没怎么注意到，而且理解也是错误的
    Time sum;
    sum.addhr(hours + t.hours);
    sum.addmin(minutes + t.minutes);
    return sum;
}

void Time::show()
{
    std::cout << "h is " << hours << ",m is " << minutes << std::endl;
}

int main(int argc, const char **argv)
{
    Time time1(1, 1);
    Time time2(2, 2);
    Time time3(3, 3);
    Time sum;
    // sum = time2.addtime(time1);
    sum = time1 + time2 + time3;
    std::cout << sum << endl << "hudshdshds";
    // sum.show();
    // time2.show();
    return 0;
}
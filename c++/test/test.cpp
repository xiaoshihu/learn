#include <cstring>
#include <iostream>

class test1
{
public:
    virtual void hello();
};

class test2 : public test1
{
public:
    virtual void hello();
};

void test1::hello()
{
    std::cout << "class test1" << std::endl;
}

void test2::hello()
{
    std::cout << "class test2" << std::endl;
}

int main(int argc, const char** argv) {
    test1 myclass;
    myclass.hello();
    test2 haha;
    haha.hello();
    return 0;
}
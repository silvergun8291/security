// g++ -o uaf-2 uaf-2.cpp
#include <string>
#include <iostream>
std::string str_func(){
        std::string a = "aaaa";
        return a;
}
void display_string(const char * buf){
        std::cout << buf << std::endl;
}
int main(void) {
    const char *str = str_func().c_str();
    display_string(str);
    std::string b = "bbbb"; //uaf
    display_string(str);  /* Undefined behavior */
}


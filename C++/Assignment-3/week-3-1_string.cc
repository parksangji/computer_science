#include <iostream>

int main() {
    char str1[] = "string";
    char str2[32] = "string";
    char str3[] = {'s','t','r','i','n','g','\0'};
    
    std ::cout << str1 << std:: endl;
    std ::cout << str2 << std:: endl;
    std ::cout << str3 << std:: endl;

    char str4[] = "string";

    str4[3] = '\0';

    std::cout << str4 << std:: endl;
    std::cout << &(str4[4]) << std:: endl;
    std::cout << (str4+4) << std::endl;

    std::string str5 = "string";
    std::cout << str5 << std:: endl;
    std::cout << "length of str5: " << str5.size() << std:: endl;

    std::cout << str5.c_str() << std:: endl;
}
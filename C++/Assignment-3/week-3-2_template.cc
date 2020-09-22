#include <iostream>

template <typename T>

void function (T a){
    std::cout << a<< std:: endl;
}

int main(){
    function<double>(97.3);
    function<int>(97.3);
    function<char>(97.3);

    return 0;
}

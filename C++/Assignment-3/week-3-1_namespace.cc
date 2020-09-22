#include<iostream>

namespace a {
    void function() {
        std::cout << "function in namespace a" << std::endl;
    }
}

namespace b{
    namespace c{
        void function(){
            std::cout << "function in namespace c in namespace b" << std:: endl;
        }
    }
    void function(){
        std::cout << "function in namespace b" << std:: endl;
    }
}

using namespace a;

int main(){
    a::function();
    b::function();
    b::c::function();
    function();
    return 0;
}
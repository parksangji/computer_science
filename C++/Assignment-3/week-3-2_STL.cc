#include <iostream>
#include <string>
#include <list>
#include <vector>


int main(){
    std :: string str = "123";

    std::list<int> list;

    list.push_back(3);
    list.push_back(2);
    list.push_back(1);

    for(int e : list){
        std::cout << e << ",";
    }

    std:: cout << std ::endl;

    std::vector<int> vec; /*다이나믹 배열과 유사하다*/

    vec.push_back(1);
    vec.push_back(2);
    vec.push_back(3);

    for (int i=0; i<3; i++)
    {
        std::cout <<vec[i] << ",";
    }

    std::cout << std:: endl;
}
#include <iostream>

int main(void) {
    int N;
    std::cin >> N;
    int star_num[100];

    for(int i=1; i<=N; i++){
        star_num[i] = i;
    }
    int k= 1;

    while(k<=N)
    {      
        for(int i =1 ; i<=star_num[k]; i++)
        {
            std::cout << "*";
        }
        std::cout << "\n";
        k++;
    }

    return 0;
}
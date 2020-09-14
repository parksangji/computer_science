#include <iostream>

struct student_t{
    int id;
    std::string name;
    std::string phone;
};


int main(){
    int N, M;
    std::cin >> N;

    student_t *student_information = (student_t*)malloc(sizeof(student_t)*N);
    int *student_search_id = (int*)malloc(sizeof(int)*N);
    int *search_id = (int*)malloc(sizeof(int)*N) ;

    for(int i=0; i< N; i++)
    {
        int input_id;
        std::string input_name;
        std::string input_phone;

        std::cin >> input_id;
        std::cin >> input_name;
        std::cin >> input_phone;

        student_information[i].id = input_id;
        student_information[i].name = input_name;
        student_information[i].phone = input_phone;

        student_search_id[i] = input_id;
    }

    std::cin >> M;

    for(int i=0; i<M; i++)
    {
        std::cin >>search_id[i];

    }

    for(int i=0; i<M;i++)
    {
        int k=0;
        for(int j=0; j<N; j++)
        {
            if(search_id[i] == student_information[j].id)
            {
                std::cout << student_information[j].name << ',' << student_information[j].phone << '\n';
                k++;
            }                 
        }
        if(k<=0)
        {
            std::cout << "Unknown" << '\n';
        }
    }


}
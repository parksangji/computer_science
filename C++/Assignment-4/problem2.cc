#include <iostream>

using namespace std;

template <typename T>
struct dynamic_array {
    T* pointer = nullptr;
    size_t cap = 0;

public:
    dynamic_array(size_t cap)
    : cap(cap) {
        this->pointer = new T[cap];
    }

    int array_real_size = 0;

    void push_front(const T& element) {
        // TODO: push_front
        // if array is [2,3] and pop_front(1) called
        // then array should be [1,2,3]

        if(array_real_size == 0)
        {
            pointer[0] = element;
            array_real_size++;
        }
        else
        {
            array_real_size++;
            int* temp_array = new int[array_real_size+1];
            for(int i=0; i<array_real_size; i++)
            {
                temp_array[i+1] = pointer[i];
            }
            temp_array[0] = element;
            for(int i=0; i<array_real_size; i++)
            {
                pointer[i] = temp_array[i];
            }
            delete[] temp_array;
        }
    }
    void push_back(const T& element) {
        // TODO: push_back
        // if array is [1,2] and pop_front(3) called
        // then array should be [1,2,3]
        if(array_real_size == 0)
        {
            push_front(element);
        }
        else
        {
            pointer[array_real_size] = element;
            array_real_size++;
        }
    }
    T pop_front() {
        // TODO: pop front
        // if array is [1,2,3], and pop_front called
        // then array should be [2,3] and return 1

        if(array_real_size == 0)
        {
            cout << "array is empty . so return value is ";
            return 0;
        }
        int return_value = pointer[0];
        int* temp_array = new int[array_real_size+1];
        for(int i = 0; i< array_real_size; i++)
        {
            temp_array[i] = pointer[i+1];
        }
        for(int i = 0; i< array_real_size; i++)
        {
            pointer[i] = temp_array[i];
        }
        array_real_size -= 1;
        pointer[array_real_size] = 0;

        delete[] temp_array;
        
        return return_value;
    
    }
    T pop_back() {
        // TODO: pop back
        // if array is [1,2,3], and pop_front called
        // then array should be [1,2] and return 3
        if(array_real_size== 0)
        {
            cout << "array is empty . so return value is " ;
            return 0;
        }

        array_real_size -= 1;
        int return_value = pointer[array_real_size];
        pointer[array_real_size] = 0;
        return return_value;

    }
    ~dynamic_array() {
        delete[] this->pointer;
    }
};

int main() {
    auto v = dynamic_array<int>(10);
   
    v.push_back(5);
    v.push_front(1);
    v.push_back(3);
    v.push_front(2);
    v.push_back(15);
    v.push_front(7);
    v.push_back(8);
    v.push_front(9);
    v.push_back(10);
    v.push_front(11);
    v.push_back(11);


    cout << v.pop_front() << endl;
    cout << v.pop_front() << endl;
    cout << v.pop_front() << endl;
    cout << v.pop_front() << endl;
    cout << v.pop_front() << endl;
    cout << v.pop_front() << endl;
    cout << v.pop_back() << endl;
    cout << v.pop_back() << endl;
    cout << v.pop_back() << endl;
    cout << v.pop_back() << endl;
    cout << v.pop_back() << endl;
    cout << v.pop_back() << endl;

    v.push_front(11);


    return 0;
}
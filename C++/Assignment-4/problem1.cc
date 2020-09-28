#include <iostream>
#include <cassert>

using namespace std;

int* array;
size_t cap = 0;

void initialize(int cap_) {
    array = new int[cap_];
    cap = cap_;
}
void release() {
    delete[] array;
}

void push_back(int element) {
    // TODO:
    // insert element to back of array
    // if array is [1,2,3], and push_back(4) called,
    // then array should be [1,2,3,4]
    if(cap == 0)
    {
        initialize(1);
        array[cap-1] = element;
    }
    else
    {
        array = (int*) realloc (array, sizeof(int) * (cap + 1));
        array[cap] = element;
        cap += 1;
    }
}

int pop_back() {
    // TODO:
    // return last element of array and remove it from array
    // if array is [1,2,3,4] and pop_back() called,
    // then array should be [1,2,3] and pop_back() return 4.
    if(cap > 0)
    {
        cap -= 1;
        int pop_value = array[cap];
        array = (int*) realloc (array, sizeof(int)*(cap));
        if(cap == 0)
        {
            release();
            return pop_value;
        }
        else
        {
            return pop_value;
        }  
    }
    else
    {
        cout << "array is not exist :(trash value)" ;
    }
    
}

int len() {
// TODO:
// return size of array
    return cap;
}

int main() {

    push_back(3);
    push_back(5);
    push_back(3);
    push_back(2);
    push_back(1);
    push_back(14);
    push_back(6);
    push_back(7);
    
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    push_back(7);
    cout<< pop_back() << endl;
    cout<< pop_back() << endl;
    push_back(7);

    return 0;
}
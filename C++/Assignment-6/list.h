#include <string>
#include <functional>

#include "node.h"

template <typename T>
class List {
public:
    List() : count(0) {
        head = new Node<T>(0, nullptr);
    }
    ~List() {
        // TODO: write your code here
        // release remain nodes before delete head node
        while(head->next != nullptr)
        {
            pop_front();
        }
        delete head;
    }

    void push_front(T value) {
        // TODO: write your code here
        // create new node with value
        // and add node to front of list
        Node<T>* new_node = new Node<T>(value,this->head->next);
        this->head->next = new_node;
        count++;
    }
    void push_back(T value) {
        // TODO: write your code here
        // create new node with value
        // and add node to back of list
        if(count == 0)
        {
            Node<T>* new_node = new Node<T>(value,this->head->next);
            this->head->next = new_node;
            count++;
        }
        else
        {
            Node<T>* new_node = new Node<T>(value,nullptr);
            Node<T>* last_node = this->head;
            while (last_node->next != nullptr)
            {
               last_node = last_node->next;
            }
            last_node->next = new_node; 
            count++;   
        }        

    }
    T pop_front() {
        // TODO: write your code here
        // remove front node(not head)
        // and return its value
        // if try to remove head node return 0
        if(this->head->next == nullptr)
        {
            return 0;
        }
        else
        {
            Node<T>* removed_node;
            removed_node = this->head->next;
            this->head->next = this->head->next->next;
            count--;
            return removed_node->value;
        }
    }
    T pop_back() {
        // TODO: write your code here
        // remove back node(not head)
        // and return its value
        // if try to remove head node return 0
        if(this->head->next == nullptr)
        {
            return 0;
        }
        else
        {
            Node<T>* removed_node;
            Node<T>* prev_removed_node= this->head;
            while (prev_removed_node->next->next != nullptr)
            {
               prev_removed_node = prev_removed_node->next;
            }
            removed_node = prev_removed_node->next;
            prev_removed_node->next = nullptr;
            count--;
            return removed_node->value;
        }    
    }

    size_t size() {
        // TODO: write your code here
        // return current items in list (except head)
        return count;
    }

    void traverse(const std::function<void(const Node<T>&)>& f) {
        for (Node<T>* node = head->next; node != nullptr; node = node->next) {
            f(*node);
        }
    }

private:
    Node<T>* head;
    size_t count;

    void delete_all_node(Node<T>* n)
    {
        if(n->next != nullptr)
        {
            delete_all_node(n->next);
        }
        delete n;
    }
    
    // OPTIONAL: you can write helper functions
};

#include <string>
#include <functional>

#include "double_linked_node.h"

template <typename T>
class List {
public:
    List() : count(0) {
        head = new Node<T>(0, nullptr, nullptr);
        tail = new Node<T>(0, nullptr, nullptr);

        head->next = tail;
        tail->prev = head;
    }
    ~List() {
        // TODO: write your code here
        // release remain nodes before delete head node
        while(head->next != tail)
        {
            pop_front();
        }
        delete head;
        delete tail;
    }

    void push_front(T value) {
        // TODO: write your code here
        // create new node with value
        // and add node to front of list
        Node<T>* new_node = new Node<T>(value, nullptr,nullptr);
        Node<T>* prev_new_node = head;
        Node<T>* next_new_node = head->next;
        next_new_node->prev =  new_node;
        prev_new_node->next = new_node;
        new_node->next = next_new_node;
        new_node->prev = prev_new_node;
        count++;
    }
    void push_back(T value) {
        // TODO: write your code here
        // create new node with value
        // and add node to back of list
        Node<T>* new_node = new Node<T>(value,nullptr,nullptr);
        Node<T>* prev_new_node = tail->prev;
        Node<T>* next_new_node = tail;
        next_new_node->prev = new_node;
        prev_new_node->next = new_node;
        new_node->next = next_new_node;
        new_node->prev = prev_new_node;
        count++;
    }
    T pop_front() {
        // TODO: write your code here
        // remove front node(not head)
        // and return its value
        // if try to remove head node return 0
        if(head->next == tail) return 0;

        Node<T>* delete_node = head->next;
        Node<T>* next_delete_node = delete_node->next;
        head->next = next_delete_node;
        next_delete_node->prev = head;
        count--;
        return delete_node->value;

    }
    T pop_back() {
        // TODO: write your code here
        // remove back node(not head)
        // and return its value
        // if try to remove head node return 0
        if(tail->prev == head) return 0;

        Node<T>* delete_node = tail->prev;
        Node<T>* prev_delete_node = tail->prev->prev;
        prev_delete_node->next = tail;
        tail->prev = prev_delete_node;
        count--;
        return delete_node->value;
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

    void reverse_traverse(const std::function<void(const Node<T>&)>& f) {
        for (Node<T>* node = tail->prev; node != nullptr; node = node->prev) {
            f(*node);
        }
    }

private:
    Node<T>* head;
    Node<T>* tail;
    size_t count;
    // OPTIONAL: you can write helper functions
};
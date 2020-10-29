template <typename T>
class Node {
public:
 Node() {}
 Node(T value) : value(value) {}
 Node(T value, Node* next, Node* prev) : value(value), next(next), prev(prev) {}

    T value;
    Node* next;
    Node* prev;
};
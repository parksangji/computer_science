#include <iostream>
#include <cassert>

#include "contacts.h"

int main() {
    int size = 4;
    auto contacts = contacts_t(size);

    // check add
    assert(contacts.add({0, "name", "phone", "mail"}));

    // check remove
    assert(contacts.remove(0));

    std::cout << "All test pass!" << std::endl;

    return 0;
}

#include <cstdlib>

#include "student.h"

namespace u {
    template <typename T>
    T* allocate(size_t size) {
        return (T *)malloc(sizeof(T) * (size + 1));
    }
}

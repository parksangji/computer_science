#include "contacts.h"

bool contacts_t::add(student_t student) {
    // TODO:
    // create student with given information and add to students
    // return true if add success else false
    // Students with duplicate IDs must not exist.
    size_t index = find_student_index(student.id);

    if(index != -1)
    {
        students[index] = student;
        return true;
    } 

    return false;
}

bool contacts_t::add(int id, std::string name) {
    // TODO:
    // create student with given information and add to students
    // add the given student to the first empty space of students.
    // return true if add success else false
    // Students with duplicate IDs must not exist.
    size_t index = find_student_index(id);

    if(index != -1)
    {
        students[index].id = id;
        students[index].name = name;
        return true;
    }
    

    return false;
}

bool contacts_t::add(int id, std::string name, std::string phone) {
    // TODO:
    // create student with given information and add to students
    // add the given student to the first empty space of students.
    // return true if add success else false
    // Students with duplicate IDs must not exist.
    size_t index = find_student_index(id);

    if(index != -1)
    {
        students[index].id = id;
        students[index].name = name;
        students[index].phone = phone;
        return true;
    }
    

    return false;
}

bool contacts_t::add(int id, std::string name, std::string phone, std::string mail) {
    // TODO:
    // create student with given information and add to students
    // add the given student to the first empty space of students.
    // return true if add success else false
    // Students with duplicate IDs must not exist.

    size_t index = find_student_index(id);

    if(index != -1)
    {
        students[index].id = id;
        students[index].name = name;
        students[index].phone = phone;
        students[index].mail = mail;
        return true;
    }


    return false;
}

bool contacts_t::remove(int id) {
    // TODO:
    // remove student which match given id
    // return true after remove If can't find a student return false

    for(size_t i =0 ; i< m_size ; i++)
    {
        if(students[i].id == id)
        {
            students[i].id = -1;
            return true;
        }
    }

    return false;
}

bool contacts_t::update(int id, std::string name, std::string phone, std::string mail) {
    // TODO:
    // Finds the student with the given ID and 
    // updates the information to the given values.
    // return true after update else false
    size_t index = find_student_index(id);

    if(index != -1)
    {
        students[index].id = id;
        students[index].name = name;
        students[index].phone = phone;
        students[index].mail = mail;
        return true;
    }


    return false;
}

student_t contacts_t::find(int id) {
    // TODO:
    // return student which match given id
    // else, return {};

    size_t index = find_student_index(id);

    if(index != -1)
    {
        return students[index];
    }

    return {};
}

size_t contacts_t::size() {
    // TODO:
    // return find_student_index of students in contacts
    size_t student_find_student_index =0;

    for(size_t i =0 ; i < m_size ; i++){
        if(students[i].id != -1)
        {
            student_find_student_index += 1;
        }
    }
    if (student_find_student_index != 0) return student_find_student_index;

    return 0;
}

size_t contacts_t :: find_student_index(int id)
{
    // find student index find_student_index if exist student id return index find_student_index
    // if not exist student id return -1
    for(size_t i = 0 ; i < m_size; i++)
    {
        if(students[i].id == id)
        {
            return i;
        }
    }
    return -1;
}

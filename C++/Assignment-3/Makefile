main : contacts.o main.o 
	g++ -std=c++11 -o contacts.out contacts.o main.o

contacts.o : contacts.cc
	g++ -std=c++11 -c -o contacts.o contacts.cc

main.o : main.cc
	g++ -std=c++11 -c -o main.o main.cc

clean :
	rm *.o contacts.out

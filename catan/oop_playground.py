class Person:
    def __init__(self, name, age):
        print("Person() constructor called")
        self.name = name
        self.age = age

    def levelup(self):
        self.age += 1

    def demote(self):
        self.age -=1

    def change_name(self, new_name):
        if new_name != self.name:
            self.name = new_name

    def __str__(self):
       return "Name: %s, Age: %d" % (self.name, self.age)

class Parent(Person):
    def __init__(self, name, age, num_kids, is_married=True):
        print("Parent() constructor called")
        super().__init__(name, age)
        self.num_kids = num_kids
        self.is_married = is_married

class Child(Person):
    def __init__(self, name, age, mom, dad):
        print ("Child() constructor called")
        super().__init__(name, age)
        if isinstance(mom, Person):
            self.mom = mom
        else:
            self.mom = "Unknown"
        if isinstance(dad, Person):
            self.dad = dad
        else:
            self.dad = "Unknown"


if __name__ == "__main__":
    person = Person("yi zhong", 28)
    adult = Parent("Mike Zhong", 28, 2, True)
    adult2 = Parent("Beverlie Sopiep", 29, 2, True)
    baby = Child("Adrian Zhong", 2, adult2, adult)

    print(person)
    print(adult)
    print(baby)

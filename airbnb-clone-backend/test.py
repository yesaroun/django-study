class Dog:
    def woof(self):
        print("woof woof")


class Beagle(Dog):
    def jump(self):
        print("jump")

    def woof(self):
        print("no")


beagle = Beagle()
beagle.woof()

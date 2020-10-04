from random import randint, uniform
from tkinter import *
from math import sqrt

class Ant :
    species = "Formica rufa"
    def __init__(self, size):
        self._x, self._y = randint(0, size), randint(0, size)
        self._food, self._age = 0, 0
        self._infected, self._alive, self._birth = False, True, False
    
    def move(self, speed, size):
        self._x += randint(0, speed) - speed 
        self._y += randint(0, speed) - speed
        self._x %= size
        self._y %= size

    def recover(self, recovery_rate):
        if self._infected and randint(0, 100) > recovery_rate:
            self.infected = False

    def update(self, speed, recovery_rate, size):
        self._birth = False
        self.recover(recovery_rate)
        self.move(speed, size)
        self._age += 1

    def deathRoll(self) : 
        if self.infected and randint(0,20) < self._age : 
            self._alive = False

    def birthRoll(self) : 
        if uniform(0,1) > 0.8 : 
            self._birth = True
            

    @property 
    def x(self) : return self._x
    @property 
    def y(self) : return self._y
    @property 
    def infected(self) : return self._infected
    @infected.setter
    def infected(self, value) : self._infected = value
    @property 
    def alive(self) : return self._alive
    @property 
    def birth(self) : return self._birth


class World :  
    def __init__(self, size, population):
        self._members = []
        self._size = size
        for i in range(population):
            self._members.append(Ant(self._size))

    def run(self, speed, recovery_rate):
        tempMembers = []
        for member in self._members:
            member.update(speed, recovery_rate, self._size)
            # check positions of members prior to test for collision. If positive, run collision on both parties.
            for prevMember in tempMembers : 
                if [prevMember.x, prevMember.y] == [member.x, member.y] : 
                    self.collision(prevMember, member)
            tempMembers.append(member)
            if not member.alive : 
                self._members.remove(member)
                tempMembers.remove(member)
            elif member.birth : 
                self._members.append(Ant(self._size))
        self.print_world()
    
    def print_world(self):
        for member in self._members:
            print(member.x, member.y, member.infected)

    def collision(self, e1, e2) : 
        e1.infected, e2.infected = True, True

    @property 
    def members(self) : return self._members

class App(Tk) : 
    def __init__(self, size, master = None) : 
        super().__init__()
        self.master = master
        self.canvas = Canvas(self.master, width = size, height = size)

    def renderScene(self) : 
        self.canvas.delete("all")
        for member in this_world.members : 
            self.renderAnt(member)
        self.canvas.pack()


    def renderAnt(self, ant) : 
        self.canvas.create_oval(ant.x-3, ant.y-3, ant.x+3, ant.y+3,outline='green',activeoutline='red',fill='green',activefill='red')

if __name__ == "__main__" :
    size = 250
    population = 10 
    app = App(size)
    this_world = World(size, population)
    while True:
        this_world.run(5, 50)
        app.renderScene()
        app.update()
        if input("[Q] to Quit: ").lower() == 'q':
            break
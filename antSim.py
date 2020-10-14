from random import randint, uniform
from tkinter import *
from math import sqrt

class Ant :
    species = "Formica rufa"
    def __init__(self, size):
        self._x, self._y = randint(0, size), randint(0, size)
        self._food, self._age = 0, 0
        self._infected, self._alive, self._birth = False, True, False
        self._colour = 'green2'
        self._history = [[] for i in range(3)]
        self._birthCD = 0

    def update(self, speed, recovery_rate, size):
        self._birth = False
        if self._birthCD : 
            self._birthCD -= 1
        self._birthRoll()
        self._deathRoll()
        self._infectionRoll()
        self._recover(recovery_rate)
        self._updateHistory(self._x, self._y)
        self._move(speed, size)
        self._age += 1
        if self._infected : 
            self._colour = 'green4'

    def _deathRoll(self) : 
        if self.infected and randint(0,20) < self._age : 
            self._alive = False

    def _birthRoll(self) : 
        if uniform(0,1) > 0.9 and not self._birthCD : 
            self._birth = True
            self._birthCD = 5

    def _infectionRoll(self) : 
        if uniform(0,1) > 0.95 or self._age >= 10 : 
            self._infected = True

    def _updateHistory(self, x, y) : 
        self._history[-1] = [x,y]
        for i in range(len(self._history)-1) : 
            self._history[i] = self._history[i+1]

    def _move(self, speed, size):
        self._x += randint(0, speed) - speed 
        self._y += randint(0, speed) - speed
        self._x %= size
        self._y %= size

    def _recover(self, recovery_rate):
        if self._infected and randint(0, 100) > recovery_rate:
            self.infected = False

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
    @property 
    def history(self) : return self._history
    @property 
    def colour(self) : return self._colour
    @property
    def birthCD(self) : return self._birthCD

class Queen(Ant) : 
    def __init__(self, size) : 
        super().__init__(size)
        self.colour = 'gold4'       

    def reproduce(self) : 
        pass

class Worker(Ant) : 
    def __init__(self, size) : 
        super().__init__(size)
        self.colour = 'blue'

    def deathRoll(self) : 
        # The chance of dying as a worker should be higher 
        if self.infected and randint(0,10) < self._age : 
            self._alive = False


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
            print(f"X: {member.x} Y: {member.y} Infected: {member.infected} Giving birth: {member.birth} Birth cooldown: {member.birthCD}")

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
        for value in ant.history : 
            try : 
                self.canvas.create_oval(value[0]-3, value[1]-3, value[0]+3, value[1]+3, outline='gray', activeoutline='black', fill='gray', activefill='black')
            except : 
                pass
        self.canvas.create_oval(ant.x-3, ant.y-3, ant.x+3, ant.y+3, outline=ant.colour, activeoutline='red', fill=ant.colour, activefill='red')

if __name__ == "__main__" :
    size = 800
    population = 10 
    app = App(size)
    this_world = World(size, population)
    while True:
        this_world.run(5, 50)
        app.renderScene()
        app.update()
        if input("[Q] to Quit: ").lower() == 'q':
            break
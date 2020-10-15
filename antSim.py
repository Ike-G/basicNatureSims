from random import randint, uniform
from tkinter import *
from math import sqrt
import asyncio

class Ant :
    species = "Formica rufa"
    def __init__(self, size):
        self._x, self._y = randint(0, size), randint(0, size)
        self._food, self._age = 0, 0
        self._infected, self._alive, self._birth = False, True, 0
        self._colour = 'green2'
        self._history = [[] for i in range(3)]
        self._birthCD, self._recoveryCD = 0, 0
        self._radius = 3

    def update(self, speed, recoveryRate, size):
        self._birth = 0
        if self._birthCD : 
            self._birthCD -= 1
        self._birthRoll()
        self._deathRoll()
        self._infectionRoll()
        self._recover(recoveryRate)
        self._updateHistory(self._x, self._y)
        self._move(speed, size)
        self._age += 1
        if self._infected : 
            self._colour = 'green4'
    
    def _updateHistory(self, x, y) : 
        self._history[-1] = [x,y]
        for i in range(len(self._history)-1) : 
            self._history[i] = self._history[i+1]
    
    def _deathRoll(self) : 
        pass

    def _birthRoll(self) : 
        pass

    def _infectionRoll(self) : 
        if uniform(0,1) > 0.95 or self._age >= 10 : 
            self._infected = True
            self._recoveryCD = 1000

    def _recover(self, recoveryRate):
            self._recoveryCD = max(self._recoveryCD - recoveryRate, 0)
            if self._infected and randint(0, 100) > recoveryRate:
                self.infected = False
    
    def _move(self, speed, size):
        self._x += randint(-(speed), speed)
        self._y += randint(-(speed), speed)
        self._x %= size
        self._y %= size

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
    @property 
    def radius(self) : return self._radius

class Queen(Ant) : 
    def __init__(self, size) : 
        super().__init__(size)
        self._colour = 'gold2'   
        self._radius = 6    

    def _move(self, speed, size) : 
        self._x += randint(-(speed//3), speed//3)
        self._y += randint(-(speed//3), speed//3)
        self._x %= size
        self._y %= size

    def _birthRoll(self) : 
        roll = randint(1,10)
        if self._age >= 5 and roll > 5 : 
            self._birth = roll-5
    
    def _deathRoll(self) : 
        if self._age >= 20 and uniform(0,1) > 0.9 and self._infected : 
            self._alive = False

class Drone(Ant) : 
    # Primary job is reproduction
    # Base movement
    # Dispensible (Low lifespan, high infection rate)
    def __init__(self, size) : 
        super().__init__(size) 
        self._colour = 'magenta3'
    
    def _deathRoll(self) : 
        if (self.infected and randint(5,15) < self._age) or randint(0,40) < self._age : 
            self._alive = False

    def _birthRoll(self) : 
        if uniform(0,1) > 0.9 and not self._birthCD : 
            self._birth = 1
            self._birthCD = 5

class Worker(Ant) : 
    def __init__(self, size) : 
        super().__init__(size)
        self._colour = 'blue'

    def _deathRoll(self) : 
        # The chance of dying as a worker should be higher 
        if self.infected and randint(5,15) < self._age : 
            self._alive = False

    def _move(self, speed, size) : 
        self._x += randint(-(2*speed), 2*speed)
        self._y += randint(-(2*speed), 2*speed)
        self._x %= size
        self._y %= size



class World :  
    def __init__(self, size, population):
        self._members = []
        self._size = size
        self._roles = [Queen, Worker, Drone]
        self._queenPresent = False
        # 0.04 chance of rolling Queen, 0.36 chance of rolling Worker, 0.60 chance of rolling Drone
        self.selectRole = lambda : self._roles[min(min(randint(0,19),1)*16,randint(13,20))//8]
        for i in range(population):
            self._members.append(self.selectRole()(self._size))
            if type(self._members[0]) == Queen : 
                self._queenPresent = True
        
    def run(self, speed, recoveryRate):
        tempMembers = []
        self._queenPresent = False
        for member in self._members:
            member.update(speed, recoveryRate, self._size)
            if type(member) == Queen : 
                self._queenPresent = True
            # check positions of members prior to test for collision. If positive, run collision on both parties.
            for prevMember in tempMembers : 
                if [prevMember.x, prevMember.y] == [member.x, member.y] : 
                    prevMember.infected, member.infected = True, True
            tempMembers.append(member)
            if not member.alive : 
                self._members.remove(member)
                tempMembers.remove(member)
            elif self._queenPresent : 
                self._members.extend([self.selectRole()(self._size) for i in range(member.birth)])
        self.printWorld()
    
    def printWorld(self):
        for member in self._members:
            print(f"X: {member.x} Y: {member.y} Infected: {member.infected} Giving birth: {bool(member.birth)} Birth cooldown: {member.birthCD}")
        print(f"Members: {len(self._members)}")

    @property 
    def members(self) : return self._members

class App(Tk) : 
    def __init__(self, size, master = None) : 
        super().__init__()
        self.master = master
        self.canvas = Canvas(self.master, width = size, height = size)

    def renderScene(self) : 
        self.canvas.delete("all")
        for member in thisWorld.members : 
            self.renderAnt(member)
        self.canvas.pack()

    def renderAnt(self, ant) : 
        for value in ant.history : 
            try : 
                self.canvas.create_oval(value[0]-3, value[1]-3, value[0]+3, value[1]+3, outline='gray', activeoutline=ant.colour, fill='gray', activefill=ant.colour)
            except : 
                pass
        self.canvas.create_oval(ant.x-ant.radius, ant.y-ant.radius, ant.x+ant.radius, ant.y+ant.radius, outline=ant.colour, fill=ant.colour)

def main(speed, recoveryRate) : 
    while True : 
        app.renderScene()
        thisWorld.run(speed, recoveryRate)
        app.update()
        request = input("[Q] to Quit: ")
        if request.lower() == 'q' : 
            break

if __name__ == "__main__" :
    app = App(800)
    thisWorld = World(800, 10)
    main(5,50)


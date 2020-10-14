from random import randint

class Crop : 
    def __init__(self, growthRate, lightReq, waterReq) : 
        self._growthRate = growthRate
        self._lightReq = lightReq
        self._waterReq = waterReq 
        self._growth = 0
        self._daysGrowing = 0
        self._stat = 'Seed'
        self._form = 'Generic'
    
    @property
    def needs(self) : 
        return {'lightReq' : self._lightReq, 'waterReq' : self._waterReq}
    
    @property 
    def report(self) : 
        return {'type': self._form, 'stat': self._stat, 'growth': self._growth, 'daysGrowing': self._daysGrowing}

    def grow(self, light, water) : 
            if self._lightReq <= light and self._waterReq <= water : 
                self._growth += self._growthRate
            self._daysGrowing += 1
            self._updateStat()
    
    def autoGrow(self, days) : 
        for i in range(days) : 
            self.grow(randint(1,10), randint(1,10))

    def _updateStat(self) : 
        labels = ['Seed','Seedling','Young','Mature','Old']
        for i in range(5) : 
            if self._growth <= i*5 : 
                self._stat = labels[i]
                break 


if __name__ == '__main__' : 
    newCrop = Crop(1,3,4)
    newCrop.grow(5,7)
    print(newCrop.report)
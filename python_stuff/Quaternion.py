def getPrimeDividers(number):
    result = []
    i = 2
    while i*i <= number:
        if number%i == 0: result.append(i)
        number /= i
    if number > 1: result.append(number)
    return result

def intersectionList(list1, list2): 
   return set(list1).intersection(list2)

class Quaternion:
    dimentionNames = ["","i","j","k"]
    #initializer
    def __init__(self,defString) -> None:
        dims = defString.split(";")
        if len(dims)>4: return "Too much dimensions"
        for i in range(0,len(dims)):
            dim = dims[i].split(",")
            if type(dim) == list:
                if len(dim) == 2:
                   dims[i] = []
                   dims[i].append(int(dim[0]))
                   dims[i].append(int(dim[1]))
                   continue
            return "Wrong dimensions"
        self.dims = dims
        while len(self.dims) < 4:
            self.dims.append([0,1])
        self.__simplify()

    #interaface functiions
    def print(self):
        resultStringList = []
        for i in range(0,len(self.dims)):
            if self.dims[i][0] == 1:
                continue
            dimList = []
            dimList.append(str(self.dims[i][0]))
            if self.dims[i][1]!= 1:
                dimList.append("/")
                dimList.append(str(self.dims[i][1]))
            dimList.append(self.dimentionNames[i])
            dimStr = "".join(dimList)
            resultStringList.append(dimStr)
        resultString = "+".join(resultStringList)
        print(resultString)

    #operators
    def __add__(self,other):
        for i in range(len(other.dims)):
            if self.dims[i][1] == other.dims[i][1]:
                self.dims[i][0]+=other.dims[i][0]
                continue
            self.dims[i][0] = int(other.dims[i][0]*self.dims[i][1] + other.dims[i][1]*self.dims[i][0] ) 
            self.dims[i][1] *= other.dims[i][1] 
            self.dims[i][1] = int(self.dims[i][1])
        self.__simplify()
        return self
    
    def __sub__(self,other):
        for i in range(len(other.dims)):
            if self.dims[i][1] == other.dims[i][1]:
                self.dims[i][0]-=other.dims[i][0]
                continue
            self.dims[i][0] = int(other.dims[i][1]*self.dims[i][0] - other.dims[i][0]*self.dims[i][1]) 
            self.dims[i][1] *= other.dims[i][1] 
            self.dims[i][1] = int(self.dims[i][1])
        self.__simplify()
        return self
    
    # private functions    
    def __simplify(self):
        for i in range(0,len(self.dims)):
            numeratorDividers = getPrimeDividers(self.dims[i][0])
            denominatorDividers = getPrimeDividers(self.dims[i][1])
            commonDividers = intersectionList(numeratorDividers,denominatorDividers)
            if len(commonDividers) == 0:
                return
            for divider in commonDividers:
                self.dims[i][0]/=divider
                self.dims[i][0] = int(self.dims[i][0])
                self.dims[i][1]/=divider 
                self.dims[i][1] = int(self.dims[i][1])
        self.__simplify() 


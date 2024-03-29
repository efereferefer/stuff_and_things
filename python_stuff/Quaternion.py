from math import sqrt

class Quaternion:
    __dimentionNames = ["","i","j","k"]
    __mulNegativesTable = [[1,1,1,1],[1,-1,1,-1],[1,-1,-1,1],[1,1,-1,-1]]
    __indList = [0,1,2,3,2,1,0]

    #initializer
    def __init__(self,defString, temporary = False) -> None:
        if type(defString) == list: defString = Quaternion.__dimsToString(defString)
        dims = defString.split(";")
        if len(dims)>4: print("Too much dimensions")
        for i in range(0,len(dims)):
            dim = dims[i].split(",")
            if type(dim) == list:
                if len(dim) == 2:
                   dims[i] = []
                   dims[i].append(int(dim[0]))
                   dims[i].append(int(dim[1]))
                   continue
            dims[i]=[0,1]
        self.dims = dims
        while len(self.dims) < 4:
            self.dims.append([0,1])
        self.__simplify()
        if not temporary:
            self.__string = self.__getString()
            self.__len = 0
            for dim in self.dims:
                self.__len += float(dim[0]/dim[1])*float(dim[0]/dim[1])

    #interaface functiions
    def len(self):
        return self.__len

    def print(self):
        print(self.__string)

    def getConjoined(self):
        return self.conjoined().__getString()
    
    def getConjoinedMult(self):
        return (self*self.conjoined())
    
    def conjoined(self):
        result = -self
        result.dims[0][0] *=-1
        return result

    def conjoinedMult(self):
        return self.__conjoinedMult

    #operators
    #math dual
    def __add__(self,other):
        result = [[0,1],[0,1],[0,1],[0,1]]
        for i in range(len(other.dims)):
            if self.dims[i][1] == other.dims[i][1]:
                result[i][0]= int(self.dims[i][0]+ other.dims[i][0])
                result[i][1] = int(self.dims[i][1])
                continue
            result[i][0] = int(other.dims[i][0]*self.dims[i][1] + other.dims[i][1]*self.dims[i][0] ) 
            result[i][1] = int(self.dims[i][1] * other.dims[i][1])
        return Quaternion(result)
    
    def __sub__(self,other):
        result = [[0,1],[0,1],[0,1],[0,1]]
        for i in range(len(other.dims)):
            if self.dims[i][1] == other.dims[i][1]:
                result[i][0]= int(self.dims[i][0]- other.dims[i][0])
                result[i][1] = int(self.dims[i][1])
                continue
            result[i][0] = int(other.dims[i][1]*self.dims[i][0] - other.dims[i][0]*self.dims[i][1])  
            result[i][1] = int(self.dims[i][1] * other.dims[i][1])
        return Quaternion(result)
    
    def __mul__(self,other):
        result = Quaternion("")
        for i in range(len(self.dims)):
            for j in range(len(other.dims)):
                result+=Quaternion.__getSingleMult(self.dims[i],other.dims[j],i,j)
        return result

    def __truediv__(self,other):
        return Quaternion([[x[0]*other.conjoinedMult()[1],x[1]*other.conjoinedMult()[0]] for x in (self*other.conjoined()).dims])

    #logical
    def __eq__(self, other) -> bool:
        return self.dims == other.dims
    
    #single
    def __neg__(self):
        return Quaternion([[-x[0],x[1]] for x in self.dims])

    #dynamic typisation
    def __str__(self) -> str:
        return self.__string

    def __bool__(self)-> bool:
        return self.__len != 0
    
    #other
    def __repr__(self) -> str:
        return self.__string

    # private methods    

    def __getString(self):
        resultStringList = []
        for i in range(0,len(self.dims)):
            if self.dims[i][0] == 0: continue
            dimList = []
            if self.dims[i][0] < -1 or self.dims[i][0] > 1 or i > 0:
                dimList.append(str(self.dims[i][0]))
            if self.dims[i][1]!= 1:
                dimList.append("/")
                dimList.append(str(self.dims[i][1]))
            dimList.append(self.__dimentionNames[i])
            dimStr = "".join(dimList)
            resultStringList.append(dimStr)
        resultString = "+".join(resultStringList).replace("+-","-")
        if resultString == "": resultString = "0"
        return resultString
    
    def __simplify(self):
        allDividers = 0
        for i in range(0,len(self.dims)):
            if self.dims[i][0] == self.dims[i][1]:
                self.dims[i][0] = 1
                self.dims[i][1] = 1 
                continue
            if self.dims[i][0]%self.dims[i][1] == 0:
                self.dims[i][0] = int(self.dims[i][0]//self.dims[i][1])
                self.dims[i][1] = 1 
                continue
            if self.dims[i][0] < 0 and self.dims[i][1] < 0:
                self.dims[i][0] *= -1
                self.dims[i][1] *= -1 
            numeratorDividers = Quaternion.__getPrimeDividers(self.dims[i][0])
            denominatorDividers = Quaternion.__getPrimeDividers(self.dims[i][1])
            commonDividers = set(numeratorDividers).intersection(denominatorDividers)
            allDividers += len(commonDividers)
            if len(commonDividers) == 0:
                continue
            for divider in commonDividers:
                self.dims[i][0]/=divider
                self.dims[i][0] = int(self.dims[i][0])
                self.dims[i][1]/=divider 
                self.dims[i][1] = int(self.dims[i][1])
        if allDividers == 0: return
        self.__simplify() 
    
    #static methods

    @staticmethod 
    def __getSingleMult(num1,num2,ind1,ind2):
        result = [[0,1],[0,1],[0,1],[0,1]]
        resultIndex = 0
        indSum = abs(ind1+ind2)
        if indSum<=3: resultIndex = Quaternion.__indList[indSum]
        if indSum>3: resultIndex =  Quaternion.__indList[-indSum]
        if ind1==ind2: resultIndex = 0
        neg = Quaternion.__mulNegativesTable[ind2][ind1]
        result[resultIndex] = [neg*(num1[0]*num2[0]),num1[1]*num2[1]]
        return Quaternion(result,True)

    @staticmethod 
    def __dimsToString(dims):
        return ";".join([",".join(list(map(str,t))) for t in dims])
    
    @staticmethod
    def __getPrimeDividers(number):
        result = []
        i = 2
        while i*i <= number:
            if number%i == 0: result.append(i)
            number /= i
        if number > 1: result.append(number)
        return result
    




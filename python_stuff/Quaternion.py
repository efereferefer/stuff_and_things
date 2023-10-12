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
    __dimentionNames = ["","i","j","k"]
    __mulNegativesTable = [[1,1,1,1],[1,-1,1,-1],[1,-1,-1,1],[1,1,-1,-1]]
    __indList = [0,1,2,3,2,1,0]

    #initializer
    def __init__(self,defString) -> None:
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

    #interaface functiions
    def print(self):
        resultStringList = []
        for i in range(0,len(self.dims)):
            if self.dims[i][0] == 0:
                continue
            dimList = []
            dimList.append(str(self.dims[i][0]))
            if self.dims[i][1]!= 1:
                dimList.append("/")
                dimList.append(str(self.dims[i][1]))
            dimList.append(self.__dimentionNames[i])
            dimStr = "".join(dimList)
            resultStringList.append(dimStr)
        resultString = "+".join(resultStringList).replace("+-","-")
        
        print(resultString)

    #operators
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

    # private functions    
    def __getSingleMult(num1,num2,ind1,ind2):
        result = [[0,1],[0,1],[0,1],[0,1]]
        resultIndex = 0
        indSum = abs(ind1+ind2)
        if indSum<=3: resultIndex = Quaternion.__indList[indSum]
        if indSum>3: resultIndex =  Quaternion.__indList[-indSum]
        neg = Quaternion.__mulNegativesTable[ind2][ind1]
        result[resultIndex] = [neg*(num1[0]*num2[0]),num1[1]*num2[1]]
        return Quaternion(result)

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

    def __dimsToString(dims):
        return ";".join([",".join(list(map(str,t))) for t in dims])


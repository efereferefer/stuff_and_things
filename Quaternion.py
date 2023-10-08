def getPrimeDividers(number):
    result = list
    i = 2
    while i*i < number:
        if number%i == 0: result.append(i)
        number /= i
    if number > 1: result.append(number)
    return number

def intersectionList(list1, list2): 
   return set(list1).intersection(list2)

class Quternion:
    dimentionNames = ["","i","j","k"]
    def __init__(self,defString) -> None:
        dims = defString.split(";")
        if len(dims)>4: return "Too much dimensions"
        for dim in dims:
            dim = dim.split(",")
            if type(dim) == list:
                if len(dim) == 2:
                   continue
            return "Wrong dimensions"
        self.dims = dims
        self.simplify()

    def print(self):
        resultStringList = list
        for dim in self.dims:
            dimList = list
            dimList.append(self.dimentionNames[self.dims.index(dim)])
            dimList.append(str(dim[0]))
            dimList.append("/")
            dimList.append(str(dim[1]))
            dimStr = "".join(dimList)
            resultStringList.append(dimStr)
        resultString = "+".join(resultStringList)
        print(resultString)
        
    def simplify(self):
        for dim in self.dims:
            numeratorDividers = getPrimeDividers(dim[0])
            denominatorDividers = getPrimeDividers(dim[1])
            commonDividers = intersectionList(numeratorDividers,denominatorDividers)
            for divider in commonDividers:
                dim[0]/=divider
                dim[1]/=divider 



from PIL import Image
from pylab import array
import numpy as np
#import matplotlib.pyplot as plt

sizeW = 8
sizeH = 10
sizeMatrix = sizeH * sizeW
Neurons = 5
numPatterns = 4
Rate = 0.5

def getImageArray(Path):
    matrix = [0.0 for _ in range(sizeMatrix)]
    binaryArray = np.array(Image.open(Path).convert('L'))
    for i in range(sizeH):
        for j in range(sizeW):
            matrix[(i * sizeW)+ j] = 1 if (binaryArray[i][j] == 255) else 0
    return matrix

def funActivation(u):
    if(u<=0):
        return 0
    else:
        return 1


#Inicializamos la matriz de pesos en 0.0
class Knowledge(object):
    listW = None
    wBias = 0
    def __init__(self):
        self.listW = [0.0 for i in range(sizeW * sizeH)]
    def show(self, t = ""):
        print(t)
        print(self.listW)

class Pattern(object):
    matrix = None
    stringPattern = ""
    Bias = None
    #Inicializa una matriz de patrones en 0.0
    def __init__(self):
        self.Bias = 1
        self.matrix = [0.0 for _ in range(sizeW * sizeH)]

    def getPattern(self, Path):
        filePath = open(Path, "r")
        self.imgPattern = filePath.read()
        filePath.close()
        index = 0
        for i in range(len(self.imgPattern)):
            if(self.imgPattern[i] != '\n'):
                self.matrix[index] = float(self.imgPattern[i])
                index += 1

    def getImg(self, Path):
        binaryArray = np.array(Image.open(Path).convert('L'))
        for i in range(sizeH):
            for j in range(sizeW):
                self.matrix[(i * sizeW)+ j] = 1 if (binaryArray[i][j] > 0) else 0

    def showPattern(self):
        print(self.imgPattern)

    def showVector(self):
        print(self.matrix)

class Digit(object):
    numberPattern = None
    wPattern = None
    wishValue = None
    remainder = None
    def __init__(self):
        self.numberPattern = [Pattern() for _ in range(numPatterns)]
        self.wPattern = [Knowledge() for _ in range(Neurons)]
        #Crea una matriz de pesos por cada neurona.

    def setDigit(self, Path, Y):
        self.wishValue = Y
        for i in range(numPatterns):
            self.numberPattern[i].getPattern(Path + "pat" + str(i + 1) + ".txt")

    def ModifyW(self, index, patternW):
        #for k in range(numPatterns):
        for i in range(sizeMatrix):
            #Regla de error
            patternW.listW[i] += (Rate * self.remainder * self.numberPattern[index].matrix[i])
        patternW.wBias += (Rate * self.remainder * self.numberPattern[index].Bias)

    def Train(self, neuronIndex, patternW):
        for i in range(numPatterns):
            SumW = float(0)
            for j in range(sizeMatrix):
                #Sumatoria
                SumW += self.numberPattern[i].matrix[j] * patternW.listW[j]
            SumW += self.numberPattern[i].Bias * patternW.wBias
            #Bias
            self.remainder = self.wishValue[neuronIndex] - funActivation(SumW)
            if(self.remainder != 0):
                self.ModifyW(i, patternW)
                return True
            else: return False #Si ya no debe seguir entrenando
            
class Perceptron(object):
    wPattern = None
    wishValues = None
    numLearn = None
    Number = None
    def __init__(self):
        self.numLearn = Neurons
        self.Number = [Digit() for _ in range(self.numLearn)]
        self.wPattern = [Knowledge() for _ in range(Neurons)]
        self.wishValues = [[(1 if(i == j) else 0 )for j in range(self.numLearn)]for i in range(self.numLearn)]
        self.initDigits()
        self.TrainStage()

    def initDigits(self):
        for i in range(self.numLearn):
            self.Number[i].setDigit("Patterns/num_" + str(i) + "/", self.wishValues[i])

    def TrainStage(self):
        for _ in range(20):
            for n in range(Neurons):
                for i in range(self.numLearn):
                    self.Number[i].Train(n, self.wPattern[n])
                
    def showPatterns(self):
        for i in range(self.numLearn):
            print(" Number ", i)
            for j in range(numPatterns):
                print(" - Pattern ", j)
                self.Number[i].numberPattern[j].showPattern()

    def showWeights(self):
        for i in range(Neurons):
            print(self.wPattern[i].listW)

    def showY(self):
        print("Valor Deseado \n")
        for i in range(self.numLearn):
            print(" Numero ", i, " -> ", self.wishValues[i])
        print("")

    def TestFromImg(self, Path):
        temp = Pattern()
        temp.getImg(Path)
        result = [float()] * Neurons

        for i in range(Neurons):
            SumW = 0
            for j in range(sizeMatrix):
                SumW += temp.matrix[j] * self.wPattern[i].listW[j]
            SumW += temp.Bias * self.wPattern[i].wBias
            result[i] = (funActivation(SumW))
        
        #self.showY()
        print("  Answer   -> ", result, "\n")
        flag = True
        for i in range(self.numLearn):
            if(self.wishValues[i] == result):
                print(" Number is ", i)
                flag  = False
                break
        if(flag):
            print("Number not recognized")


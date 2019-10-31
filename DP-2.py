'''
Design Parameter Program
McMaster University
1P10 Design Project 2
Yousam Asham, Diana Cancelliere, Varun Jain, Emily Kim
'''

from time import sleep
import math

# Global Variables
teamNumber = 20
bodyWeight = 823.2  # Newtons
outerDia = 35  # Millimetres
canalDia = 18  # Millimetres
canalOffset = 52  # Millimetres
modulusBone = 17  # Gigapascals
ultTenStrength = 950  # Megapascals (TI6AL4V)
modulusImplant = 114  # Gigapascals (TI6AL4V)
stemDia = 18  # Millimetres



def SubProgram1():
    print("", "Subprogram 1 calculates the minimum allowable implant stem diameter under the combined loading scenario",
          "where the weight of the patient acts through the center of the femoral head", sep="\n")
    sleep(0.5)

    print("", "The body weight of the patient is: " + str(bodyWeight), "The canal diameter is: " + str(canalDia),
          "The Ultimate Tensile Strength (UTS) is: " + str(ultTenStrength), sep="\n")

    loadActing = 3.5 * bodyWeight
    moment = loadActing * canalOffset
    minStemDia = canalDia

    while True:
        crossSectionArea = (math.pi / 4) * (minStemDia) ** 2
        radius = 0.5 * minStemDia
        inertia = (math.pi / 64) * (minStemDia) ** 4

        axialStress = loadActing / crossSectionArea
        bendingStress = (moment * radius) / inertia
        appTenStress = -axialStress + bendingStress

        if appTenStress <= ultTenStrength:
            minStemDia -= 0.00001  ##not sure how precisely close to 950 we want to get....like this it takes time though
        else:
            break
    return appTenStress, minStemDia


def SubProgram2(minStemDia):
    inFile = open("SN Data - Sample Metal.txt")
    dataList = inFile.readlines()
    inFile.close()

    crossSectionArea = (math.pi / 4) * (minStemDia) ** 2
    cyclicalLoad = 10 * bodyWeight * 9.8
    stressAmplitude = cyclicalLoad / crossSectionArea

    for i in range(len(data_list)):
        line = dataList[i]
        splitStr = line.split('\t')
        splitFloat = [float(splitStr[0]), float(splitStr[1])]
        if splitFloat[0] == stressAmplitude:
            cyclesFail = splitFloat[1]

    stressConFactor = 6 + math.log((cyclesFail), 10) ** (teamNumber / 30)
    stressFailMax = stressConFactor * stressAmplitude
    return stressFailMax, cyclesFail

def SubProgram3():
     boneArea = (math.pi)/4*(outerDia**2 - canalDia**2)
     compressiveLoad = 30*bodyWeight*9.8
     compStress = compressiveLoad/boneArea
        
     stressReduc = compStress * ((2 * modulusBone)/(modulusBone + modulusImplant)**(0.5))
     compStrength = stressReduc
     Eratio = math.sqrt(modulusImplant/modulusBone)
        
     a = 0.001
     b = -3.437*Eratio
     c = 181.72 - compStrength #is this what we use?
     yrsFail = ( -b + math.sqrt(b**2 - 4*a*c) ) / 2*a
     stressFail = compStrength
        
     print("","The number of years post-implantation before there is risk of femoral fracture: " + str(yrsFail), "The compressive stress on the bone that corresponds to fracture risk after " + str(yrsFail) + " years post-implantation is " + str(stressFail), "", sep="\n")

def Exit():
    print("Hello")

def main ():
    run = True
    while run == True:
        print("Program Menu: ","1. Subprogram 1", "2. Subprogram 2", "3. Subprogram 3", "4. Exit from program", sep="\n\t")
        sleep(0.5)

        choice = int(input("Please choose one of the options listed above: "))

        if choice == 1:
            appTenStress, minStemDia = SubProgram1()
            print("", "The minimum implant stem diameter is: " + str(round(minStemDia, 2)),
                  "The applied tensile stress is: " + str(round(appTenStress,2)), "", sep="\n")
            sleep(1)

        elif choice == 2:
            stressFailMax, cyclesFail = SubProgram2()
            print("","The number of cycles at which failure to fatigue is expected to occur after: " + str(cyclesFail), "The maximum stress amplitude that corresponds to failure: " + str(stressFailMax), "", sep="\n")
            sleep(1)

        elif choice ==3:

            print("","The number of years post-implantation before there is risk of femoral fracture: " + str(yrsFail), "The compressive stress on the bone that corresponds to fracture risk after " + str(yrsFail) + " years post-implantation is " + str(stressFail), "", sep="\n")

        else:
            run = False
            print("Goodbye!")

main()

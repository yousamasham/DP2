'''
Design Parameter Program
McMaster University
1P10 Design Project 2
Yousam Asham, Diana Cancelliere, Varun Jain, Emily Kim
'''

from time import sleep
import math


def SubProgram1(bodyWeight, canalDia, ultTenStrength, canalOffset):
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


def SubProgram2(stemDia, bodyWeight, teamNumber):
    inFile = open("SN Data - Sample Ceramic.txt", "r")
    data_list = inFile.readlines()
    inFile.close()

    crossSectionArea = (math.pi / 4) * (stemDia) ** 2
    cyclicalLoadMax = 10 * bodyWeight
    stressMax = cyclicalLoadMax / crossSectionArea
    cyclicalLoadMin = -10 * bodyWeight
    stressMin = cyclicalLoadMin / crossSectionArea
    stressAmplitude = (stressMax - stressMin) / 2
    file_list = []
    for value in data_list:
        split_float = value.split("\t")
        split_float[0] = float(split_float[0])
        split_float[1] = float(split_float[1])
        file_list.append(split_float)
    for i in range(len(file_list)):
        stressConcen = 6 + math.pow(math.log(file_list[i][1], 10), teamNumber / 30)
        maxStressAmp = stressAmplitude * stressConcen
        if file_list[i][0] < maxStressAmp:
            cyclesFail = file_list[i][1]  ##N, an underestimate is better than an overestima
            return maxStressAmp, cyclesFail
    return print("This implant does not fail with this material according to the S-N curve")


def SubProgram3(outerDia, canalDia, bodyWeight, modulusBone, modulusImplant):
    boneArea = (math.pi / 4) * (outerDia ** 2 - canalDia ** 2)
    compressiveLoad = 30 * bodyWeight
    compStress = compressiveLoad / boneArea

    stressReduc = compStress * ((2 * modulusBone) / (modulusBone + modulusImplant)) ** (0.5)
    Eratio = math.sqrt(modulusImplant / modulusBone)

    numyears = 0
    compStrength = 181.72
    while stressReduc < compStrength:
        numyears += 1
        compStrength = 0.001 * ((numyears) ** 2) - (3.437 * numyears * Eratio) + 181.72
    if stressReduc >= compStrength:
        numyears -= 1
        compStrength = 0.001 * ((numyears) ** 2) - (3.437 * numyears * Eratio) + 181.72

    return numyears, compStrength


def Exit():
    print("Hello")


def main():
    teamNumber =
    bodyWeight =   # Newtons
    outerDia =  # Millimetres
    canalDia =  # Millimetres
    canalOffset =   # Millimetres
    modulusBone =  # Gigapascals
    ultTenStrength =   # Megapascals (TI6AL4V)
    modulusImplant =   # Gigapascals (TI6AL4V)
    stemDia =   # Millimetres
    run = True
    while run == True:
        print("Program Menu: ", "1. Subprogram 1", "2. Subprogram 2", "3. Subprogram 3", "4. Exit from program",
              sep="\n\t")
        sleep(0.5)

        choice = int(input("Please choose one of the options listed above: "))

        if choice == 1:
            appTenStress, minStemDia = SubProgram1(bodyWeight, canalDia, ultTenStrength, canalOffset)
            print("", "The minimum implant stem diameter is: " + str(round(minStemDia, 2)),
                  "The applied tensile stress is: " + str(round(appTenStress, 2)), "", sep="\n")
            sleep(1)

        elif choice == 2:
            stressFailMax, cyclesFail = SubProgram2(stemDia, bodyWeight, teamNumber)
            print("", "The number of cycles at which failure to fatigue is expected to occur after: " + str(cyclesFail),
                  "The maximum stress amplitude that corresponds to failure: " + str(stressFailMax), "", sep="\n")
            sleep(1)

        elif choice == 3:
            yrsFail, stressFail = SubProgram3(outerDia, canalDia, bodyWeight, modulusBone, modulusImplant)

            print("", "The number of years post-implantation before there is risk of femoral fracture: " + str(yrsFail),
                  "The compressive stress on the bone that corresponds to fracture risk after " + str(
                      yrsFail) + " years post-implantation is " + str(stressFail), "", sep="\n")
            sleep(1)

        else:
            run = False
            print("Goodbye!")


main()

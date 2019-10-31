'''
Design Parameter Program
McMaster University
1P10 Design Project 2
Yousam Asham (ashamy1), Diana Cancelliere (cancelld), Varun Jain (jainv8), Emily Kim (kimm101)
'''

# In the line below, the math library and sleep function are imported for use in the program
from time import sleep
import math

# Author: Diana C., Co-Author: Varun J.
# SubProgram 1,calculates for the applied tensile stress and computes the minimum stem diameter through a while loop
# The program uses the bodyweight, canal diameter, ultimate tensile strength and canal offset as values for calculations
# The formulas used are given from the project pack as well as during the 1P10 lectures
def SubProgram1(bodyWeight,canalDiameter, ultTenStrength, canalOffset):
    print("", "Subprogram 1 calculates the minimum allowable implant stem diameter under the combined loading scenario",
          "where the weight of the patient acts through the center of the femoral head", sep="\n")
    sleep(0.5)
    print("", "The body weight of the patient is: " + str(bodyWeight), "The canal diameter is: " + str(canalDiameter),
          "The Ultimate Tensile Strength (UTS) is: " + str(ultTenStrength), sep="\n")
    loadActing = 3.5 * bodyWeight
    moment = loadActing * canalOffset
    minStemDia = canalDiameter
# The while True allows for the lines below to continue to iterate until there is a break (else function)
    while True:
        crossSectionArea = (math.pi / 4) * (minStemDia) ** 2
        radius = 0.5 * minStemDia
        inertia = (math.pi / 64) * (minStemDia) ** 4
        axialStress = loadActing / crossSectionArea
        bendingStress = (moment * radius) / inertia
        appTenStress = -axialStress + bendingStress
# The if loop below causes the minimum stem diameter to continue to iterate until it is at a minimum
        if appTenStress <= ultTenStrength:
            minStemDia -= 0.00001
        else:
            break
    return appTenStress, minStemDia

# Author: Varun J., Co-Author: Yousam A.
# Subprogram 2 uses File I/O to read the SN Data and from that find the maximum stress amplitude and cycles till failure
def SubProgram2(stemDia,bodyWeight, teamNumber):
    inFile = open("SN Data - Sample Ceramic.txt", "r")
    data_list = inFile.readlines()
    inFile.close()
    crossSectionArea = (math.pi / 4) * (stemDia) ** 2
    cyclicalLoadMax = 10 * bodyWeight
    stressMax=cyclicalLoadMax/crossSectionArea
    cyclicalLoadMin = -10 * bodyWeight
    stressMin=cyclicalLoadMin/crossSectionArea
    stressAmplitude = (stressMax-stressMin) / 2
# A new list was created below where the values from the text file will be put into as floats
    file_list = []
    for value in data_list:
        split_float = value.split("\t")
        split_float[0] = float(split_float[0])
        split_float[1] = float(split_float[1])
        file_list.append(split_float)
# The for loop below allows for each cycles number to iterate through the lines until the if statement is achieved
    for i in range(len(file_list)):
        stressConcen = 6 + math.pow(math.log(file_list[i][1], 10), teamNumber / 30)
        stressFail = stressAmplitude * stressConcen
        if file_list[i][0] < stressFail:
            cyclesFail = file_list[i][1]
            return stressFail, cyclesFail
# This line is included because there are some instances where the material will not fail with the S-N curve
# It is important to make these considerations when choosing a material
    return print("This implant does not fail with this material according to the S-N curve")

# Author: Varun J., Co-Author: Yousam A.
# Subprogram 3 calculates for the years at which the material will fail as well as the compressive strength
def SubProgram3(outerDia,canalDiameter,bodyWeight,modulusBone,modulusImplant):
    boneArea = (math.pi/4)*(outerDia**2 - canalDiameter**2)
    compressiveLoad = 30*bodyWeight
    compStress = compressiveLoad/boneArea
    stressReduc = compStress * ((2 * modulusBone)/(modulusBone + modulusImplant))**(0.5)
    Eratio = math.sqrt(modulusImplant/modulusBone)
    yrsFail = 0
    compStrength = 181.72
# This while loop increases the years by 1 if the reduced stress is less than compressive strength
    while stressReduc < compStrength:
        yrsFail += 1
        compStrength = 0.001*((yrsFail)**2) - (3.437 * yrsFail * Eratio) + 181.72
# This if statement subtracts the number of years by 1 if the reduced for that stress surpasses the compressive strength
# This is because without the if statement, the program would calculate the year it would break, not the year before
    if stressReduc >= compStrength:
        yrsFail -= 1
        compStrength = 0.001 * ((yrsFail) ** 2) - (3.437 * yrsFail * Eratio) + 181.72
    return yrsFail, compStrength

# Author: Varun J.
def main ():
# These are the variables used throughout the program
    teamNumber = 20
    bodyWeight = 823.2  # Newtons
    outerDia = 35  # Millimetres
    canalDiameter = 18  # Millimetres
    canalOffset = 52  # Millimetres
    modulusBone = 17  # Gigapascals
    ultTenStrength = 950  # Megapascals (TI6AL4V)
    modulusImplant = 114  # Gigapascals (TI6AL4V)
    stemDia = 18  # Millimetres
# The lines make the function continues to run and go back to the home screen after going through the SubProgram
# This however is broken in if the user selects Option 4 which exits the program
    run = True
    while run == True:
        print("------------------------------HOME------------------------------")
        print("Program Menu: ","1. Subprogram 1", "2. Subprogram 2", "3. Subprogram 3", "4. Exit from program", sep="\n\t")
        sleep(0.5)
# The user is given the choice as to which SubProgram they would like to run
        choice = input("Please choose one of the options listed above: ")
        if choice == "1":
            appTenStress, minStemDia = SubProgram1(bodyWeight,canalDiameter,ultTenStrength,canalOffset)
            print("", "The minimum implant stem diameter is: " + str(round(minStemDia, 2)),
                  "The applied tensile stress is: " + str(round(appTenStress,2)), "", sep="\n")
            sleep(1)
        elif choice == "2":
            stressFail, cyclesFail = SubProgram2(stemDia,bodyWeight, teamNumber)
            print("","The number of cycles at which failure to fatigue is expected to occur after: " + str(cyclesFail), "The maximum stress amplitude that corresponds to failure: " + str(stressFail), "", sep="\n")
            sleep(1)
        elif choice == "3":
            yrsFail, stressFail=SubProgram3(outerDia,canalDiameter,bodyWeight,modulusBone,modulusImplant)
            print("","The number of years post-implantation before there is risk of femoral fracture: " + str(yrsFail), "The compressive stress on the bone that corresponds to fracture risk after " + str(yrsFail) + " years post-implantation is " + str(stressFail), "", sep="\n")
            sleep(1)
        elif choice == "4":
            run = False
            print("Goodbye!")
        else:
            print("Please choose a valid option!","",sep = "\n")
            sleep(1)
main()

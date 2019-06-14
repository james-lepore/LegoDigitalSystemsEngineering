'''
Created on Jun 3, 2019

@author: jlepore
'''
from cmath import isclose


''' REQUIREMENTS '''
def getPartsList(filename):
    """Returns a parts list as a dictionary where the key is the 
    BrickLink ID Number and the data is a list of the different 
    instances of that part within the model"""
    parts_list = {}
    f = open(filename + ".ldr")
    for line in f:
        lst = line.split(" ")
        if lst[0] == '1':
            part = lst[-1].replace(".dat\n", "")
            if part not in parts_list:
                parts_list[part] = [];
            parts_list[part] += [list(map(float, lst[1:-1]))]
    f.close()
    return parts_list


def seatFacingFront(parts_list, part):
    """Helper function for seatOrientation function to check if it is facing
    front i.e. towards the console"""
    front = False
    if "3829c01" in parts_list and len(parts_list["3829c01"]) == 1:
        front = True
        console = parts_list["3829c01"][0]
        for i in range(4, 13):
            if(not isclose(console[i], part[i], rel_tol = .0005, abs_tol = .0005)):
                front = False
    return front    


def seatOrientation(parts_list):
    """Vehicle shall have at least one seat facing forward."""
    # to-do
    if "4079" in parts_list:
        for seat in parts_list["4079"]:
            if seatFacingFront(parts_list, seat):
                return True
    return False
    

def seatObstruction(parts_list):
    """Seat area shall not be obstructed by components."""
    # to-do
    

def consoleFacingSeat(parts_list, seat):
    """Helper function that determines whether the seat is positioned facing the console"""
    ret = False
    console = parts_list["3829c01"][0]
    if abs(seat[1] - console[1]) <= 30 and abs(seat[2] - console[2]) <= 10 and abs(seat[3] - console[3]) <= 30:
            ret = True
    return ret
    

def consoleOrientation(parts_list):
    """Vehicle shall have exactly one steering wheel facing a seat."""
    if "3829c01" in parts_list and len(parts_list["3829c01"]) == 1:
        if "4079" in parts_list:
            for seat in parts_list["4079"]:
                if seatFacingFront(parts_list, seat) and consoleFacingSeat(parts_list, seat):
                    return True
    return False


def countWheels(parts_list):
    """Helper function for numWheels that counts the number of wheels on ground level"""
    count = 0
    if "30027bc01" in parts_list:
        min_height = parts_list["30027bc01"][0][2]
        for wheel in parts_list["30027bc01"]:
            if wheel[2] < min_height:
                min_height = wheel[2]
        for wheel in parts_list["30027bc01"]:
            if isclose(min_height, wheel[2], rel_tol=.0005, abs_tol=.0005):
                count+=1
    return count


def numWheels(parts_list):
    """Vehicle shall have at least four wheels."""
    return countWheels(parts_list) >= 4
    

def findWheelPairs(parts_list, wheels, axels):
    """Helper function for wheel orientation that finds the corresponding wheel
    pairs and their axels"""
    i = 0
    while i in range(len(axels)):
        axel = axels[i]
        j = 0
        while j in range(len(wheels)):
            wheel1 = wheels[j]
            k = 0
            while k in range(len(wheels)):
                wheel2 = wheels[k]
                if isclose((wheel1[1] + wheel2[1])/2, axel[1], rel_tol = 1.5, abs_tol = 1.5) and \
                   isclose(wheel1[2], axel[2] + 5, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(wheel2[2], axel[2] + 5, rel_tol = .0005, abs_tol = .0005) and \
                   isclose((wheel1[3] + wheel2[3])/2, axel[3], rel_tol = 1.5, abs_tol = 1.5) and \
                   isclose(wheel1[4], wheel1[12], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(wheel1[12], axel[6], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(axel[6], -axel[10], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-axel[10], -wheel2[4], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-wheel2[4], -wheel2[12], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(wheel1[6], -wheel1[10], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-wheel1[10], -axel[4], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-axel[4], -axel[12], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-axel[12], -wheel2[6], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-wheel2[6], wheel2[10], rel_tol = .0005, abs_tol = .0005):
                    del(axels[i])
                    wheels.remove(wheel1)
                    wheels.remove(wheel2)
                    return findWheelPairs(parts_list, wheels, axels)
                k+=1       
            j+=1
        i+=1
    return axels, wheels

def wheelOrientation(parts_list):
    """All wheels shall be securely attached to axels."""
    if "2926" in parts_list and "30027bc01" in parts_list and len(parts_list["2926"]) * 2 == len(parts_list["30027bc01"]):
        axels, wheels = findWheelPairs(parts_list, list(parts_list["30027bc01"]), list(parts_list["2926"]))
    else:
        return False
    return len(axels) == 0 and len(wheels) == 0


def headlightCounter(parts_list):
    """Helper function for headlightOrientation to count the number of
    properly positioned headlights"""
    count = 0
    if "3829c01" in parts_list and "98138" in parts_list:
        console = parts_list["3829c01"][0]
        for stud in parts_list["98138"]:
            if stud[0] == 47:
                #check orientation
                if isclose(stud[5], console[6], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(stud[8], 0, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(stud[11], console[12], rel_tol = .0005, abs_tol = .0005):
                    count+=1
    return count

def headlightOrientation(parts_list):
    """Vehicle shall have at least two clear lights visible from the front."""
    return headlightCounter(parts_list) >= 2
   
def taillightCounter(parts_list):
    """Helper function for taillightOrientation to count the number of
    properly positioned taillights"""
    count = 0
    if "3829c01" in parts_list and "98138" in parts_list:
        console = parts_list["3829c01"][0]
        for stud in parts_list["98138"]:
            if stud[0] == 36:
                #check orientation
                if isclose(stud[5], -console[6], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(stud[8], 0, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(stud[11], -console[12], rel_tol = .0005, abs_tol = .0005):
                    count+=1
    return count
                    
    
def taillightOrientation(parts_list):
    """Vehicle shall have at least two red lights visible from the rear"""
    return taillightCounter(parts_list) >= 2

def licensePlateOrientation(parts_list):
    """Vehicle shall have a yellow license plate visible from the rear."""
    if "3829c01" in parts_list and "3069b" in parts_list:
        console = parts_list["3829c01"][0]
        for plate in parts_list["3069b"]:
            if plate[0] == 14.0:
                #check orientation
                if isclose(abs(plate[4]), abs(console[4]), rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-plate[5], console[6], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(plate[6], 0, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(plate[7], 0, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(plate[8], 0, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(abs(plate[9]), 1, rel_tol = .0005, abs_tol = .0005) and \
                   isclose(abs(plate[10]), abs(console[10]), rel_tol = .0005, abs_tol = .0005) and \
                   isclose(-plate[11], console[12], rel_tol = .0005, abs_tol = .0005) and \
                   isclose(plate[12], 0, rel_tol = .0005, abs_tol = .0005):
                    return True
    return False


def connectivity(parts_list):
    """All components shall be secured to the chassis without gaps."""
    # to-do


def numChassis(parts_list):
    """Only one chassis shall be used."""
    count = 0
    chassis = ["3032", "3035", "3030"]
    for c in chassis:
        if c in parts_list:
            count += len(parts_list[c])
    return count == 1


def cargoSpace(parts_list):
    """Internal cargo space shall not be filled with wall pieces."""
    # to-do


''' MARKET RESEARCH '''
def getCost(parts_list):
    f = open("PartsList.csv")
    cost_list = {}
    for line in f:
        line = line.split(",")
        cost_list[line[-3]] = line[-2] 
    cost_list.__delitem__("BrickLink ID")
    
    total_cost = 0
    for part in parts_list:
        total_cost += len(parts_list[part]) * float(cost_list[part])
    f.close()
    return "%.2f" % (total_cost*100)


def getMarketPrice(parts_list):
    pass


def getSeatingScore(parts_list):
    seatingMap = [0, 40, 60, 65, 75, 80, 90, 95, 100];
    try:
        return seatingMap[len(parts_list["4079"])]
    except IndexError:
        return seatingMap[8]
    except KeyError:
        return seatingMap[0]


def getVentilationScore(parts_list):
    ventilationMap = [40, 45, 70, 75, 90, 95, 100];
    num_parts = 0
    vent_parts = ["2412b", "61409"]
    for part in vent_parts:
        try:
            num_parts += parts_list[part]
        except:
            continue
    
    try:
        return ventilationMap[num_parts]
    except IndexError:
        return ventilationMap[6]


def getStabilityScore(parts_list):
    wheel_count = countWheels(parts_list)
    if(wheel_count) < 4:
        return 0
    if(wheel_count) < 6:
        return 90
    return 100


def getHeadlightScore(parts_list):
    headlightMap = [0, 0, 60, 65, 80, 85, 90, 95, 100];
    num_lights = headlightCounter(parts_list)
    try:
        return headlightMap[num_lights]
    except IndexError:
        return headlightMap[8]


def getTaillightScore(parts_list):
    taillightMap = [0, 0, 80, 90, 100];
    num_lights = taillightCounter(parts_list)
    try:
        return taillightMap[num_lights]
    except IndexError:
        return taillightMap[4]
    

def getCargoSpaceScore(parts_list):
    pass    


def getAerodynamicsScore(parts_list):
    aero_parts = {"50950":2, "30602":3, "60481":1.5, "93273":1, "6091":1, "15068":2.5, "85984":1, "54200":0.5}
    aerodynamicsMap = [20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 100];
    aero_score = 0
    if "3829c01" in parts_list:
        console = parts_list["3829c01"][0]
        for part in aero_parts:
            if part in parts_list:
                for instance in parts_list[part]:
                    if isclose(instance[6], console[6], rel_tol = .0005, abs_tol = .0005) and \
                       isclose(instance[9], console[9], rel_tol = .0005, abs_tol = .0005) and \
                       isclose(instance[12], console[12], rel_tol = .0005, abs_tol = .0005):
                        aero_score+=aero_parts[part]
    try:
        return aerodynamicsMap[int(aero_score)]
    except IndexError:
        return aerodynamicsMap[10]


''' TEST '''
car = "modelA"
parts_list = getPartsList(car)
# for item in parts_list:
#     print(item, "\n", parts_list[item])
    
print("--Requirements Check--")
print("Num Chassis:\t", numChassis(parts_list))
print("Num Wheels:\t", numWheels(parts_list))
print("Seat Pos:\t", seatOrientation(parts_list))
print("Console Pos:\t", consoleOrientation(parts_list))
print("License Pos:\t", licensePlateOrientation(parts_list))
print("Taillight Pos:\t", taillightOrientation(parts_list))
print("Headlight Pos:\t", headlightOrientation(parts_list))
print("Wheel Pos:\t", wheelOrientation(parts_list))
print("Seat Clear:\t", seatObstruction(parts_list))
print("Cargo Clear:\t", cargoSpace(parts_list))
print("Connectivity:\t", connectivity(parts_list))


print("\n--Market Research--")
print("Seating:\t",getSeatingScore(parts_list))
print("Ventilation:\t", getVentilationScore(parts_list))
print("Stability:\t", getStabilityScore(parts_list))
print("Headlight:\t", getHeadlightScore(parts_list))
print("Taillight:\t", getTaillightScore(parts_list))
print("Cargo Space:\t", getCargoSpaceScore(parts_list))
print("Aerodynamics:\t", getAerodynamicsScore(parts_list))
print("Mfg. Cost:\t", getCost(parts_list))
print("Market Price:\t", getMarketPrice(parts_list))


cargoMap = [[0,0], [3,25], [4,40], [5,45], [6,50], [7,80], [8,85], [9,90], [11,95], [12,100]];



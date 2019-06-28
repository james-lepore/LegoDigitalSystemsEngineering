'''
Created on Jun 3, 2019

@author: jlepore
'''
from cmath import isclose


''' REQUIREMENTS '''
def getPartsList(lines):
    """Returns a parts list as a dictionary where the key is the 
    BrickLink ID Number and the data is a list of the different 
    instances of that part within the model"""
    parts_list = {}
    for line in lines:
        lst = line.split(" ")
        if lst[0] == '1':
            part = lst[-1].replace(".dat\r", "")
            if part not in parts_list:
                parts_list[part] = [];
            parts_list[part] += [list(map(float, lst[1:-1]))]
    return parts_list


def seatFacingFront(parts_list, part):
    """Helper function for seatOrientation function to check if it is facing
    front i.e. towards the console"""
    front = False
    if "3829c01" in parts_list and len(parts_list["3829c01"]) == 1:
        front = True
        console = parts_list["3829c01"][0]
        for i in range(4, 13):
            if(not isclose(console[i], part[i], abs_tol = .0005)):
                front = False
    return front    


def seatOrientation(parts_list):
    """Vehicle shall have at least one seat facing forward."""
    if "4079" in parts_list:
        for seat in parts_list["4079"]:
            if seatFacingFront(parts_list, seat):
                return True
    return False
    

def seatObstruction(parts_list):
    """Seat area shall not be obstructed by components."""
    if "4079" in parts_list:
        for seat in parts_list["4079"]:
            for part in parts_list:
                for instance in parts_list[part]:
                    if abs(seat[1] - instance[1]) < 29 and abs(seat[3] - instance[3]) < 29 and \
                       isclose(seat[2], instance[2] + 45, abs_tol = 40):
                        return False
    return True
    

def consoleFacingSeat(parts_list, seat):
    """Helper function that determines whether the seat is positioned facing the console"""
    console = parts_list["3829c01"][0]
    if abs(seat[1] - console[1]) <= 30 and abs(seat[2] - console[2]) <= 10 and abs(seat[3] - console[3]) <= 30:
            return True
    return False
    

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
            if isclose(min_height, wheel[2], abs_tol=.0005):
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
                if isclose((wheel1[1] + wheel2[1])/2, axel[1], abs_tol = 1.5) and \
                   isclose(wheel1[2], axel[2] + 5, abs_tol = .0005) and \
                   isclose(wheel2[2], axel[2] + 5, abs_tol = .0005) and \
                   isclose((wheel1[3] + wheel2[3])/2, axel[3], abs_tol = 1.5) and \
                   isclose(wheel1[4], wheel1[12], abs_tol = .0005) and \
                   isclose(wheel1[12], axel[6], abs_tol = .0005) and \
                   isclose(axel[6], -axel[10], abs_tol = .0005) and \
                   isclose(-axel[10], -wheel2[4], abs_tol = .0005) and \
                   isclose(-wheel2[4], -wheel2[12], abs_tol = .0005) and \
                   isclose(wheel1[6], -wheel1[10], abs_tol = .0005) and \
                   isclose(-wheel1[10], -axel[4], abs_tol = .0005) and \
                   isclose(-axel[4], -axel[12], abs_tol = .0005) and \
                   isclose(-axel[12], -wheel2[6], abs_tol = .0005) and \
                   isclose(-wheel2[6], wheel2[10], abs_tol = .0005):
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
                if isclose(stud[5], console[6], abs_tol = .0005) and \
                   isclose(stud[8], 0, abs_tol = .0005) and \
                   isclose(stud[11], console[12], abs_tol = .0005):
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
                if isclose(stud[5], -console[6], abs_tol = .0005) and \
                   isclose(stud[8], 0, abs_tol = .0005) and \
                   isclose(stud[11], -console[12], abs_tol = .0005):
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
                if isclose(abs(plate[4]), abs(console[4]), abs_tol = .0005) and \
                   isclose(-plate[5], console[6], abs_tol = .0005) and \
                   isclose(plate[6], 0, abs_tol = .0005) and \
                   isclose(plate[7], 0, abs_tol = .0005) and \
                   isclose(plate[8], 0, abs_tol = .0005) and \
                   isclose(abs(plate[9]), 1, abs_tol = .0005) and \
                   isclose(abs(plate[10]), abs(console[10]), abs_tol = .0005) and \
                   isclose(-plate[11], console[12], abs_tol = .0005) and \
                   isclose(plate[12], 0, abs_tol = .0005):
                    return True
    return False


def connectivity(parts_list):
    """All components shall be secured to the chassis without gaps."""
    # to-do
    return True;


def numChassis(parts_list):
    """Only one chassis shall be used."""
    count = 0
    chassis = ["3032", "3035", "3030"]
    for c in chassis:
        if c in parts_list:
            count += len(parts_list[c])
    return count == 1



''' MARKET RESEARCH '''
def getCost(parts_list):
    f = open("PartsList.csv")
    cost_list = {}
    for line in f:
        line = line.split(",")
        cost_list[line[-3]] = line[-2] 
    cost_list.pop("BrickLink ID")
    f.close()
    
    total_cost = 0
    for part in parts_list:
        total_cost += len(parts_list[part]) * float(cost_list[part])
    
    return "%.2f" % (total_cost * 10)


def getMarketPrice(parts_list):
    price = getSeatingScore(parts_list) * .25 + getVentilationScore(parts_list) * .15 \
        + getStabilityScore(parts_list) * .05 + getHeadlightScore(parts_list) * .05 \
        + getTaillightScore(parts_list) * .05 + getCargoSpaceScore(parts_list) * .25 \
        + getAerodynamicsScore(parts_list) * .20
    return "%.2f" % (price)


def getProfit(parts_list):
    return "%.2f" % (float(getMarketPrice(parts_list)) - float(getCost(parts_list)))


def getSeatingScore(parts_list):
    seatingMap = [0, 40, 60, 65, 75, 80, 90, 95, 100];
    try:
        return seatingMap[len(parts_list["4079"])]
    except IndexError:
        return seatingMap[8]
    except KeyError:
        return seatingMap[0]


def getVentilationScore(parts_list):
    ventilationMap = [25, 45, 60, 75, 85, 95, 100];
    num_parts = 0
    vent_parts = ["2412b", "61409"]
    for part in vent_parts:
        try:
            num_parts += len(parts_list[part])
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
    

def findMaxVolume(parts_list):
    if "3032" in parts_list:
        chassis = parts_list["3032"][0]
        base = 9600
        multiplier = 1.0
    elif "3035" in parts_list:
        chassis = parts_list["3035"][0]
        base = 12800
        multiplier = 1.3
    else:
        chassis = parts_list["3030"][0]
        base = 16000
        multiplier = 1.5
        
    hmin = hmax = chassis[2]
    for part in parts_list:
        for instance in parts_list[part]:
            if instance[2] < hmin:
                hmin = instance[2]
            if instance[2] > hmax:
                hmax = instance[2]
    
    height = hmax - hmin + 8
    return base * height * multiplier

def getCargoSpaceScore(parts_list):
    cargoMap = [0, 15, 25, 40, 50, 65, 85, 90, 95, 100];
    if numChassis(parts_list):
        max_vol = findMaxVolume(parts_list)
    else:
        max_vol = 1
    
    f = open("PartsList.csv")
    volume_list = {}
    for line in f:
        line = line.split(",")
        volume_list[line[-3]] = line[-1] 
    volume_list.pop("BrickLink ID")
    f.close()
    
    vol = 0
    for part in parts_list:
        vol += len(parts_list[part]) * float(volume_list[part])
    ratio =  vol/max_vol 
    
    if ratio > .8:
        return cargoMap[0]
    elif ratio > .7:
        return cargoMap[1]
    elif ratio > .65:
        return cargoMap[2]
    elif ratio > .6:
        return cargoMap[3]
    elif ratio > .5:
        return cargoMap[4]
    elif ratio > .4:
        return cargoMap[5]
    elif ratio > .35:
        return cargoMap[6]
    elif ratio > .3:
        return cargoMap[7]
    elif ratio > .25:
        return cargoMap[8]
    else:
        return cargoMap[9]


def getAerodynamicsScore(parts_list):
    aero_parts = {"50950":2, "30602":3, "60481":1.5, "93273":1, "6091":1, "15068":2.5, "85984":1, "54200":0.5}
    aerodynamicsMap = [20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 100];
    aero_score = 0
    if "3829c01" in parts_list:
        console = parts_list["3829c01"][0]
        for part in aero_parts:
            if part in parts_list:
                for instance in parts_list[part]:
                    if isclose(instance[6], console[6], abs_tol = .0005) and \
                       isclose(instance[9], console[9], abs_tol = .0005) and \
                       isclose(instance[12], console[12], abs_tol = .0005):
                        aero_score+=aero_parts[part]
    try:
        return aerodynamicsMap[int(aero_score)]
    except IndexError:
        return aerodynamicsMap[10]


''' TEST '''
if __name__ == "__main__":
    car = "modelA"
    parts_list = getPartsList(car)
    print(car)
    
    #for item in parts_list:
    #    print(item, "\n", parts_list[item])
    
    print("\n--Requirements Check--")
    print("Num Chassis:\t", numChassis(parts_list))
    print("Num Wheels:\t", numWheels(parts_list))
    print("Seat Pos:\t", seatOrientation(parts_list))
    print("Console Pos:\t", consoleOrientation(parts_list))
    print("License Pos:\t", licensePlateOrientation(parts_list))
    print("Taillight Pos:\t", taillightOrientation(parts_list))
    print("Headlight Pos:\t", headlightOrientation(parts_list))
    print("Wheel Pos:\t", wheelOrientation(parts_list))
    print("Seat Clear:\t", seatObstruction(parts_list))
    print("Connectivity:\t", connectivity(parts_list))
    
    print("\n--Market Research--")
    print("Seating:\t",getSeatingScore(parts_list))
    print("Ventilation:\t", getVentilationScore(parts_list))
    print("Stability:\t", getStabilityScore(parts_list))
    print("Headlight:\t", getHeadlightScore(parts_list))
    print("Taillight:\t", getTaillightScore(parts_list))
    print("Cargo Space:\t", getCargoSpaceScore(parts_list))
    print("Aerodynamics:\t", getAerodynamicsScore(parts_list))
    
    print("\n--Summary--")
    print("Mfg. Cost:\t$", getCost(parts_list))
    print("Market Price:\t$", getMarketPrice(parts_list))
    print("Net Profit:\t$", getProfit(parts_list))
    

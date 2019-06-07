'''
Created on Jun 3, 2019

@author: jlepore
'''
from cmath import isclose


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


def numWheels(parts_list):
    """Vehicle shall have at least four wheels."""
    if "30027bc01" in parts_list:
        return len(parts_list["30027bc01"]) >= 4
    return False
    

def helper(parts_list, wheels, axels):
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
                    return helper(parts_list, wheels, axels)
                k+=1       
            j+=1
        i+=1
    return axels, wheels

def wheelOrientation(parts_list):
    """All wheels shall be securely attached to axels."""
    if "2926" in parts_list and "30027bc01" in parts_list and len(parts_list["2926"]) * 2 == len(parts_list["30027bc01"]):
        axels, wheels = helper(parts_list, parts_list["30027bc01"], parts_list["2926"])
    else:
        return False
    return len(axels) == 0 and len(wheels) == 0


def headlightOrientation(parts_list):
    """Vehicle shall have at least two clear lights visible from the front."""
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
    return count >= 2
   

def taillightOrientation(parts_list):
    """Vehicle shall have at least two red lights visible from the rear"""
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
    return count >= 2

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



""" TEST """
parts_list = getPartsList("modelA")
for item in parts_list:
    print(item, "\n", parts_list[item])
    
print("\n")

print(numChassis(parts_list))
print(numWheels(parts_list))
print(seatOrientation(parts_list))
print(consoleOrientation(parts_list))
print(licensePlateOrientation(parts_list))
print(taillightOrientation(parts_list))
print(headlightOrientation(parts_list))
print(wheelOrientation(parts_list))


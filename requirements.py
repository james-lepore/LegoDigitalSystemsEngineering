'''
Created on Jun 3, 2019

@author: jlepore
'''
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
            parts_list[part] += [lst[1:-1]]
    f.close()
    return parts_list


def seatOrientation(parts_list):
    """Vehicle shall have at least one seat facing forward."""
    # to-do
    

def seatObstruction(parts_list):
    """Seat area shall not be obstructed by components."""
    # to-do
    

def consoleOrientation(parts_list):
    """Vehicle shall have exactly one steering wheel facing a seat."""
    # to-do


def numWheels(parts_list):
    """Vehicle shall have at least four wheels."""
    # to-do
    if "30028" in parts_list and "74967" in parts_list:
        return len(parts_list["30028"]) >= 4 and len(parts_list["74967"]) >= 4
    return False
    

def wheelOrientation(parts_list):
    """All wheels shall be securely attached to axels."""
    # to-do


def headlightOrientation(parts_list):
    """Vehicle shall have at least two clear lights visible from the front."""
    # to-do
   

def taillightOrientation(parts_list):
    """Vehicle shall have at least two red lights visible from the rear"""
    # to-do
    

def licensePlateOrientation(parts_list):
    """Vehicle shall have a yellow license plate visible from the rear."""
    # to-do


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
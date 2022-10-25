# BATTLESIM 2.13.0
import random
import math
import copy

# global setup below

global PIrregulars
global PInfantry
global PCavalry
global PArtillery
global PCars
global PTanks
global CIrregulars
global CInfantry
global CMilitia
global ATTtotal
global DEFtotal
global DEFTactics
global ATTTactics
global landUnits
global retreatThreshold
global Researches
Researches = []
retreatThreshold = 100
PIrregulars = 0
PInfantry = 0
PCavalry = 0
PArtillery = 0
CIrregulars = 0
CInfantry = 0
CMilitia = 0
AttackerADV = 0
DefenderADV = 0
ATTTactics = []
DEFTactics = []

tactics = {
    # ARMY ORG: Frontrow Capacity / Overall Damage Given
    'FA': [1.05, .95],
    'BA': [1, 1],
    'RA': [.95, 1.05],
    # REINFORCE DOCTRINE: Speed to Reinforce / Damage Taken Multi
    'RR': [1.25, 1.05],
    'BR': [1, 1],
    'SR': [.75, .95],
    # BATTLE TACTICS: Damage Given / HP
    'PB': [.85, 1.05],
    'BB': [1, 1],
    'AB': [1.05, .85],
    # PURSUIT TYPE: Entrenched For Free if counterattacked (1/0), Split army in two ( cannot support eachother), total progress made
    'CP': [1, 0, .5],
    'BP': [0, 0, 1],
    'RP': [0, 1, 1.5],

}
climates = {

    # Mallusses here: 1 = full effectiveness 0 = no effectiveness
    # organized as [Irregular, Infantry, Cavalry, Artillery], MILITIAS are worse irregulars
    # Tropical / A
    'Af': [1.5, .75, .55, .75, 0],
    'Am': [1.5, .75, .55, .75, 0],
    'Aw': [1.25, .85, .65, .75, 0],
    # Dry / B
    'Bwh': [1.25, .85, 1, 1, 0],
    'Bsh': [1.25, .85, 1, 1, 0],
    'Bwk': [1, .95, 1.25, 1, 0],
    'Bsk': [1, .95, 1.25, 1, 0],
    # Temporate / C
    'Csa': [1, 1, 1, 1, 0],
    'Csb': [1, 1, 1, 1, 0],
    'Cwa': [1, 1, 1, 1, 0],
    'Cwb': [1, 1, 1, 1, 0],
    'Cfa': [1, 1, 1, 1, 0],
    'Cfb': [1, 1, 1, 1, 0],
    # Continental / D1
    'Dsb': [1.1, 1, .9, 1.1, 0],
    'Dwa': [1.1, 1, .9, 1.1, 0],
    'Dwb': [1.1, 1, .9, 1.1, 0],
    'Dfa': [1, 1, 1, 1, 0],
    'Dfb': [1.1, 1, .9, 1.1, 0],
    # Subartic / D2
    'Dsc': [1.3, .7, .7, 1, 0],
    'Dwc': [1.3, .7, .7, 1, 0],
    'Dfc': [1.3, .7, .7, 1, 0],
    # Polar / E
    'ET': [.7, .5, .3, 1, 0],
    'EF': [.6, .4, .1, 1, 0],
}
landUnits = [[.30, .25], [.5, .45], [.6, .7], [.4, .12], [1000, 50], [10000, 100], [.20, .20], [.4, .40], [.25, .20]]
# NAVAL DICTIONARIES: DEPRECATED
navalTactics = {  # BB damage, Cruiser damage, torpedo boat damage, transport damage multiplier
    'FBB': [1.5, .75, .75, .75],
    'FCA': [.75, 1.5, .75, .75],
    'FTB': [.75, .75, 1.5, .75],
    'FTS': [.75, .75, .75, 1.5],
    'FBS': [1, 1, 1, 1],
}


# Damager/Reciever should be just be the HP list
# remember to set naval researches to who is shooting the shots
def ShootShip(i, rawReciever, Reciever, nonPopReciever, damagedReciever, phase, navalResearches, DecommisionPercentages, DamageArray):
    valid = False
    zeroes = 0
    for z in range(len(nonPopReciever)):
        if nonPopReciever[z][1] == 0:
            nonPopReciever.append(nonPopReciever[z])
            nonPopReciever.pop(z)
            zeroes += 1
    print(nonPopReciever)
    print("zeroes")
    print(zeroes)
    while valid == False:
        targettedShip = random.randint(0, len(nonPopReciever) - 1)
        if nonPopReciever[targettedShip][1] > 0 and targettedShip - zeroes < len(Reciever):
            valid = True
            print("printing targettedShip")
            print(targettedShip)
            print(targettedShip - zeroes)
            print(nonPopReciever)
            print("VALID TRUE")
            print(nonPopReciever[targettedShip])
    print("target1")
    # Chance to hit is a number from 0-100, It is based on phase of battle, research, Decommission %,
    chanceToHit = ((phase * .15) + (navalResearches / 20) + (DecommisionPercentages * 3)) * 100
    print(chanceToHit)
    if random.randint(0, 100) <= chanceToHit:
        print("hit!")
        Reciever[targettedShip - zeroes][1] -= DamageArray[i]

        if Reciever[targettedShip - zeroes][1] == 0 and Reciever[targettedShip - zeroes][1] != 0 and Reciever[targettedShip - zeroes][1] <= 4500:
            damagedReciever[0] += 1
        if Reciever[targettedShip - zeroes][1] == 1 and Reciever[targettedShip - zeroes][1] != 0 and Reciever[targettedShip - zeroes][1] <= 3000:
            damagedReciever[1] += 1
        if Reciever[targettedShip - zeroes][1] == 2 and Reciever[targettedShip - zeroes][1] != 0 and Reciever[targettedShip - zeroes][1] <= 1500:
            damagedReciever[2] += 1
        if Reciever[targettedShip - zeroes][1] == 3 and Reciever[targettedShip - zeroes][1] != 0 and Reciever[targettedShip - zeroes][1] <= 650:
            damagedReciever[3] += 1
        if Reciever[targettedShip - zeroes][1] == 3 and Reciever[targettedShip - zeroes][1] != 0 and Reciever[targettedShip - zeroes][1] <= 200:
            damagedReciever[3] += 1
        if Reciever[targettedShip - zeroes][1] == 3 and Reciever[targettedShip - zeroes][1] != 0 and Reciever[targettedShip - zeroes][1] <= 250:
            damagedReciever[3] += 1

        if Reciever[targettedShip - zeroes][1] <= 0:
            print("SUNK!" + str(i))
            if Reciever[targettedShip - zeroes][0] == 0:
                rawReciever[0] -= 1
                damagedReciever[0] -= 1
                print("KILLED DR ###########################")
            else:
                if Reciever[targettedShip - zeroes][0] == 1:
                    rawReciever[1] -= 1
                    damagedReciever[1] -= 1
                    print("KILLED BB ###########################")
                else:
                    if Reciever[targettedShip - zeroes][0] == 2:
                        rawReciever[2] -= 1
                        damagedReciever[2] -= 1
                        print("KILLED CA ###########################")
                    else:
                        if Reciever[targettedShip - zeroes][0] == 3:
                            rawReciever[3] -= 1
                            damagedReciever[3] -= 1
                            print("KILLED DD ###########################")
                        else:
                            if Reciever[targettedShip - zeroes][0] == 4:
                                rawReciever[4] -= 1
                                damagedReciever[4] -= 1
                                print("KILLED TB ###########################")
                            else:
                                if Reciever[targettedShip - zeroes][0] == 5:
                                    rawReciever[5] -= 1
                                    damagedReciever[5] -= 1
                                    print("KILLED TS ###########################")
            nonPopReciever[targettedShip][1] = 0
            Reciever.pop(targettedShip - zeroes)
    else:
        print("miss!")
    return i, rawReciever, Reciever, nonPopReciever, damagedReciever, phase, navalResearches, DecommisionPercentages, DamageArray


def navalPhase(ATTFleet, DEFFleet, navalTactics, navalResearches, DecommisionPercentages):
    phases = 5
    DRHP = 4500
    BBHP = 3000
    CAHP = 1500
    DDHP = 650
    TBHP = 200
    TSHP = 250
    HPArray = [DRHP, BBHP, CAHP, TBHP, TSHP]
    DamageArray = [1625, 900, 600, 350, 200, 0]
    salvos = 20
    # reorganize fleets into arrays of HP
    HPATTFleet = []
    for k in range(len(HPArray)):
        for i in range(ATTFleet[k]):
            HPATTFleet.append([k, HPArray[k]])

    print(ATTFleet)
    HPDEFFleet = []
    for k in range(len(HPArray)):
        for i in range(DEFFleet[k]):
            HPDEFFleet.append([k, HPArray[k]])

    print(DEFFleet)
    # this is to compare to see if the fleet is small enough to start rolling to retreat
    originalSizeDEF = len(HPDEFFleet)
    originalSizeATT = len(HPATTFleet)
    nonPopDEF = HPATTFleet
    nonPopATT = HPDEFFleet
    damagedDEF = [0, 0, 0, 0, 0, 0]
    damagedATT = [0, 0, 0, 0, 0, 0]
    chanceToRetreat = 0
    # beginning actual sim
    # each ship attacks one other so long as it is in range, closer range means more damage
    for phase in range(1, phases + 1):
        # calculating for all ships
        print("phase: " + str(phase) + " ############################################################")
        for i in range(len(ATTFleet) - 1):  # ignores transports this way
            print("type: " + str(i) + " ############################################################")
            # this should make it so it will always fire for all ships without having to do other silly stuff
            for k in range(max((DEFFleet[i]), (ATTFleet[i]))):
                # for each type of ship, do damage to a random other ship so long as it is in range
                for salvo in range(salvos):
                    if phase > i:
                        # ignore c,d,x,y,z they are just random things cause idc about those outputs
                        c, rawReciever, Reciever, nonPopReciever, damagedReciever, d, x, y, z = ShootShip(i, DEFFleet, HPDEFFleet, nonPopDEF, damagedDEF, phase, navalResearches[0],
                                                                                                          DecommisionPercentages[0], DamageArray)
                        DEFFleet = rawReciever
                        HPDEFFleet = Reciever
                        nonPopDEF = nonPopReciever
                        damagedDEF = damagedReciever
                        c, rawReciever, Reciever, nonPopReciever, damagedReciever, d, x, y, z = ShootShip(i, ATTFleet, HPATTFleet, nonPopATT, damagedATT, phase, navalResearches[1],
                                                                                                          DecommisionPercentages[1], DamageArray)
                        ATTFleet = rawReciever
                        HPATTFleet = Reciever
                        nonPopATT = nonPopReciever
                        damagedATT = damagedReciever
                        print(str(phase) + " " + str(i) + " " + str(DamageArray[i]) + " ")
                        print("RAW LISTS:")
                        print(ATTFleet)
                        print(DEFFleet)
                        # print("POPPED LISTS:")
                        # print(HPATTFleet)
                        # print(HPDEFFleet)
                        # print("NON POPPED LISTS:")
                        # print(nonPopDEF)
                        # print(nonPopATT)
                        # print("END FOR PHASE REPORT")
                        if originalSizeATT / 2 >= len(HPATTFleet) or originalSizeDEF / 2 >= len(HPDEFFleet):
                            chanceToRetreat += 10
                        if (random.randint(10, 100) < chanceToRetreat) or (phase == 3 and i == 2):
                            # Battle ends
                            winner = ""
                            print("###########BATTLE OVER!###########")
                            print("#########REMAINING SHIPS##########")
                            # print("Attackers | Defenders ; numbers are orderred as Damaged/Remaining")
                            print("Ships remaining: (Attackers | Defenders)")
                            print("DR:" + str(ATTFleet[0]) + " | " + str(DEFFleet[0]))
                            print("BB:" + str(ATTFleet[1]) + " | " + str(DEFFleet[1]))
                            print("CA:" + str(ATTFleet[2]) + " | " + str(DEFFleet[2]))
                            print("DD:" + str(ATTFleet[3]) + " | " + str(DEFFleet[3]))
                            print("TB:" + str(ATTFleet[4]) + " | " + str(DEFFleet[4]))
                            print("TS:" + str(ATTFleet[5]) + " | " + str(DEFFleet[5]))

                            # print("BB:"+str(damagedATT[0])+"/"+str(ATTFleet[0])+" | "+str(damagedDEF[0])+"/"+str(DEFFleet[0]))
                            # print("CA:"+str(damagedATT[1])+"/"+str(ATTFleet[1])+" | "+str(damagedDEF[1])+"/"+str(DEFFleet[1]))
                            # print("TB:"+str(damagedATT[2])+"/"+str(ATTFleet[2])+" | "+str(damagedDEF[2])+"/"+str(DEFFleet[2]))
                            # print("TS:"+str(damagedATT[3])+"/"+str(ATTFleet[3])+" | "+str(damagedDEF[3])+"/"+str(DEFFleet[3]))
                            return winner
    winner = ""
    print("###########BATTLE OVER!###########")
    print("#########REMAINING SHIPS##########")
    print("Attackers | Defenders ; numbers are orderred as Damaged/Remaining")
    print("DR:" + str(damagedATT[0]) + "/" + str(ATTFleet[0]) + " | " + str(damagedDEF[0]) + "/" + str(DEFFleet[0]))
    print("BB:" + str(damagedATT[1]) + "/" + str(ATTFleet[1]) + " | " + str(damagedDEF[1]) + "/" + str(DEFFleet[1]))
    print("CA:" + str(damagedATT[2]) + "/" + str(ATTFleet[2]) + " | " + str(damagedDEF[2]) + "/" + str(DEFFleet[2]))
    print("DD:" + str(damagedATT[3]) + "/" + str(ATTFleet[3]) + " | " + str(damagedDEF[3]) + "/" + str(DEFFleet[3]))
    print("TB:" + str(damagedATT[4]) + "/" + str(ATTFleet[4]) + " | " + str(damagedDEF[4]) + "/" + str(DEFFleet[4]))
    print("TS:" + str(damagedATT[5]) + "/" + str(ATTFleet[5]) + " | " + str(damagedDEF[5]) + "/" + str(DEFFleet[5]))
    return winner

    # phase goes from 1+3, 1; battleships fire, 2; battleships and cruisers, 3; battleships cruisers and torpedo boats
    # Each ship fires at a random other ship at a time
    # Salvos increase each phase


def Setup(climates):
    # global setup
    global PIrregulars
    global PInfantry
    global PCavalry
    global PArtillery
    global PCars
    global PTanks
    global CIrregulars
    global CInfantry
    global CMilitia
    global AttackerADV
    global DefenderADV
    global DEFTactics
    global ATTTactics
    global retreatThreshold
    global Researches
    # SHEET EXTRACTOR
    # ATT SHEET
    navalBattle = int(input("Naval Battle [0] : no [1]: yes : "))
    # naval battle yes or no
    if navalBattle == 3:
        navalBattle = False
        # LAND BATTLE
        # TERRAIN SETUP:
        print("Terrain Knowledge 0-5 | Attacker:Defender; ex: (5:5)")
        TerrainKnowledge = "2:5"
        # terrain knowledge modifier for combat effectiveness
        print("Input Climate ID (Cold Desert = Bwk")
        climateID = "Cwa"
        climateMalusses = climates[climateID]
        print("Troop Mallusses:" + str(climates[climateID]))
        entrenchement = 0
        hill = 0
        river = 0
        city = 0
        landing = 0
        encircled = 0
        fort = 0
        # UNIT QUALITY:
        GDPpercap = "1200:1200"
        Research = "8:6"
        year = 1913
        DecommissionPercentage = "0:0"
        # GM Values
        ATTBoost = 0
        DEFBoost = 0
        # - These two will buff or debuff army capability if required
        # UNIT QUANTITY:
        print("UNIT COUNTS organize as Attacker:Defender; (x:y)")
        # P = proffesional / C = conscript
        PIrregulars = "0:0"
        PInfantry = "582400:285400"
        PCavalry = "2800:6900"
        PArtillery = "322:140"
        PCars = "0:0"
        PTanks = "0:0"
        CIrregulars = "0:0"
        CInfantry = "0:70100"
        CMilitia = "0:0"
        print("ARMY TACTICS organize as Attacker:Defender; ex: (Aggressive:Protective)")

        # BATTLE TACTICS:

        print("LIST OF BATTLE TACTICS AND RESPECTIVE IDS CAN BE FOUND IN PINS #MILITARY-INFO")
        # All tactics organized by TactictypeTacticfamily (FA means (F)rontrow prefrence of (A)rmy Org family)
        print("ARMY ORG: FA/BA/RA")
        armyOrg = "BA:BA"
        # Frontrow / Balanced / Rearrow
        print("REINFORCE DOCTRINE: RR/BR/SR")
        reinforceDoctrine = "BR:BR"
        # Rushed reinforces / Balanced / Slow Reinforces
        print("BATTLE TACTICS: PB/BB/AB")
        battleTactic = "AB:BB"
        # Protective/Balanced/Aggressive
        print("PURSUIT TYPES: CP/BP/RP")
        pursuitTactic = "BP:BP"
        retreatThreshold = 125
        # Consolidate/Balanced/Rushed
        # SEE VALUES IN SWITCH STATEMENT NEAR TOP

        # MILITIAS are better irregulars suck my fat balls

        # CALC EFFECTIVENESS #####################################################

        # Climate + local terrain (rivers, city) + unit quality + unit quantity(overwhelming numbers)

    elif navalBattle == 1:
        navalBattle = True
        # NAVAL BATTLE

        # SETUP
        print("UNIT QUALITY organize as Attacker:Defender; ex: (100:90)")
        navalResearch = (input("Research index (x:y):"))
        year = int(input("year (one integer):"))
        DecommissionPercentage = (input("Decommission % (decimal):"))
        print("UNIT COUNTS organize as Attacker:Defender; ex: (100:90)")
        Dreadnoughts = input("Fordragases:")
        Battleships = input("Battleships:")
        Cruisers = input("Cruisers:")
        Destroyers = input("Destroyers:")
        TorpedoBoats = input("Torpedo Boats:")
        Transports = input("Transport Ships:")
        # SPLITTING
        navalResearches = navalResearch.split(":")
        navalResearches = [float(i) for i in navalResearches]
        for i in range(len(navalResearches)):
            navalResearches[i] = navalResearches[i] / 9
        print("RESEARCHES:" + str(navalResearches))
        DecommisionPercentages = DecommissionPercentage.split(":")
        DecommisionPercentages = [float(i) for i in DecommisionPercentages]
        Dreadnoughts = Dreadnoughts.split(":")
        Dreadnoughts = [int(i) for i in Dreadnoughts]
        Battleships = Battleships.split(":")
        Battleships = [int(i) for i in Battleships]
        Cruisers = Cruisers.split(":")
        Cruisers = [int(i) for i in Cruisers]
        Destroyers = Destroyers.split(":")
        Destroyers = [int(i) for i in Destroyers]
        TorpedoBoats = TorpedoBoats.split(":")
        TorpedoBoats = [int(i) for i in TorpedoBoats]
        Transports = Transports.split(":")
        Transports = [int(i) for i in Transports]
        ATTFleet = [Dreadnoughts[0], Battleships[0], Cruisers[0], Destroyers[0], TorpedoBoats[0], Transports[0]]
        DEFFleet = [Dreadnoughts[1], Battleships[1], Cruisers[1], Destroyers[0], TorpedoBoats[1], Transports[1]]

        navalPhase(ATTFleet, DEFFleet, navalTactics, navalResearches, DecommisionPercentages)

    elif navalBattle == 0:
        navalBattle = False
        # LAND BATTLE

        # TERRAIN SETUP:
        print("Terrain Knowledge 0-5 | Attacker:Defender; ex: (5:5)")
        TerrainKnowledge = input("TerrainKnowledge:")
        # terrain knowledge modifier for combat effectiveness
        print("Input Climate ID (Cold Desert = Bwk")
        climateID = input("ClimateID?")
        # get climate for certain maluses
        climateMalusses = climates[climateID]
        print("Troop Mallusses:" + str(climates[climateID]))
        entrenchement = int(input("Entrenchment [0] : no [1]: yes"))
        # Entrenchment yes or no
        hill = int(input("Elevation advantage? [0] : no [1]: yes : "))
        river = int(input("Defending a river? [0] : no [1]: yes : "))
        city = int(input("Defending a city? [0] : no [1]: yes : "))
        fort = int(input("Defending a fort? [0] : no [1-3]: level (3 is max, 1 is minimum) : "))
        landing = int(input("Disembarkment ? [0] : no [1]: yes : "))  # these two calculated in quality
        encircled = int(input("Encircled ? [0] : no [1]: yes : "))  # ^

        # UNIT QUALITY:

        Research = (input("Research index (x:y):"))
        GDPpercap = (input("GDP per capita (x:y):"))
        year = int(input("year (integer, x):"))
        # BELOW IS DEPECATED - richard said it was a bad idea
        # DraftPercentage = (input("Draft % (decimal):"))
        DecommissionPercentage = (input("Decommission %  (.x:.y) (.05 = 5%):"))
        # Values above effect unit effectiveness aswell as the terrain stuff

        # UNIT QUANTITY:

        print("UNIT COUNTS organize as Attacker:Defender; (x:y)")
        # P = proffesional / C = conscript
        PIrregulars = (input("Prof. Irregulars (x:y):"))
        PInfantry = (input("Prof. Infantry (x:y):"))
        PCavalry = (input("Prof. Cavalry (x:y):"))
        PCars = (input("Prof. Cars (x:y):"))
        PTanks = (input("Prof. Tanks (x:y):"))
        PArtillery = (input("Prof. Artillery (x:y):"))
        CIrregulars = (input("Con. Irregulars (x:y):"))
        CInfantry = (input("Con.Infantry (x:y):"))
        CMilitia = (input("Con. Militia (x:y):"))

        print("ARMY TACTICS organize as Attacker:Defender; ex: (Aggressive:Protective)")

        # BATTLE TACTICS:

        print("LIST OF BATTLE TACTICS AND RESPECTIVE IDS CAN BE FOUND IN PINS #MILITARY-INFO")
        # All tactics organized by TactictypeTacticfamily (FA means (F)rontrow prefrence of (A)rmy Org family)
        print("ARMY ORG: FA/BA/RA")
        armyOrg = input("Army Org:")
        # Frontrow / Balanced / Rearrow
        print("REINFORCE DOCTRINE: RR/BR/SR")
        reinforceDoctrine = input("Reinforce Doctrine:")
        # Rushed reinforces / Balanced / Slow Reinforces
        print("BATTLE TACTICS: PB/BB/AB")
        battleTactic = input("Battle Tactics:")
        # Protective/Balanced/Aggressive
        print("PURSUIT TYPES: CP/BP/RP")
        pursuitTactic = input("Battle Tactics:")
        retreatThreshold = int(input("Battle Length (1 Integer ex:100): "))
        # Consolidate/Balanced/Rushed
        # SEE VALUES IN SWITCH STATEMENT NEAR TOP

        # MILITIAS are better irregulars suck my fat balls

        # CALC EFFECTIVENESS #####################################################

        # Climate + local terrain (rivers, city) + unit quality + unit quantity(overwhelming numbers)
        # TODO: add overwhelming numbers disadvantage <3

    if navalBattle == False:
        # Calc setup
        # Splits up the string into indivial float-point arrays

        TerrainKnowledge = TerrainKnowledge.split(":")
        TerrainKnowledge = [int(i) for i in TerrainKnowledge]
        PIrregulars = PIrregulars.split(":")
        PIrregulars = [int(i) for i in PIrregulars]
        PInfantry = PInfantry.split(":")
        PInfantry = [int(i) for i in PInfantry]
        PCavalry = PCavalry.split(":")
        PCavalry = [int(i) for i in PCavalry]
        PArtillery = PArtillery.split(":")
        PArtillery = [int(i) for i in PArtillery]
        PCars = PCars.split(":")
        PCars = [int(i) for i in PCars]
        PTanks = PTanks.split(":")
        PTanks = [int(i) for i in PTanks]
        CIrregulars = CIrregulars.split(":")
        CIrregulars = [int(i) for i in CIrregulars]
        CInfantry = CInfantry.split(":")
        CInfantry = [int(i) for i in CInfantry]
        CMilitia = CMilitia.split(":")
        CMilitia = [int(i) for i in CMilitia]

        # SPLITTING TACTICS

        armyOrgs = armyOrg.split(":")
        reinforceDoctrines = reinforceDoctrine.split(":")
        battleTactics = battleTactic.split(":")
        pursuitTactics = pursuitTactic.split(":")
        ATTTactics = [tactics[armyOrgs[0]], tactics[reinforceDoctrines[0]], tactics[battleTactics[0]],
                      tactics[pursuitTactics[0]]]
        DEFTactics = [tactics[armyOrgs[1]], tactics[reinforceDoctrines[1]], tactics[battleTactics[1]],
                      tactics[pursuitTactics[1]]]
        print("Attacker Tactics:" + str(ATTTactics))
        print("Defender Tactics:" + str(DEFTactics))

        # SPLITTING PERCENTS
        GDPpercap = GDPpercap.split(":")
        GDPpercap = [float(i) for i in GDPpercap]
        Researches = Research.split(":")
        Researches = [float(i) for i in Researches]
        for i in range(len(Researches)):
            Researches[i] = Researches[i] * (0.35 * (math.log(GDPpercap[i] + 600) / math.log(math.e)) - 2.2907835)

        print("RESEARCHES:" + str(Researches))
        # DraftPercentages = DraftPercentage.split(":")
        # DraftPercentages = [float(i) for i in DraftPercentages]
        DecommisionPercentages = DecommissionPercentage.split(":")
        DecommisionPercentages = [float(i) for i in DecommisionPercentages]
        # Below thing is for ease of use:
        AttackerADVPercentages = float(
            ((1 + 4 * DecommisionPercentages[0])) * (Researches[0]) * (1 - (float(.3 * landing))) / 4)
        DefenderADVPercentages = float(
            ((1 + 4 * DecommisionPercentages[1])) * (Researches[1]) * (1 - (float(.5 * encircled))) / 4)
        # *1.1 part is defender advantage
        # FIXED RATIOS (haha get ratioed)
        cavMalus = 1 - .2 * ((year - 1880) / 25)
        # As time goes on, cav will be less effective
        artBonus = 1 + .2 * ((year - 1880) / 30)
        # As time goes on, artilery will be better and better
        # TODO: updated militia is now a worse infantry dunno if this is fixed
        MilitiaMalus = 1.2  # Militia just better Irregulars
        # TODO: further fix militia-irregular-infantry ability

        # BELOW IS DEPRECATED #########################
        # getting ratios to give malus based on ratio of proffessional to conscript units
        # ATTACKERPCRatioIrr = PIrregulars[0]/(PIrregulars[0]+CIrregulars[0])
        # ATTACKERPCRatioInf = PInfantry[0]/(PInfantry[0]+CInfantry[0])
        # DEFENDERPCRatioIrr = PIrregulars[1] / (PIrregulars[1] + CIrregulars[1])
        # DEFENDERPCRatioInf = PInfantry[1] / (PInfantry[1] + CInfantry[1])
        # print(DEFENDERPCRatioInf)
        # ABOVE IS DEPRECATED #########################

        # attacker ADV:
        AttackerADVIrr = float(climateMalusses[0]) + AttackerADVPercentages * .75
        AttackerADVInf = float(climateMalusses[1]) + AttackerADVPercentages
        AttackerADVCav = float(climateMalusses[2]) + float(cavMalus) * AttackerADVPercentages * .87
        ATTACKERADVCAR = float(climateMalusses[2]) + AttackerADVPercentages
        ATTACKERADVTANK = float(climateMalusses[2]) + AttackerADVPercentages
        AttackerADVArt = float(climateMalusses[3]) + float(artBonus) * AttackerADVPercentages * 2
        AttackerADVMil = float(climateMalusses[0]) + float(MilitiaMalus) * AttackerADVPercentages
        AttackerADV = [AttackerADVIrr, AttackerADVInf, AttackerADVCav, AttackerADVArt, ATTACKERADVCAR, ATTACKERADVTANK, AttackerADVIrr, AttackerADVInf, AttackerADVMil]
        print("Attacker Quality:" + str(AttackerADV))
        # defender ADV:
        DefenderADVIrr = float(climateMalusses[0]) + DefenderADVPercentages * .75
        DefenderADVInf = float(climateMalusses[1]) + DefenderADVPercentages
        DefenderADVCav = float(climateMalusses[2]) + float(cavMalus) * DefenderADVPercentages * .87
        DefenderADVCAR = float(climateMalusses[2]) + DefenderADVPercentages
        DefenderADVTANK = float(climateMalusses[2]) + DefenderADVPercentages
        DefenderADVArt = float(climateMalusses[3]) + float(artBonus) * DefenderADVPercentages * 2
        DefenderADVMil = float(climateMalusses[0]) + float(MilitiaMalus) * DefenderADVPercentages
        DefenderADV = [DefenderADVIrr, DefenderADVInf, DefenderADVCav, DefenderADVArt, DefenderADVCAR, DefenderADVTANK, DefenderADVIrr, DefenderADVInf, DefenderADVMil]
        print("DEFENDER LEN")
        print(len(DefenderADV))
        print("Defender Quality:" + str(DefenderADV))

        # TERRAIN/STRATEGIC ATTRIBUTES:
        # each side gets points, depending on certain attributes of the terrain
        AttackerTerrainPoints = 0
        DefenderTerrainPoints = 0
        AttackerTerrainPoints += (TerrainKnowledge[0]) / (1 + landing * 1.2)+ATTBoost
        # last 3 can be 1 or 0, so 0 would contibute nothing
        DefenderTerrainPoints += (TerrainKnowledge[1] + 1.5 * city + 1 * hill + 1.5 * river + 1 * entrenchement + .75 * (fort)) / (1 + encircled * 5)+DEFBoost

        for i in range(0, len(DefenderADV)):
            DefenderADV[i] = DefenderADV[i] * ((1 + DefenderTerrainPoints / (1 + AttackerTerrainPoints)) / 2)

        for i in range(0, len(AttackerADV)):
            AttackerADV[i] = AttackerADV[i] * ((1 + AttackerTerrainPoints / (1 + DefenderTerrainPoints)) / 2)

        print("DEF")
        print(DefenderADV)
        print("ATT")
        print(AttackerADV)
        Casaulties(year)


def Casaulties(year):
    global PIrregulars
    global PInfantry
    global PCavalry
    global PArtillery
    global PCars
    global PTanks
    global CIrregulars
    global CInfantry
    global CMilitia
    global ATTtotal
    global DEFtotal
    global AttackerADV
    global DefenderADV
    global landUnits
    # Calculate casaulties stuff; list organized by Attacker, Defender:
    startingUnits = [0, 0]
    startingunitsA = [[], []]
    retreatChance = 0
    ATTpoints = 0
    DEFpoints = 0
    print(AttackerADV)
    print(DefenderADV)
    ATTtotalactive = []
    ATTtotalinactive = []
    DEFtotalactive = []
    DEFtotalinactive = []
    combatWidth = (100000)  # 50k per unit in active battle at base, increases as years go on past 1880 EDIT: this is tupid ignore this coment
    # changing it to 100k and ACTUALLY making it like the sum of the whole army as otherwise it fucks conscripts for no reason
    # if you're reading this fuck you
    ATTtotal = [PIrregulars[0], PInfantry[0], PCavalry[0], PArtillery[0], PCars[0], PTanks[0], CIrregulars[0], CInfantry[0],
                CMilitia[0]]
    DEFtotal = [PIrregulars[1], PInfantry[1], PCavalry[1], PArtillery[1], PCars[1], PTanks[1], CIrregulars[1], CInfantry[1],
                CMilitia[1]]
    for i in range(len(ATTtotal)):
        startingunitsA[0].append(copy.deepcopy(ATTtotal[i]))
        startingunitsA[1].append(copy.deepcopy(DEFtotal[i]))
        startingUnits[0] += (copy.deepcopy(ATTtotal[i]))
        startingUnits[1] += (copy.deepcopy(DEFtotal[i]))
    retreat = False
    print("starting units")
    print(startingUnits)
    ATTtotalactive = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ATTtotalinactive = (copy.deepcopy(ATTtotal))
    DEFtotalactive = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    DEFtotalinactive = (copy.deepcopy(DEFtotal))
    print(ATTtotal)
    print(DEFtotal)

    while retreat == False:

        ATTMaxReinforce = ((ATTTactics[1][0]) - .5)
        DEFMaxReinforce = ((DEFTactics[1][0]) - .5)
        print("Max Reinforces:")
        print(str(ATTMaxReinforce) + "/" + str(DEFMaxReinforce))
        print("PRE REINFORCE")
        print("ACTIVE COMBAT:")
        print(ATTtotalactive)
        print(DEFtotalactive)
        print("INACTIVE COMBAT:")
        print(ATTtotalinactive)
        print(DEFtotalinactive)
        ATTactivelimit = []
        DEFactivelimit = []
        for i in range(0, len(landUnits)):
            ATTactivelimit.append(math.floor((ATTtotal[i] / (sum(ATTtotal))) * combatWidth * ATTTactics[0][0]))
            DEFactivelimit.append(math.floor((DEFtotal[i] / (sum(DEFtotal))) * combatWidth * DEFTactics[0][0]))
        print("LIMITS")
        print(ATTactivelimit)
        print(DEFactivelimit)
        for i in range(0, len(landUnits)):  # this shit is just to run through all units, not just attackers
            # man I am a genius
            # if there is more units than can fit in the active section
            # if there is less units than can fit in the active section
            if (ATTactivelimit[i] - ATTtotalactive[i]) * ATTMaxReinforce <= ATTtotalinactive[i]:
                ATTchange = (copy.deepcopy(math.floor((ATTactivelimit[i] - ATTtotalactive[i]) * ATTMaxReinforce)))
                ATTtotalactive[i] += ATTchange
                ATTtotalinactive[i] -= ATTchange

            elif (ATTactivelimit[i] - ATTtotalactive[i]) * ATTMaxReinforce >= ATTtotalinactive[i]:
                ATTchange = (copy.deepcopy(math.floor(ATTtotalinactive[i] * ATTMaxReinforce)))
                ATTtotalactive[i] += ATTchange
                ATTtotalinactive[i] -= ATTchange

            if (DEFactivelimit[i] - DEFtotalactive[i]) * DEFMaxReinforce <= DEFtotalinactive[i]:
                DEFchange = (copy.deepcopy(math.floor((DEFactivelimit[i] - DEFtotalactive[i]) * DEFMaxReinforce)))

                DEFtotalactive[i] += DEFchange
                DEFtotalinactive[i] -= DEFchange

            elif (DEFactivelimit[i] - DEFtotalactive[i]) * DEFMaxReinforce >= DEFtotalinactive[i]:
                DEFchange = (copy.deepcopy(math.floor(DEFtotalinactive[i] * DEFMaxReinforce)))
                DEFtotalactive[i] += DEFchange
                DEFtotalinactive[i] -= DEFchange
        print("POST REINFORCE")
        print("ACTIVE COMBAT:")
        print(ATTtotalactive)
        print(DEFtotalactive)
        print("INACTIVE COMBAT:")
        print(ATTtotalinactive)
        print(DEFtotalinactive)
        for i in range(0, len(landUnits)):
            ATTtotal[i] = ATTtotalactive[i] + ATTtotalinactive[i]
            DEFtotal[i] = DEFtotalactive[i] + DEFtotalinactive[i]
        print("POST TOTAL")
        print("ACTIVE COMBAT:")
        print(ATTtotalactive)
        print(DEFtotalactive)
        print("INACTIVE COMBAT:")
        print(ATTtotalinactive)
        print(DEFtotalinactive)

        # THIS sets active units filled at start
        # TODO: ACTIVE/INACTIVE COMBAT

        if len(ATTtotal) == len(ATTtotalactive) and len(ATTtotalactive) == len(ATTtotalinactive):
            # for loop gets the damages that each will do
            rollAmountATT = 0
            rollAmountDEF = 0
            for m in range(len(ATTtotalactive)):
                rollAmountATT += ATTtotalactive[m] * landUnits[m][1] / 30
                rollAmountDEF += DEFtotalactive[m] * landUnits[m][1] / 30
            rollAmountATT = rollAmountATT - (DEFtotalactive[4] * 5 + DEFtotalactive[5] * 10)
            rollAmountDEF = rollAmountDEF - (ATTtotalactive[4] * 5 + ATTtotalactive[5] * 10)
            if rollAmountATT < 0:
                rollAmountATT = 0
            if rollAmountDEF < 0:
                rollAmountDEF = 0

            # note thise used to be ()/10 >=
            print("rollAmounts")
            print(rollAmountATT)
            print(rollAmountDEF)
            # if (ATTtotal[0]+ATTtotal[1])/10 >= rollAmountDEF or (DEFtotal[0]+DEFtotal[1])/10 >= rollAmountATT:
            if True:
                # currentRoll = random.randint(0,9) #EU4 reference lol
                currentRoll = random.randint(0, 9)
                print("Rolled:" + str(currentRoll))
                print("##################" + str(AttackerADV) + " ################### " + str(DefenderADV))
                # DAMAGES BELOW:
                # CANNON SHIT BELOW AAAAAAAAAAAAAAAAAAAAAAHHHHHHHHH
                if (ATTtotalactive[0] + ATTtotalactive[4] < combatWidth) and (ATTtotalactive[1] + ATTtotalactive[5] < combatWidth):
                    if ATTtotalactive[3] > math.floor(((rollAmountDEF * (1 - (currentRoll / 10)) * (DefenderADV[3])) * DEFTactics[0][1] * DEFTactics[2][0]) * ATTTactics[2][1]) / 100:
                        ATTtotalactive[3] -= math.floor(((rollAmountDEF * (1 - (currentRoll / 10)) * (DefenderADV[3])) * DEFTactics[0][1] * DEFTactics[2][0]) * ATTTactics[2][1] / 100)

                else:
                    if ATTtotalactive[3] > math.floor(.005 * PArtillery[1]):
                        ATTtotalactive[3] -= math.floor(.005 * PArtillery[1])

                if (DEFtotalactive[0] + DEFtotalactive[4] < combatWidth) and (DEFtotalactive[1] + DEFtotalactive[5] < combatWidth):
                    if DEFtotalactive[3] > math.floor(((rollAmountATT * (currentRoll / 10) * (AttackerADV[3])) * ATTTactics[0][1] * ATTTactics[2][0]) * DEFTactics[2][1] / 100):
                        DEFtotalactive[3] -= math.floor(((rollAmountATT * (currentRoll / 10) * (AttackerADV[3])) * ATTTactics[0][1] * ATTTactics[2][0]) * DEFTactics[2][1] / 100)

                else:
                    if DEFtotalactive[3] > math.floor(.005 * PArtillery[0]):
                        DEFtotalactive[3] -= math.floor(.005 * PArtillery[0])

                for i in range(0, 8):
                    if i != 3:
                        if i == 4 or i == 5:
                            currentRoll = currentRoll / 100
                            if ATTtotalactive[i] > math.floor(((rollAmountDEF * (1 - (currentRoll / 10)) * (DefenderADV[i])) * DEFTactics[0][1] * ATTTactics[1][1] * DEFTactics[2][0]) / (landUnits[i][0] * ATTTactics[2][1]) + PArtillery[1]) * 2:  # FORMER 1.25*1.25 makes sure there is not negatives EVER b/c max for ArmyOrg & Reinforce is the 1.25
                                ATTtotalactive[i] -= math.floor(((rollAmountDEF / 1000 * (1 - (currentRoll / 10)) * (DefenderADV[i])) * DEFTactics[0][1] * ATTTactics[1][1] * DEFTactics[2][0]) / (landUnits[i][0] * ATTTactics[2][1]) + PArtillery[1])
                            elif ATTtotalactive[i] > 0:
                                ATTtotalactive[i] -= math.floor(ATTtotalactive[i] / 4)
                            if DEFtotalactive[i] > math.floor(((rollAmountATT * (currentRoll / 10) * (AttackerADV[i])) * ATTTactics[0][1] * DEFTactics[1][1] * ATTTactics[2][0]) / (landUnits[i][0] * DEFTactics[2][1]) + PArtillery[0]) * 2:
                                DEFtotalactive[i] -= math.floor(((rollAmountATT / 1000 * (currentRoll / 10) * (AttackerADV[i])) * ATTTactics[0][1] * DEFTactics[1][1] * ATTTactics[2][0]) / (landUnits[i][0] * DEFTactics[2][1]) + PArtillery[0])
                            elif DEFtotalactive[i] > 0:
                                DEFtotalactive[i] -= math.floor(DEFtotalactive[i] / 4)
                            currentRoll = currentRoll * 100
                        else:
                            print(DefenderADV[i])
                            print(ATTtotalactive[i])
                            print(landUnits[i][0])
                            if ATTtotalactive[i] > math.floor(((rollAmountDEF * (1 - (currentRoll / 10)) * (DefenderADV[i])) * DEFTactics[0][1] * ATTTactics[1][1] * DEFTactics[2][0]) / (landUnits[i][0] * ATTTactics[2][1]) + PArtillery[1] * 3) * 2:  # FORMER 1.25*1.25 makes sure there is not negatives EVER b/c max for ArmyOrg & Reinforce is the 1.25
                                ATTtotalactive[i] -= math.floor(((rollAmountDEF * (1 - (currentRoll / 10)) * (DefenderADV[i])) * DEFTactics[0][1] * ATTTactics[1][1] * DEFTactics[2][0]) / (landUnits[i][0] * ATTTactics[2][1]) + PArtillery[1] * 3)
                            elif ATTtotalactive[i] > 0:
                                ATTtotalactive[i] -= math.floor(.706 * ATTtotalactive[i])
                            if DEFtotalactive[i] > math.floor(((rollAmountATT * (currentRoll / 10) * (AttackerADV[i])) * ATTTactics[0][1] * DEFTactics[1][1] * ATTTactics[2][0]) / (landUnits[i][0] * DEFTactics[2][1]) + PArtillery[0] * 3) * 2:
                                DEFtotalactive[i] -= math.floor(((rollAmountATT * (currentRoll / 10) * (AttackerADV[i])) * ATTTactics[0][1] * DEFTactics[1][1] * ATTTactics[2][0]) / (landUnits[i][0] * DEFTactics[2][1]) + PArtillery[0] * 3)
                            elif DEFtotalactive[i] > 0:
                                DEFtotalactive[i] -= math.floor(.706 * DEFtotalactive[i])
                        # print("Attackers's " + str(i) + " took " + str(((rollAmountDEF * (1 - (currentRoll / 10)) * (DefenderADV[i]))*DEFTactics[0][1]*ATTTactics[1][1]*DEFTactics[2][0])/(landUnits[i][0]*ATTTactics[2][1])+PArtillery[1]*3) + " Casaulties.")

                        # print("Defenders's "+ str(i)+" took " + str(math.floor(((rollAmountATT * (currentRoll / 10) * (AttackerADV[i]))*ATTTactics[0][1]*DEFTactics[1][1]*ATTTactics[2][0])/(landUnits[i][0]*DEFTactics[2][1])+PArtillery[0]*3)) + " Casaulties.")

                # cannons die to quickly so this fixes it ^^
                # RETREAT/TOTAL POINTS FOR AFTER-BATTLE
                ATTpoints += currentRoll
                DEFpoints += 9 - currentRoll
                retreatChance += currentRoll + (9 - currentRoll)
                # Below is ugly stuff needed
                print("POSTBATTLE LIST")
                print("ACTIVE COMBAT:")
                print(ATTtotalactive)
                print(DEFtotalactive)
                print("INACTIVE COMBAT:")
                print(ATTtotalinactive)
                print(DEFtotalinactive)
                for i in range(0, len(landUnits)):
                    ATTtotal[i] = ATTtotalactive[i] + ATTtotalinactive[i]
                    DEFtotal[i] = DEFtotalactive[i] + DEFtotalinactive[i]
                # above is bad practice but can't get this working without it so smd
                print("PIrregulars: " + str(ATTtotal[0]) + " / " + str(DEFtotal[0]))
                print("PInfantry: " + str(ATTtotal[1]) + " / " + str(DEFtotal[1]))
                print("PCavalry: " + str(ATTtotal[2]) + " / " + str(DEFtotal[2]))
                print("PArtillery: " + str(ATTtotal[3]) + " / " + str(DEFtotal[3]))
                print("PCars: " + str(ATTtotal[4]) + " / " + str(DEFtotal[4]))
                print("PTanks: " + str(ATTtotal[5]) + " / " + str(DEFtotal[5]))
                print("CIrregulars: " + str(ATTtotal[6]) + " / " + str(DEFtotal[6]))
                print("CInfantry: " + str(ATTtotal[7]) + " / " + str(DEFtotal[7]))
                print("CMilitia: " + str(ATTtotal[8]) + " / " + str(DEFtotal[8]))
                # REINFORCE WAVE
                # TODO: Reinforces need fixes stat: below is changelist planned
                # have a "max reinforce" for each side
                # did the above
                # max reinforce increases with year, tech, and decomission rate

                # REFILL UNITS ^ tho this is all really confusing probs cause 4 am fml

                # for i in range(6):
                #    clear = lambda: os.system('clear')
                #    clear()
                # make the outputs look pretty ^

                if retreatChance >= retreatThreshold or sum(ATTtotalactive) < rollAmountDEF * 2 or sum(DEFtotalactive) < rollAmountATT * 2:
                    retreat = True
                    ATTRemainingTroops = 0
                    DEFRemainingTroops = 0
                    #ratio from dead to wounded, where wounded + dead equal original size minus the remaining troops
                    ATTbattleCasaultiesRatio = max(.30, (min(.70, ((startingUnits[1]) / (startingUnits[0])))))
                    DEFbattleCasaultiesRatio = max(.30, (min(.70, ((startingUnits[0]) / (startingUnits[1])))))
                    # SCORE COUNT: Winning side surviving units / Total roll score of winner (i.e Pasia rolls a total of 78 of the 100 dice rolls compared to Carrisa's 22 of the 100)
                    for i in range(len(ATTtotal)):
                        ATTRemainingTroops += ATTtotal[i]
                        DEFRemainingTroops += DEFtotal[i]
                    if (ATTRemainingTroops/startingUnits[0])*AttackerADV[0]> (DEFRemainingTroops/startingUnits[1])*DefenderADV[0]:
                        print("################################")
                        print("ATTACK WINS")
                        print("################################")
                        print("REMAINING TROOPS:")
                        print(str(ATTRemainingTroops) + " " + str(DEFRemainingTroops))
                        Ratio = ATTpoints / retreatChance
                        territoryGain = math.ceil(15 * ((ATTRemainingTroops / (.75 * DEFRemainingTroops)) * Ratio) * ATTTactics[3][2])
                        print(ATTTactics[3])
                        print("TERRITORY GAINED: " + str(territoryGain))
                    else:
                        print("################################")
                        print("DEFENSE WINS")
                        print("################################")
                        print("REMAINING TROOPS:")
                        print(str(ATTRemainingTroops) + " " + str(DEFRemainingTroops))
                        Ratio = DEFpoints / retreatChance
                        territoryGain = math.ceil(15 * ((DEFRemainingTroops / (.75 * ATTRemainingTroops)) * Ratio) * DEFTactics[3][2])
                        print(DEFTactics[3])
                        print("TERRITORY GAINED: " + str(territoryGain))
                        print(ATTtotal)
                        print(DEFtotal)
                        print(startingunitsA)
                        print(ATTbattleCasaultiesRatio)
                        print(DEFbattleCasaultiesRatio)
                    print("Attacker KILLED/WOUNDED/REMAINING | Defender KILLED/WOUNDED/REMAINING(Remaining excludes Wounded)")
                    postBattlePrefixes = ["Prof. Irr: ", "Prof. Inf: ", "Prof. Cav: ", "Artillery: ", "Cars: ", "Tanks: ", "Con. Irr: ", "Con. Inf: ", "Con. Mil: ", ]
                    for i in range(len(ATTtotal)):
                        SigFig = 1
                        if (startingunitsA[1][i] > 1000 or startingunitsA[1][i] == 0) and (startingunitsA[1][i] > 1000 or startingunitsA[1][i] == 0):
                            SigFig = 100
                            # SigFig = 10**(min(len(str(ATTtotal[i])),len(str(DEFtotal[i]))))
                        elif (startingunitsA[1][i] > 100 or startingunitsA[1][i] == 0) and (startingunitsA[1][i] > 100 or startingunitsA[1][i] == 0):
                            SigFig = 10
                        roundedTotalA = (math.floor(((startingunitsA[0][i] - ATTtotal[i]) * ATTbattleCasaultiesRatio) / SigFig) * SigFig) + (math.floor(((startingunitsA[0][i] - ATTtotal[i]) * (1 - ATTbattleCasaultiesRatio)) / SigFig) * SigFig) + (math.ceil(ATTtotal[i] / SigFig) * SigFig)
                        roundedTotalD = (math.floor(((startingunitsA[1][i] - DEFtotal[i]) * DEFbattleCasaultiesRatio) / SigFig) * SigFig) + (math.floor(((startingunitsA[1][i] - DEFtotal[i]) * (1 - DEFbattleCasaultiesRatio)) / SigFig) * SigFig) + (math.ceil(DEFtotal[i] / SigFig) * SigFig)

                        print(
                            postBattlePrefixes[i] + str(math.floor(((startingunitsA[0][i] - ATTtotal[i]) * ATTbattleCasaultiesRatio) / SigFig) * SigFig) + "/" + str(math.floor(((startingunitsA[0][i] - ATTtotal[i]) * (1 - ATTbattleCasaultiesRatio)) / SigFig) * SigFig) + "/" + str(math.ceil(ATTtotal[i] / SigFig) * SigFig + startingunitsA[0][i] - roundedTotalA) + " | " + str(math.floor(((startingunitsA[1][i] - DEFtotal[i]) * DEFbattleCasaultiesRatio) / SigFig) * SigFig) + "/" + str(math.floor(((startingunitsA[1][i] - DEFtotal[i]) * (1 - DEFbattleCasaultiesRatio)) / SigFig) * SigFig) + "/" + str(
                                math.ceil(DEFtotal[i] / SigFig) * SigFig + startingunitsA[1][i] - roundedTotalD))
                    print(retreatChance >= retreatThreshold or sum(ATTtotalactive) < rollAmountDEF * 2 or sum(DEFtotalactive) < rollAmountATT * 2)
                    print("BATTLE OVER")
                    input("Press enter to exit")
                # SCORE COUNT: Winning side surviving units / Total roll score of winner (i.e Pasia rolls a total of 78 of the 100 dice rolls compared to Carrisa's 22 of the 100)
            # these kill % of rollAmount people based on roll and Attacker/Defender ADV
    # Casaulties decided by "rolls". Each roll effects rollAmount soldiers of each class,
    # in which it will max each roll to a thousand, and will display on sidebar casaulties after

    # each roll


# GRAPHICS #########

# def Win():
#
Setup(climates)

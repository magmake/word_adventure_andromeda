import mysql.connector

#START THE GAME
def start():
    global loc
    print("Space Legacy: A nightmare in Andromeda\n")
    print("Done by: Markus Saronsalo, Arttu Jokinen, Sami Tanhua\n")
    print("\n")
    print("It’s the year 3701. After 50 years of rigorous quantum research, a group of scientists deciphered a message hidden in the atomic resonance.\n"
          "The message seemed to be originating from a part of Andromeda galaxy. A research vessel named IRV Rahman was built, and a crew of 8, consisting of trained marines and scientists,\n"
          "were dispatched to locate the origin of the message. The spacecraft can travel at multiple times the speed of light with its cutting-edge propulsion system.\n"
          "Nevertheless, the full journey is estimated to take up to 120 years therefore everyone aboard will be put into hibernation.\n"
          "Just moments prior to arriving to the destination, the ship gets attacked by an unknown, seemingly hostile, alien spacecraft.\n"
          "The aliens board your ship with the goal to capture it. Most of the crew die in their hibernation chambers without ever knowing of the incident.\n"
          "Only you and two others survive the attack. Fortunately, the ship’s electrical engineer who has been in the control room, decides to turn off the main power generator.\n"
          "This causes your chamber to turn off. \n")
    start = input("Press enter to start...")
    while start!= "":
        print("Invalid input!")
        start = input("Press enter to start...")
    else:
        loc = "START"
        print("You wake up in your cabin unbeknownst of what is happening on the ship\n")
    return

#SHOW PLAYER'S HP
def get_health():
    cur = db.cursor()
    sql = "SELECT Health FROM Hero"
    cur.execute(sql)
    for row in cur.fetchall():
        print("You have",row[0],"health")
    return

#SHOW PLAYER'S LOCATION
def show_location(loc):
    cur = db.cursor()
    sql = "SELECT Details, Description FROM LOCATION WHERE ID='" + loc + "'"
    cur.execute(sql)
    for row in cur:
        print (row[0],"\n")

    return

#SHOW POSSIBLE PASSAGES
def show_passages(loc):
    print("The possible passages are:  "),
    cur = db.cursor()
    sql = "SELECT Description, Locked, Locknote FROM PASSAGE INNER JOIN DIRECTION ON PASSAGE.Direction=DIRECTION.Id WHERE Source='" + loc + "'"
    cur.execute(sql)
    i = 0;
    for row in cur.fetchall() :
        print (row[0], end=' ')
        i = i+1
        if row[1]==1:
            print("("+ row[2] + ")", end=' ')
        if i < cur.rowcount:
            print(",", end=' ')
    print("")
    return

#TAKE ITEM
def get_target(target):
    cur = db.cursor()
    sql = "UPDATE Item SET LocId= 'PLAYER',Available=FALSE, Takeable=FALSE WHERE ItemtypeId='" + target + "' AND LocId='" + loc + "' AND Available=TRUE AND TAKEABLE=TRUE"
    cur.execute(sql)
    if cur.rowcount==1:
        print("You take the " + target + ".")
    else:
        print("You can't take the " + target + ".")
    return cur.rowcount

#TARGET´S HP
def get_enemyhp(target):
    cur = db.cursor()
    sql = "SELECT Health FROM Enemy WHERE Enemy.Name = '" + target + "'"
    cur.execute(sql)
    for row in cur.fetchall():
        print( target+ " has",row[0],"health left" )
    return

#THE DAMAGE PLAYER TAKES IN BATTLE
def damtaken(target):
    cur = db.cursor()
    sql = "UPDATE Hero SET Health = Health - (SELECT Damage FROM Enemy WHERE Name='"+target+"')"
    cur.execute(sql)
    if cur.rowcount >=1:
        sql ="SELECT Health FROM Hero"
        cur.execute(sql)
        for row in cur.fetchall():
            hp = int(row[0])
            if hp > 0:
                print("You have" ,row[0]," health left.")
            else:
                print("You have DIED!")
                cont=input("\nDo you want to restart the game? [y/n]")
                if cont=='y':
                    db.rollback()
                    start()               
                else:
                    print("\nThe game will be closed...")
                    quit()
    return

#BATTLE / ATTACK FUNCTION

def battle(target,loc):
    cur = db.cursor()
    sql = "SELECT LocId FROM Enemy WHERE '"+loc+"' = Enemy.LocId AND Enemy.Name = '"+target+"'"
    cur.execute(sql)
    if cur.rowcount>=1:
        weapon = input("Which item do you want to "+action+" "+target+" with: ")
        sql = "SELECT ID FROM ITEM WHERE ID = '"+weapon+"' AND LocId= 'PLAYER'"
        cur.execute(sql)
        if cur.rowcount>=1:
            sql = "UPDATE Enemy SET Health = Health - (SELECT Damage FROM Itemtype WHERE ID='"+weapon+"') WHERE Enemy.Name = '"+target+"'"
            cur.execute(sql)
            if cur.rowcount>=1:
                sql = "SELECT Health FROM Enemy WHERE Enemy.Name ='"+target+"'"
                cur.execute(sql)
                for row in cur.fetchall():
                    ints = int(row[0])
                    if ints > 0:
                        print("You "+action+" "+target+" with "+weapon)
                        print(""+target+" has",row[0]," health left")
                        damtaken(target)
                    else:
                        sql = "DELETE FROM Enemy WHERE Name='"+target+"'"
                        cur.execute(sql)
                        print(""+target+" has died!")
                        get_health()
        
        else:
            print("You dont have "+weapon)
    else:
        print("There's no "+target)
    

    return

def weaponsafe(insert):
    insert = input("Please, insert a 4-digit passcode: ")
    if insert=='3293':
        cur = db.cursor()
        sql = "SELECT Id from location WHERE DETAILS = 'Main deck corridor 2. There is an open safe against the wall' AND Id ='2CORR2'"
        cur.execute(sql)
        if cur.rowcount >= 1:
            print("The safe is already open")
        else:
            sql2 = "UPDATE Item SET Available = TRUE , Takeable = TRUE WHERE Item.Id = 'RIFLE'"
            cur.execute(sql2)
            print("You unlock the safe. There is a rifle inside")
            sql3 = "UPDATE Location SET DETAILS = 'Main deck corridor 2. There is an open safe against the wall' WHERE Id = '2CORR2'"
            sql4 = "UPDATE Item SET DETAILS = 'This safe looks impossible to break' WHERE Id = 'safe'"
            cur.execute(sql3)
            cur.execute(sql4)
    elif insert!='3293':
        cur = db.cursor()
        sql = "SELECT Id from location WHERE DETAILS = 'Main deck corridor 2. There is an open safe against the wall' AND Id ='2CORR2'"
        cur.execute(sql)
        if cur.rowcount >= 1:
            print("The safe is already open")
        else:
            print("Error, wrong passcode")
    else:
        print("You cannot enter: '"+insert)

           
#Unlock
def unlock(item):
    item = input("Which item do you want to use? ")
    if item=='crowbar' and loc=='2CORR5':
        cur = db.cursor()
        sql = "SELECT ID From Item WHERE LocId='PLAYER' AND Item.Id ='"+item+"'"
        cur.execute(sql)
        if cur.rowcount>=1:
            sql = " SELECT Locked FROM Passage WHERE ID ='p12a' AND Locked=TRUE"
            cur.execute(sql)
            if cur.rowcount>=1:
                sql = "UPDATE PASSAGE SET Locked=FALSE WHERE ID='p12a' AND Locked=TRUE"
                cur.execute(sql)
                if cur.rowcount==1:
                    print("You slowly pry open the elevator door with the "+item+"")
            else:
                print("The elevator door is already open")
        else:
            print("You don´t have "+item)
    elif item=='keycard' and loc=='ELV3':
        cur = db.cursor()
        sql = "SELECT ID From Item WHERE LocId='PLAYER' AND Item.Id ='"+item+"'"
        cur.execute(sql)
        if cur.rowcount >=1:
            sql = " SELECT Locked FROM Passage WHERE ID ='p25a' AND Locked=TRUE"
            cur.execute(sql)
            if cur.rowcount>=1:
                sql = "UPDATE PASSAGE SET Locked=FALSE WHERE ID='p25a' AND Locked=TRUE"
                cur.execute(sql)
                if cur.rowcount==1:
                    print("You unlock the door with the "+item+"")
            else:
                print("The door is already unlocked")
        else:
            print("You don´t have "+item)
    elif item=='detonator':
        cur = db.cursor()
        sql = "SELECT Id From ITEM Where LocId='PLAYER' AND Item.Id = '"+item+"'"
        cur.execute(sql)
        if cur.rowcount >= 1:
            print("You decide to use the noisier method and blow up everyone. Good job!\n"
                  "Now, all that is left, is a chunk of space metal. Well, at least the aliens are gone now\n"
                  "GAME OVER!")
            cont=input("\nDo you want to restart the game? [y/n]")
            if cont=='y':
                db.rollback()
                start() 
            else:
                print("\nThe game will be closed...\n")
                quit()
        elif cur.rowcount == 0:
            print("You don´t have "+item)
    else:
        print("I don´t know what to use")
    return

                
      
#PLAYER'S INVENTORY
def inventory():
    cur = db.cursor()
    sql = "SELECT Description FROM Item INNER JOIN hero ON Item.LocId='PLAYER' AND Hero.Id=1 AND NOT Item.Id = 'Fists'"
    cur.execute(sql)
    if cur.rowcount>=1:
        print("You carry the following items:")
        for row in cur.fetchall() :
            print (" - " + row[0])
    else:
        print("You don't carry anything.")
    return
  
#MOVE FUNCTION
def move(loc, direction):
        destination=loc
        cur = db.cursor()
        sql = "SELECT Destination FROM PASSAGE WHERE Direction='" + direction + "' AND Source='" + loc + "' AND LOCKED=0"
        cur.execute(sql)
        if cur.rowcount>=1:
            for row in cur.fetchall():
                destination = row[0]
        else:
            destination = loc; # movement not possible
        return destination

#INSPECT ITEM IN INVENTORY
def look(target, loc):
    cur = db.cursor()
    sql = "SELECT Details FROM Item WHERE ItemtypeId='" + target + "' AND ((LocId='" + loc + "' OR LocId='PLAYER'))"
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall() :
            print (row[0])
    else:
        print("There's nothing to "+action+".\n")
    return

#SHOW PASSAGES
def look_around(loc):
    if (loc!="EXIT" or "EXIT2"):
        show_location(loc)
        show_passages(loc)
    elif loc=="EXIT" or "EXIT2":
        start()
    elif loc=="BRIDGE":
        print("")
    return

def healing():
    cur = db.cursor()
    sql = "SELECT Id FROM Item WHERE LocId = 'PLAYER' AND ItemtypeId='Medkit'"
    cur.execute(sql)
    if cur.rowcount>=1:
        cur = db.cursor()
        sql = "UPDATE hero set health = (SELECT HEALING from itemtype where name = 'Medkit')"
        cur.execute(sql)
        if cur.rowcount>=1:
            print("You have healed yourself to full hp")
    else:
        print("You don´t have anything to heal with")
    return

#SHOW ITEMS IN THE AREA
def items(loc):
    cur = db.cursor()
    sql = "SELECT Description FROM Item WHERE  ((LocId='" + loc + "' AND Available=TRUE AND Takeable=TRUE))"
    cur.execute(sql)
    if cur.rowcount>=2:
        print("There are items in the area: ")
        for row in cur.fetchall():
            print(" - " + row[0])
    elif cur.rowcount==1:
        print("You see an item: ")
        for row in cur.fetchall():
            print(" - " + row[0])
    else:
        print("There are no items in the area. ")
    return 

def inventory():
    cur = db.cursor()
    sql = "SELECT Description FROM Item INNER JOIN hero ON Item.LocId='PLAYER' AND Hero.Id=1 AND NOT Item.Id = 'Fists'"
    cur.execute(sql)
    if cur.rowcount>=1:
        print("You carry the following items:")
        for row in cur.fetchall() :
            print (" - " + row[0])
    else:
        print("You don't carry anything.")
    return

def spec_keyappears():
    cur = db.cursor()
    sql = "UPDATE Item SET Available=TRUE , Takeable = TRUE WHERE Itemtypeid='keycard' AND LocId='CAPTQ' AND Available=FALSE"
    cur.execute(sql)
    if cur.rowcount==1:
        print("You open the drawer. There's a keycard inside")    
    return

def spec_magboots():
    cur = db.cursor()
    sql = "UPDATE Item SET Available=FALSE LocId='PLAYER' WHERE Itemtypeid='Boots' AND LocId='2CORR5'"
    cur.execute(sql)
    if cur.rowcount==1:
        print("The corpse has magnetic boots. Those might be useful")    
    return

def deadcheck(target):
    cur = db.cursor()
    sql = "SELECT * FROM Enemy WHERE Name = '"+target+"'"
    cur.execute(sql)
    if cur.rowcount ==0 and loc=="REACT2":
        sql2 = "UPDATE Passage SET Locked = FALSE, Locknote = NULL WHERE Id = 'P19a'"
        cur.execute(sql2)
    return

def deadcheck2(target):
    cur = db.cursor()
    sql = "SELECT * FROM Enemy WHERE Name = '"+target+"'"
    cur.execute(sql)
    if cur.rowcount ==0 and loc=="ELV1":
        sql2 = "UPDATE Location SET Details = '' WHERE ID = 'ELV1'"
        sql3 = "UPDATE PASSAGE SET LOCKED = FALSE, Locknote = '' WHERE ID in('P23a', 'P15a', 'p13b')"
        cur.execute(sql2)
        cur.execute(sql3)
    else:
        print("")
    return

def deadcheck3(target):
    cur = db.cursor()
    sql = "SELECT * FROM Enemy"
    cur.execute(sql)
    if cur.rowcount == 0 and loc=="BRIDGE":
        print("You land the killing blow and the alien boss collapses to the floor. You have successfully and nearly single-handedly saved the day.\n"
                  "The captain has been saved and the ship still operational, you might have a chance to get to safety.\n"
                  "There is still much to do and many challenges to face, but now there is a chance.\n"
                  "Your journey continues, but that is a story for another time, and space\n"
                  "Game over!\n")
        win()
    return

def help_information():
    cur = db.cursor()
    sql = "SELECT Information, Description FROM helptable"
    cur.execute(sql)
    i = 0;
    print("-"*120)
    print("Available Commands:")
    for row in cur.fetchall():
        print(" - ",row[0]+": "+row[1])
        i = i+1
        if i == cur.rowcount:
            print("-"*120)


    return

def power_on():
    cur = db.cursor()
    sql = "UPDATE PASSAGE SET LOCKED = FALSE WHERE ID NOT IN ('P25A','P26A') ";
    cur.execute(sql)
    if cur.rowcount>=1:
        print("\nAs you enter the control room, you see electrical engineer Gerard Liebermann, the head of ship's maintenance, cowering in fear. After a brief moment he notices that it's you who entered the room.\n"
              "The engineer thanks you and turns on the main power for the ship.")
    else:
        print("\nThe engineer is still in awe of your bravery and greets you as you enter the control room. Alas, there is nothing left to do here.")
    return


def Escape():
    print("The door closes and you are ejected out of the spaceship in a small box. \n"
          "While drifting aimlessly away from the ship, you soon begin to realise that no one is ever going find you.\n"
          "GAME OVER!")
    cont=input("\nDo you want to restart the game? [y/n]")
    if cont=='y':
        db.rollback()
        start() 
    else:
        print("\nThe game will be closed...\n")
        quit()

    return

def win():
    cont=input("\nDo you want to restart the game? [y/n]")
    if cont=='y':
        db.rollback()
        start() 
    else:
        print("\nThe game will be closed...\n")
        quit()

    return

def lose():
    cont=input("\nDo you want to restart the game? [y/n]")
    if cont=='y':
        db.rollback()
        start()               
    else:
        print("\nThe game will be closed...\n")
        quit()


def throw(item):
    cur = db.cursor()
    sql = "SELECT Id FROM Item WHERE LocId = 'PLAYER' AND ItemtypeId='BOOTS'"
    cur.execute(sql)
    if cur.rowcount==1:
        item=input("Which item do you want to throw? ")
        if item == 'crowbar':
            print("The window breaks and the Alien is thrown out of the window\n"
            "The emergency doors shut the window and you are able to breath again\n")
            win()
        elif item!= 'crowbar':
            print("Your hesitation agitates the alien boss. If you don´t find a way out of this situation soon, it migh end badly")
            item=input("Which item do you want to throw? ")
            if item=='crowbar':
                print("The window breaks and the Alien is thrown out of the window\n"
                "The emergency doors shut the window and you are able to breath again\n")
                win()
            elif item=='':
                print("You decide to wave your hands like an idiot. In a blink of an eye, the life of both you, and the captain has been sucked out\n"
                        "Your space adventure ends here.\n"
                          "GAME OVER!\n")
                lose()
            else:
                print("You decide to throw '"+item+"' at the window, which really doesn't do anything\n"
                        "Standing there frozen, you look at the alien boss for the last time. In a blink of an eye, the life of both you, and the captain has been sucked out\n"
                        "Your space andenture ends here.\n"
                        "GAME OVER!\n")
                lose()
    elif cur.rowcount==0:
        item=input("Which item do you want to throw? ")
        if item == 'crowbar':
            print("You throw the crowbar at the window. It breaks instantly and before you even manage realise how dumb of a choice it was,\n"
                  "you get sucked out to the cold space.  Maybe next time you remember to take a pair of magnetic boots\n"
                  "or a safety tether with you, when you feel like going for a space walk.\n"
                  "GAME OVER!\n")
            lose()
        elif item!= 'crowbar':
            print("Your hesitation agitates the alien boss. If you don´t find a way out of this situation soon, it migh end badly")
            item=input("Which item do you want to throw? ")
            if item=='crowbar':
                print("You throw the crowbar at the window. It breaks instantly and before you even manage realise how dumb of a choice it was,\n"
                  "you get sucked out to the cold space.  Maybe next time you remember to take a pair of magnetic boots\n"
                  "or a safety tether with you, when you feel like going for a space walk.\n"
                    "GAME OVER!\n")
                lose()
            elif item=='':
                print("You decide to wave your hands like an idiot. In a blink of an eye, the life of both you, and the captain has been sucked out\n"
                        "Your space adventure ends here.\n"
                          "GAME OVER!\n")
                lose()
            else:
                print("You decide to throw '"+item+"' at the window, which really doesn't do anything\n"
                        "Standing there frozen, you look the alien boss for the last time. In a blink of an eye, the life of both you, and the captain has been sucked out\n"
                        "Your space andenture ends here.\n"
                        "GAME OVER!\n")
                lose()
    
    return


def spec_search():
    cur = db.cursor()
    sql = "SELECT Id FROM Item WHERE Available=FALSE AND Takeable=FALSE AND Id='BOOTS' or 'DETONATOR'"
    cur.execute(sql)
    if cur.rowcount>=1:
        sql = "UPDATE Item SET Available=TRUE, Takeable=TRUE WHERE Itemtypeid='Boots'"
        sql2 = "UPDATE Item SET Available=TRUE, Takeable=TRUE WHERE ItemtypeId='Detonator'"
        cur.execute(sql)
        cur.execute(sql2)
        print("You see a lifeless corpse of an alien. The other corpse, which seems to be human, has magnetic boots. Those might be useful.\n"
            "There is also an explosive device: A Thermal detonator. It looks dangerous")
    else:
        print("There is nothing to search")

    return
def loppu():
    cur = db.cursor()
    sql = "SELECT Locked FROM Passage WHERE Id='p26b' AND Locked=FALSE"
    cur.execute(sql)
    if cur.rowcount ==1:
        cur = db.cursor()
        sql = "UPDATE Passage SET Locked=TRUE WHERE Id='p26b'"
        cur.execute(sql)
        print("You enter the ship´s bridge. First you notice the captain, strapped in the chair. \n"
          "There´s a huge alien boss standing just a few feet away from you aiming his weapon at you and shouting weird things\n"
          "Suddendly you realise that you need to be fast in order to survive the situation.\n"
            "After assessing the situation briefly, your options seem to be:\n"
              "- Throw something to break the window\n"
              "- Shoot the alien boss\n"
              "- Maybe do nothing?\n")
        
    else:
        print("")
    return
        
    
    
          
def locknote(loc,action):
    cur = db.cursor()
    sql = "SELECT Locknote FROM PASSAGE INNER JOIN DIRECTION ON PASSAGE.Direction=DIRECTION.Id WHERE Source='" + loc + "' AND Direction='" +action+ "'"
    cur.execute(sql)
    for row in cur.fetchall() :
        print (row[0])

    return
    
    


#Open DB connection
db = mysql.connector.connect(host="localhost",
                             user="dbuser09",
                             passwd="dbpass",
                             db="androdb",
                             buffered=True)

# Initialize player location and starting weapon
loc = ""
action = ""
weapon = ""
item = ""
target = ""
sql = ""
insert = ""
print("\n"*10)


# Main loop

start()
help_information()

while action!="quit" and loc!="EXIT" or "EXIT2":


    print("")
    input_string=input("Your action? ").split()
    if len(input_string)>=1:
        action = input_string[0].lower()
    else:
        action = ""
    if len(input_string)>=2:
        target = input_string[len(input_string)-1].lower()
    else:
        target = ""
    print("")
    if action=="":
        print("Please, enter a proper command\n")
        help_information()
        
              
    # get
    elif (action=="get" or action=="take"):
        if target !="":
            get_target(target)
        else:
            print("What would you like to take?")

    elif action=="use":
            unlock(item)


       
    # look
    elif (action=="inspect" or action=="examine"):
        if target !="":
            look(target,loc)
        else:
            print("There is nothing to "+action)

    #items
    elif (action=="look" or action=="view"):
        if target=="":
            items(loc)
            look_around(loc)
        else:
            print("You can´t "+action+" at "+target+"!")

    # inventory
    elif action=="inventory" or action=="i":
        inventory()

    #movement
    elif action=="n" or action=="e" or action=="s" or action=="w" or action=="d" or action=="u":
        newloc = move(loc,action)
        if loc==newloc:
            print("You can't move to that direction.");
            locknote(loc,action)
        else:
            loc = newloc
            look_around(loc)
    
    elif action=="help" or action=="h":
        
        help_information()

    elif action=="health":
        get_health()

    elif action=="open" and loc=="CAPTQ":
        spec_keyappears()

    elif action=="hit" or action=="attack":
        if target !="":
            battle(target,loc)
            deadcheck(target)
            deadcheck2(target)
            deadcheck3(target)
        else:
            print("I don't want to be hit!")
    elif action=="throw":
        if loc=="BRIDGE":
            throw(item)
            newloc = "EXIT"
            loc = newloc
            look_around(loc)
        else:
            print("Don´t start throwing things")

    if loc=="CONTROL":
        power_on()

    elif loc=="BRIDGE":
        loppu()
        

    elif action =="push" or action=="press":
        if target=="button":
            Escape()
        elif target!="button":
            print("I can´t "+action+""+target)
        else:
            print("I don't want to "+action)

    elif action =="insert" and loc=="2CORR2":
        if target=="code" or target=="passcode":
            weaponsafe(insert)
        else:
            print("I do not know what you are implying")

    elif action=="search" and loc=="2CORR5":
        spec_search()

    elif action=="heal":
        healing()
        
    
print("goodbye!")        
db.rollback()
         





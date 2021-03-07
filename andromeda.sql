DROP DATABASE IF EXISTS andromeda;
DROP USER IF EXISTS dbuser09@localhost;
CREATE USER 'dbuser09'@'localhost' IDENTIFIED BY 'dbpass';
GRANT SELECT, INSERT, UPDATE, DELETE ON andromeda.* TO dbuser09@localhost;
CREATE DATABASE andromeda;
USE andromeda;

DROP TABLE IF EXISTS Passage;
DROP TABLE IF EXISTS Direction;
DROP TABLE IF EXISTS Enemy;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Itemtype;
DROP TABLE IF EXISTS Hero;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Helptable;
CREATE TABLE Location (
	ID Varchar(10) NOT NULL,
	DESCRIPTION VARCHAR(150),
	DETAILS VARCHAR(1000),
	PRIMARY KEY (ID)
);
CREATE TABLE Hero (
	ID INT NOT NULL,
	Name VARCHAR(40) NOT NULL,
	Health INT NOT NULL,
	Damage INT NOT NULL,
	locID Varchar(10) NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (locID) REFERENCES Location(ID)
);
CREATE TABLE Itemtype (
	ID VARCHAR(10) NOT NULL,
	Name VARCHAR(40) NOT NULL,
	Damage INT,
	Healing INT,
	PRIMARY KEY (ID)
);
CREATE TABLE Item ( 
	ID VARCHAR(10) NOT NULL,
	Description VARCHAR(100),
	Details VARCHAR(1000),
	ItemtypeId Varchar(10) NOT NULL,
	LocId VARCHAR(10),
	Available BOOLEAN,
	Takeable BOOLEAN,
	PRIMARY KEY (ID),
	FOREIGN KEY (ItemtypeId) REFERENCES Itemtype(ID),
	FOREIGN KEY (LocId) REFERENCES Location(ID)
	
);
CREATE TABLE Enemy (
	EnemyID VARCHAR(20) NOT NULL,
	Health VARCHAR(10),
	Name VARCHAR(10) NOT NULL,
	Damage INT NOT NULL,
	locID Varchar(10) NULL,
	FOREIGN KEY (locID) REFERENCES Location(ID),
	PRIMARY KEY(EnemyID)
);
CREATE TABLE DIRECTION (
	Id Varchar(10) NOT NULL,
	Description VARCHAR(40),
	PRIMARY KEY (ID)

);
CREATE TABLE PASSAGE (
	Id VARCHAR(10) NOT NULL,
	Source Varchar(10),
	Destination Varchar(10),
	Direction VARCHAR(10),
	Locked BOOLEAN,
	Locknote VARCHAR(80),
	PRIMARY KEY (Id),
	FOREIGN KEY (Source) REFERENCES Location(Id),
	FOREIGN KEY (Destination) REFERENCES Location(Id),
	FOREIGN KEY (Direction) REFERENCES Direction(Id)
);
CREATE TABLE Helptable (
    Information VARCHAR (1000),
    Description VARCHAR (1000)
);






INSERT INTO LOCATION VALUES ('PLAYER', 'Player', 'You');
INSERT INTO LOCATION VALUES ('START', 'Your cabin','Your own private cabin. Not that classy, but nevertheless functional');
INSERT INTO LOCATION VALUES ('CAPTQ', 'Captain´s Quarters.','There is a metallic table and drawer in the room');
INSERT INTO LOCATION VALUES ('CAFE', 'The Ship´s cafe.','There is a medical cabin hanging on the wall. It´s open');
INSERT INTO LOCATION VALUES ('LOCKER', 'Storage and Locker room.','A ship´s storage room. Small, but surprisingly spacious. A slightly odd smell lingers in the air');
INSERT INTO LOCATION VALUES ('BRIDGE', 'The Bridge.', 'The ship`s main bridge. This is where all the navigation and combat would be mainly handled.');
INSERT INTO LOCATION VALUES ('OFFICE', 'Captain´s Office.', '');
INSERT INTO LOCATION VALUES ('ELV1', 'Elevator Level 1', 'There is grunt in the elevator');
INSERT INTO LOCATION VALUES ('ELV2', 'Elevator Level 2', 'Cue the elevator music');
INSERT INTO LOCATION VALUES ('ELV3', 'Elevator Level 3', 'There is a keycard reader on the door ');
INSERT INTO LOCATION VALUES ('REACT1', 'Reactor room 1', 'Ship´s main reactor room. Reactor seems to be heavily shielded to prevent serious injuries. Handles energy production and transfers it to the propulsion systems');
INSERT INTO LOCATION VALUES ('REACT2', 'Reactor room 2', 'Ship´s secondary reactor room. There are a few monitors and a duckload of buttons. Low level access to reactor controls');
INSERT INTO LOCATION VALUES ('ENGROOM', 'Engine room', 'The ship´s main propulsion system. Seems fancy');
INSERT INTO LOCATION VALUES ('CONTROL', 'Control room', 'Maintenance of the and all the major computational systems and controls for reactor are located here');
INSERT INTO LOCATION VALUES ('ESCPODS', 'Escape pods', 'The ship´s evacuation center. This is the place if there´s a major emergency or a dispute with someone, which you can´t handle otherwise. There´s a control panel in the middle. There´s a button which has a text "eject" on it');
INSERT INTO LOCATION VALUES ('CABIN3', 'Cabin #3', 'A run-of-the-mill cabin. There seems to be only stale air in it');
INSERT INTO LOCATION VALUES ('CABIN4', 'Cabin #4', 'A cabin for one. Looks like someone messy resides here.');
INSERT INTO LOCATION VALUES ('CABIN5', 'Cabin #5', 'A cabin for two. A common cabin. Nothing of interest in here.');
INSERT INTO LOCATION VALUES ('2CORR1', 'LeveL 2 Corridor 1', 'Main deck corridor 1. The ship´s cafeteria is located to the west, locker and storage room is to the north and a cabin to the south with no discernible label or sign.');
INSERT INTO LOCATION VALUES ('2CORR2', 'LeveL 2 Corridor 2', 'Main deck corridor 2. There is a sturdy safe against the wall. It has a keypad on the front with buttons from 0 to 9.');
INSERT INTO LOCATION VALUES ('2CORR3', 'LeveL 2 Corridor 3', 'Main deck corridor 3. There´s cabin to the north: It has no label. Also there is a cabin to the south with a sign which says: "Cadet Jason Smith". Oh, a familiar name.');
INSERT INTO LOCATION VALUES ('2CORR4', 'LeveL 2 Corridor 4', 'Main deck corridor 4. To the north there is the captain´s quarters. There is a big sign which says: "Captain Sascha Stukova".');
INSERT INTO LOCATION VALUES ('2CORR5', 'LeveL 2 Corridor 5', 'Main deck corridor 5. There are 2 bodies lying on the floor. You should probably search them for useful items...');
INSERT INTO LOCATION VALUES ('1CORR1', 'LeveL 1 Corridor 1', 'Lower deck corridor 1. There is a room to the south. A label on the wall says: Escape vessel');
INSERT INTO LOCATION VALUES ('1CORR2', 'LeveL 1 Corridor 2', 'Lower deck corridor 2. Nothing much interesting here');
INSERT INTO LOCATION VALUES ('1CORR3', 'LeveL 1 Corridor 3', 'Lower deck corridor 3. Nothing else');
INSERT INTO LOCATION VALUES ('1CORR4', 'LeveL 1 Corridor 4', 'Lower deck corridor 4. Reactor room to the south and elevator to the east. There´s a corridor leading to west.');


INSERT INTO DIRECTION VALUES ('N', 'North');
INSERT INTO DIRECTION VALUES ('S', 'South');
INSERT INTO DIRECTION VALUES ('E', 'East');
INSERT INTO DIRECTION VALUES ('W', 'West');
INSERT INTO DIRECTION VALUES ('U', 'Up');
INSERT INTO DIRECTION VALUES ('D', 'Down');

INSERT INTO PASSAGE VALUES('p1a','START','2CORR3','N', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P1b','2CORR3','START','S', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P2a','2CORR2','CABIN4','S', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P2b','CABIN4','2CORR2','N', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P3a','2CORR3','2CORR2','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P3b','2CORR2','2CORR3','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P4a','2CORR2','2CORR1','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P4b','2CORR1','2CORR2','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P5a','2CORR1','CAFE','W', TRUE, "The door has no electricity");
INSERT INTO PASSAGE VALUES('P5b','CAFE','2CORR1','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P6a','2CORR1','LOCKER','N', FALSE, NULL);
INSERT INTO PASSAGE VALUES('p6b','LOCKER','2CORR1','S', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P7a','2CORR1','CABIN3','S', TRUE, "The door has no electricity");
INSERT INTO PASSAGE VALUES('P7b','CABIN3','2CORR1','N', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P8a','2CORR3','CABIN5','N', TRUE, "The door has no electricity");
INSERT INTO PASSAGE VALUES('P8b','CABIN5','2CORR3','S', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P9a','2CORR3','2CORR4','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P9b','2CORR4','2CORR3','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P10a','2CORR4','CAPTQ','N', TRUE, "The door has no electricity");
INSERT INTO PASSAGE VALUES('P10b','CAPTQ','2CORR4','S', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P11a','2CORR4','2CORR5','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P11b','2CORR5','2CORR4','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P12a','2CORR5','ELV2','E', TRUE, "The elevator door seems to be stuck, you might use something to open it");
INSERT INTO PASSAGE VALUES('P12b','ELV2','2CORR5','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P13a','ELV2','ELV1','D', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P13b','ELV1','ELV2','U', TRUE, "Can´t leave the combat!");
INSERT INTO PASSAGE VALUES('P14','ELV2','ELV3','U', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P15a','ELV1','1CORR4','W', TRUE, "Can´t leave the combat!");
INSERT INTO PASSAGE VALUES('P15b','1CORR4','ELV1','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P16a','1CORR4','1CORR3','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P16b','1CORR3','1CORR4','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P17a','1CORR4','REACT1','S', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P17b','REACT1','1CORR4','N', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P18a','REACT1','REACT2','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P18b','REACT2','REACT1','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P19a','REACT2','CONTROL','W', TRUE, "There´s an Alien blocking the way");
INSERT INTO PASSAGE VALUES('P19b','CONTROL','REACT2','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P20a','1CORR3','1CORR2','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P20b','1CORR2','1CORR3','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P21a','1CORR2','1CORR1','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P21b','1CORR1','1CORR2','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P22a','1CORR1','ESCPODS','S', TRUE, "There´s no electricity");
INSERT INTO PASSAGE VALUES('P22b','ESCPODS','1CORR1','N', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P23a','ELV1','ENGROOM','E', TRUE, "Can´t leave the combat!");
INSERT INTO PASSAGE VALUES('P23b','ENGROOM','ELV1','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P24b','ELV3','ELV2','D', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P25a','ELV3','OFFICE','W', TRUE, "You need a keycard for the door");
INSERT INTO PASSAGE VALUES('P25b','OFFICE','ELV3','E', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P26a','OFFICE','BRIDGE','W', FALSE, NULL);
INSERT INTO PASSAGE VALUES('P26b','BRIDGE','OFFICE','E', TRUE, "You can´t leave this fight, the captain needs you!");

INSERT INTO HERO VALUES('1','Player','200','0','START');


INSERT INTO ITEMTYPE VALUES('CROWBAR', 'Crowbar', '10','0');
INSERT INTO ITEMTYPE VALUES('RIFLE', 'Laser rifle', '50','0');
INSERT INTO ITEMTYPE VALUES('PISTOL', 'Plasma pistol', '35','0');
INSERT INTO ITEMTYPE VALUES('DETONATOR', 'Thermal detonator', '500','0');
INSERT INTO ITEMTYPE VALUES('MEDKIT', 'Medkit','0','200');
INSERT INTO ITEMTYPE VALUES('BOOK', 'A Book','0','0');
INSERT INTO ITEMTYPE VALUES('KEYCARD', 'Keycard','0','0');
INSERT INTO ITEMTYPE VALUES('BOOTS', 'Magnetic boots','0','0');
INSERT INTO ITEMTYPE VALUES('DRAWER', 'Drawer','0','0');
INSERT INTO ITEMTYPE VALUES('CORPSE', 'Corpse','0','0');
INSERT INTO ITEMTYPE VALUES('ELEDOOR','Elevator door','0','0');
INSERT INTO ITEMTYPE VALUES('FISTS','Bare Fists','5','0');
INSERT INTO ITEMTYPE VALUES('NOTE','Simple paper note','0','0');
INSERT INTO ITEMTYPE VALUES('GERARD','Electrical engineer','0','0');
INSERT INTO ITEMTYPE VALUES('SAFE','Weapon safe','0','0');

INSERT INTO ITEM VALUES('CROWBAR','A Futuristic crowbar','A tool that can be used to open jammed doors.', 'CROWBAR', 'LOCKER', TRUE,TRUE);
INSERT INTO ITEM VALUES('PISTOL','A Pistol','A basic personal sidearm that shoots hot plasma. Nimble and deals respectable amount of damage','PISTOL','START',TRUE,TRUE);
INSERT INTO ITEM VALUES('RIFLE','An assault rifle','A strong rifle that shoots laser projectiles. Can be used to decimate enemies','RIFLE','2CORR2',FALSE,FALSE);
INSERT INTO ITEM VALUES('DETONATOR','Extremely strong explosive','There´s text on the side which says: do not use this item','DETONATOR','2CORR5',FALSE,FALSE);
INSERT INTO ITEM VALUES('MEDKIT','A Medkit','A strong healing item. Can be used to heal yourself','MEDKIT','CAFE',TRUE,TRUE);
INSERT INTO ITEM VALUES('BOOK','A book, looks like a diary.','After browsing the diary you learn some facts about her: Born somewhere in Siberia. She was able to move to Moscow after hunting bears and selling their pelts for many years. She enlisted for the Russian Space Flight Academy. She graduated at the age of 25 and is now 33 years old. She got bored of the mundane life in the academy, so she decided to volunteer for this new mission to Andromeda.','BOOK','CAPTQ',TRUE,TRUE);
INSERT INTO ITEM VALUES('KEYCARD','A Keycard for office','Can be used to unlock the door which leads to the ship´s office and bridge','KEYCARD','CAPTQ',FALSE,FALSE);
INSERT INTO ITEM VALUES('BOOTS','A Magnetic boots','These are used to lock you into the ships hull','BOOTS','2CORR5',FALSE,FALSE);
INSERT INTO ITEM VALUES('DRAWER', 'A metallic drawer', 'It is a drawer.', 'DRAWER','CAPTQ', TRUE,FALSE);
INSERT INTO ITEM VALUES('CORPSE', 'A human body', 'The body seems to be lifeless and cold to the touch.', 'CORPSE','2CORR5', TRUE,FALSE);
INSERT INTO ITEM VALUES('ELEDOOR','An elevator door','The door is shut','ELEDOOR','2CORR5',FALSE,FALSE);
INSERT INTO ITEM VALUES('FISTS','A tasty knuckle sandwich','Your own fists','FISTS','PLAYER',FALSE,FALSE);
INSERT INTO ITEM VALUES('NOTE','A Note to Jim','The note reads: Jim you forgot to change the combination for the weapon safe. Use my emergency key for it: 3293 -Steve','NOTE','LOCKER',TRUE,TRUE);
INSERT INTO ITEM VALUES('GERARD','Electrical Engineer Gerard Liebermann','A 34-year-old electrical engineer. Born in Germany. Nothing much is known of him, except that he enjoys being alone and is the main person responsible of maintenance of the ship. He keeps the ship’s reactors and electrical systems running.','GERARD','CONTROL',TRUE,FALSE);
INSERT INTO ITEM VALUES('SAFE','A Weapon safe','This safe looks impossible to break. You may try unlocking it by inserting passcode', 'SAFE', '2CORR2', FALSE,FALSE);

INSERT INTO ENEMY VALUES('1','100','Alien','25','REACT2');
INSERT INTO ENEMY VALUES('2','100','Grunt','25','ELV1');
INSERT INTO ENEMY VALUES('3','200','Boss','50','BRIDGE');


INSERT INTO HELPTABLE VALUES('help / h','Opens up the help table');
INSERT INTO HELPTABLE VALUES('look / view','Look around');
INSERT INTO HELPTABLE VALUES('hit / attack (enemyname)','Attacks the defined target enemy');
INSERT INTO HELPTABLE VALUES('examine / inspect (item)','Shows additional info about the item');
INSERT INTO HELPTABLE VALUES('open','Usable in certain situations');
INSERT INTO HELPTABLE VALUES('use','This command will use an item.');
INSERT INTO HELPTABLE VALUES('take (item)','This command will pickup an item');
INSERT INTO HELPTABLE VALUES('health','Shows the health you have left');
INSERT INTO HELPTABLE VALUES('heal','Heals yourself to full hp (200), if you have a medkit');
INSERT INTO HELPTABLE VALUES('n,w,e,s,d,u','Player movement, (n)orth (w)est (e)ast (s)outh (d)own (u)p');
INSERT INTO HELPTABLE VALUES('search','You can search certain areas for objects');
INSERT INTO HELPTABLE VALUES('insert code / passcode','You can insert a passcode on a numpad')
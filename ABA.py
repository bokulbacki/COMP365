"""
Name: ABA.py
Date: 4/18/2021
Author: Quinn Bigane, Tom Padova, Bo Kulbacki
Description: This is a secure implementation of an Address Book database 
"""
import datetime 
import re

class Address_record:
    def __init__(self, recordID, SN='', GN='', PEM='', WEM='', PPH='', WPH='', SA='', CITY='', STP='', CTY='', PC=''):
        self.recordID = recordID
        self.SN = SN
        self.GN = GN
        self.PEM = PEM
        self.WEM = WEM
        self.PPH = PPH
        self.WPH = WPH
        self.SA = SA
        self.CITY = CITY
        self.STP = STP
        self.CTY = CTY
        self.PC = PC
        
class Address_Book:
    def __init__(self, login_state = 0,current_user = None):
        #0 = not logged in
        #1 = logged in
        self.login_state = login_state
        
        self.driver()
    
    def driver(self):
            
        """
        Main looping module of the function, waits for user input
        """  
        print("Address Book Application, version 1.0. Type “HLP” for a list of commands") #print this when the program first starts
         
        while(1):
            #prompt user to enter a command
            command = input("ABA > ")
            self.command_line_interpreter(command)

    def command_line_interpreter(self, command):
        """
        Interprets user input and decides what to do based on that
        """   
        #parse command entered on spaces
        self.tokens = None
        self.tokens = command.split(" ")

        #based on commanded entered, decide next step
        if self.tokens[0] == "HLP": #help
            self.display_help()
        elif self.tokens[0] == "LIN": #login
            self.login()
        elif self.tokens[0] == "LOU": #logout
            self.logout()
        elif self.tokens[0] == "CHP": #change password
            self.change_password()
        elif self.tokens[0] == "ADU": #add user
            self.add_user()
            pass
        elif self.tokens[0] == "DEU": #delete user
            self.delete_user()
            pass
        elif self.tokens[0] == "LSU": #list users
            self.list_users()
        elif self.tokens[0] == "DAL": #display audit log
            self.display_audit_log()
            pass
        elif self.tokens[0] == "ADR": #add record
            self.add_record()
        elif self.tokens[0] == "DER": #delete record
            self.delete_record()
            pass
        elif self.tokens[0] == "EDR": #edit record
            self.edit_record()
            pass
        elif self.tokens[0] == "GER": #get record
            self.get_record()
            pass
        elif self.tokens[0] == "IMD": #import database
            self.import_database()
        elif self.tokens[0] == "EXD": #export database
            self.export_database()
        elif self.tokens[0] == "EXT": #exit
            self.exit()
        else:
            print("Unrecognized command")
    
    def exit(self):
        """
        Exits ABA
        """    
        exit()

    def login(self):
        """
        Verifies user login credentials based on a database of login info
        """  
        #TODO: Add error handling if user does not enter a username with LIN
        username = self.tokens[1]
        infile = open("logininfo.txt", "r")

        #if there is currently an active login
        if self.login_state != 0: 
            print("An account is currently active; logout before proceeding")
        

        #if there is no currently active login
        else:
            #loop through all login data
            lines = infile.readlines()
            for i in range(len(lines)):
                toks = lines[i].split(",")
                #matching username found
                if toks[0].rstrip() == username:
                    #no password associated with username
                    if len(toks) == 1: 
                        new_password = input("This is the first time the account is being used. You must create a new password. Passwords may contain 1-24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.")
                        pw_confirmation = input("Reenter the same password: ")
                        #TODO: add error handling if user does not meet password specifications
                        if new_password != pw_confirmation:
                            print("Passwords do not match")
                            infile.close()
                            self.add_to_audit_log("LF")
                            return
                        else:
                            lines[i] = lines[i].rstrip() + "," + new_password + "\n"
                            infile = open("logininfo.txt", "w")
                            infile.writelines(lines)
                            infile.close()
                            print("OK")
                            self.current_user = toks[0]
                            self.login_state = 1
                            infile.close()
                            self.add_to_audit_log("L1")
                            self.add_to_audit_log("LS")
                            return
                    #username has a password
                    else:
                        password = toks[1].rstrip() #users's password
                        password_guess = input("Enter your password: ")
                        if password == password_guess: #correct password entered
                            #set current user variables
                            self.current_user = toks[0]
                            self.login_state = 1
                            print("OK")
                            infile.close()
                            self.add_to_audit_log("LS")
                            return
            infile.close()
            print("Invalid credentials")
            self.add_to_audit_log("LF")    

    def logout(self):
        """
        Logs out current user
        """
        if self.login_state == 0: #no active login session
            print("No active login session")

        else:
            self.login_state = 0
            self.add_to_audit_log("LO")
            self.current_user = None
            print("OK")
 
    def change_password(self):
        """
        Logs out current user
        """ 
        if self.login_state == 0: #no active login session
            print("No active login session")
            self.add_to_audit_log("FPC") #if failed password change
            return 

        infile = open("logininfo.txt", "r")
        lines = infile.readlines()
        for i in range(len(lines)):
                toks = lines[i].split(",")
                #matching username found
                if toks[0].rstrip() == self.current_user:
                    if toks[1].rstrip() == self.tokens[1]:
                        new_password = input("Create a new password. Passwords may contain up to 24 upper- or lower-case letters or numbers. Choose an uncommon password that would be difficult to guess.\n")
                        pw_confirmation = input("Reenter the same password: ")
                        #TODO: add error handling if user does not meet password specifications
                        if new_password != pw_confirmation:
                            print("Passwords do not match")
                            infile.close()
                            self.add_to_audit_log("FPC")
                            return
                        else:
                            lines[i] = toks[0].rstrip() + "," + new_password + "\n"
                            infile = open("logininfo.txt", "w")
                            infile.writelines(lines)
                            infile.close()
                            print("OK")
                            self.current_user = toks[0]
                            self.login_state = 1
                            infile.close()
                            self.add_to_audit_log("SPC")
                            return
                    else: 
                        print("Invalid credentials")
                        self.add_to_audit_log("FPC")
                        return
    
    def list_users(self):
        """
        Display Users
        """          
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if the admin is not logged in
        if self.current_user != "admin":
            print("Admin not active")
            return
        #if the admin is logged in
        infile = open("logininfo.txt", "r")
        lines = infile.readlines()
        for i in range(len(lines)):
            toks = lines[i].split(",")
            #if a matching username is found
            print(toks[0].rstrip())
        infile.close()
        print("Ok")

    def display_help(self):
        """
        Displays the help commands
        """    
        if len(self.tokens) == 2:
            if self.tokens[1] == "HLP": #help
                print("HLP [<command name>]")
            elif self.tokens[1] == "LIN": #login
                print("LIN <userID>")
            elif self.tokens[1] == "LOU": #logout
                print("LOU")
            elif self.tokens[1] == "CHP": #change password
                print("CHP <old password>")
            elif self.tokens[1] == "ADU": #add user
                print("ADU <userID>")
            elif self.tokens[1] == "DEU": #delete user
                print("DEU <userID>")
            elif self.tokens[1] == "LSU": #list users
                print("LSU")
            elif self.tokens[1] == "DAL": #display audit log
                print("DAL [<userID>]")
            elif self.tokens[1] == "ADR": #add record
                print("ADR <recordID> [<field1=value1> <field2=value2> ...]")
            elif self.tokens[1] == "DER": #delete record
                print("DER <recordID>")
            elif self.tokens[1] == "EDR": #edit record
                print("EDR <recordID> <field1=value1> [<field2=value2> ...]")
            elif self.tokens[1] == "GER": #get record
                print("GER [<recordID>] [<fieldname> ...]")
            elif self.tokens[1] == "IMD": #import database
                print("IMD <Input_File>")
            elif self.tokens[1] == "EXD": #export database
                print("EXD <Output_file>")
            elif self.tokens[1] == "EXT": #exit
                print("EXT")
            else:
                print("LIN <userID>")
                print("LOU")
                print("CHP <old password>")
                print("ADU <userID>")
                print("DEU <userID>")
                print("LSU")
                print("DAL [<userID>]")
                print("ADR <recordID> [<field1=value1> <field2=value2> ...]")
                print("DER <recordID>")
                print("EDR <recordID> <field1=value1> [<field2=value2> ...]")
                print("GER [<recordID>] [<fieldname> ...]")
                print("IMD <Input_File>")
                print("EXD <Output_file>")
                print("HLP [<command name>]")
                print("EXT")
        
        else: #if user only entered HLP or an incorrect command
            print("LIN <userID>")
            print("LOU")
            print("CHP <old password>")
            print("ADU <userID>")
            print("DEU <userID>")
            print("LSU")
            print("DAL [<userID>]")
            print("ADR <recordID> [<field1=value1> <field2=value2> ...]")
            print("DER <recordID>")
            print("EDR <recordID> <field1=value1> [<field2=value2> ...]")
            print("GER [<recordID>] [<fieldname> ...]")
            print("IMD <Input_File>")
            print("EXD <Output_file>")
            print("HLP [<command name>]")
            print("EXT")

        print("OK")

    def import_database(self):
        """
        Imports a database
        """
        #TODO: check formatting of records being input
        if self.login_state == 0: #no active login
            print("No active login session")
            return
        if self.current_user == "admin": #admin user currently logged in
            print("Admin not authorized")
            return
        if len(self.tokens) < 2: #no input file specified
            print("No Input_file specified")
            return
        
        try:
            infile = open(self.tokens[1], "r")
        except OSError: #if file cannot be opened
            print("Can’t open Input_file")
            return
            
        #check file format
        for line in infile:
            num_semicolons = 0
            for char in line:
                if char == ";":
                    num_semicolons += 1
            
            #might be a better way to validate the file is in the correct format
            if num_semicolons != 11:
                print(num_semicolons)
                print("Input_file invalid format")
                return
            
            toks = line.split(";")
            recordID = toks[0]

            if self.check_recordID(recordID) == 1:
                print("Duplicate recordID")
                return

        infile.close()
        infile = open(self.tokens[1], "r")

        #count number of records that are attempting to be inputted
        new_records = 0
        for line in infile:
            new_records += 1    
        
        #count the # of records in the user's database already and store in num_records_in_db (maybe a self. variable?)
        num_records_in_db = self.count_records()
        if num_records_in_db + new_records > 256:
           print("Number of records exceeds maximum")
           return

        infile.close()
        infile = open(self.tokens[1], "r")

        #add each record to the user's database
        for line in infile:
            line.rstrip()
            self.tokens = line.split(";")
            self.add_record_from_import()   

        infile.close()
        return
        
    def count_records(self):
        """
        Returns the number of records stored in a user's database.
        """

        try:
            infile = open((self.current_user + ".txt"), "r")

            num_records = 0
            for line in infile:
                num_records += 1

            infile.close()
            return num_records
        except OSError: #if file cannot be opened
            return 0

    def check_recordID(self, recordID):
        """
        Checks a user's database for recordID and returns 0 if the recordID 
        is not in the user’s database and 1 if it already exists
        """
        #loop through all lines of user text file and checks to see if recordID is 
        # the same as any of the ones in the text file 
        try:
            f = open((self.current_user + ".txt"), "r")
            for line in f:
                tokens = line.split(";")
                if (recordID == tokens[0]):
                    f.close() 
                    return 1
            return 0        
        except OSError: #if file cannot be opened
            return 0

    def export_database(self):
        """
        Exports current user database 
        """ 
        if self.login_state == 0: #no active login
            print("No active login session")
            return
        if self.current_user == "admin": #admin user currently logged in
            print("Admin not authorized")
            return
        if len(self.tokens) < 2: #no input file specified
            print("No Output_file specified")
            return
        
        try:
            outfile = open(self.tokens[1], "a")
        except OSError: #if file cannot be opened
            print("Can’t open Output_file")
            return
        
        infile = open((self.current_user + ".txt"), 'r')
        
        try:
            for line in infile:
                outfile.write(line)
        except Exception: #error writing to file
            print("Error writing Output_file")
        
        outfile.close()
        
        print("OK")
        return       

    def add_record(self):
        """
        Adds a new record for user
        """ 
        #TODO: check formatting of records being input
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        if self.current_user == "admin":
            print("Admin not authorized")
            return

        if (self.check_recordID(self.tokens[1]) == 0):
                for entry in self.tokens[1:]:
                    if (len(entry) > 64):
                        print("One or more invalid record data fields")
                        return
                if (self.count_records() > 255):
                    print("Number of records exceeds maximum") 
                    return
                if (len(self.tokens[1])>16):
                    print("Invalid recordID")
                    return 

                newRecord = Address_record(self.tokens[1])
                #clean the input commands
                self.tokens = " ".join(self.tokens[2:])
                self.tokens = self.tokens.split('" ')  
                self.tokens[-1] = self.tokens[-1][0:-2]   

                for entry in self.tokens:#searches tokens 0 to end 
                    command = entry[0:entry.index("=")] #the command which will be entered
                    #check for less than 64 characters 
                    #num of records < 256
                    if (command == "SN"):
                        newRecord.SN = entry[entry.index("=")+2:]
                    elif(command == "GN"):
                        newRecord.GN = entry[entry.index("=")+2:]
                    elif(command =="PEM"):
                        newRecord.PEM = entry[entry.index("=")+2:]
                    elif (command =="WEM"):
                        newRecord.WEM = entry[entry.index("=")+2:]
                    elif(command=="PPH"):
                        newRecord.PPH = entry[entry.index("=")+2:]
                    elif(command=="WPH"):
                        newRecord.WPH = entry[entry.index("=")+2:]
                    elif (command=="SA"):
                        newRecord.SA = entry[entry.index("=")+2:]
                    elif (command=="CITY"):
                        newRecord.CITY = entry[entry.index("=")+2:]
                    elif (command=="STP"):
                        newRecord.STP = entry[entry.index("=")+2:]
                    elif (command =="CTY"):
                        newRecord.CTY = entry[entry.index("=")+2:]
                    elif (command =="PC"):
                        newRecord.PC = entry[entry.index("=")+2:]
                    
                    else:
                        print("Invalid entry. Please try to add record again.")
                        return
                #newRecord is added to the user's personal database 
                f = open((self.current_user + ".txt"), "a")#"a" for appending to textfile so not to erase data
                f.write(newRecord.recordID+";"+newRecord.SN+";"+newRecord.GN+";"+newRecord.PEM+";"+newRecord.WEM+";"+
                newRecord.PPH+";"+newRecord.WPH+";"+newRecord.SA+";"+newRecord.CITY+";"+newRecord.STP+";"+
                newRecord.CTY+";"+newRecord.PC+"\n")
                f.close()
                print("OK")
                return
            
        else: 
            print("Duplicate recordID")
            return

    def add_record_from_import(self):
        """
        Adds a new record for user
        """ 
            
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        if self.current_user == "admin":
            print("Admin active")
            return

        if (self.check_recordID(self.tokens[0]) == 0):
            for entry in self.tokens[0:]:
                if (len(entry) > 64):
                    print("One or more invalid record data fields")
                    return
            if (self.count_records() > 255):
                print("Number of records exceeds maximum")
                return
            if (len(self.tokens[0])>16):
                print("Invalid recordID")
                return                 
                
            newRecord = Address_record(self.tokens[0])
    
            newRecord.SN = self.tokens[1]     
            newRecord.GN = self.tokens[2] 
            newRecord.PEM = self.tokens[3]                   
            newRecord.WEM = self.tokens[4]                    
            newRecord.PPH = self.tokens[5]    
            newRecord.WPH = self.tokens[6]
            newRecord.SA = self.tokens[7]
            newRecord.CITY = self.tokens[8]
            newRecord.STP = self.tokens[9]
            newRecord.CTY = self.tokens[10]
            newRecord.PC = self.tokens[11].rstrip()
                        
            #newRecord is added to the user's personal database 
            f = open((self.current_user + ".txt"), "a")#"a" for appending to textfile so not to erase data
            f.write(newRecord.recordID+";"+newRecord.SN+";"+newRecord.GN+";"+newRecord.PEM+";"+newRecord.WEM+";"+
            newRecord.PPH+";"+newRecord.WPH+";"+newRecord.SA+";"+newRecord.CITY+";"+newRecord.STP+";"+
            newRecord.CTY+";"+newRecord.PC+"\n")
            f.close()
                
        else: 
            print("Duplicate recordID")
            return
    
    def delete_record(self):
        """
        Deletes a record from the database
        """ 
        if self.login_state == 0: 
            print("No active login session")
            return
        if self.current_user == "admin":
            print("Admin not authorized")
            return
        
        if self.tokens[1] == None:
            print("No recordID")
            return
        if (len(self.tokens[1])) >64:
            print("Invalid recordID")
            return

        if (self.check_recordID(self.tokens[1]) == 0):
            print("RecordID not found")
            return

        else:
            #delete it
            f = open((self.current_user + ".txt"), "r")
            lines = f.readlines()
            for i in range(len(lines)):
                tokens = lines[i].split(";")
                if (tokens[0] == self.tokens[1]):
                    lines[i] = ""
                    f.close()
                    outFile = open((self.current_user + ".txt"), "w")
                    outFile.writelines(lines)
                    outFile.close()
                
            print("OK") 
            return   
  
    def edit_record(self):
        """
        Edits a record from the database
        """  

        if self.login_state == 0: 
            print("No active login session")
            return
        if self.current_user == "admin":
            print("Admin not authorized")
            return
        
        if self.tokens[1] == None:
            print("No recordID")
            return
        if (len(self.tokens[1])) >64:
            print("Invalid recordID")
            return
        if (self.check_recordID(self.tokens[1]) == 0):
            print("RecordID not found")
            return
        else:
            #edit it
            for entry in self.tokens[0:]:
                if (len(entry) > 64):
                    print("One or more invalid record data fields")
                    return



            f = open((self.current_user + ".txt"), "r")
            #lines is arry of all lines in current_user.txt
            lines = f.readlines()
            #loops through all lines
            #splits tokens in each line by ";"
            #tokens[0] = recordID
            for i in range(len(lines)):
                tokens = lines[i].split(";") 
                #if recordID from textfile is the same as the given recordID
                if (tokens[0] == self.tokens[1]):
                    
                    #clean the input commands
                    self.tokens = " ".join(self.tokens[2:])
                    self.tokens = self.tokens.split('" ')
                    
                    for entry in self.tokens:
                        command = entry[0:entry.index("=")] #the command which will be entered
                        #check for less than 64 characters 
                        #num of records < 256
                        
                        if (command == "SN"):
                            tokens[1] = entry[entry.index("=")+2:]
                        elif(command == "GN"):
                            tokens[2] = entry[entry.index("=")+2:]
                        elif(command =="PEM"):
                            tokens[3] = entry[entry.index("=")+2:]
                        elif (command =="WEM"):
                            tokens[4] = entry[entry.index("=")+2:]
                        elif(command=="PPH"):
                            tokens[5] = entry[entry.index("=")+2:]
                        elif(command=="WPH"):
                            tokens[6] = entry[entry.index("=")+2:]
                        elif (command=="SA"):
                            tokens[7] = entry[entry.index("=")+2:]
                        elif (command=="CITY"):
                            tokens[8] = entry[entry.index("=")+2:]
                        elif (command=="STP"):
                            tokens[9] = entry[entry.index("=")+2:]
                        elif (command =="CTY"):
                            tokens[10] = entry[entry.index("=")+2:]
                        elif (command =="PC"):
                            tokens[11] = entry[entry.index("=")+2:]
                        else:
                            print("One or more invalid record data fields")
                    lines[i] = (tokens[0]+";"+ tokens[1]+";"+ tokens[2]+";"+ tokens[3]+";"+ tokens[4]+";"+ 
                    tokens[5]+";"+ tokens[6]+";"+ tokens[7]+";"+ tokens[8]+";"+ tokens[9]+";"+ tokens[10]+";"+ 
                    tokens[11])
                    
                    f.close()
                    outFile = open((self.current_user + ".txt"), "w")
                    outFile.writelines(lines)
                    outFile.close()
                        
                    print("OK") 
                    return
                    
                
            f.close()
            print("RecordID not found")      
            return         
    
    def get_record(self): 
        """
        Gets a record from the database 
        """
        if self.login_state == 0: 
            print("No active login session")
            return
        if self.current_user == "admin":
            print("Admin not authorized")
            return
        
        if self.tokens[1] == None:
            print("No recordID")
            return
        if (len(self.tokens[1])) >64:
            print("Invalid recordID")
            return

        if (self.check_recordID(self.tokens[1]) == 0):
            print("RecordID not found")
            return
        
        #print all elements 
        if (len(self.tokens)<=2):
            f = open((self.current_user + ".txt"), "r")
            lines = f.readlines()
            for i in range(len(lines)):
                tokens = lines[i].split(";")
                if (tokens[0] == self.tokens[1]):
                    print(tokens[0] + " SN="+tokens[1] +" GN="+tokens[2] +" PEM="+tokens[3] +" WEM="+tokens[4] 
                    +" PPH="+tokens[5] +" WPH="+tokens[6] +" SA="+tokens[7] +" CITY="+tokens[8] +" STP="+tokens[9]
                    +" CTY="+tokens[10] +" PC="+tokens[11].rstrip())
            f.close()
            print("OK")
            return

        else:
            f = open((self.current_user + ".txt"), "r")
            lines = f.readlines()
            for i in range(len(lines)):
                tokens = lines[i].split(";")
            #field is valid
            outputValue=self.tokens[1] + " "
            for i in range(2,len(self.tokens)):
                #i and loop through all self.tokens
                if (self.tokens[i] == "SN"): 
                    outputValue + "SN="+ tokens[1]+" "
                if self.tokens[i] == "GN":
                    outputValue + "GN="+ tokens[2]+" "
                if self.tokens[i] == "PEM":
                    outputValue + "PEM="+ tokens[3]+" "
                if self.tokens[i] == "WEM":
                    outputValue + "WEM="+ tokens[4]+" "
                if self.tokens[i] == "PPH":
                    outputValue + "PPH="+ tokens[5]+" "
                if self.tokens[i] == "WPH":
                    outputValue + "WPH="+ tokens[6]+" "
                if self.tokens[i] == "SA":
                    outputValue + "SA="+ tokens[7]+" "
                if self.tokens[i] == "CITY":
                    outputValue + "CITY="+ tokens[8]+" "
                if self.tokens[i] == "STP":
                    outputValue + "STP="+ tokens[9] +" "
                if self.tokens[i] == "CTY":
                    outputValue + "CTY="+ tokens[10] +" "
                if self.tokens[i] == "PC":
                    outputValue + "PC="+ tokens[11].rstrip +" "

                else:
                    #field invalid
                    print("Invalid fieldname (s)")
                    return

            print(outputValue)
            f.close()
            return
              
        
        
        # if self.login_state == 0: 
        #     print("No active login session")
        #     return
        # if self.current_user == "admin":
        #     print("Admin not authorized")
        #     return
        
        # #if self.tokens[1] == None:
        # #    print("No recordID")
        # #    return
        
        # if (len(self.tokens[1])) >64:
        #     print("Invalid recordID")
        #     return

        # if (check_recordID(self.recordID)==0)
        # {
           
        # }

        # #TODO: Invalid fieldname(s)

        # if (self.check_recordID(self.tokens[1]) == 0):
        #     print("RecordID not found")
        #     return 
    
    def display_audit_log(self):
        """
        Displays the audit log 
        """   
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if the admin is not logged in
        if self.current_user != "admin":
            print("Admin not active")
            return
        #if the admin is logged in
        auditlog = open("audit_log.csv", "r")
        for line in auditlog:
            print(line.rstrip())  
    
    def delete_user(self):
        """
        Deletes a user from the Address Book
        """  
        #TODO: dont let admin delete himself?

        username = self.tokens[1]
        
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if the admin is not logged in
        if self.current_user != "admin":
            print("Admin not active")
            return
        #if the admin is logged in
        infile = open("logininfo.txt", "r")
        lines = infile.readlines()
        for i in range(len(lines)):
            toks = lines[i].split(",")
            #if a matching username is found
            if toks[0].rstrip() == username:
                #delete it
                lines[i] = ""
                infile = open("logininfo.txt", "w")
                infile.writelines(lines)
                infile.close()
                print("Ok")
                self.add_to_audit_log("DU")
                return
        infile.close()
        print("Invalid userID")

    def add_user(self):
        """
        Adds a new user to the Address Book
        """   
        #TODO: dont let admin add more admins

        username = self.tokens[1]
        
        #if there is currently an active login
        if self.login_state == 0: 
            print("No active login session")
            return
        #if the admin is not logged in
        if self.current_user != "admin":
            print("Admin not active")
            return
        #if the admin is logged in
        infile = open("logininfo.txt", "r")
        lines = infile.readlines()
        for i in range(len(lines)):
            toks = lines[i].split(",")
            #if a matching username is found
            if toks[0].rstrip() == username:
                #do not add it
                infile.close()
                print("Account already exists")
                return
        #if account does not exist
        infile = open("logininfo.txt", "a")
        infile.write(username + "\n")
        infile.close()
        self.add_to_audit_log("AU")
        print("Ok")

    def add_to_audit_log(self, audit_type):
        #TODO: implement circualr aspect of audit log
        auditlog = open("audit_log.csv", "a")
        e = datetime.datetime.now()
        auditlog.write(str(e.day) +"-"+ str(e.month) +"-"+  str(e.year) + "," +
            str(e.hour) +":"+ str(e.minute) +":"+ str(e.second) + "," +
            audit_type + "," + str(self.current_user) + "\n")      
        auditlog.close()

        

if __name__ == "__main__":
    Address_Book()

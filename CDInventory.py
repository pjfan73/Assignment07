#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# jstevens, 2020-Feb-25, created functions
# jstevens, 2020-Mar-02, finished docstrings and comments
# jstevens, 2020-Mar-15, added pickle and error handling
#------------------------------------------#

import pickle
import sys

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileNamed = 'CDInventory.dat'  # data storage file
saveFlag = 0    # save flag

# -- PROCESSING -- #
class DataProcessor:
    """Processing the data during runtime"""
 
    @staticmethod
    def write_row (idn, title, artist, table):
        """Function to write data as one dictionary row in a table

        Takes user input or data from a file and forms a dictionary row
        Then appends the row to the list of dictionaries 

        Args:
            idn (string): ID number of the CD, entered by user or read from file, saved as int()
            title (string): Title of the CD, entered by user or read from file, saved as string()
            artist (string): Artist of the CD, entered by user or read from file, saved as string()
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        dicRow = {'ID': int(idn), 'Title': title, 'Artist': artist}
        table.append(dicRow)


    @staticmethod
    def add_cd(strID, strTitle, stArtist, table):
        """Add a CD to the current inventory table

        Calls the fuction to show the next available ID and displays it, then asks for user input for the ID,
        when received then calls the Check_ID function, if the ID was used then display and start the add_cd function again.
        If the ID was not used then get user input for the title and artist and call the fuction to write the cd to the table,
        set the saveFlag to 1 and call the fuction to show the inventory with the added CD.

        Args:
            strID (int): ID number of the CD to be that was entered by user
            strTitle (str): Returns the user inputed string for the Title.
            stArtist (str): Returns the user inputed string for the Artist.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            saveFlag (int): Returns the saveFlag as 1 if a CD was saved.
        """
        DataProcessor.write_row(strID, strTitle, stArtist, table)
        saveFlag = 1
        print('The CD was added')
        return saveFlag


    @staticmethod
    def del_cd (idndel, table):
        """Function to delete a CD row in a table

        Takes the user input of a ID number of the CD to be deleted
        Then deletes the matching row in the list of dictionaries 

        Args:
            idndel (int): ID number of the CD to be deleted, entered by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
           saveFlag (int): Returns the saveFlag as 1 if a CD was removed.
        """
        intRowNr = -1
        cdremoved = 0
        for row in table:
            intRowNr += 1
            if row['ID'] == idndel:
                del table[intRowNr]
                saveFlag = 1
                cdremoved = 1
                print('The CD was removed') 
                return saveFlag                
        if cdremoved == 0:
            print('Could not find this CD!')
            

    @staticmethod
    def sort_table (table):
        """Function to sort the table

        Takes the table and sorts by ascending the ID value of the dictionaries in the list 

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list): Returns the list sorted ascending by ID
        """
        table = sorted(table, key = lambda i: i['ID']) 
        return table
    

    @staticmethod
    def find_next_ID (table):
        """Function to find the next available ID number

        Takes the table and looks for the next ID number that has not been used by matching the ID value of each dict starting at 1 and ascending until no match is found

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            next_ID (int): Returns the number of the next available ID
        """
        # Default ID value
        next_ID = 1

        # Generate a list of all ID's currently in use
        used_id = [cd['ID'] for cd in table]

        # Loop and increment next_ID until a free value is found.
        while next_ID in used_id:
            next_ID += 1
        print('The next available ID is: ' + str(next_ID))
        return next_ID
    

    @staticmethod
    def check_ID (idnf, table):
        """Function to check if the user entered ID has been used 

        Takes the user entered ID number and the table and looks in the ID value to see if it has been used before in any of the dict in the table

        Args:
            idnf (int): ID number of the CD to be checked, entered by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            usedid (boolean): Returns True if the ID of the CD was matched or False if it was not matched
        """
        if any(row.get('ID') == int(idnf) for row in table):
            usedid = True       
        else:
            usedid = False     
        return usedid


# -- FILE HANDLING -- #
class FileProcessor:
    """Processing the data to and from text file"""
    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from the binary file identified by file_name into a 2D table
        Uses pickle to unpack the file that is binary file.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            data (list) = list of dicts loaded from file_name
        """
        while True:
            try:
                open(file_name, 'rb') 
            except OSError as e:
                print('The file CDInventory.dat was not found, Please make sure the file is in the correct path.', e)
                userexit = (input ("If you want to load the file, please put it in the corrct path and press enter to exit without saving type 'exit'\n"))
                if userexit.lower() == 'exit':
                    print('Goodbye!')
                    sys.exit()
                else:
                    print("Attepting to load the file!")
                    print()
                    continue
            else:
                with open(file_name, 'rb') as fileObj:
                    data = pickle.load(fileObj)
                return data


    @staticmethod
    def save_file(file_name, table):
        """Function to manage data degestion from a list of dictionaries to a file

        Writes the data from a 2D table to the binary file identified by file_name.
        Uses pickle to unpack the file that is binary file.

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table, fileObj)
        saveFile = 0    
        return saveFile    
       

# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    
    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')


    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice


    @staticmethod
    def get_input(value_type, input_message, error_message):
        """ Prompts the user for a value of specified type and returns


        Args:
            value_type (type): Requested data type (int, str, float...)
            input_message (str): Message displayed to the user via input() prompting for data
            error_message (str): Message displayed to the user if an incorrect data type is entered.

        Returns:
            new_value (value_type): Data of the requested type provided by the user
        
        """
        while True:
            try:
                new_value = value_type(input(input_message).strip())
                return new_value
            except ValueError:
                print(error_message)


    @staticmethod
    def load_inventory():
        """Function that will get user input to reload the inventory from a file

        Will ask for user confirmation then if received the returns loadchoice as True
        If the user chooses not to load then the user is informed

        Args:
            None.

        Returns:
            loadchoice (Boolean): Returns the loadchoice as True if file is to be reloaded
        """
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            loadchoice = True
            print('reloading...')
            return loadchoice
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table with sorting

        Calls the fuction to display the table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')


    @staticmethod
    def save_inventory(table):
        """Function to get user input to save the inventory to a file

        Call the show inventory fuction then ask for user input to save the file, 
        if received then call the function to save the file and set and return the saveFlag,
        if not received then return to the main menu.

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            saveCon (int): Returns the saveCon as 1 if the file is to be saved
        """
        IO.show_inventory(table)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        saveCon = 0
        if strYesNo == 'y':
           saveCon = 1
           print('File Saved!')
           return saveCon
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        


    @staticmethod
    def exit_script():
        """Fuction that handles exiting the script

        Checks the SaveFlag, if 1 then prompts the user for confirmation to exit without saving
        otherwise exits the script.

        Args:
            None.

        Returns:
            None.
        """
        if saveFlag == 1:
            userexit = (input ("You have not saved the list yet,\nto exit without saving type 'exit'\nor press enter to continue "))
            if userexit.lower() == 'exit':
                print('Goodbye!')
                quit()
            else:
                print("Please Save your List!")
                print()
        else:
            print('Goodbye!')
            quit()

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileNamed)
print('The following CDs have been loaded from ' + strFileNamed)
IO.show_inventory(lstTbl) #show loaded inventory at start of script
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection

    # 3.1 process exit first
    if strChoice == 'x':
        IO.exit_script()
    # 3.2 process load inventory
    if strChoice == 'l':
        loadchoice = IO.load_inventory()
        if loadchoice == True:
            lstTbl = FileProcessor.read_file(strFileNamed)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        DataProcessor.find_next_ID(lstTbl)
        strID = IO.get_input(int, 'Enter ID: ', 'Please enter an integer value')
        usedid = DataProcessor.check_ID(strID, lstTbl)
        if usedid == True:
            print('That ID is already being used, Please try again!')
            continue
        strTitle = IO.get_input(str, 'What is the CD\'s title? ', 'Please enter letters and numbers only')
        stArtist = IO.get_input(str, 'What is the Artist\'s name? ', 'Please enter letters and numbers only')
        saveFlag = DataProcessor.add_cd(strID, strTitle, stArtist, lstTbl)
        lstTbl=DataProcessor.sort_table(lstTbl)
        IO.show_inventory(lstTbl)     
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        lstTbl=DataProcessor.sort_table(lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        IO.show_inventory(lstTbl)
        intIDDel = IO.get_input(int, 'Which ID would you like to delete? ', 'Please enter an integer value')
        saveFlag = DataProcessor.del_cd(intIDDel, lstTbl)
        lstTbl=DataProcessor.sort_table(lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        lstTbl=DataProcessor.sort_table(lstTbl) 
        saveCon = IO.save_inventory(lstTbl)
        if saveCon == 1:
            saveFlag = FileProcessor.save_file(strFileNamed, lstTbl)
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')





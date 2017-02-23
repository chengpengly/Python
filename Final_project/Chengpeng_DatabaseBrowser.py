import tkinter
import sqlite3
import os
#GUI customization
bgcolor = 'blanchedalmond'
fgcolor = 'darkslategray'
label_fg = 'darkcyan'
pad =20
data_font = "Verdana 10 normal"
label_font = "Verdana 12 bold"

db = None

# The DB_Browser class defines the GUI for this application
class DB_Browser:
    def __init__(self, rows):
        # Main window definition
        self.main_window = tkinter.Tk()
        self.main_window.title("Restaurant Browser")
        self.main_window.geometry('500x500')
        self.main_window.resizable(width="true", height="true")

        # Variables for search button and search value
        self.selected_column = 'Name'                    # variable that contains the user-selected column; initially set to 'Name'
        self.search_button_text = tkinter.StringVar()    # variable that contains text for the search button
        self.search_button_text.set('Search by Name')    # initial text for the search button
        self.search_value = tkinter.StringVar()          # variable that contains user-provided search value

        # Widgets for row 0 of the grid layout: Label, Button, and Entry field
        tkinter.Label(self.main_window, text='Restaurant Browser').grid(row=0,column=0)
        tkinter.Button(self.main_window, textvariable = self.search_button_text, command=self.search_db,fg=fgcolor,bg=bgcolor).grid(row=0, column=2)
        self.search_value_entry = tkinter.Entry(self.main_window, width=15, textvariable=self.search_value).grid(row=0, column=3)

        #Create a list to store previous records
        self.list=[]
        # Each Restaurant column header is represented by a Button widget.
        # When one of these buttons is clicked, the select_column function is called
        #   with an argument value equal to the column name (Name, City, State, or Cuisine)
        try:
            r = 1
            cols = ['Name','City','State','Cuisine']
            tkinter.Button(self.main_window, text=cols[0], command=lambda: self.select_column(cols[0]),fg=fgcolor,bg=bgcolor,padx=pad,font=label_font).grid(row=r, column=0,sticky=tkinter.constants.W)
            tkinter.Button(self.main_window, text=cols[1], command=lambda: self.select_column(cols[1]),fg=fgcolor,bg=bgcolor,padx=pad,font=label_font).grid(row=r, column=1,sticky=tkinter.constants.W)
            tkinter.Button(self.main_window, text=cols[2], command=lambda: self.select_column(cols[2]),fg=fgcolor,bg=bgcolor,padx=pad,font=label_font).grid(row=r, column=2,sticky=tkinter.constants.W)
            tkinter.Button(self.main_window, text=cols[3], command=lambda: self.select_column(cols[3]),fg=fgcolor,bg=bgcolor,padx=pad,font=label_font).grid(row=r, column=3,sticky=tkinter.constants.W)
            self.display_rows(rows)   # Displays all restaurant data when the GUI is initially displayed
            tkinter.mainloop()
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ', err)

    # When the display_rows function is called, it displays the rows fetched from the last SQL query (search or sort)
    # Clear any previous rows of data before displaying results of current search or sort
    # If the list of rows is empty, display 'No results found'
    def display_rows(self, rows):
        try:
            r = 2
            # clear the previous data which are stored in list
            for i in range(len(self.list)):
              self.list[i].grid_forget()
            if len(rows) > 0:
                for a in rows:
                    self.l1=tkinter.Label(self.main_window, text=a[1],font=data_font)
                    self.l1.grid(row=r, column=0,sticky=tkinter.constants.W)
                    self.list.append(self.l1)
                    self.l2=tkinter.Label(self.main_window, text=a[2],font=data_font)
                    self.l2.grid(row=r, column=1,sticky=tkinter.constants.W)
                    self.list.append(self.l2)
                    self.l3=tkinter.Label(self.main_window, text=a[3],font=data_font)
                    self.l3.grid(row=r, column=2,sticky=tkinter.constants.W)
                    self.list.append(self.l3)
                    self.l4=tkinter.Label(self.main_window, text=a[4],font=data_font)
                    self.l4.grid(row=r, column=3,sticky=tkinter.constants.W)
                    self.list.append(self.l4)
                    r = r + 1
            else:
                tkinter.Label(self.main_window, text='No results found',bg=bgcolor,fg=label_fg,font=label_font).grid(row=r, column=0)
        except IndexError as err:
            print('Index error: ', err)
        except Exception as err:
            print('An error occurred: ',err)

    # When the select_column function is called, it is passed the name of the column corresponding to the button that was clicked.
    # This function changes the text of the search button to indicate which column can be searched.
    # For example, if the user clicks the 'City' button, then the search button label is changed to 'Search by City'
    # This function also calls the sort_db() function to sort the restaurant data in the order specified by the column name
    def select_column(self, colname):
        try:
            print("select_column", colname)
            self.search_button_text.set("Search by"+colname)
            self.sort_db(colname)
        except Exception as err:
            print("An error occur:",err)

    # When the sort_db function is called, an SQL query is created and executed to fetch all of the
    #   restaurant data in sorted order using the selected column.
    # The SQL query should look like this: 'SELECT * FROM RESTAURANT ORDER BY ' + column
    # After the data is fetched from the database, call display_rows(rows)
    def sort_db(self,colname):
        try:
              print("sort_db")
              sql="select * from restaurant order by "+colname
              self.selected_column=colname
              cursor=db.cursor()
              cursor.execute(sql)
              records=cursor.fetchall()
              if len(records)>0:
                 self.display_rows(records)
        except sqlite3.OperationalError as err:
            print("Operational Error:",err)
        except Exception as err:
            print('An error occurred: ', err)


    # When the search_db function is called, an SQL query is created and executed to fetch all of the
    #    restaurant data where the selected column has a value like the user-provided search value (or pattern).
    # The SQL query should look like this: 'SELECT * FROM RESTAURANT WHERE ' + column + ' LIKE "%' + pattern + '%" ORDER BY Name'
    # If no search value is provided, fetch all restaurant data in Name order.
    # After the data is fetched from the database, call display_rows(rows)
    def search_db(self):
        try:
                 print("search_db")
                 sql="select * from RESTAURANT where "+self.selected_column+" LIKE '%"+self.search_value.get()+"%'order by Name"
                 print(sql)
                 cursor=db.cursor()
                 cursor.execute(sql)
                 rows=cursor.fetchall()
                 self.search_value.set("")
                 self.display_rows(rows)
        except sqlite3.OperationalError as err:
            print("Operational Error:", err)
        except Exception as err:
            print('An error occurred: ', err)


def main():
    global db

    try:
        dbname = 'restaurants.db'
        if os.path.exists(dbname):
            db = sqlite3.connect(dbname)
            cursor = db.cursor()
            sql = 'SELECT * FROM RESTAURANT ORDER BY Name'
            cursor.execute(sql)
            rows = cursor.fetchall()
            DB_Browser(rows)
            db.close()
        else:
            print('Error:', dbname, 'does not exist')
    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on connect:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)


main()
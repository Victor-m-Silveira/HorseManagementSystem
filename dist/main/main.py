from PyQt5 import QtWidgets, uic
import mysql.connector

# Set up a connection to the MySQL database on the local machine with default user 'root' and no password.
# The database is called 'horse_data'.
connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='horse_data'
)

number_id = 0

def delete_data():
    remove_data = report.tableWidget.currentRow()
    report.tableWidget.removeRow(remove_data)
    cursor = connection.cursor()
    cursor.execute('SELECT horseID FROM horses')
    read_database = cursor.fetchall()
    value_id = read_database [remove_data][0]
    cursor.execute('DELETE FROM horses WHERE horseID=%s', (value_id,))
    connection.commit()  # Save changes to the database



    

def changedata():
    global number_id
    chosendata = report.tableWidget.currentRow()
    cursor = connection.cursor()
    cursor.execute('SELECT horseID FROM horses')
    read_database = cursor.fetchall()
    value_id = read_database [chosendata][0]
    cursor.execute('SELECT * FROM  horses WHERE horseid='+ str(value_id))
    read_database = cursor.fetchall()
    
    data.show()
    
    number_id = value_id
    
    data.txtChangeId.setText(str(read_database[0][0]))
    data.txtChangeName.setText(str(read_database[0][1]))
    data.txtChangePrice.setText(str(read_database[0][2]))
    data.txtChangeStock.setText(str(read_database[0][3]))
    
def save_data():
    global number_id
    # Gather updated horse data from the form fields
    horse_id = data.txtChangeId.text()
    horse_name = data.txtChangeName.text()
    horse_price = data.txtChangePrice.text()
    availableHorses = data.txtChangeStock.text()

    # Execute an update query with parameterized inputs for security
    cursor = connection.cursor()
    update_query = (
        "UPDATE horses SET horseID=%s, horseName=%s, horsePrice=%s, availableHorses=%s WHERE horseID=%s"
    )
    cursor.execute(update_query, (horse_id, horse_name, horse_price, availableHorses, number_id))
    connection.commit()  # Save changes to the database

    # Close the data entry window and refresh the report
    data.close()
    report.close()
   

# Function to generate a report from the database.
def report():
    # Make the report window visible.
    report.show()
    # Create a cursor, which is a control structure that enables traversal over the records in the database.
    cursor = connection.cursor()
    # SQL query to select all records from the 'horses' table.
    command_SQL ='SELECT * FROM horses'
    # Execute the query.
    cursor.execute(command_SQL)
    # Fetch all rows of the query result, returning them as a list of tuples.
    read_database = cursor.fetchall()
    # Set the number of rows in the table widget equal to the number of entries fetched.
    report.tableWidget.setRowCount(len(read_database))
    # The table will have 4 columns.
    report.tableWidget.setColumnCount(4)
    
    # # The 'range' function generates a sequence of numbers, which is used here to iterate over the indices of the list 'read_database'.
# 'len(read_database)' determines the total number of entries fetched from the database,
# which corresponds to the number of rows in the table widget.
    for i in range(len(read_database)):  # Iterate over each row in the data
        for j in range(4):  # Iterate over each of the 4 columns
        # For each cell in the table, create and set a QTableWidgetItem object with the data.
            report.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(read_database[i][j])))

# Function to insert new data into the 'horses' table.
def insert_data():
    # Retrieve the text from each QLineEdit widget.
    horse = equinedata.txtHorseName.text()
    price = equinedata.txtPrice.text()
    stock = equinedata.txtStock.text()
    
    # Create a cursor for database operations.
    cursor = connection.cursor()
    # SQL command for inserting new data into the 'horses' table.
    # The placeholders (%s) will be replaced by the tuple 'data'.
    command_SQL ='INSERT INTO horses (horseName, horsePrice, availableHorses) VALUES (%s, %s, %s)'
    # Group the inputs into a tuple to pass as parameters into the SQL command.
    data = (horse, price, stock)
    # Execute the SQL command with the provided data.
    cursor.execute(command_SQL, data)
    # Commit the changes to make them persistent in the database.
    connection.commit()
    # Clear the input fields for the next data entry.
    equinedata.txtHorseName.clear()
    equinedata.txtPrice.clear()
    equinedata.txtStock.clear()

# Set up the application environment for PyQt.
app = QtWidgets.QApplication([])
# Load the interface design from the 'equine.ui' file created in Qt Designer.
equinedata = uic.loadUi('equine.ui')

# Connect the 'Register' button to the function that inserts data into the database.
equinedata.btnRegister.clicked.connect(insert_data)
# Connect the 'Report' button to the function that displays the data report.
equinedata.btnReport.clicked.connect(report)
# Load the UI for the report window.
report = uic.loadUi('report.ui')
report.btnChange.clicked.connect(changedata)
report.btnDelete.clicked.connect(delete_data)
changedata = uic.loadUi('data.ui')
# Make sure `data` UI is loaded before trying to connect signals
data = uic.loadUi('data.ui')
data.btnConfirm.clicked.connect(save_data)
  

# Display the main window of the application.
equinedata.show()
# Start the application's event loop, waiting for user interaction.
app.exec_()

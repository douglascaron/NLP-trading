from PyQt5 import QtWidgets

def button_clicked():
    print("Button clicked!")

app = QtWidgets.QApplication([])

# Create a main window
window = QtWidgets.QWidget()
window.setStyleSheet("background-color: #1f1f1f;")
window.setWindowTitle("NLP trading")

# Create a layout for the buttons
button_layout = QtWidgets.QHBoxLayout()

# Create sample buttons
button1 = QtWidgets.QPushButton("Button 1")
button1.setStyleSheet("background-color: #363636; color: white;")
button1.clicked.connect(button_clicked)
button_layout.addWidget(button1)



# Set the layout for the main window
window.setLayout(button_layout)

# Show the main window
window.show()

# Start the application event loop
app.exec_()

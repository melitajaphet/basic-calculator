import sys
import re
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QGridLayout, QPushButton, QMainWindow


# Class to define a stack
class Stack:
    def __init__(self):                                                                                     # Initialize an empty stack
        self.stack = []                                                                                     

    def is_empty(self):                                                                                     # Check if stack is empty
        return len(self.stack) == 0                                                                         

    def push(self, v):                                                                                      # Push to stack
        self.stack.append(v)                                                                                

    def pop(self):                                                                                          # Pop from stack
        if self.is_empty():
            raise Exception('Stack is empty.')                                                              # Raise exception if stack is empty
        return self.stack.pop()

    def read(self):                                                                                         # Peak at stack
        if self.is_empty():
            return None
        return self.stack[-1]
    
    def __repr__(self):                                                                                     # String representation of stack
        return "stack:" + str(self.stack)


# Class to define the calculator application
class Calculator(QMainWindow):
    
    # Initialize GUI
    def __init__(self):
        super().__init__()
        
        # Window layout
        self.setWindowTitle("Calculator Qt")                                                                # Set window title
        self.setFixedSize(235, 235)                                                                         # Set window size        
        self.layout = QVBoxLayout()                                                                         # Define layout type
        centralWidget = QWidget(self)                                                                       # Define container widget to organize other widgets
        centralWidget.setLayout(self.layout)                                                                # Assign the layout type to the central widget
        self.setCentralWidget(centralWidget)                                                                # Set container widget as the central widget for the main window
        
        # Input field layout
        self.input_field = QLineEdit()                                                                      # Set input field layout
        self.input_field.setFixedHeight(40)                                                                 # Set input field height
        self.input_field.setPlaceholderText("Enter expression")                                             # Set input field hint
        self.input_field.setAlignment(Qt.AlignmentFlag.AlignRight)                                          # Set input text alignment to right
        self.input_field.setReadOnly(True)                                                                  # Set input field to read only
        self.layout.addWidget(self.input_field)                                                             # Add the input field widget to main layout
        self.stack = Stack()                                                                                # Initialize a stack
        
        # Button layout
        button_layout = [                                                                                   # Define nested list for buttons
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '%', '.', '+', '=']
        ]
        
        grid_layout = QGridLayout()                                                                         # Define numpad layout
        for row, buttons in enumerate(button_layout):                                                       # Iterate through each list in the nested list to get access to first row of buttons
            for col, button_text in enumerate(buttons):                                                     # Iterate through each element of the first row of buttons to access individual buttons
                button = QPushButton(button_text)                                                           # Create button widget
                button.setFixedSize(40, 40)                                                                 # Set button size
                grid_layout.addWidget(button, row, col)                                                     # Add widget to the numpad layout
                button.clicked.connect(lambda _, text=button_text: self.handle_button_click(text))          # Link the button click to the value it is supposed to represent using a lambda function so that the button click can be handled

        self.layout.addLayout(grid_layout)                                                                  # Add the numpad layout to main layout

    # Handle button inputs
    def handle_button_click(self, button_text):
        # Condition if '=' is hit
        if button_text == '=':
            self.calculate()                                                                                # Calculate expression
        # Condition if 'C' is hit
        elif button_text == 'C':
            self.clear()                                                                                    # Clear input field
        # Condition if '(' or ')' is hit
        elif button_text in ['(', ')']:                                                                                               
            self.validate_paranthesis(button_text)                                                          # Validate any paranthesis entry
        # Any other button input
        else:
            self.input_field.setText(self.input_field.text() + button_text)                                 # Concatenate text to the current text in input field

    # Keep track of paranthesis in expression
    def validate_paranthesis(self, button_text):
        if button_text == '(':                                                                              # Condition for '('
            self.stack.push(button_text)                                                                    # Push '(' in stack
            self.input_field.setText(self.input_field.text() + button_text)                                 # Concatenate text to the current text in input field
        if button_text == ')':                                                                              # Condition for ')'
            if not self.stack.is_empty():                                                                   # Check if mismatched opening braces are present
                self.stack.pop()                                                                            # Pop '(' from stack
                self.input_field.setText(self.input_field.text() + button_text)                             # Concatenate text to the current text in input field

    # Remove leading zeros from all numbers
    def remove_leading_zeros(self, expression):
        components = re.findall(r'\d+\.\d+|\d+|\S', expression)                                             # Split expression into numbers and non-numeric characters
        processed_components = []                                                                           # Initialize empty list to hold processed components
        for component in components:                                                                        # Loop through components
            if component.isdigit():                                                                         # Check if component is numeric
                processed_components.append(str(int(component)))                                            # Convert to int and back to str to remove leading zeros
            else:                                                                                           
                processed_components.append(component)                                                      # Append non-numeric components to list
        
        expression = ''.join(processed_components)                                                          # Reconstruct the expression
        return expression

    # Calculate expression output
    def calculate(self):
        self.input_field.setText(self.remove_leading_zeros(self.input_field.text()))                        # Remove any leading zeros from the expression

        if not self.stack.is_empty():                                                                       # Check if any mismatched opening braces are present
            while not self.stack.is_empty():                                                                # True while stack is not empty
                self.input_field.setText(self.input_field.text() + ')')                                     # Append closing brace for every mismatched opening brace
                self.stack.pop()                                                                            # Pop opening brace from stack
        
        expression = self.input_field.text()                                                                # Grab the expression from the input field
        
        # Evaluate the expression
        try:
            result = eval(expression)                                                                       # Calculate output
            self.input_field.setText(str(result))                                                           # Display result
        except Exception as e:
            self.input_field.setText("Error")                                                               # Display error for invalid expressions

    # Clear the input field
    def clear(self):
        self.input_field.clear()

# Main function to run app
def main():
    app = QApplication(sys.argv)                                                                            # Define an instance of QApplication to control application flow
    calculator = Calculator()                                                                               # Create an instance of Calculator class
    calculator.show()                                                                                       # Show the application to the user
    sys.exit(app.exec())                                                                                    # Start the application execution, waiting for inputs. Exit when window is closed

# Run the main function
if __name__ == "__main__":
    main()
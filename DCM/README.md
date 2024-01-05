# PACEMAKER UI - MECHTRON 3K04

## Environment and Libraries
- Python3
- TKinter
- customtkinter 5.2.0
- "Lexend" font

## Git

Please use GIT to maintain version control.

### Clone repository
clone the repository onto your local device and edit on that

### Branches
When pulling from the repository, create your own branch off of the dev branch, not the main branch. Work on your own branch and commit your work to your OWN branch that was off of dev. Do not merge onto dev willy nilly.

### push/commits
Use ```git add <filename>```, ```git commit -m "Insert commit msg here"``` and ```git push <branchname> ``` to push the changes onto the repository. When writing comments for git commit, please keep them short and descriptive. **DO NOT** copy your code, paste it into GitHub, and commit your code in that manner.

## Coding Conventions

### Class Structure:
- Define classes in a separate .py file and **NOT** within the main_app.py file unless it is the main app class loop
  - You can call the other classes by adding the following line to the top of the class
    ``` py
    from <file_name> import <class_name>
    ```
- Use accessor and mutator methods to change class variables, do not change use them or change them outside of the class
  
### Variable Naming:
- For Tkinter variables, name them appropriately based on the type of object it is (ie. button, frames, etc), where in the app it is supposed to be located (ie. welcome screen, main interface), and what the button is meant to represent
  - Example: Sign In button on welcome screen --> btn_welcome_signin

    
    **Naming Convention Table:**
    Tkinter Object  | Variable Prefix
    --------------- | ---------------
    Button     | btn
    Frame      | frm
    Window     | win
    Scroll Bar | sb
    Label      | lbl
    Text Box   | txtbx
    
- For other generic variables that are not objects, include the data type of the variable within the variable name and what it is meant to do
  - Example: integer counter --> Variable Name: int_counter
  - Example: string username --> Variable Name: str_username
 
    **Naming Convention Table:**
    Type  | Variable Prefix
    --------------- | ---------------
    Integer     | int
    String      | str
    Boolean     | bool
    Float       | flt
    List        | lst

  - For functions, name them with the return type of the function, where the function is meant to be called, and general name:
    - Example: Function returns int after pressing button 1 --> Variable Name:
      ```py
      def int_btn1_response():
      ```
   
  - For Private variables within classes, add an "_" prefix to the variable name to change it to a private variable
    - Example: Private variable x which contains an int value of 5 --> Variable Name:
      ```py 
      self._int_x = 5
      ``` 

### Using CustomTkinter:
- When creating objects in customtkinter and passing in arguments for the object (Ex. root, text, etc), please include the variable of the argument. Ex.
  ```py
  btn_welcome_signin = customtkinter.CTkButton(master=root, width = 191, height=43, text="Sign In", command=response, font=font1)
  ```
  **NOT**
  ```py
  btn_welcome_signin = customtkinter.CTkButton(mroot, 191, 43, "Sign In", response, font1)
  ```

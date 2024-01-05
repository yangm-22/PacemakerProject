''' Import Libraries '''
from tkinter import *
import customtkinter
from tkinter import font
import json
import os
from time import strftime
import datetime

''' Import External file variables and classes '''
from program_files.user_class import user

from program_files.app_widgets import successful_register_prompt
from program_files.app_widgets import admin_login
from program_files.app_widgets import delete_account
from program_files.app_widgets import scroll_parameters_frame
from program_files.app_widgets import egram_window

from program_files.app_colors import *
from program_files.mode_variables import *
from program_files.serialcomm import *

''' Main App Class '''
# Main app classs
class DCM(customtkinter.CTk):
  ''' Constructor Method '''
  def __init__(self):
    super().__init__()
    # variables too be monitored devlared here
    self._perms = StringVar(value="Client")
    self._can_edit = BooleanVar(value=False)
    self._mode_choice = StringVar(value="None")
    self._updated_parameter_values = None
    self._updated_parameter_values_indexed = None
    self._saved_parameter_values = None
    self._saved_parameter_values_indexed = None
    self._serPacemaker = None
    self._connected_status = StringVar(value="X")
    self._battery_level = StringVar(value="N/A")

    self._all_battery_statuses = ['BOL', 'ERN', 'ERT', 'ERP'] # battery statuses for eventual implementation

    # monitor variables
    self._perms.trace_add("write", self._callback)
    self._can_edit.trace_add("write", self._callupdate)
    self._mode_choice.trace_add("write", self._callupdate)
    self._connected_status.trace_add("write", self._monitor_connection)
    self._battery_level.trace_add("write", self._monitor_battery_level)

    self._current_user = None # current user that is logged in is initially set to none

    self._admin_password = "coffee" # admin password
    self._root_dir = 'user_data'

    # intiialize window and begin the call for the first screen
    self.title("G29 - MECHTRON 3K04 - DCM")
    self.geometry("1000x700")
    self.resizable(height=False, width=False)
    self._create_login_screen()
    self._toplevel_window = None
    self._egram_window = None

    self._about_info = {"Institution" : "McMaster University", "Software Version" : "V 2.0", "Serial Number" : "000 000 001", "Model Number" : "1"}

    photo = PhotoImage(file = "icons/pacemaker_logo.png")
    self.iconphoto(True, photo)
    

  ''' Methods for page navigation '''
  # login screen
  def _create_login_screen(self):
    # get all users

    lst_all_cur_users = self._get_current_users(self._root_dir)

    self._frm_login_screen = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_login_screen.pack(fill='both', expand=True)

    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_sub_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=13)
    font_signup = customtkinter.CTkFont(family="Lexend", weight="bold",size=12)
    font_signup_underline = customtkinter.CTkFont(family="Lexend", weight="bold", underline = 1, size=12)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)
    font_status = customtkinter.CTkFont(family="Lexend", size=15)

    # center screen frame
    customtkinter.CTkFrame(master=self._frm_login_screen, width=357, height=601, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Login label title
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Login", width=143, height=63, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)
    
    # username text 
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Username or Email", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=235)
    
    # username text box
    self._txtbx_username = customtkinter.CTkEntry(master=self._frm_login_screen, placeholder_text="Enter Username or Email", width=295, height=39, fg_color=white_1, 
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_username.place(relx = 0.5, rely=0.4, anchor=CENTER)
    
    # password text 
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Password", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=340)
    
    # password text box
    self._txtbx_password = customtkinter.CTkEntry(master=self._frm_login_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_password.place(relx = 0.5, rely=0.55, anchor=CENTER)


    # sign in button
    customtkinter.CTkButton(master=self._frm_login_screen, width = 191, height=43, text="Sign In", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=blue_1, bg_color = gray_1, command = lambda:self._attempt_login(self._txtbx_username.get(), self._txtbx_password.get(), lst_all_cur_users, self._root_dir)).place(relx = 0.5, rely = 0.7, anchor = CENTER)

    # watch for keystrokes
    #self.bind("<Return>", lambda e:self._attempt_login(self._txtbx_username.get(), self._txtbx_password.get(), lst_all_cur_users, self._root_dir))

    # "Don't Have an Account?" label 
    customtkinter.CTkLabel(master=self._frm_login_screen, text="Don't Have an Account?", width=100, height=25, fg_color=gray_1, text_color=gray_2, font=font_sub_labels, bg_color = gray_1).place(relx=0.465, rely=0.76, anchor=CENTER)


    # forgot password button
    self._forgot_button = customtkinter.CTkButton(master=self._frm_login_screen, width = 20, height=25, text="Forgot Password?", font=font_sub_labels, 
                            state="normal", fg_color=gray_1, text_color=gray_2, hover_color = gray_1, bg_color = gray_1)
    self._forgot_button.place(relx=0.592, rely=0.6, anchor=CENTER)
    self._forgot_button.bind("<Enter>", lambda e: self._forgot_button.configure(font=font_sub_labels_underlined))
    self._forgot_button.bind("<Leave>", lambda e: self._forgot_button.configure(font=font_sub_labels))

    # x/10 users label 
    active_users = len(lst_all_cur_users[0])
    maximum_users = 10 
    customtkinter.CTkLabel(master=self._frm_login_screen, text=f"{active_users}/{maximum_users} Users", width=100, height=25, fg_color=gray_1, text_color=gray_2 if active_users < maximum_users else red_1, font=font_sub_labels, bg_color = gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)

    # sign up button
    self._signup_button = customtkinter.CTkButton(master=self._frm_login_screen, width=20, height=25, text="Sign Up", font=font_signup,
                                        state="normal" if active_users < maximum_users else "disabled", fg_color=gray_1, text_color=blue_1, text_color_disabled=red_1, hover_color=gray_1, 
                                        bg_color=gray_1, command=self._create_signup_screen)
    self._signup_button.place(relx=0.575, rely=0.76, anchor=CENTER)
    self._signup_button.bind("<Enter>", lambda e: self._signup_button.configure(font=font_signup_underline))
    self._signup_button.bind("<Leave>", lambda e: self._signup_button.configure(font=font_signup))
    
    self._create_header(self._frm_login_screen, self._back_to_login)

  # main interface
  def _create_main_interface(self):
    for widget in self.winfo_children():
      widget.destroy()
    
    #fonts
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_username = customtkinter.CTkFont(family="Lexend", weight="bold",size=35)
    font_sections = customtkinter.CTkFont(family="Lexend", weight="bold",size=24)
    font_curmode = customtkinter.CTkFont(family="Lexend", size=20)
    font_status = customtkinter.CTkFont(family="Lexend", size=15)

    #frame
    self._frm_main_interface = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_main_interface.pack(fill='both', expand=True)
   
    #admin button
    self._btn_admin = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Admin", state="normal", font=font_buttons, fg_color=blue_1, command=self._open_admin_login)
    self._btn_admin.place(x = 22, y = 260)

    #run button 
    self._btn_run = customtkinter.CTkButton(master=self._frm_main_interface, width = 117, height=43, text="Run", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=green_2, border_width=2, border_color=green_1, command=lambda:self._start_button_cmd(self._mode_choice.get()))
    self._btn_run.place(x = 22, y = 380)

    #stop button 
    self._btn_stop = customtkinter.CTkButton(master=self._frm_main_interface, width = 117, height=43, text="Stop", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=red_2, border_width=2, border_color=red_1, command=self._stop_button_cmd)
    self._btn_stop.place(x = 159, y = 380)

    #sign out button 
    customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Sign Out", state="normal", font=font_buttons, fg_color=blue_1, command=self._sign_out).place(x = 22, y = 546)
    
    #delete account button 
    self._btn_delete = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=33, text="Delete Account", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=red_2, border_width=2, border_color=red_1,  command=self._open_delete_account)
    self._btn_delete.place(x = 22, y = 603)

    # download bradycardia parameters report button
    self._btn_bradycardia_report = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=33, text="Bradycardia Report", state="normal", font=font_buttons, fg_color=blue_1)
    self._btn_bradycardia_report.place(x = 475, y = 653)

    # download temporary parameters report button
    self._btn_temporary_report = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=33, text="Temporary Report", state="normal", font=font_buttons, fg_color=blue_1)
    self._btn_temporary_report.place(x = 737, y = 653)
  
    #text for permissions
    self._perm_label = customtkinter.CTkLabel(master=self._frm_main_interface, text=f"Permission: {self._perms.get()}", width=143, height=34, fg_color=bg_colour, text_color=gray_3, font=font_status, anchor="w")
    self._perm_label.place(x=22, y=651)
    #text for username
    customtkinter.CTkLabel(master=self._frm_main_interface, text=f'{self._current_user.get_username()}', width=199, height=40, fg_color=bg_colour, text_color=white_1, font=font_username, justify="left", anchor="w").place(x=22, y=49)
    #text for mode
    customtkinter.CTkLabel(master=self._frm_main_interface, text="Mode", width=67, height=30, fg_color=bg_colour, text_color=gray_3, font=font_sections).place(x=22, y=104)
    #text for current mode
    self._current_mode_lbl = customtkinter.CTkLabel(master=self._frm_main_interface, text=f"Current Mode: {self._current_user.get_current_mode()}", width=200, height=15, fg_color=bg_colour, text_color=gray_3, font=font_curmode)
    self._current_mode_lbl.place(x=22, y=188)

    #text for parameters
    customtkinter.CTkLabel(master=self._frm_main_interface, text="Parameters", width=142, height=30, fg_color=bg_colour, text_color=gray_3, font=font_sections).place(x=300, y=49)

    self._btn_verify = customtkinter.CTkButton(master=self._frm_main_interface, width = 100, height=33, text="Verify", state="disabled", font=font_buttons, fg_color=gray_1, border_width=2, border_color=blue_1, command=self._verify_data_on_pacemaker)
    self._btn_verify.place(x = 460, y = 49)

    # text for verification
    self._lbl_verify = customtkinter.CTkLabel(master=self._frm_main_interface, text="", width=20, height=20, fg_color=bg_colour, text_color=gray_3, font=font_buttons)
    self._lbl_verify.place(x = 580, y = 63, anchor=CENTER)

    ''' Code for the scrollable frame and the items in it for each parameter '''
    self._frm_scroll_parameters = scroll_parameters_frame(master=self._frm_main_interface, can_edit=self._can_edit.get(), width=665, height=540, fg_color=gray_1, send_data_func=self._get_parameter_data, init_data_func=self._init_parameters_on_mode_selection)
    self._frm_scroll_parameters.place(x=303,y=92)

    # dropdown menu for modes
    def load_parameters_from_mode(choice):
      self._mode_choice.set(choice)
    
    # function when the edit/save button is pressed
    def press_edit():
      new_can_edit = False if self._can_edit.get() else True
      if new_can_edit: # code if edit button is rpessed
        self._btn_edit.configure(text="Save")
      else: # code if save button is pressed
        self._btn_edit.configure(text="Edit")
        # save the parameters
        if self._mode_choice.get() != "None" and self._updated_parameter_values != None:
          dict_mode_parameters_for_user = self._current_user.get_all_mode_data()
    
          parameters_for_mode = dict_mode_parameters_for_user[self._mode_choice.get()]

          for index, parameter in enumerate(parameters_for_mode):
            parameters_for_mode[parameter] = self._updated_parameter_values[index]

          dict_mode_parameters_for_user[self._mode_choice.get()] = parameters_for_mode

          self._current_user.set_all_mode_data(dict_mode_parameters_for_user)
          self._current_user.save_to_json(self._root_dir)

          ''' SEND PARAMETER TO PACEMAKER '''
          self._saved_parameter_values_indexed = self._updated_parameter_values_indexed.copy()

          #self._pacing(self._mode_choice.get())
          #need to change to send to simulink when pacemaker functions

      # update the current perms
      self._can_edit.set(new_can_edit)

    # edit button
    self._btn_edit = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Edit", state="disabled", font=font_buttons, fg_color=gray_1, hover_color=orange_2, border_width=2, 
                                            border_color=orange_1, command=press_edit)
    self._btn_edit.place(x = 22, y = 440)

    str_default_text_mode = StringVar(value="Select a Mode")
    available_modes = [mode for mode in dict_modes]
    self._combobox_select_mode = customtkinter.CTkOptionMenu(master=self._frm_main_interface, values=available_modes, width=252, height=43, font=font_buttons, anchor="center",dynamic_resizing=True, command=load_parameters_from_mode,
                                                            dropdown_font=font_status, fg_color=blue_1, dropdown_fg_color=blue_2, dropdown_hover_color=blue_3, corner_radius=15, bg_color=bg_colour, variable=str_default_text_mode)
    self._combobox_select_mode.place(x=23,y=147)

    # show egram button
    if self._serPacemaker == None:
      self._btn_show_egram = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Show Electrogram", state="disabled", font=font_buttons, fg_color=gray_1, border_width=2, border_color=blue_1, command=self._open_egram)
    else:
      self._btn_show_egram = customtkinter.CTkButton(master=self._frm_main_interface, width = 252, height=43, text="Show Electrogram", state="normal", font=font_buttons, fg_color=blue_1, border_width=2, border_color=blue_1, command=self._open_egram)
    self._btn_show_egram.place(x = 22, y = 320)

    self._create_header(self._frm_main_interface, self._create_main_interface)

  # navigate back to log in screen
  def _back_to_login(self):
    for widget in self.winfo_children():
      widget.destroy()
    self._create_login_screen()
  
  # register an account page
  def _create_signup_screen(self):
    # get all users
    lst_all_cur_users = self._get_current_users(self._root_dir)
    for widget in self.winfo_children():
      widget.destroy()

    self._frm_signup_screen = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_signup_screen.pack(fill='both', expand=True)

    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)
    font_backtologin_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_backtologin_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=15)
    font_status = customtkinter.CTkFont(family="Lexend", size=15)

    # center screen frame
    customtkinter.CTkFrame(master=self._frm_signup_screen, width=357, height=601, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Sign Up label title
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Sign Up", width=143, height=63, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)

    # email text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Email", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=201)
    
    # email text box
    self._txtbx_email = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Enter Email", width=295, height=39, fg_color=white_1, 
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_email.place(relx = 0.5, rely=0.35, anchor=CENTER)

    # username text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Username", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=278)
    
    # username text box
    self._txtbx_username = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Enter Username", width=295, height=39, fg_color=white_1, 
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_username.place(relx = 0.5, rely=0.46, anchor=CENTER)

    # password text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Password", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=355)
    
    # password text box
    self._txtbx_password = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Enter Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_password.place(relx = 0.5, rely=0.57, anchor=CENTER)

    # confirm password text 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text="Confirm Password", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(x=355, y=432)
    
    # confirm password text box
    self._txtbx_confirm_password = customtkinter.CTkEntry(master=self._frm_signup_screen, placeholder_text="Confirm Password", width=295, height=39, fg_color=white_1, show="•",
                                                text_color=gray_1, placeholder_text_color=gray_2, font=font_text_box, corner_radius=5, bg_color=gray_1)
    self._txtbx_confirm_password.place(relx = 0.5, rely=0.68, anchor=CENTER)

    # sign up button
    sign_up_page_button = customtkinter.CTkButton(master=self._frm_signup_screen, width = 191, height=43, text="Sign Up", font=font_buttons, 
                            state="normal",corner_radius=40, fg_color=blue_1, bg_color = gray_1, command=lambda: self._sign_up_check(self._txtbx_username.get(), self._txtbx_email.get(), self._txtbx_password.get(), self._txtbx_confirm_password.get()))
    sign_up_page_button.place(relx = 0.5, rely = 0.80, anchor = CENTER)

    # x/10 users label 
    active_users = len(lst_all_cur_users[0]) #temporary 
    maximum_users = 10 
    customtkinter.CTkLabel(master=self._frm_signup_screen, text= str(active_users) + "/" + str(maximum_users) + " Users", width=100, height=25, fg_color=gray_1, text_color=gray_2, font=font_sub_labels, bg_color = gray_1).place(relx=0.5, rely=0.88, anchor=CENTER)

    # Back to login button
    backtologin_button = customtkinter.CTkButton(master=self._frm_signup_screen, width=20, height=25, text="< Back to Login", font=font_backtologin_labels,
                                        state="normal", fg_color=bg_colour, text_color=gray_2, hover_color=bg_colour, bg_color=bg_colour, command=self._back_to_login)
    backtologin_button.place(relx=0.1, rely=0.95, anchor=CENTER)
    backtologin_button.bind("<Enter>", lambda e: backtologin_button.configure(font=font_backtologin_labels_underlined))
    backtologin_button.bind("<Leave>", lambda e: backtologin_button.configure(font=font_backtologin_labels))

    self._create_header(self._frm_signup_screen, self._create_signup_screen)

  # sign out function
  def _sign_out(self):
    self._mode_choice.set("None")
    self._can_edit.set(False)
    self._perms.set("Client")
    self._current_user = None
    self._stop_pacing()
    self._back_to_login()
  
  # open about apge
  def _create_about_page(self, back_to_previous_page):
    for widget in self.winfo_children():
      widget.destroy()
    
    self._frm_about_screen = customtkinter.CTkFrame(master=self, fg_color = bg_colour)
    self._frm_about_screen.pack(fill='both', expand=True)

    # fonts
    font_back_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_back_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=15)
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=15)
    font_sub_labels = customtkinter.CTkFont(family="Lexend", size=13)
    font_sub_labels_underlined = customtkinter.CTkFont(family="Lexend", underline = 1, size=13)
    font_signup = customtkinter.CTkFont(family="Lexend", weight="bold",size=12)
    font_signup_underline = customtkinter.CTkFont(family="Lexend", weight="bold", underline = 1, size=12)
    font_text_box = customtkinter.CTkFont(family="Lexend", size=15)
    font_buttons = customtkinter.CTkFont(family="Lexend SemiBold", size=20)
    font_title = customtkinter.CTkFont(family="Lexend", weight="bold",size=50)
    font_status = customtkinter.CTkFont(family="Lexend", size=15)

    # center screen frame
    customtkinter.CTkFrame(master=self._frm_about_screen, width=357, height=601, fg_color=gray_1, corner_radius=15, border_width=3, 
                           border_color=blue_1).place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # About label title
    customtkinter.CTkLabel(master=self._frm_about_screen, text="About", width=143, height=63, fg_color=gray_1, text_color=white_1, font=font_title, bg_color = gray_1).place(relx=0.5, rely=0.2, anchor=CENTER)

    ### about information
    # applicaiton model number
    customtkinter.CTkLabel(master=self._frm_about_screen, text=f"Application Model Number: {self._about_info['Model Number']}", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(relx=0.5, y=235, anchor=CENTER)

    # Software version
    customtkinter.CTkLabel(master=self._frm_about_screen, text=f"DCM Software Version: {self._about_info['Software Version']}", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(relx=0.5, y=305, anchor=CENTER)

    # serial number
    customtkinter.CTkLabel(master=self._frm_about_screen, text=f"DCM SN: {self._about_info['Serial Number']}", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(relx=0.5, y=375, anchor=CENTER)

    # instutition name
    customtkinter.CTkLabel(master=self._frm_about_screen, text=f"Institution: {self._about_info['Institution']}", width=10, height=20, fg_color=gray_1, text_color=gray_2, font=font_user_pass_labels, bg_color = gray_1).place(relx=0.5, y=445, anchor=CENTER)

    # back button
    back_button = customtkinter.CTkButton(master=self._frm_about_screen, text=f'<', width=34, height=34, fg_color=bg_colour, font=font_status, text_color=gray_3, border_width=2, border_color=gray_3, hover_color=bg_colour, command=back_to_previous_page)
    back_button.place(x=22, y=9)

    # create header
    self._create_header(self._frm_about_screen)

  def _create_header(self, master, back_to_previous_page=None):
    font_status = customtkinter.CTkFont(family="Lexend", size=15)
    # label for connection status

    self._lbl_connected_status = customtkinter.CTkLabel(master=master, text=f"Pacemaker Connection {self._connected_status.get()}", width=154, height=34, fg_color=bg_colour, text_color=gray_3, font=font_status, justify="left", anchor="w")
    self._lbl_connected_status.place(x=78, y=9)

    # battery status label
    self._lbl_battery_status = customtkinter.CTkLabel(master=master, text=f'{self._battery_level.get()} 🔋', width=154, height=34, fg_color=bg_colour, text_color=gray_3, font=font_status, justify="right", anchor="e")
    self._lbl_battery_status.place(x=824, y=9)

    if back_to_previous_page != None:
      # about button
      self._btn_about_page = customtkinter.CTkButton(master=master, text=f'?', width=34, height=34, fg_color=bg_colour, font=font_status, text_color=gray_3, border_width=2, border_color=gray_3, hover_color=bg_colour, command=lambda:self._create_about_page(back_to_previous_page))
      self._btn_about_page.place(x=22, y=9)
    
    # recusrive time function to update the current time
    def time():
      timestring = strftime('%x - %I:%M:%S %p')
      #timestring = datetime.datetime.now()
      self._lbl_time.configure(text=timestring)

      # constantly check for a connected device
      if self._serPacemaker == None:
        commports = list_serial_ports()
        for com in commports:

          try:
            if self._serPacemaker == None:
              self._serPacemaker = SerialCommunication(port='/dev/tty.usbmodem0006210000001')
              #self._serPacemaker = SerialCommunication(port=com)
              self._serPacemaker.receive_packet()
              self._connected_status.set("✓")
              self._battery_level.set("100%")
          except:
            self._serPacemaker = None
      else:
        try:
         self._serPacemaker.receive_packet()
        except:
          self._serPacemaker = None
          self._connected_status.set("X")
          self._battery_level.set("N/A")
          if self._egram_window != None:
            self._egram_window.destroy()

      self._lbl_time.after(1000, time)


    # time label
    self._lbl_time = customtkinter.CTkLabel(master=master, width=154, height=34, fg_color=bg_colour, font=font_status, text_color=gray_3)
    self._lbl_time.place(relx=0.5, y=9, anchor="n")

    time()
  ''' prompts and pop up windows '''

  # opens a top level window if username or password is incorrect
  def _open_credential_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_login_screen, text = "Username and/or Password is incorrect", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=385, y=445)

  # opens a top level window if register is successful
  def _open_successful_register_prompt(self):
    if self._toplevel_window is None or not self._toplevel_window.winfo_exists():
        self._toplevel_window = successful_register_prompt()  # create window if its None or destroyed
        self._toplevel_window.focus()
        self._toplevel_window.grab_set() # focus window and cant close it
    else:
        self._toplevel_window.focus()  # if window exists focus it
        self._toplevel_window.grab_set() # focus window and cant close it
  
  # opens a top level window if username is taken
  def _open_username_taken_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_signup_screen, text = "Username is already taken", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=490, y=281)
  
  # opens a top level window if email is incorrect
  def _open_email_taken_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_signup_screen, text = "Email is already taken", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=515, y=204)

  # opens a top level window if password and confirm password do not match
  def _open_password_confirm_bad_prompt(self):
    font_user_pass_labels = customtkinter.CTkFont(family="Lexend", size=12)
    customtkinter.CTkLabel(master=self._frm_signup_screen, text = "Confirm Password Invalid", width=10, height=20, fg_color=gray_1, text_color=red_1, font=font_user_pass_labels, bg_color = gray_1).place(x=495, y=435)

 # opens a top level window if user wants to access admin privileges
  def _open_admin_login(self):
    if self._toplevel_window is None or not self._toplevel_window.winfo_exists():
      self._toplevel_window =  admin_login(self._submit_admin_password, self._admin_password)  # create window if its None or destroyed
      self._toplevel_window.focus()
      self._toplevel_window.grab_set() # focus window and cant close it
    else:
      self._toplevel_window.focus()  # if window exists focus it
      self._toplevel_window.grab_set() # focus window and cant close it

# opens a top level window if admin wants to delete a user account
  def _open_delete_account(self):
    if self._toplevel_window is None or not self._toplevel_window.winfo_exists():
      self._toplevel_window =  delete_account(self._delete_account, self._admin_password)  # create window if its None or destroyed
      self._toplevel_window.focus()
      self._toplevel_window.grab_set() # focus window and cant close it
    else:
      self._toplevel_window.focus()  # if window exists focus it
      self._toplevel_window.grab_set() # focus window and cant close it

  # opens the egram data window
  def _open_egram(self):
    if self._egram_window is None or not self._egram_window.winfo_exists():
        self._egram_window = egram_window(serial=self._serPacemaker)  # create window if its None or destroyed
        self._egram_window.focus()
        self._egram_window.grab_set()
    else:
        self._egram_window.focus()  # if window exists focus it
        self._egram_window.grab_set()

  ''' Variable monitoring functions '''
    # function to monitor changes to the current perms
  def _callback(self, *args):
    if self._perms.get() == "Admin": # going from client --> admin
      self._perm_label.configure(text=f"Permission: {self._perms.get()}")
      if self._serPacemaker != None and self._connected_status.get() != "X": # buttons that depends on admin + pacemaker ocnnection
        self._enable_button(self._btn_run)
        self._enable_button(self._btn_stop)
        self._enable_button(self._btn_verify)

      self._enable_button(self._btn_delete)
      self._enable_button(self._btn_edit)
      self._btn_admin.configure(text="Sign Out Admin", command=lambda: self._perms.set("Client"))
    else: # going from admin --> client
      self._perm_label.configure(text=f"Permission: {self._perms.get()}")
      self._disable_button(self._btn_run)
      self._disable_button(self._btn_stop)
      self._disable_button(self._btn_delete)
      self._disable_button(self._btn_edit)
      self._disable_button(self._btn_verify)
      self._can_edit.set(False)
      self._btn_edit.configure(text="Edit")
      self._btn_admin.configure(text="Admin", command=self._open_admin_login)

  # update funciton whenever the edit button is pressed or a new choice has been made from drop down menu
  def _callupdate(self, *args):
    if self._mode_choice.get() != 'None':
      self._frm_scroll_parameters.destroy() # destroy the current window so it prevents overlap
      dict_mode_parameters_for_user = self._current_user.get_all_mode_data()
      self._frm_scroll_parameters = scroll_parameters_frame(master=self._frm_main_interface, can_edit=self._can_edit.get(), width=665, height=540, fg_color=gray_1, current_mode=self._mode_choice.get(), current_mode_data=dict_mode_parameters_for_user[self._mode_choice.get()], send_data_func=self._get_parameter_data, init_data_func=self._init_parameters_on_mode_selection)
      self._frm_scroll_parameters.place(x=303,y=92)

  # monitors the connection status variable and changes the text of the label
  def _monitor_connection(self, *args):
    self._lbl_connected_status.configure(text=f'Pacemaker Connection {self._connected_status.get()}')
    try:
      if self._serPacemaker != None: # buttons that depends on pacemaker connection
        if self._perms.get() == "Admin": # buttons that depends on both admin and pacemaker conneciton
          self._enable_button(self._btn_run)
          self._enable_button(self._btn_stop)
          self._enable_button(self._btn_verify)

        self._enable_button(self._btn_show_egram) 
        self._pacing_on_connection(self._current_user.get_formatted_data()) # immediately send a pace to pacemaker when user logs in based on their last saved active mode
      else:
        self._disable_button(self._btn_run)
        self._disable_button(self._btn_show_egram)
        self._disable_button(self._btn_stop)
        self._disable_button(self._btn_verify)
    except:
      pass

  # monitor the battery status and update the text
  def _monitor_battery_level(self, *args):
    self._lbl_battery_status.configure(text=f'{self._battery_level.get()} 🔋')

  ''' Other Methods '''
  #Check if register user is valid
  def _sign_up_check(self, username, email, password, confirm_password):
    list_users = self._get_current_users(self._root_dir)
    c = len(list_users[0])
    remove_term = ".json"
    stat = 1

    for i in range(c):
      strip_username = list_users[0][i].replace(remove_term, '')
      if strip_username == username:
        stat = 0
        self._open_username_taken_prompt()
        break
      elif list_users[1][i] == email:
        stat = 0
        self._open_email_taken_prompt()
        break
      else:
        continue
    if password != confirm_password or password == '' or confirm_password == '':
      stat = 0 
      self._open_password_confirm_bad_prompt()

    if stat == 1:
      new_user = user(username = username, password = encrypt_password(password), email = email)
      new_user.save_to_json(self._root_dir)
      self._create_signup_screen()
      self._back_to_login()
      self._open_successful_register_prompt()

  # function to read all of the json file user data
  def _get_current_users(self, root_dir):
    all_user_data = [entry for entry in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, entry))]
    all_emails = []
    for user_file in all_user_data:
      with open(f"{root_dir}/{user_file}", 'r') as file:
        dict_user = json.load(file)
        all_emails.append(dict_user["_email"])
        
    return [all_user_data, all_emails]
  
  # attempt a login with the username and password
  def _attempt_login(self, username, password, all_user_data, root_dir):
    if f"{username}.json" in all_user_data[0]: # check for username
      with open(f"{root_dir}/{username}.json", 'r') as file:
        dict_user = json.load(file)
        
      if password == decrypt_password(dict_user["_password"]):
        current_user = user.load_from_json(dict_user)
        self._current_user = current_user
        self._pacing_on_connection(self._current_user.get_formatted_data())
        self._create_main_interface()
      else:
        dict_user.clear()
        self._open_credential_prompt()

    elif username in all_user_data[1]: # check for email is in system
      associated_user = all_user_data[0][all_user_data[1].index(username)] # associates an email with a username
      with open(f"{root_dir}/{associated_user}", 'r') as file: # opens that users file
        dict_user = json.load(file)
      
      if password == decrypt_password(dict_user["_password"]): # if passwords match then login
        current_user = user.load_from_json(dict_user)
        self._current_user = current_user
        self._pacing_on_connection(self._current_user.get_formatted_data())
        self._create_main_interface()
      else: # if it doesnt match then clear and give a notificaiton
        dict_user.clear()
        self._open_credential_prompt()

    else:
        self._open_credential_prompt()
  
  # submit the admin password from the popup window
  def _submit_admin_password(self):
    self._toplevel_window.destroy()
    self._perms.set("Admin")
  
  # delete the account
  def _delete_account(self):
    self._current_user.delete_account(self._root_dir)
    self._current_user = None
    self._toplevel_window.destroy()
    self._stop_pacing() # stop pacing when a user is deleted
    self._back_to_login()

  # toggles the button between the normal and disabled state
  def _toggle_button(self, btn):
    current_state = btn.cget('state')
    new_state = "normal" if current_state == "disabled" else "disabled"
    if new_state == "disabled":
      btn.configure(state=new_state, fg_color=gray_1)
    elif new_state == "normal":
      btn.configure(state=new_state, fg_color=btn.cget("border_color"))
  
  # disables all important buttons
  def _disable_button(self, btn):
    btn.configure(state="disabled", fg_color=gray_1)
  
  # enables all import buttons
  def _enable_button(self, btn):
    btn.configure(state="normal", fg_color=btn.cget("border_color"))

  # function to retrieve data from the scrollable frame class with the sliders to bring it into the main app class
  def _get_parameter_data(self, values, value_indexed):
    self._updated_parameter_values = values.copy()
    self._updated_parameter_values_indexed = value_indexed.copy()

  def _init_parameters_on_mode_selection(self, values, value_indexed):
    self._saved_parameter_values = values.copy()
    self._saved_parameter_values_indexed = value_indexed.copy()

    self._updated_parameter_values = values.copy()
    self._updated_parameter_values_indexed = value_indexed.copy()
  
  # command when the stop button is pressed
  def _stop_button_cmd(self):
    self._current_user.set_current_mode("Off")
    self._current_mode_lbl.configure(text=f'Current Mode: {self._current_user.get_current_mode()}')
    self._current_user.save_to_json(self._root_dir)
    self._pacing(selected_mode="Off")

  # command when the start button is pressed
  def _start_button_cmd(self, selected_mode):
    if self._mode_choice.get() != "None":
      self._current_user.set_current_mode(selected_mode)
      self._current_mode_lbl.configure(text=f'Current Mode: {self._current_user.get_current_mode()}')
      self._current_user.save_to_json(self._root_dir)
      self._pacing(selected_mode)
      self._verify_data_on_pacemaker()
    
  # command to send the current user parameters to simulink
  def _pacing(self, selected_mode):
    if self._saved_parameter_values_indexed != None:
      index_mode = dict_modes_enumeration[selected_mode]
      self._saved_parameter_values_indexed[0] = index_mode
    elif self._saved_parameter_values_indexed == None and selected_mode == "Off":
      self._saved_parameter_values_indexed = [0] * 26

    ''' Send to Pacemaker '''
    #print(f'PACED MODE: {self._saved_parameter_values_indexed}')
    self._serPacemaker.send_packet(self._saved_parameter_values_indexed)
    print(f'SENT TO PACEMAKER: {self._serPacemaker.receive_packet()}')

  def _pacing_on_connection(self, data): # function to control pacing when the pacemaker is connected
    if self._serPacemaker != None:
      self._serPacemaker.send_packet(data)
      print(f'PACEMAKER CONNECTED - SENT DATA: {self._serPacemaker.receive_packet()}')

  def _stop_pacing(self): # stop pacing when a user is deleted or when they log out
    if self._serPacemaker != None:
      self._serPacemaker.send_packet([0] * 26)
      print(f"PACMAKER STOP PACING")

  def _verify_data_on_pacemaker(self):
    if self._mode_choice.get() != "None":
      self._lbl_verify.configure("")
      time.sleep(0.5)
      data_on_pacemaker = list(self._serPacemaker.receive_packet()) # convert the tuple into a list for comparison
      current_check = self._updated_parameter_values_indexed.copy()
      current_check[0] = dict_modes_enumeration[self._mode_choice.get()]

      if data_on_pacemaker == current_check:
        self._lbl_verify.configure(text="✓")
      else:
        self._lbl_verify.configure(text="X")



''' Main '''
if __name__ == "__main__": 
  dcm = DCM() # intialize the app class
  dcm.protocol("WM_DELETE_WINDOW", dcm.quit) # close the window
  dcm.mainloop() # main loop

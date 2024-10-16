import sys
import time
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from PyQt5.QtCore import QCoreApplication
from design import Ui_MainWindow  # Import the generated UI class

class VehicleInstaller(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Set up the UI from the .ui file
        self.stackedWidget.setCurrentIndex(0)  # Ensure the first page is loaded at the start
        
        # Handle top window close event
        self.setWindowTitle("Vehicle Software Manager.")
        
        # Initialize variables to store combo box selections
        self.count = 0
        self.mode = 'install'
        self.robot = None

        self.amr_safety_lidar_selection_value = None
        self.amr_nav_lidar_selection_value = None
        self.amr_version_selection_value = None
        
        self.bopt_safety_lidar_selection_value = None
        self.bopt_nav_lidar_selection_value = None
        self.bopt_cam_selection_value = None
        self.bopt_version_selection_value = None
        
        self.save_data_to_file()

        self.init_ui_logic()

    def init_ui_logic(self):
        
        print("count is ",self.count)

        
        # Setting up common buttons
        cancel_buttons = [self.cancel_1, self.cancel_2, self.cancel_3, self.cancel_4, self.cancel_5, self.cancel_6, self.cancel_7]
        exit_buttons = [self.exit_1, self.exit_2]  
        for button in cancel_buttons:
            button.clicked.connect(self.confirm_cancel_action)
        for button in exit_buttons:
            button.clicked.connect(self.close_application)

            
        
        # Connect radio buttons to actions for 'mode_select_page'
        self.radioButton.setChecked(True)  # Install Software selected by default
        self.set_mode("install") # by default the install mode selected.
        self.radioButton.clicked.connect(lambda: self.set_mode("install"))
        self.radioButton_2.clicked.connect(lambda: self.set_mode("update"))
        self.radioButton_3.clicked.connect(lambda: self.set_mode("uninstall")) 
        self.pushButton_18.clicked.connect(self.next_page)  # Next button
        
        
        
        # Connect 'robot_select_page' push buttons
        
        self.amr_button.clicked.connect(self.handle_amr_robot)  # ACCUMOVER button
        self.bopt_button.clicked.connect(self.handle_bopt_robot)  # BOPT button
        self.rt_button.clicked.connect(self.handle_rt_robot)  # REACH TRUCK button
        self.shuttle_button.clicked.connect(self.handle_shuttle_robot)  # SHUTTLE button
        
        
        # Connect 'amr_snsr_select_page' push buttons and cobo boxes
        
        self.amr_safety_lidar_selection.setCurrentIndex(0)  # Default Safety Lidar selection
        self.amr_nav_lidar_selection.setCurrentIndex(0)     # Default Navigation Lidar selection
        
        self.amr_safety_lidar_selection_value = self.amr_safety_lidar_selection.itemText(0)
        self.amr_nav_lidar_selection_value = self.amr_nav_lidar_selection.itemText(0)

        
        self.amr_safety_lidar_selection.currentIndexChanged.connect(self.handle_amr_safety_lidar_selection) # Attach change events to combo box to capture the selected value
        self.amr_nav_lidar_selection.currentIndexChanged.connect(self.handle_amr_nav_lidar_selection) # Attach change events to combo box to capture the selected value
        
        self.pushButton_9.clicked.connect(self.next_page)  # NEXT button
        self.pushButton_10.clicked.connect(self.back_page)  #! BACK button
        
        
        
        # Connect 'amr_ver_select_page' combo_box and buttons 
        self.amr_version_selection.setCurrentIndex(0)  # Default Safety Lidar selection
        self.amr_version_selection_value = self.amr_nav_lidar_selection.itemText(0)

        self.amr_version_selection.currentIndexChanged.connect(self.handle_amr_version) # Attach change events to combo box to capture the selected value
        
        self.pushButton_38.clicked.connect(self.confirm_install_software)  # INSTALL button
        self.pushButton_37.clicked.connect(self.back_page)  #! BACK button
        
        
        
        
        # Connect 'bopt_snsr_select_page' push buttons and cobo boxes
        
        self.bopt_safety_lidar_selection.setCurrentIndex(0)  # Default Safety Lidar selection
        self.bopt_nav_lidar_selection.setCurrentIndex(0)     # Default Navigation Lidar selection
        self.bopt_cam_selection.setCurrentIndex(0)  #Default Camera Selection
        
        self.bopt_safety_lidar_selection_value = self.bopt_safety_lidar_selection.itemText(0) # Default value for bopt safety lidar
        self.bopt_nav_lidar_selection_value = self.bopt_nav_lidar_selection.itemText(0) # Default value for bopt nav lidar
        self.bopt_cam_selection_value = self.bopt_cam_selection.itemText(0) # Default value for bopt cam
        
        self.bopt_safety_lidar_selection.currentIndexChanged.connect(self.handle_bopt_safety_lidar_selection) # Attach change events to combo box to capture the selected value
        self.bopt_nav_lidar_selection.currentIndexChanged.connect(self.handle_bopt_nav_lidar_selection) # Attach change events to combo box to capture the selected value
        self.bopt_cam_selection.currentIndexChanged.connect(self.handle_bopt_cam_selection) # Attach change events to combo box to capture the selected value
        
        self.pushButton_12.clicked.connect(self.next_page)  # NEXT button
        self.pushButton_13.clicked.connect(lambda:self.go_to_page('robot_select_page'))  #! BACK button
        
        
        
        # Connect 'bopt_ver_select_page' combo_box and buttons 
        self.bopt_version_selection.setCurrentIndex(0)  # Default Safety Lidar selection
        self.bopt_version_selection_value = self.bopt_version_selection.itemText(0) # Default value for bopt version.

        self.bopt_version_selection.currentIndexChanged.connect(self.handle_amr_version) # Attach change events to combo box to capture the selected value
        
        self.pushButton_34.clicked.connect(self.confirm_install_software)  # INSTALL button
        self.pushButton_33.clicked.connect(self.back_page)  #! BACK button
        
        # Connect 'progress_page' ok button
        self.ok.clicked.connect(self.close_application)
        
        
        # Reach Struct Code....
            # Incomplete...

        # Shuttle Code....
            # Incomplete...
     
     
     
     
        
    # Below are the functions which will be envoked as the radio, combo, or push buttons pressed.



    def set_mode(self, mode):
        """Set the current mode based on user selection (Install, Update, Uninstall)."""
        self.mode = mode
        print(f"Mode selected: {self.mode}")
    
    def next_page(self):
        """Navigate to the next page in the stacked widget."""
        current_index = self.stackedWidget.currentIndex()
        if current_index < 10:
            print(f"Page({current_index}) --> {current_index+1}")
            self.stackedWidget.setCurrentIndex(current_index + 1)
        else:
            print("Already on last page.")

                    
    # def go_to_page(self, desired_index):
    #     """Navigate to the desired page."""
    #     current_index = self.stackedWidget.currentIndex()
    #     if desired_index <= 10 and desired_index >= 0:
    #         print(f"Going to page {desired_index} from {current_index}")
    #         self.stackedWidget.setCurrentIndex(desired_index)
    #     else:
    #         print("Bad Page Index value.", desired_index)

    def go_to_page(self, desired_object_name):
        """Navigate to the desired page by its object name."""
        current_widget = self.stackedWidget.currentWidget()  # Get the current page
        desired_page = self.findChild(QWidget, desired_object_name)  # Find the desired page by object name
        
        if desired_page:
            print(f"Page {current_widget.objectName()} --> {desired_object_name}")
            self.stackedWidget.setCurrentWidget(desired_page)
        else:
            print(desired_object_name,"Page Does not exist.")


    def back_page(self):
        """Navigate back to the previous page in the stacked widget."""
        current_index = self.stackedWidget.currentIndex()
        if current_index > 0:
            print(f"Page ({current_index}) --> {current_index-1}")
            self.stackedWidget.setCurrentIndex(current_index - 1)
        else:
            print("Already on the first page.")

    def confirm_cancel_action(self):
        """Show a confirmation dialog before canceling."""
        self.close()      
    
    def close_application(self):
        """Close the application when Exit is clicked or on Cancel."""
        QCoreApplication.quit()
        # self.close()

    def closeEvent(self, event):
        """Handle the window close button event."""
        close_confirmation = QMessageBox.question(self, "Exit Application",
                                                  "Are you sure you want to exit?",
                                                  QMessageBox.Yes | QMessageBox.No,
                                                  QMessageBox.No)
        if close_confirmation == QMessageBox.Yes:
            print("Exiting the application.")
            event.accept()
        else:
            event.ignore()
            
            
    def handle_amr_robot(self):
        print("amr selected.")
        self.robot = 'amr'
        self.go_to_page("amr_snsr_select_page")
        
    def handle_bopt_robot(self):
        print("bopt selected.")
        self.robot = 'bopt'
        self.go_to_page("bopt_snsr_select_page")
    
    def handle_rt_robot(self):
        print("rt selected.")
        self.robot = 'rt'
        self.go_to_page("rt_snsr_page")
    
    def handle_shuttle_robot(self):
        print("amr selected.")
        self.robot = 'shuttle'
        self.go_to_page("shuttle_page")
            
    
    
    # Define the handlers for combo box selections

    def handle_amr_safety_lidar_selection(self, index):
        """Handle AMR safety lidar selection and store the selected value."""
        self.amr_safety_lidar_selection_value = self.amr_safety_lidar_selection.itemText(index)
        print(f"AMR safety lidar selected: {self.amr_safety_lidar_selection_value}")

    def handle_amr_nav_lidar_selection(self, index):
        """Handle AMR navigation lidar selection and store the selected value."""
        self.amr_nav_lidar_selection_value = self.amr_nav_lidar_selection.itemText(index)
        print(f"AMR navigation lidar selected: {self.amr_nav_lidar_selection_value}")

    def handle_amr_version(self, index):
        """Handle AMR version selection and store the selected value."""
        self.amr_version_selection_value = self.amr_version_selection.itemText(index)
        print(f"AMR version selected: {self.amr_version_selection_value}")

    def handle_bopt_safety_lidar_selection(self, index):
        """Handle BOPT safety lidar selection and store the selected value."""
        self.bopt_safety_lidar_selection_value = self.bopt_safety_lidar_selection.itemText(index)
        print(f"BOPT safety lidar selected: {self.bopt_safety_lidar_selection_value}")

    def handle_bopt_nav_lidar_selection(self, index):
        """Handle BOPT navigation lidar selection and store the selected value."""
        self.bopt_nav_lidar_selection_value = self.bopt_nav_lidar_selection.itemText(index)
        print(f"BOPT navigation lidar selected: {self.bopt_nav_lidar_selection_value}")
        
    def handle_bopt_cam_selection(self, index):
        """Handle BOPT navigation cam selection and store the selected value."""
        self.bopt_cam_selection_value = self.bopt_cam_selection.itemText(index)
        print(f"BOPT navigation lidar selected: {self.bopt_nav_lidar_selection_value}")

    def handle_bopt_version(self, index):
        """Handle BOPT version selection and store the selected value."""
        self.bopt_version_selection_value = self.bopt_version_selection.itemText(index)
        print(f"BOPT version selected: {self.bopt_version_selection_value}")
        
    
    # Installation.
        
    def confirm_install_software(self,):
        """Show a confirmation dialog before proceeding with installation."""
        action = self.mode.capitalize()
        reply = QMessageBox.question(self, f'{action} Confirmation',
                                        f'Are you sure you want to {self.mode} the software?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save_data_to_file()
            self.go_to_page('progress_page')
        else:
            print(f"{self.mode.capitalize()} canceled.")
        
    
    # def install_software(self):
    #     """Handle the installation process based on the selected conditions."""
    #     if self.mode == "install":
    #         if self.robot == 'amr':
    #             print("Installing software for amr...")
    #             print(f"AMR Safety Lidar: {self.amr_safety_lidar_selection_value}")
    #             print(f"AMR Navigation Lidar: {self.amr_nav_lidar_selection_value}")
    #             print(f"AMR Version: {self.amr_version_selection_value}")
    #             # Use these variables to handle different conditions in your installation logic
    #             self.go_to_page('progress_page')
    #             self.installed()
    #         elif self.robot == 'bopt':
    #             print("Installing software...")
    #             print(f"bopt Safety Lidar: {self.bopt_safety_lidar_selection_value}")
    #             print(f"bopt Navigation Lidar: {self.bopt_nav_lidar_selection_value}")
    #             print(f"bopt Version: {self.bopt_version_selection_value}")
    #             # Use these variables to handle different conditions in your installation logic
    #             self.go_to_page('progress_page')
    #             self.installed()

    #         else:
    #             print("Nothing to install.")       
            
    #     elif self.mode == "update":
    #         print("Updating software...")
    #         self.go_to_page('progress_page')
    #     elif self.mode == "uninstall":
    #         print("Uninstalling software...")
    #         self.go_to_page('progress_page')
    #     else:
    #         print("No mode selected. Please choose Install, Update, or Uninstall.")
            
        
        
    def installed(self):
        print("Software Installed Successfully.")
        time.sleep(2)
        self.stackedWidget.setCurrentIndex(9)  # Final success page.
    
    # Method to save the data to a JSON file
    def save_data_to_file(self):
        data = {
            "mode": self.mode,
            "robot": self.robot,
            "amr_safety_lidar": self.amr_safety_lidar_selection_value,
            "amr_nav_lidar": self.amr_nav_lidar_selection_value,
            "amr_version": self.amr_version_selection_value,
            "bopt_safety_lidar": self.bopt_safety_lidar_selection_value,
            "bopt_nav_lidar": self.bopt_nav_lidar_selection_value,
            "bopt_cam": self.bopt_cam_selection_value,
            "bopt_version": self.bopt_version_selection_value,
        }
        
        print(data)

        with open('vehicle_installer_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("Data saved to file successfully.")
    
   



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VehicleInstaller()
    window.show()
    sys.exit(app.exec_())

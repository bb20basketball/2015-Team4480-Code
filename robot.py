import wpilib
import wpilib.buttons
class MyRobot(wpilib.IterativeRobot):
    
    
    ##############SET UP FOR XBOX CONTROLLER###################
    
    
    def robotInit(self):
        #Motor controllers, joysticks, and setting up the drive type
        self.motor1=wpilib.Jaguar(0)
        self.motor2=wpilib.Jaguar(1)
        self.slide_motor=wpilib.Jaguar(2)
        self.non_existant_motor=wpilib.Jaguar(4)
        self.tryit=wpilib.Jaguar(6)
        self.red=wpilib.Jaguar(9)
        self.blue=wpilib.Jaguar(8)
        self.green=wpilib.Jaguar(7)
        self.robot_drive = wpilib.RobotDrive(self.motor2,self.motor1)
        self.stick1 = wpilib.Joystick(0)
        self.joystick_button=wpilib.buttons.JoystickButton(self.stick1, 1)
        
        self.lights=wpilib.buttons.JoystickButton(self.stick1, 2)
        #All our clicky switches
        self.clicky1=wpilib.DigitalInput(9)
        self.clicky2=wpilib.DigitalInput(8)
        self.clicky3=wpilib.DigitalInput(7)
        wpilib.SmartDashboard.putBoolean("Clicky1",self.clicky1.get())
        self.chooser=wpilib.SendableChooser()
        self.chooser.addObject("Auto 1","1")
        wpilib.SmartDashboard.putData('What Automous', self.chooser)
        self.counter=0
    
    def autonomousInit(self):
        
        self.auto_loop_counter = 1
    #self.user_choice=self.chooser.getSelected()
    
    def autonomousPeriodic(self):

        
        #100 loops == about 2 seconds
        default=(0,0)
        non=0
        if self.auto_loop_counter <= 100 and self.auto_loop_counter>0:
            default=(-.5,0) # Drive forwards at half speed
            self.auto_loop_counter += 1
            self.sol.set(False)
        else:
            pass    #Stop robot
    
        #Doing this so there is no motor safety error#
        self.robot_drive.drive(default[0],default[1])
        self.non_existant_motor.set(non)
    
    
    def teleopPeriodic(self):
        """This function is called periodically dturing operator control."""
        #Smart Dashboad things#
        
        #Sends either a True or False to the Dashboard so drivers can drive better#
        wpilib.SmartDashboard.putBoolean("Clicky1",self.clicky1.get())
        wpilib.SmartDashboard.putBoolean("Clicky2",self.clicky2.get())
        wpilib.SmartDashboard.putBoolean("Clicky3",self.clicky3.get())
        
        #Getting the right stick of the xbox controller#
        self.right_stickX=self.stick1.getRawAxis(4)
        #self.green.set(1)
        #Getting the triggers#
        self.right_trig=self.stick1.getRawAxis(2)
        self.left_trig=-1*self.stick1.getRawAxis(3)
        #Boost mode for more speed#
        if self.joystick_button.get()==True: #If "a" is pressed, fire the piston on port 4#
            multi=.75
        else:
            multi=.5
        #The motor might not get enough power with 40 percent so might need to change it#
        total=.4*(self.right_trig+self.left_trig)
        #Dead zone for the slide motor#
        if self.right_stickX<.1 and self.right_stickX >-.1:
            new_right=0
        else:
            new_right=self.right_stickX
        #If button pressed, change counter#
        if self.lights.get()==True:
            if self.counter>6:
                self.counter=0
            wpilib.Timer.delay(.05)
            self.counter+=1
        
        #I set up 6 random colors for LEDs. Every time you press it, it changes color or if the counter is on 7, shutoff
        #LEDs#
        if self.counter==1:
            green=0
            blue=1
            red=1
        elif self.counter==2:
            green=0
            blue=0
            red=1
        elif self.counter==3:
            green=1
            blue=0
            red=0
        elif self.counter==4:
            green=1
            blue=1
            red=0
        elif self.counter==5:
            green=0
            blue=1
            red=0
        elif self.counter==6:
            green=0
            blue=1
            red=1
        else:
            green=0
            blue=0
            red=0
        #Turns on the LEDs#
        self.green.set(green)
        self.red.set(red)
        self.blue.set(blue)
        
        #Running all the motors#
        self.non_existant_motor.set(total)
        self.slide_motor.set(new_right)
        self.robot_drive.arcadeDrive(multi*self.stick1.getY(),multi*self.stick1.getX(),True)

if __name__ == "__main__":
    wpilib.run(MyRobot)

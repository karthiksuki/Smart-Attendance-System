import os  # os functions
from Code import capture_image, check_camera, recognize, train_image


def title_bar():
    os.system('cls')
    print("\t***** Face Recognition Attendance System *****")


def mainMenu():
    title_bar()
    print()
    print(10 * "*", "SMART ATTENDANCE SYSTEM => MENU", 10 * "*")
    print("[1] Check Camera")
    print("[2] Capture Faces (DATA)")
    print("[3] Train Images (MODEL)")
    print("[4] Recognize & Attendance (PREDICTION)")
    print("[5] Auto Mail")
    print("[6] Quit")
    while True:
        try:
            choice = int(input("Enter Choice: "))
            if choice == 1:
                check_camera.camera()
                break
            elif choice == 2:
                CaptureFaces()
                break
            elif choice == 3:
                Trainimages()
                break
            elif choice == 4:
                recognizeFaces()
                break
            elif choice == 5:
                os.system("python automail.py")
                break
                mainMenu()
            elif choice == 6:
                print("Thank You")
                break
            else:
                print("Invalid Choice. Enter 1-4")
                mainMenu()
        except ValueError:
            print("Invalid Choice. Enter 1-4\n Try Again")
    exit


# camera test function from check camera.py file
def checkCamera():
    check_camera.camera()
    key = input("Enter any key to return main menu")
    mainMenu()


# image function form capture image.py file
def CaptureFaces():
    capture_image.takeImages()
    key = input("Enter any key to return main menu")
    mainMenu()


# train images from train_images.py file
def Trainimages():
    train_image.TrainImages()
    key = input("Enter any key to return main menu")
    mainMenu()


# recognize_attendance from recognize.py file
def recognizeFaces():
    recognize.recognize_attendence()
    key = input("Enter any key to return main menu")
    mainMenu()


# main driver
mainMenu()

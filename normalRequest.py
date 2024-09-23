from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,Toplevel,Menu,Menubutton,StringVar
from MysqlCode import Database
from reportInsertion import DatabaseManager

class unregisteredRequest:
    OUTPUT_PATH = Path(__file__).parent
    # ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\admin\OneDrive\VS-CODE\SEM4_MiniProject\Foundmate_3.1\ReportOthers\assets\frame0")
    ASSETS_PATH = OUTPUT_PATH / Path(r"ReportOthers\assets\frame0")

    def relative_to_assets(self, path: str) -> Path:
        file_path = self.ASSETS_PATH / Path(path)
        if file_path.exists():
            return file_path
        else:
            print(f"Warning: File not found: {file_path}")
            return file_path

    def __init__(self,master,userId):
        self.master=Toplevel()
        self.master.geometry("433x643")
        self.master.configure(bg = "#FFFFFF")
        self.userId = userId
        self.db = Database()
        self.ri = DatabaseManager(self.userId)
        self.setup_ui()

    def setup_ui(self):
        self.canvas = Canvas(
            self.master,
            bg = "#FFFFFF",
            height = 643,
            width = 433,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            433.9263916015625,
            642.0,
            fill="#D9D9D9",
            outline="black")

        image_details = [
            {"file": "image_9.png", "position": (216.649169921875, 326.37127685546875)},
            {"file": "image_2.png", "position": (214.255859375, 474.5950927734375)},
            {"file": "image_3.png", "position": (315.19970703125, 393.4459533691406)},
            {"file": "image_4.png", "position": (142.746826171875, 393.4459533691406)},
            {"file": "image_5.png", "position": (212.77001953125, 342.35296630859375)},
            {"file": "image_6.png", "position": (120.77001953125, 130.9427490234375)},
            {"file": "image_7.png", "position": (209.327392578125, 180.6349334716797)},
            {"file": "image_8.png", "position": (120.763671875, 82.76364135742188)},
        ]

        self.image_objects = {}

        for idx, details in enumerate(image_details):
            image_path = self.relative_to_assets(details["file"])
            self.image_objects[idx] = PhotoImage(file=image_path)
            canvas_image = self.canvas.create_image(
                details["position"][0],
                details["position"][1],
                image=self.image_objects[idx]
            )

        self.submit_button = Button(
            self.master,
            text="Submit",
            bg="#5C4D4D",
            fg="#FFFFFF",
            font=("InknutAntiqua Regular", 16),
            command=self.putdata,
            relief="raised", 
            bd=5,  
            padx=10, 
            pady=5,  
            activebackground="#7F6E6E",
            activeforeground="#000000",
            highlightthickness=0 
        )
        self.submit_button.place(
            x=162.393798828125,
            y=538.4631958007812,
            width=109.02468872070312,
            height=40.05535888671875
        )

        self.canvas.create_text(
            20.9124755859375,
            15.742431640625,
            anchor="nw",
            text="UNREGISTERED REQUEST",
            fill="#3E3333",
            font=("InknutAntiqua Regular", 30 * -1,'bold')
        )

        self.description_textBox = Text(
            self.master,
            bd=5,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("InknutAntiqua Regular", 12)
        )
        self.description_textBox.place(
            x=88.27197265625,
            y=213.0947265625,
            width=257.0615539550781,
            height=101.01718139648438
        )

        self.create_building_menu()
        self.create_floor_menu()
        self.create_room_menu()

        self.create_others_color_menu()
        self.create_catagory_menu()

    def create_catagory_menu(self):
        catagory_options = ["Laptop", "Mobile phone", "Calculator", "USB flash drive", "Headphones","Books", "Stationery (pens, pencils, erasers, etc.)", "ID card", "Keys (room keys, locker keys, etc.)","Water bottle", "Wallet or purse", "Jacket or coat", "Sunglasses", "Umbrella","Charger (phone charger, laptop charger, etc.)", "Sports equipment", "Lab equipment or tools","Glasses or sunglasses", "Backpack or bag", "Lunch box or food container"]
        self.selected_category_option=StringVar(self.master)
        self.selected_category_option.set(catagory_options[0])

        self.create_menu_button(self.canvas,x=185,y=65, width=170, height=35,options=catagory_options,var=self.selected_category_option)   

    def create_others_color_menu(self):
        laptop_colors = ["None","red", "green", "blue", "yellow", "magenta", "cyan", "maroon", "green2", "navy", "olive", "purple", "teal", "orange", "gray", "white", "black"]

        self.selected_mobile_color=StringVar(self.master)
        self.selected_mobile_color.set(laptop_colors[0])

        self.create_menu_button(self.canvas,x=185,y=112, width=170, height=35,options=laptop_colors,var=self.selected_mobile_color)           

    def create_building_menu(self):
        building_options = ["None", "New Building", "Old Building"]
        self.selected_building = StringVar(self.master)
        self.selected_building.set(building_options[0])
        self.selected_building.trace_add("write", self.update_floor_options)

        self.create_menu_button(self.canvas, x=60, y=415, width=165, height=35,options=building_options,var=self.selected_building)

    def create_floor_menu(self):
        self.floor_options = {
            "New Building": ["None", "Ground Floor" ,"1st Floor", "2nd Floor", "3rd Floor", "4th Floor", "5th Floor", "6th Floor", "7th Floor"],
            "Old Building": ["None", "Ground Floor", "1st Floor", "2nd Floor", "3rd Floor", "4th Floor", "5th Floor", "6th Floor", "7th Floor", "8th Floor", "9th Floor", "10th Floor", "11th Floor"]
        }

        self.selected_floor = StringVar(self.master)
        building = self.selected_building.get()
        
        # Check if the selected building is in floor_options dictionary
        if building in self.floor_options:
            self.selected_floor.set(self.floor_options[building][0])
        else:
            self.selected_floor.set("None")

        self.menu_floor = self.create_menu_button(self.canvas, x=270, y=415, width=90, height=35,options=self.floor_options.get(building, ["None"]),var=self.selected_floor)
                
    def update_floor_options(self, *args):
        selected_building = self.selected_building.get()
        new_floor_options = self.floor_options.get(selected_building, ["None"])

        # Set the selected floor to "None" when building option changes
        self.selected_floor.set("None")

        # Update the floor options in the menu
        self.menu_floor.delete(0, "end")

        for floor in new_floor_options:
            self.menu_floor.add_command(label=floor, command=lambda f=floor: self.selected_floor.set(f))

    def create_room_menu(self):
        catagory_room= ["None", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Ladies toilet", "Gents Toilet"]
        self.selected_room=StringVar(self.master)
        self.selected_room.set(catagory_room[0])

        self.create_menu_button(self.canvas, x=170, y=495, width=90, height=35,options=catagory_room,var=self.selected_room)


    def create_menu_button(self, master, x, y, width, height, options, var):
        menubutton = Menubutton(
            master,
            textvariable=var,
            font=("Helvetica", 12, "bold"),
            indicatoron=True,
            borderwidth=1,
            relief="ridge",
            bd=5,
            bg="#5C4D4D",
            fg="#DBDBDB"
        )
        menubutton.place(x=x, y=y, width=width, height=height)

        menu = Menu(menubutton, tearoff=False)
        menubutton["menu"] = menu

        for option in options:
            menu.add_command(label=option, command=lambda o=option: var.set(o))

        return menu  

    def putdata(self):
            building_name=self.selected_building.get()
            floor=self.selected_floor.get()
            room=self.selected_room.get()
            color = self.selected_mobile_color.get()
            if self.ri.check_for_request(userId = self.userId, name = self.selected_category_option.get() ,color = self.selected_mobile_color.get() ,building = self.selected_building.get(), floor = self.selected_floor.get(), room = self.selected_room.get(),description = self.description_textBox.get("1.0", "end-1c")):
                c = self.db.insert_ReportOthers_data(
                    userId=self.userId,
                    name=self.selected_category_option.get(),
                    color=self.selected_mobile_color.get(),
                    building=self.selected_building.get(),
                    floor=self.selected_floor.get(),
                    room=self.selected_room.get(),
                    description=self.description_textBox.get("1.0", "end-1c")
                )
                self.master.destroy()
            else:
                self.master.destroy()



    def showrequestUnRegisteredDevice(self):
        self.master.wait_window(self.master)

if __name__=="__main__":
    master = Tk()
    master.resizable(False, False)
    app=unregisteredRequest(master,4)
    master.mainloop()

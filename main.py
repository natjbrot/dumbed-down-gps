from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_title("Dumbed Down GPS")
set_site_information(
    author="N. Brothers",
    description="Calculate travel distance and time.",
    sources=[],
    planning=[],
    links=[]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class StateInfo:
    Name: str
    Xcord: int
    Ycord: int
    
@dataclass
class modeInfo:
    Type: str
    average_mph: int
    
@dataclass
class State:
    Current_state: str
    Destination_state:str
    mode_of_Transport: str
    Distance: int
    Travel_time: int
    allstates: dict
    allmodes: dict
    
allmodes = {
    "Walk": modeInfo("Walk",3),
    "Run": modeInfo("Run",6),
    "Car": modeInfo("Car",30),
    "Train": modeInfo("Train",40),
    "Bike": modeInfo("Bike",15),
    "Plane": modeInfo("Plane",500)
}


allstates = {
    "Delaware": StateInfo("Delaware",414,122),
    "Alabama": StateInfo("Alabama",363,87),
    "Alaska": StateInfo("Alaska",80,325),
    "Hawaii": StateInfo("Hawaii",47,18),
    "California": StateInfo("California",210,110),
    "Oregon": StateInfo("Oregon",208,150),
    "Washington": StateInfo("Washington",208,175),
    "Idaho": StateInfo("Idaho",235,155),
    "Nevada": StateInfo("Nevada",225,123),
    "Utah": StateInfo("Utah",249,123),
    "Arizona": StateInfo("Arizona",249,95),
    "Montana": StateInfo("Montana",260,170),
    "Wyoming": StateInfo("Wyoming",268,147),
    "Colorado": StateInfo("Colorado",277,121),
    "New Mexico": StateInfo("New Mexico",275,95),
    "Texas": StateInfo("Texas",305,80),
    "Oklahoma": StateInfo("Oklahoma",315,101),
    "Kansas": StateInfo("Kansas",310,115),
    "Nebraska": StateInfo("Nebraska",302,137),
    "South Dakota": StateInfo("South Dakota",302,155),
    "North Dakota": StateInfo("North Dakota",300,175),
    "Minnesota": StateInfo("Minnesota",328,165),
    "Iowa": StateInfo("Iowa",333,140),
    "Missouri": StateInfo("Missouri",337,117),
    "Arkansas": StateInfo("Arkansas",338,98),
    "Louisiana": StateInfo("Louisiana",337,78),
    "Wisconsin": StateInfo("Wisconsin",350,155),
    "Illinois": StateInfo("Illinois",352,126),
    "Mississippi": StateInfo("Mississippi",350,85),
    "Michigan": StateInfo("Michigan",370,157),
    "Tennessee": StateInfo("Tennessee",364,102),
    "Kentucky": StateInfo("Kentucky",369,112),
    "Indiana": StateInfo("Indiana",366,126),
    "Ohio": StateInfo("Ohio",381,128),
    "Florida": StateInfo("Florida",386,65),
    "Georgia": StateInfo("Georgia",379,86),
    "South Carolina": StateInfo("South Carolina",391,91),
    "North Carolina": StateInfo("North Carolina",398,101),
    "Virginia": StateInfo("Virginia",400,112),
    "West Virginia": StateInfo("West Virginia",390,118),
    "Maryland": StateInfo("Maryland",409,122),
    "Pennsylvania": StateInfo("Pennsylvania",404,132),
    "New Jersey": StateInfo("New Jersey",419,128),
    "New York": StateInfo("New York",415,145),
    "Rhode Island": StateInfo("Rhode Island",433,138),
    "Connecticut": StateInfo("Connecticut",428,137),
    "Massachusetts": StateInfo("Massachusetts",431,141),
    "Vermont": StateInfo("Vermont",427,151),
    "New Hampshire": StateInfo("New Hampshire",433,150),
    "Maine": StateInfo("Maine",444,160)
}



@route("/")
def homepage(state: State) -> Page:
    """the starting page of the site, has buttons including
    the disclaimer, about page, and first step in planning."""
    return Page(
        state,
        [
            Header("Dumbed Down GPS"),
            Text("Welcome to Dumbed Down GPS!"),
            Text("Calculate the distance between two states."),
            Button("Begin Planning", "/firststate"),
            Button("About", "/aboutpage"),
            Button("Disclaimer","/disclaimerpage")
        ]
    )
    
@route("/aboutpage")
def about_page(state: State) -> Page:
    """takes the user to a page in which they are provided
    with general information about the site"""
    return Page(
        state,
        [
            Header("About this site"),
            Text("In this site, you will be able to loosely determine the distance and time required to travel from one state to another, acting as a primitive sort of GPS. Just input your current state, the state you wihs to go to, and then how you will get there. After that, everything will be calculated and given to you."),
            Button("Back", "/")
        ]
    )
    
@route("/disclaimerpage")
def disclaimer_page(state: State) -> Page:
    """allows the user to view a page in which they are detailed
    with a disclaimer that warns the user of potential misinformation"""
    return Page(
        state,
        [
            Header("Small Disclaimer"),
            Text("The values given in this site are not ones that should be taken to heart. The distances are calculated with straight line paths, from the center of states, with no regard for conditions that may affect the journey. The time is also loosely based off of average travel speeds in a straight line nonstop, so should not be taken entirely to heart. They are mere estimates."),
            Button("Back", "/")
        ]
    )

@route("/firststate")
def state_page(state: State) -> Page:
    """allows the user to pick out the state they wish to 
    start their travels from"""
    return Page(
        state,
        [
            Header("Choose your travel plan!"),
            Text("Type your current state"),
            TextBox("Current", state.Current_state),
            Button("Confirm", "/otherstate")
        ]
    )
    
@route("/otherstate")
def statet_page(state: State, Current: str = "") -> Page:
    """switches to the page in which the user can input
    their destination state"""
    state.Current_state = Current
    return Page(
        state,
        [
            Header("Finish the plan!"),
            Text("Type your destination state"),
            TextBox("Destination", state.Destination_state),
            Button("Confirm", "/modeselect")
        ]
    )
    
@route("/modeselect")
def transport_page(state: State, Destination: str = "") -> Page:
    """allows the user to select the mode of transportation
    they would like to use"""
    state.Destination_state = Destination
    return Page(
        state,
        [
            Header("How will you travel?"),
            Text("Type how you will travel"),
            Text("(Walk,Run,Car,Train,Bike,Plane)"),
            TextBox("mode", state.mode_of_Transport),
            Button("Confirm", "/resultspage")
        ]
     )
     
@route("/resultspage")
def result_page(state: State, mode: str = "") -> Page:
    """displays the completed calculations of the website,
    along with the states and mode of transportation chosen.
    Also gives the option to restart."""
    state.mode_of_Transport = mode
    
    if state.Current_state not in allstates:
        return Page(state, [
            Header("Error"),
            Text("State not recognized."),
            Button("Retry", "/firststate")
        ])
        
    if state.Destination_state not in allstates:
        return Page(state, [
            Header("Error"),
            Text("State not recgonized."),
            Button ("Retry", "/otherstate")
        ])
        
    if mode not in allmodes:
        return Page(state, [
            Header("Error"),
            Text("mode not recognized"),
            Button("Retry", "/modeselect")
        ])
        
    state.Distance = get_distance(
        state.Current_state,
        state.Destination_state,
        state.allstates
    )
    
    state.Travel_time = get_time(state.Distance, mode)
    
    return Page(
        state,
        [
            Header("Trip Details"),
            Row(Text("Starting State: "+ state.Current_state)),
            Row(Text("Destination State: "+ state.Destination_state)),
            Row(Text("mode of Transport: "+ state.mode_of_Transport)),
            Row(Text("Distance: "+ str(state.Distance) + " miles")),
            Row(Text("Travel Time: "+ str(state.Travel_time) + " hours")),
            Button("Start Over", "/")
        ]
     )
    
def get_state_y(loca:str, states: dict) -> int:
    """identifies the y coordinate for the chosen state."""
    for state_info in states.values():
        if state_info.Name == loca:
            return state_info.Ycord
            
def get_state_x(loca:str, states: dict) -> int:
    """identifies the x coordinate for the chosen state."""
    for state_info in states.values():
        if state_info.Name == loca:
            return state_info.Xcord

def calc_distance(x1: int, x2: int, y1: int, y2: int) -> int:
    """defines the formula that will be used to calculate the distances
    being travelled."""
    xdistance =  0
    ydistance =  0
    if x2 >= x1:
        xdistance = int(x2 - x1)
    else:
        xdistance = int(x1 - x2)
    if y2 >= y1:
        ydistance = int(y2 - y1)
    else:
        ydistance = int(y1 - y2)
    return int((((xdistance**2)+(ydistance**2))**0.5))

def get_distance(curstate:str,destate:str, states: dict) -> float:
    """Takes the names of two states, and calculates the distance in miles
    between their centers."""
    x1 = get_state_x(curstate, states)
    y1 = get_state_y(curstate, states)
    x2 = get_state_x(destate, states)
    y2 = get_state_y(destate, states)
    distance =  (calc_distance(x1,x2,y1,y2)*10 ) 
    return distance

def get_time(distance: int, mode:str) -> int:
    """Calculates an estimated travel time using the 
    previously calculated distance and the given mode"""
    for mod in allmodes:
        if mod == mode:
            average_speed = allmodes[mode].average_mph
            return int(distance / average_speed)
            
assert_equal(calc_distance(0,3,0,4),5)
assert_equal(get_state_x("Delaware", allstates), 414)
assert_equal(get_state_y("Delaware",allstates), 122)
assert_equal(get_distance("Delaware","Maryland", allstates), 50)
assert_equal(get_time(120, "Car"), 4)
    
    
start_server(State("", "", "", 0, 0, allstates, allmodes))           


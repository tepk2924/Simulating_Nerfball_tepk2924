import math
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import yaml

ball_diameter = 0.045 #Ball diameter
A = math.pi * ball_diameter**2 / 4 #Ball Cross-Section Area, m^2
m = 0.004 #Ball mass, kg
rho = 1.29 #Air Density, kg/m^3
g = 9.81 #gravitational acc, m/s^2

h = 0.0001 #step_size, sec
ITERATIONS = 5000

deg = math.pi/180

with open(input("yaml file dir : "), "r") as f:
    configs = yaml.safe_load(f)

class vec4:
    def __init__(self, x, y, X, Y):
        self.x = x
        self.y = y
        self.X = X
        self.Y = Y
    
    def __rmul__(self, c):
        return vec4(c*self.x, c*self.y, c*self.X, c*self.Y)
    
    def __add__(self, other:"vec4"):
        return vec4(self.x + other.x,
                    self.y + other.y,
                    self.X + other.X,
                    self.Y + other.Y)
    
    def __repr__(self):
        return f"vec4({self.x}, {self.y}, {self.X}, {self.Y})"

size = len(configs)
rows = cols = math.ceil(size**0.5)

for idx, configkey in enumerate(configs, start=1):

    config = configs[configkey]
    print(config)

    plt.subplot(rows, cols, idx)

    Cd = config["Cd"]
    initial_height = config["initial_height"]
    initial_angle = config["initial_angle"]
    initial_speed = config["initial_speed"]
    x_hoop = config["x_hoop"]
    backboard = config["backboard"]
    e = config["e"]
    y_hoop = 0.195
    hoop_radius = 0.075

    x = [0] #ball x-coor
    y = [initial_height] #ball y-coor
    X = [initial_speed*math.cos(initial_angle*deg)] #ball x-vel
    Y = [initial_speed*math.sin(initial_angle*deg)] #ball y-vel

    def f(vec: vec4):
        return vec4(vec.X,
                    vec.Y,
                    (-1/(2*m))*vec.X*Cd*rho*A*(vec.X**2 + vec.Y**2)**0.5,
                    (-1/(2*m))*vec.Y*Cd*rho*A*(vec.X**2 + vec.Y**2)**0.5 - g)

    vec = vec4(x[0], y[0], X[0], Y[0])

    for i in range(ITERATIONS):
        k1: vec4 = f(vec)
        k2: vec4 = f(vec + (h/2)*k1)
        k3: vec4 = f(vec + (h/2)*k2)
        k4: vec4 = f(vec + h*k3)
        vec = vec + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        if backboard and vec.x > x_hoop + hoop_radius - ball_diameter/2 and vec.y > y_hoop and vec.X > 0:
            vec.X = -e*vec.X
        if i%50 == 0:
            plt.gca().add_patch(pat.Circle((vec.x, vec.y), ball_diameter/2, edgecolor="b", facecolor="none"))

        x.append(vec.x)
        y.append(vec.y)
        X.append(vec.X)
        Y.append(vec.Y)

    plt.scatter(x, y, s=1, marker=".", label=configkey+"_ballcenter")
    plt.scatter(x_hoop, y_hoop, s=100, marker=".", label=configkey+"_hoopcenter")
    plt.scatter([x_hoop - hoop_radius, x_hoop + hoop_radius], [y_hoop]*2, s=100, marker=".", label=configkey+"_hooprim")
    if backboard:
        plt.plot([x_hoop + hoop_radius]*2, [y_hoop, y_hoop + 0.15], label=configkey+"_backboard")
    plt.xlim(0, 1)
    plt.ylim(0, 0.5)
    plt.legend()
    plt.title(configkey)

plt.show()
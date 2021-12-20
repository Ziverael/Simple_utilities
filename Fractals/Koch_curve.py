import turtle as tt
from math import sqrt

def koch_curve(level : int, turtle : tt.Turtle, step : int) -> None :

    if not level:
        turtle.fd(step)
        return
    
    step /= 3
    koch_curve(level - 1, turtle, step)
    turtle.lt(60)
    koch_curve(level - 1, turtle, step)
    turtle.rt(120)
    koch_curve(level - 1, turtle, step)
    turtle.lt(60)
    koch_curve(level - 1, turtle, step)

def koch_snow_flake(level : int, turtle : tt.Turtle, step : int) -> None :
    turtle.penup()
    turtle.lt(150)
    turtle.fd(step * sqrt(3) / 3)
    turtle.rt(150)
    turtle.pendown()
    turtle.begin_fill()
    koch_curve(level, turtle, step)
    turtle.rt(120)
    koch_curve(level, turtle, step)
    turtle.rt(120)
    koch_curve(level, turtle, step)
    turtle.end_fill()


def main():
    level = ''
    while not type(level) == int:
        level = input("pass level of Koch curve... ")
        try:
            level = int(level)
            if level < 1:
                print("you must pass positive number" )
                level = ''
        except:
            print("you must pass positive number" )
        
    window = tt.getscreen()
    window.title('Koch Curve')
    window.screensize(500, 500)
    tt.ht()
    turtle = tt.Turtle(visible = False)
    turtle.speed(10)
    turtle.color('black', 'blue')
    turtle.ht()
    koch_snow_flake(level, turtle, 500)
    tt.done()

if __name__ == '__main__':
    main()
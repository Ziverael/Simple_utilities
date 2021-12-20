#!/usr/bin/env python
import turtle as tt
import sys

class Hilbert_turtle(tt.Turtle):
    def __init__(self, scr_size, angle: int = 90):
        super().__init__()
        self.ang =angle
        self.size = scr_size
    
    def set_at_beg(self):
        self.penup()
        self.goto( - self.size / 2, self.size / 2)
        self.pendown()

    def draw_hilbert(self, level : int = 3, angle : int = None, step : int = 30) -> None:
        if not angle:
            angle = self.ang
        if not level:
            return
            
        self.rt(angle)
        self.draw_hilbert(level - 1, -angle, step)

        self.fd(step)
        self.lt(angle)
        self.draw_hilbert(level - 1, angle, step)

        self.fd(step)
        self.draw_hilbert(level - 1, angle, step)

        self.lt(angle)
        self.fd(step)
        self.draw_hilbert(level - 1, -angle, step)
        self.rt(angle)
                
def drawing(turt : Hilbert_turtle, level : int) -> None :
    turt.set_at_beg()
    turt.draw_hilbert(level, step = turt.size / (2 ** level - 1))
    tt.done()

def main(arg : int):
    try:
        arg = int(arg)
        if arg <= 0:
            sys.stderr.write("Argument must be positive integer.")
            sys.exit(1)

    except:
        sys.stderr.write("Argument must be positive integer.")
        sys.exit(1)
    
    scr = tt.getscreen()
    scr.screensize(400, 400)
    scr.title("Hilbert curve")
    t = Hilbert_turtle(400)
    

    drawing(t, arg)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        main(5)
    else:
        main(sys.argv[1])
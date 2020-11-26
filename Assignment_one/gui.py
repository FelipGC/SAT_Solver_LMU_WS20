from Assignment_one.game import GameEncoderBinomial, GameEncoderSequential
from Assignment_one.performance import print_encoding_details

import tkinter as tk
from PIL import Image, ImageTk

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Home")
       label.pack(side="top", fill="both", expand=True)

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="Game")
       label.pack(side="top", fill="both")


class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="About Page")
       label.pack(side="top", fill="both")

       about_text = tk.Label(self, text="Julian,Felipe,Branso")
       about_text.pack()


class Page4(Page):
        def __init__(self, *args, **kwargs):
            Page.__init__(self, *args, **kwargs)
            index_x=200
            index_y=80
            counter = 0
            var_y = 0

            with open('tent-inputs/tents-8x8-e1.txt') as data:
                for line in data:
                    var_x = 0
                    stripped_line = line.strip()
                    textoutput = ''
                    for variable in stripped_line:
                        if variable == 'T':
                                load = Image.open('assets/pictures/tree.jpg')
                                image = load.resize((40, 40))
                                render = ImageTk.PhotoImage(image)
                                img = tk.Label(self, image=render)
                                img.image = render
                                img.place(x=index_x+var_x*40, y=index_y+var_y*40)
                                img.size()
                                textoutput = textoutput+'T'


                        if variable == '.':
                                load = Image.open('assets/pictures/gras.jpg')
                                image = load.resize((40, 40))
                                render = ImageTk.PhotoImage(image)
                                img = tk.Label(self, image=render)
                                img.image = render
                                img.place(x=index_x+var_x*40, y=index_y+var_y*40)
                                img.size()
                                textoutput = textoutput+' '

                        var_x = var_x + 1
                    print('Line '+str(counter)+': '+textoutput)
                    counter = counter + 1
                    var_y = var_y + 1


class Page5(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        t = GameEncoderBinomial.from_text_file("tent-inputs\\tents-8x8-e1.txt")
        t.solve_sat_problem()
        print(t.output_field("tent-inputs\\tents-8x8-e1-solution.txt"))
        stats = print_encoding_details(t)
        index_x = 200
        index_y = 120
        counter = 0
        var_y = 0


        with open('tent-inputs/tents-8x8-e1-solution.txt') as data:
            for line in data:
                var_x = 0
                stripped_line = line.strip()
                textoutput = ''
                for variable in stripped_line:
                    if variable == 'T':
                        load = Image.open('assets/pictures/tree.jpg')
                        image = load.resize((40, 40))
                        render = ImageTk.PhotoImage(image)
                        img = tk.Label(self, image=render)
                        img.image = render
                        img.place(x=index_x + var_x * 40, y=index_y + var_y * 40)
                        img.size()
                        textoutput = textoutput + 'T'

                    if variable == '.':
                        load = Image.open('assets/pictures/gras.jpg')
                        image = load.resize((40, 40))
                        render = ImageTk.PhotoImage(image)
                        img = tk.Label(self, image=render)
                        img.image = render
                        img.place(x=index_x + var_x * 40, y=index_y + var_y * 40)
                        img.size()
                        textoutput = textoutput + ' '

                    if variable == 'C':
                        load = Image.open('assets/pictures/camp.jpg')
                        image = load.resize((40, 40))
                        render = ImageTk.PhotoImage(image)
                        img = tk.Label(self, image=render)
                        img.image = render
                        img.place(x=index_x + var_x * 40, y=index_y + var_y * 40)
                        img.size()
                        textoutput = textoutput + ' '

                    var_x = var_x + 1
                print('Line ' + str(counter) + ': ' + textoutput)
                counter = counter + 1
                var_y = var_y + 1

        label = tk.Label(self, text=stats)
        label.pack(side="bottom", fill="both")


class Page6(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="SAT-Solver Statistics")
       label.pack(side="top", fill="both")

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)
        p5 = Page5(self)
        p6 = Page6(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


        b1 = tk.Button(buttonframe, text="Home", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Game Settings", command=p2.lift)
        b3 = tk.Button(buttonframe, text="About", command=p3.lift)
        b4 = tk.Button(buttonframe, text="Exit", command=quit)
        b5 = tk.Button(buttonframe, text="Show Map", command=p4.lift)
        b6 = tk.Button(buttonframe, text="Solve Map", command=p5.lift)
        b7 = tk.Button(buttonframe, text="Stats", command=p6.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b5.pack(side="left")
        b4.pack(side="right")
        b3.pack(side="right")
        b6.pack(side="left")
        b7.pack(side="right")



        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800")
    root.mainloop()

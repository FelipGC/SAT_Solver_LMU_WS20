import tkinter as tk  # python3
from Assignment_one.game import GameEncoderBinomial, GameEncoderSequential, GameEncoderBinary, write_to_text_file, \
    remove_tents
from Assignment_one.performance import analyse_sat_solvers, get_encoding_details
from PIL import Image, ImageTk


class MyButton:
    def __init__(self, variable, tile_size, index_x, index_y, var_x, var_y):
        def my_call():
            self.variable = 'C' if self.variable == '.' else '.'
            self.button = tk.Button(page, image=grass_tile if self.variable == '.' else camp_tile,
                                    command=my_call).place(x=x, y=y)

        x = index_x + var_x * tile_size
        y = index_y + var_y * tile_size
        self.variable = variable
        self.pos = (var_x, var_y)
        if variable == 'T':
            self.button = tk.Button(page, image=tree_tile).place(x=x, y=y)
        elif variable == '.':
            self.button = tk.Button(page, image=grass_tile, command=my_call).place(x=x, y=y)
        elif variable == 'C':
            self.button = tk.Button(page, image=camp_tile, command=my_call).place(x=x, y=y)


# Global cursor values


def load_game_id(game_id_string):
    clear_screen()
    # Game ID
    game_id_label.place(relx=0, rely=0, relwidth=0.2, relheight=0.075)
    game_id.place(relx=0.2, rely=0.01, relwidth=0.3, relheight=0.05)
    game_id_button.place(relx=0.52, rely=0.01, relwidth=0.1, relheight=0.05)
    # Size
    size_label.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.075)
    eight_button.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.075)
    ten_button.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.075)
    fifteen_button.place(relx=0.4, rely=0.1, relwidth=0.1, relheight=0.075)
    twenty_button.place(relx=0.5, rely=0.1, relwidth=0.1, relheight=0.075)
    twentyfive_button.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.075)
    thirty_button.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.075)
    # Difficulty
    difficulty_label.place(relx=0., rely=0.2, relwidth=0.2, relheight=0.05)
    easy_button.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.05)
    middle_button.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.05)
    hard_button.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.05)

    global game_field
    game_field = GameEncoderBinomial.from_path_or_id(game_id_string)

    size_game = [2]

    output_field = game_field.output_field()

    if output_field[:1] == '8':
        size_game[0] = 8

    else:
        size_game[0] = int(output_field[:2])

    # HERE
    write_to_text_file(game_field.output_field(), 'tent-inputs/gamefield.txt')
    display_game_field(difficulty, size)

    game_field.solve_sat_problem()
    write_to_text_file(game_field.output_field(), 'tent-inputs/gamefield-solution.txt')


def display_game_field(difficulty_game, size_game, create_game=False, print_solution=False):
    global game_field

    if create_game:
        game_field = GameEncoderSequential.from_randomness(size_game, difficulty_game)
        write_to_text_file(game_field.output_field(), 'tent-inputs/gamefield-solution.txt')
        write_to_text_file(remove_tents(game_field.output_field()), 'tent-inputs/gamefield.txt')

    if size_game[0] >= 40:
        # Game Size Values
        border_size = 7.5
        border_x = 0
        border_y = -3
        index_x = 120
        index_y = 130
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 0.1)
        font_size = 6

    elif size_game[0] >= 30:
        # Game Size Values
        border_size = 7.5
        border_x = 0
        border_y = -3
        index_x = 120
        index_y = 130
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 0.2)
        font_size = 6

    elif size_game[0] >= 25:
        # Game Size Values
        border_size = 7.5
        border_x = 0
        border_y = -4
        index_x = 120
        index_y = 140
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 0.35)
        font_size = 8

    elif size_game[0] >= 20:
        # Game Size Values
        border_size = 7.5
        border_x = 3
        border_y = -2
        index_x = 120
        index_y = 140
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 0.6)
        font_size = 8

    elif size_game[0] >= 15:
        # Game Size Values
        border_size = 7.5
        border_x = 2
        border_y = -1
        index_x = 120
        index_y = 120
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 1.2)
        font_size = 14

    elif size_game[0] >= 10:
        # Game Size Values
        border_size = 7.5
        border_x = 10
        border_y = 6
        index_x = 120
        index_y = 120
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 3)
        font_size = 14
    else:
        # Game Size Values
        border_size = 7.5
        border_x = 10
        border_y = 7.5
        index_x = 120
        index_y = 120
        counter = 0
        var_y = 0
        tile_size = int(size_game[1] * 4.5)
        font_size = 14

    global tree_tile
    global camp_tile
    global grass_tile
    global pos_to_button

    tree_tile = Image.open('assets/tree.png')
    camp_tile = Image.open('assets/camp.png')
    grass_tile = Image.open('assets/grass.png')

    tree_tile = tree_tile.resize((tile_size, tile_size))
    tree_tile = ImageTk.PhotoImage(tree_tile)
    camp_tile = camp_tile.resize((tile_size, tile_size))
    camp_tile = ImageTk.PhotoImage(camp_tile)
    grass_tile = grass_tile.resize((tile_size, tile_size))
    grass_tile = ImageTk.PhotoImage(grass_tile)
    tile_size = tile_size + border_size

    with open('tent-inputs/gamefield{}.txt'.format("-solution" if print_solution else "")) as data:
        for line in data:
            var_x = 0
            stripped_line = line.strip()

            for variable in stripped_line:
                pos_to_button[(var_x, var_y)] = MyButton(variable, tile_size, index_x, index_y, var_x, var_y)

                if variable not in ['T', '.', 'C', ' '] and var_y > 0:
                    tk.Label(page, text=variable,
                             bg='#836dd2',
                             fg='white',
                             font=('bold', font_size)
                             ).place(x=index_x + var_x * tile_size + border_x, y=index_y + var_y * tile_size + border_y)

                if not variable == ' ':
                    var_x = var_x + 1

            counter = counter + 1
            var_y = var_y + 1

    pass


def change_button(event):
    """
    global camp_tile
    global mouse_pos_x, mouse_pos_y

    mouse_pos_x = event.x
    mouse_pos_y = event.y

    print(mouse_pos_x, mouse_pos_y)

    """


def display_solved_game():
    global game_field

    if game_field is None:
        tk.Label(page, text="Please start a new game!", fg='white', bg='#836dd2', font=('bold', 14)).place(x=180, y=60)

    else:
        encoding_details = (get_encoding_details(game_field))

        tk.Label(page, text="Encoding Statistics: ", fg='white', bg='#836dd2', font=('bold', 14)).place(x=200, y=20)
        tk.Label(page, text="Number of variables: " + str(encoding_details[0]), fg='white', bg='#836dd2',
                 font=('bold', 10)).place(x=200, y=60)
        tk.Label(page, text="Number of clauses: " + str(encoding_details[1]), fg='white', bg='#836dd2',
                 font=('bold', 10)).place(x=200, y=90)
        tk.Label(page, text="Number of literals: " + str(encoding_details[2]), fg='white', bg='#836dd2',
                 font=('bold', 10)).place(x=200, y=120)
        display_game_field(difficulty, size, print_solution=True)


def set_difficulty(difficulty_button):
    global difficulty

    difficulty = difficulty_button

    clear_screen()
    new_game_page()

    return print(difficulty)


def set_size(size_button):
    global size

    size = size_button

    clear_screen()
    new_game_page()

    return print(size)


def clear_screen():
    for child in page.winfo_children():
        child.place_forget()


def new_game_page():
    clear_screen()
    # Game ID
    game_id_label.place(relx=0, rely=0, relwidth=0.2, relheight=0.075)
    game_id.place(relx=0.2, rely=0.01, relwidth=0.3, relheight=0.05)
    game_id_button.place(relx=0.52, rely=0.01, relwidth=0.1, relheight=0.05)
    # Size
    size_label.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.075)
    eight_button.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.075)
    ten_button.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.075)
    fifteen_button.place(relx=0.4, rely=0.1, relwidth=0.1, relheight=0.075)
    twenty_button.place(relx=0.5, rely=0.1, relwidth=0.1, relheight=0.075)
    twentyfive_button.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.075)
    thirty_button.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.075)
    # Difficulty
    difficulty_label.place(relx=0., rely=0.2, relwidth=0.2, relheight=0.05)
    easy_button.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.05)
    middle_button.place(relx=0.4, rely=0.2, relwidth=0.2, relheight=0.05)
    hard_button.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.05)

    display_game_field(difficulty, size, create_game=True)


def solve_page():
    clear_screen()
    display_solved_game()


def stats_page():
    clear_screen()
    global game_field

    if game_field is None:
        tk.Label(page, text="Please start a new game!", fg='white', bg='#836dd2', font=('bold', 14)).place(x=180, y=60)

    else:
        g1 = GameEncoderBinomial.from_text_file("tent-inputs\\gamefield.txt")
        g2 = GameEncoderSequential.from_text_file("tent-inputs\\gamefield.txt")
        g3 = GameEncoderBinary.from_text_file("tent-inputs\\gamefield.txt")

        analyse_sat_solvers([g1, g2, g3], show_png=True)

        load = Image.open("data/solver_performance_analysis.png")
        image = load.resize((640, 480))
        render = ImageTk.PhotoImage(image)
        img = tk.Label(page, image=render)
        img.image = render
        tk.Label(page, text='Encoding Statistics', fg='white', bg='#836dd2', font=('bold', 18)).place(x=200, y=0)
        img.place(x=0, y=40)

    """
    analysis_image = Image.open('assets/stats.png')

    analysis_image = analysis_image.resize((533, 400))


    analysis_image = ImageTk.PhotoImage(analysis_image)

    tk.Label(page, text='Encoding Statistics', fg='white',  bg='#836dd2', font=('bold', 18)).place(x=200, y=20)
    tk.Label(page, image=analysis_image).place(x=35, y=100)

    """


def about_page():
    clear_screen()
    # Names & Emails
    members_label.place(relx=0.35, rely=0, relwidth=0.3, relheight=0.075)
    about_felipe_label.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.070)
    about_felipe_label2.place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.070)
    about_julian_label.place(relx=0.1, rely=0.15, relwidth=0.3, relheight=0.070)
    about_julian_label2.place(relx=0.5, rely=0.15, relwidth=0.4, relheight=0.070)
    about_branislav_label.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.070)
    about_branislav_label2.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.070)

    # Github
    github_label.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.075)
    github_link_label.place(relx=0.115, rely=0.5, relwidth=0.8, relheight=0.075)

    # Ressources
    ressources_label.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.075)
    ressources_label_link1.place(relx=0.115, rely=0.8, relwidth=0.8, relheight=0.06)
    ressources_label_link2.place(relx=0.115, rely=0.85, relwidth=0.8, relheight=0.06)


def main():
    # Blank spaces workaround to get the title centered as it depends on the OS
    root.title(' ' * 100 + 'Tents Puzzle')
    root.iconbitmap("assets/game_icon.ico")
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    # GUI Init
    mouse_pos_x = 0
    mouse_pos_y = 0
    canvas = tk.Canvas(root, height=780, width=780)
    canvas.pack()
    background_image = tk.PhotoImage(file="assets/bg.png")
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    menu = tk.Frame(root, bg='#181a43', bd=5)
    menu.place(relx=0.1, rely=0.025, relwidth=0.8, relheight=0.06)
    # Menu Bar
    newgame_button = tk.Button(menu, text="New Game", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                               command=lambda: new_game_page())
    newgame_button.place(relx=0.01, rely=0.1, relwidth=0.15, relheight=0.8)

    solve_button = tk.Button(menu, text="Solve Puzzle", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                             command=lambda: solve_page())
    solve_button.place(relx=0.2175, rely=0.1, relwidth=0.15, relheight=0.8)

    stats_button = tk.Button(menu, text="Stats", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                             command=lambda: stats_page())
    stats_button.place(relx=0.425, rely=0.1, relwidth=0.15, relheight=0.8)

    about_button = tk.Button(menu, text="About Us", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                             command=lambda: about_page())
    about_button.place(relx=0.6325, rely=0.1, relwidth=0.15, relheight=0.8)

    exit_button = tk.Button(menu, text="Exit", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'), command=exit)
    exit_button.place(relx=0.84, rely=0.1, relwidth=0.15, relheight=0.8)

    # Page
    page_border = tk.Frame(root, bg='#181a43')
    page_border.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.75)

    # Welcome Page
    page = tk.Frame(root, bg='#836dd2')
    page.place(relx=0.115, rely=0.165, relwidth=0.77, relheight=0.72)

    greeting_1 = tk.Label(page, text="Welcome to the Tents Puzzle!", fg='white', bg='#836dd2',
                          font=('Roboto', '12', 'bold'))
    greeting_2 = tk.Label(page, text="by Felipe, Julian & Branislav", fg='white', bg='#836dd2',
                          font=('Roboto', '10', 'bold'))
    greeting_1.place(relx=0.31, rely=0.45)
    greeting_2.place(relx=0.34, rely=0.5)

    # New Game Page
    game_id = tk.Entry(page, font=12)
    game_id.insert(0, "Enter game ID/path here")

    game_id_label = tk.Label(page, text="Path/ID: ", fg='white', bg='#836dd2',
                             font=('Roboto', '10', 'bold'))
    size_label = tk.Label(page, text="Size: ", fg='white', bg='#836dd2',
                          font=('Roboto', '10', 'bold'))
    difficulty_label = tk.Label(page, text="Difficulty: ", fg='white', bg='#836dd2',
                                font=('Roboto', '10', 'bold'))
    easy_button = tk.Button(page, text="easy", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                            command=lambda: set_difficulty(0.2))
    middle_button = tk.Button(page, text="middle", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                              command=lambda: set_difficulty(0.3))
    hard_button = tk.Button(page, text="hard", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                            command=lambda: set_difficulty(0.5))

    eight_button = tk.Button(page, text="8x8", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                             command=lambda: set_size((8, 8)))
    ten_button = tk.Button(page, text="10x10", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                           command=lambda: set_size((10, 10)))
    fifteen_button = tk.Button(page, text="15x15", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                               command=lambda: set_size((15, 15)))
    twenty_button = tk.Button(page, text="20x20", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                              command=lambda: set_size((20, 20))
                              )
    twentyfive_button = tk.Button(page, text="25x25", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                                  command=lambda: set_size((25, 25)))
    thirty_button = tk.Button(page, text="30x30", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                              command=lambda: set_size((30, 30)))

    game_id_button = tk.Button(page, text="Load", bg='#836dd2', fg='white', font=('Roboto', '10', 'bold'),
                               command=lambda: load_game_id(game_id.get()))

    # About Page:
    members_label = tk.Label(page, text="Members:", fg='#181a43', bg='#836dd2',
                             font=('Roboto', '16', 'bold'))

    github_label = tk.Label(page, text="Github:", fg='#181a43', bg='#836dd2',
                            font=('Roboto', '16', 'bold'))

    ressources_label = tk.Label(page, text="Ressources:", fg='#181a43', bg='#836dd2',
                                font=('Roboto', '16', 'bold'))

    github_link_label = tk.Label(page, text="https://github.com/FelipGC/SAT_Solver_LMU_WS20", fg='#181a43',
                                 bg='#836dd2',
                                 font=('Roboto', '12', 'bold'))

    ressources_label_link1 = tk.Label(page, text="freepik.com - Designed by macrovector", fg='#181a43', bg='#836dd2',
                                      font=('Roboto', '12', 'bold'))

    ressources_label_link2 = tk.Label(page, text="freepik.com - Designed by brgfx", fg='#181a43', bg='#836dd2',
                                      font=('Roboto', '12', 'bold'))

    about_julian_label = tk.Label(page, text="Julian Finkenzeller: ", fg='white', bg='#836dd2',
                                  font=('Roboto', '10', 'bold'))
    about_felipe_label = tk.Label(page, text="Felip Guimerà Cuevas: ", fg='white', bg='#836dd2',
                                  font=('Roboto', '10', 'bold'))
    about_branislav_label = tk.Label(page, text="Branislav Blagojevic: ", fg='white', bg='#836dd2',
                                     font=('Roboto', '10', 'bold'))
    about_julian_label2 = tk.Label(page, text="Julian.Finkenzeller@campus.lmu.de", fg='#181a43', bg='#836dd2',
                                   font=('Roboto', '10', 'bold'))
    about_felipe_label2 = tk.Label(page, text="Felip.Guimera@campus.lmu.de", fg='#181a43', bg='#836dd2',
                                   font=('Roboto', '10', 'bold'))
    about_branislav_label2 = tk.Label(page, text="B.Blagojevic@campus.lmu.de", fg='#181a43', bg='#836dd2',
                                      font=('Roboto', '10', 'bold'))

    # Default game variables
    difficulty = 0.2
    size = (10, 10)

    # Tiles for the game field
    tree_tile = Image.open('assets/tree.png')
    camp_tile = Image.open('assets/camp.png')
    grass_tile = Image.open('assets/grass.png')

    # Global gamefield variable
    game_field = None
    pos_to_button = {}
    main()

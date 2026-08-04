import tkinter as tk
from tkinter import ttk

CELL_SIZE = 30
ROWS = 20
COLUMNS = 20

# Cell states
EMPTY = "white"
WALL = "black"
START = "green"
END = "red"
GRAVEL = "grey"
MUD = "brown"
ICE = "CadetBlue1"
FOOD = "yellow"

class MazeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
 
        self.title("Build Your Maze")
        self.resizable(False, False)
 
        # ---- state ----
        self.mode = tk.StringVar(value="wall")   # "wall", "start", "end", "eraser"
        self.cells = {}          # (row, col) -> canvas rectangle id
        self.cell_state = {}     # (row, col) -> state string
        self.start_cell = None
        self.end_cell = None
 
        # ---- outer frame gives padding around everything ----
        outer = ttk.Frame(self, padding=20)
        outer.pack(fill="both", expand=True)
 
        # ---- toolbar of buttons ----
        toolbar = ttk.Frame(outer)
        toolbar.pack(fill="x", pady=(0, 10))

        #Row 1
        row1 = ttk.Frame(toolbar)
        row1.pack(fill="x", pady=(0, 6))
        ttk.Radiobutton(row1, text="Start", variable=self.mode,
                            value="start").pack(side="left", padx=4)
        ttk.Radiobutton(row1, text="End", variable=self.mode,
                            value="end").pack(side="left", padx=4)


        #Row 2
        row2 = ttk.Frame(toolbar)
        row2.pack(fill="x", pady=(0, 6))

        ttk.Radiobutton(row2, text="Wall", variable=self.mode,
                         value="wall").pack(side="left", padx=4)
        ttk.Radiobutton(row2, text="Eraser", variable=self.mode,
                         value="eraser").pack(side="left", padx=4)


        row3 = ttk.Frame(toolbar)
        row3.pack(fill="x", pady=(0, 6))

        ttk.Radiobutton(row3, text="Gravel(2)", variable=self.mode,
                            value="gravel").pack(side="left", padx=4)
        ttk.Radiobutton(row3, text="Mud(4)", variable=self.mode,
                            value="mud").pack(side="left", padx=4)
        ttk.Radiobutton(row3, text="Ice(0.5)", variable=self.mode,
                                    value="ice").pack(side="left", padx=4)
        ttk.Radiobutton(row3, text="Food(-1)", variable=self.mode,
                            value="food").pack(side="left", padx=4)
        
        ttk.Button(row3, text="Clear", command=self.clear_grid
                   ).pack(side="left", padx=(20, 4))
        ttk.Button(row3, text="Submit", command=self.run_astar
                   ).pack(side="left", padx=4)
 
        # ---- canvas with its own padding ----
        canvas_frame = ttk.Frame(outer, padding=10, relief="sunken")
        canvas_frame.pack()
 
        self.canvas = tk.Canvas(
            canvas_frame,
            width=COLUMNS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.canvas.pack()
 
        self.create_empty_grid()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)  # click-and-drag walls
 
        self.mainloop()
 
    # ------------------------------------------------------------------
    def create_empty_grid(self):
        for r in range(ROWS):
            for c in range(COLUMNS):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
 
                cell_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=EMPTY,
                    outline="gray"
                )
                self.cells[(r, c)] = cell_id
                self.cell_state[(r, c)] = EMPTY
 
    # ------------------------------------------------------------------
    def _cell_from_event(self, event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLUMNS:
            return row, col
        return None
 
    def on_click(self, event):
        cell = self._cell_from_event(event)
        if cell:
            self.set_cell(cell)
 
    def on_drag(self, event):
        # only paint walls while dragging, so start/end don't get smeared
        if self.mode.get() in ["start", "end"]:
            return
        cell = self._cell_from_event(event)
        if cell:
            self.set_cell(cell)
 
    def set_cell(self, cell):
        mode = self.mode.get()
 
        if mode == "wall":
            # toggle wall on/off, but never overwrite start/end
            if self.cell_state[cell] in (START, END):
                return
            self._paint(cell, WALL)
 
        elif mode == "start":
            if self.start_cell:
                self._paint(self.start_cell, EMPTY)
            self._paint(cell, START)
            self.start_cell = cell
 
        elif mode == "end":
            if self.end_cell:
                self._paint(self.end_cell, EMPTY)
            self._paint(cell, END)
            self.end_cell = cell

        elif mode == "eraser":
            # toggle wall on/off, but never overwrite start/end
            if self.cell_state[cell] in (START, END):
                return
            self._paint(cell, EMPTY)

        elif mode == "gravel":
                    # toggle wall on/off, but never overwrite start/end
                    if self.cell_state[cell] in (START, END):
                        return
                    self._paint(cell, GRAVEL)

        elif mode == "mud":
                    # toggle wall on/off, but never overwrite start/end
                    if self.cell_state[cell] in (START, END):
                        return
                    self._paint(cell, MUD)

        elif mode == "ice":
                    # toggle wall on/off, but never overwrite start/end
                    if self.cell_state[cell] in (START, END):
                        return
                    self._paint(cell, ICE)

        elif mode == "food":
                    # toggle wall on/off, but never overwrite start/end
                    if self.cell_state[cell] in (START, END):
                        return
                    self._paint(cell, FOOD)
 
    def _paint(self, cell, state):
        self.cell_state[cell] = state
        self.canvas.itemconfig(self.cells[cell], fill=state)
 
    # ------------------------------------------------------------------
    def clear_grid(self):
        for cell in self.cells:
            self._paint(cell, EMPTY)
        self.start_cell = None
        self.end_cell = None
 
    def run_astar(self):
        if not self.start_cell or not self.end_cell:
            print("Set both a start and an end cell first.")
            return
 
        walls = {c for c, s in self.cell_state.items() if s == WALL}
        print("Start:", self.start_cell)
        print("End:", self.end_cell)
        print("Walls:", len(walls))
        # TODO: call your A* implementation here, e.g.
        # path = astar(self.start_cell, self.end_cell, walls, ROWS, COLUMNS)
        # then draw it on the canvas
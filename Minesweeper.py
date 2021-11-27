from tkinter import *
import random

def get_neighbors(pos, height, width):
        '''get_neighbors(pos, height, width) -> list
        gets a list of the positions of the neighbors'''
        (row, col) = pos

        neighbor_pos = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                nr = row + r
                nc = col + c
                if nr in range(height) and nc in range(width):
                    if not (nr == row and nc == col):
                        neighbor_pos.append((nr, nc))

        return neighbor_pos


class MinesweeperTile(Button):
    '''represents a Minesweeper tile'''
    colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
    
    def __init__(self, master, pos):
        '''MinesweeperTile(master, pos) -> Tile
        creates a new Minesweeper Tile'''
        super().__init__(master,height=1,width=3,text='',\
                       bg='white',font=('Arial',24),relief=RAISED)
        
        # attributes
        self.pos = pos
        self.clicked = False
        self.flagged = False

        # listeners for mouse clicks
        self.bind('<Button-1>',self.reveal)
        self.bind('<Button-3>',self.flag)

    def get_position(self):
        '''MinesweeperTile.get_position() -> tuple
        gets the position of Tile'''
        return self.pos

    def is_clicked(self):
        '''MinesweeperTile.is_clicked() -> bool
        returns True if the tile is clicked'''
        return self.clicked

    def is_flagged(self):
        '''MinesweeperTile.is_flagged() -> bool
        returns True if tile is flagged'''
        return self.flagged

    def set_inside(self, inside):
        '''MinesweeperTile.set_inside()
        sets what is inside of the tile'''
        self.inside = inside

    def get_inside(self):
        '''MinesweeperTile.get_inside() -> str or int
        returns what is in Tile'''
        return self.inside

    def reveal(self,event):
        '''MinesweeperTile.reveal(event)
        handler for left-mouse click
        reveals what is in Tile'''
        # make sure Tile has not been clicked or flagged
        if not self.clicked and not self.flagged:
            self.focus_set()
            # check if the inside is a mine
            if self.inside == '*':
                self['text'] = self.inside
                self['bg'] = 'red'
            elif self.inside == 0:
                self['text'] = ''
                neighbors = get_neighbors(self.pos, self.master.height, self.master.width)
                for n_tile in neighbors:
                    n_tile.reveal(event)
            else:
                self['text'] = str(self.inside)
                self['fg'] = self.colormap[self.inside]

                # change the color and appearance of Tile
                self['relief'] = SUNKEN
                self['bg'] = 'lightgrey'
                
            self.clicked = True

    def flag(self,event):
        '''MinesweeperTile.flag(event)
        handler for right-mouse click
        inserts or removes flag from Tile'''
        # make sure Tile has not been clicked
        if not self.clicked:
            self.focus_set()
            # unflag Tile
            if self.flagged:
                self['text'] = ''
                self.flagged = False
            # flag Tile
            else:
                self['text'] = '*'
                self.flagged = True


class MinesweeperFrame(Frame):
    '''frame for a game of minesweeper'''
    
    def __init__(self, master, width=12, height=10, num_bombs=15):
        '''MinesweeperFrame(master[, width=12, height=10, num_bombs=15])
        creates a new width * height minesweeper frame with num_bombs bombs'''
        super().__init__(master,bg='black')
        self.grid()

        self.width = width
        self.height = height
        self.num_bombs = num_bombs

        # fill the frame with tiles
        self.tiles = {}
        for row in range(height):
            for col in range(width):
                self.tiles[(row, col)] = MinesweeperTile(self, (row, col))
                self.tiles[(row, col)].set_inside(0)
                self.tiles[(row, col)].grid(row=row,column=col)

        for pos in self.get_random_coord():
            self.tiles[pos].set_inside('*')

        for pos in self.tiles:
            if self.tiles[pos].get_inside() != '*':
                neighbor_list = get_neighbors(pos, self.height, self.width)
                mine_count = 0
                for np in neighbor_list:
                    if self.tiles[np].get_inside() == '*':
                        mine_count += 1
                self.tiles[pos].set_inside(mine_count)

    def get_random_coord(self):
        '''MinesweeperFrame.get_random_coord() -> list
        gets random coordinates of tiles to be mined'''
        pos_seq = random.sample(range(self.width*self.height), self.num_bombs)

        positions = []
        for p in pos_seq:
            positions.append((p//self.width, p%self.width))

        return positions


def play_minesweeper(width=12, height=10, num_bombs=15):
    '''play_minesweeper([width=12, height=10, num_bombs=15])
    plays minesweeper'''
    pass

root = Tk()
mf = MinesweeperFrame(root)
root.mainloop()
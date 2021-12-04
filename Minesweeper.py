from tkinter import messagebox
from tkinter import *
import random

class MinesweeperTile(Label):
    '''represents a Minesweeper tile'''
    colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
    
    def __init__(self, master):
        '''MinesweeperTile(master, coord) -> Tile
        creates a new Minesweeper Tile'''
        super().__init__(master,height=1,width=3,text='',\
                       bg='white',font=('Arial',24),relief=RAISED)
        
        # Tile has been clicked, flagged, frozen
        self.clicked = False
        self.flagged = False
        self.frozen = False

        # listeners for mouse events
        self.bind('<Button-1>', self.reveal)
        self.bind('<Button-2>', self.flag)
        self.bind('<Button-3>', self.flag)

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

    def disable(self):
        '''MinesweeperTile.disable()
        disables Tile by freezing it'''
        self.frozen = True

    def reveal(self,event):
        '''MinesweeperTile.reveal(event)
        handler for left-mouse click
        reveals what is in Tile'''
        # make sure Tile has not been clicked, flagged, frozen
        if not self.clicked and not self.flagged and not self.frozen:
            # check if the inside is a mine
            if self.inside == '*':
                self['text'] = self.inside
                self['bg'] = 'red'
            else:
                # no mines surrounding Tile
                if self.inside == 0:
                    self['text'] = ''
                # some mines surrounding Tile
                else:
                    self['text'] = str(self.inside)
                    self['fg'] = self.colormap[self.inside]

                # change the color and appearance of Tile
                self['relief'] = SUNKEN
                self['bg'] = 'grey'

            # change Tile to clicked and do actions if Tile is empty or mined    
            self.clicked = True
            self.master.sweep()
            self.master.hit_mine()
            
            # check for a win
            if self.master.check_for_win():
                messagebox.showinfo('Minesweeper','Congratulations -- you won!',parent=self)
 
    def flag(self,event):
        '''MinesweeperTile.flag(event)
        handler for right-mouse click
        inserts or removes flag from Tile'''
        # make sure Tile has not been clicked or frozen
        if not self.clicked and not self.frozen:
            # unflag Tile
            if self.flagged:
                self['text'] = ''
            # flag Tile
            else:
                self['text'] = '*'
            
            self.flagged = not self.flagged

        # decrease the potential mine counter
        self.master.flag_tiles()

    def expose(self):
        '''MinesweeperTile.expose()
        exposes what is inside the Tile'''
        # make sure Tile has not been clicked, flagged, frozen
        if not self.clicked and not self.flagged and not self.frozen:
            # check if the inside is a mine
            if self.inside == '*':
                self['text'] = self.inside
                self['bg'] = 'red'
            else:
                # no mines surrounding Tile
                if self.inside == 0:
                    self['text'] = ''
                # some mines surrounding Tile
                else:
                    self['text'] = str(self.inside)
                    self['fg'] = self.colormap[self.inside]

                # change the color and appearance of Tile
                self['relief'] = SUNKEN
                self['bg'] = 'grey'

            # make the Tile clicked and sweep if Tile is empty    
            self.clicked = True
            self.master.sweep()


class MinesweeperFrame(Frame):
    '''frame for a game of minesweeper'''
    
    def __init__(self, master, height, width, num_bombs):
        '''MinesweeperFrame(master, height, width, num_bombs)
        creates a new width * height minesweeper frame with num_bombs bombs'''
        super().__init__(master,bg='black')
        self.grid()

        # set the width, height, number of bombs
        self.width = width
        self.height = height
        self.num_bombs = num_bombs

        # fill the frame with tiles
        self.tiles = {}
        for row in range(height):
            for col in range(width):
                self.tiles[(row, col)] = MinesweeperTile(self)
                self.tiles[(row, col)].set_inside(0)
                self.tiles[(row, col)].grid(row=row,column=col)

        # place the mines
        for pos in self.get_random_coord():
            self.tiles[pos].set_inside('*')

        # assign the values to the Tiles
        for pos in self.tiles:
            # make sure tile does not have a mine
            if self.tiles[pos].get_inside() != '*':
                # count the number of mines
                mine_count = 0
                for np in self.get_neighbors(pos):
                    if self.tiles[np].get_inside() == '*':
                        mine_count += 1
                
                self.tiles[pos].set_inside(mine_count)

        # display the number of potential mines left
        self.flag_count = Label(self, text=str(num_bombs), font=('Arial',24))
        self.flag_count.grid(row=height, column=(width-1)//2)

    def get_random_coord(self):
        '''MinesweeperFrame.get_random_coord() -> list
        gets random coordinates of tiles to be mined'''
        pos_seq = random.sample(range(self.width*self.height), self.num_bombs)

        # append the randomly selected positions to a list
        positions = []
        for p in pos_seq:
            positions.append((p//self.width, p%self.width))

        return positions

    def get_neighbors(self, pos):
        '''MinesweeperFrame.get_neighbors(pos) -> list
        gets a list of the positions of the neighbors'''
        (row, col) = pos

        # append possible neighbor positions to a list
        neighbor_pos = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                # get the coordinates of the possible neighbor
                nr = row + r
                nc = col + c
                
                # make sure the tiles are in the frame
                if nr in range(self.height) and nc in range(self.width):
                    # make sure the position is not itself
                    if not (nr == row and nc == col):
                        neighbor_pos.append((nr, nc))

        return neighbor_pos

    def sweep(self):
        '''MinesweeperFrame.expose_auto()
        exposes the surrounding squares
        only activates if the clicked tile has no surrounding mines'''
        for pos in self.tiles:
            # make sure the tile is empty
            if self.tiles[pos].is_clicked() and self.tiles[pos].get_inside() == 0:
                # expose the neightboring tiles
                for np in self.get_neighbors(pos):
                    self.tiles[np].expose()

    def flag_tiles(self):
        '''MinesweeperFrame.flag_tiles()
        decreases the flag count if a tile has been flagged'''
        flag_count = 0
        # count the number of flagged tiles
        for pos in self.tiles:
            # check if a tile has been flagged
            if self.tiles[pos].is_flagged():
                flag_count += 1

        # change the count of the number of potential mines
        self.flag_count['text'] = str(self.num_bombs - flag_count)

    def hit_mine(self):
        '''MinesweeperFrame.hit_mine()
        exposes all mines if a mine has been clicked'''
        for pos in self.tiles:
            # a mine has been clicked
            if self.tiles[pos].is_clicked() and self.tiles[pos].get_inside() == '*':
                messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)
                # go through all the other tiles and expose the mines
                for op in self.tiles:
                    if self.tiles[op].get_inside() == '*':
                        self.tiles[op].expose()
                    # remove the flags from the tiles that are not mined
                    elif self.tiles[op].is_flagged():
                        self.tiles[op]['text'] = ''
                    
                    # freeze the tile
                    self.tiles[op].disable()
                break

    def check_for_win(self):
        '''MinesweeperFrame.check_for_win() -> bool
        checks if all mineless tiles have been exposed'''
        is_win = True
        for pos in self.tiles:
            # make sure that all non-mined tiles have been clicked
            if not self.tiles[pos].is_clicked() and self.tiles[pos].get_inside() != '*':
                is_win = False
                break

        # freeze all tiles if a win occurs
        if is_win:
            for pos in self.tiles:
                self.tiles[pos].disable()

        return is_win
 

# main loop for the game
def play_minesweeper(width=12, height=10, numBombs=15):
    '''play_minesweeper([width=12, height=10, numBombs=15])
    plays minesweeper'''
    root = Tk()
    root.title('Minesweeper')
    MinesweeperFrame(root, height, width, numBombs)
    root.mainloop()

play_minesweeper()
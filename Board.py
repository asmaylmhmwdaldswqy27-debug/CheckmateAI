import pygame as py
import chess

class DisplayBoard():

    def __init__(self, board):

       
        self.run = False
        self.intro = True
        self.game_over = False

        self.dim = 700
        self.sq_size = 71        
        self.offset_x = 64      
        self.offset_y = 567       

        self.boardPos = {}
        self.boardLayout = {}
        self.show_moves_surf_list = []
        self.selected_square = None
        self.square_to_move_too = None
        self.player_color = None
        self.clock = py.time.Clock()
        self.board = board
        self.fen = board.fen()

        
        py.init()
        self.win = py.display.set_mode((self.dim, self.dim))
        py.display.set_caption("Think Chess")
        

        self.chessBoard = py.Surface((self.dim, self.dim))
        self.chessBoard.fill((60,45,35))  
        light_color = (238, 238, 210) 
        dark_green = (110, 135, 158)    

        for x in range(8):
            for y in range(8):
                
                is_light_square = (x + y) % 2 != 0
                square_color = light_color if is_light_square else dark_green
                
             
                pos_x = x * self.sq_size + self.offset_x
                pos_y = self.offset_y - (y * self.sq_size)
                
               
                py.draw.rect(self.chessBoard, square_color, (pos_x, pos_y, self.sq_size, self.sq_size))
      
        self.show_moves_surf = py.Surface((self.sq_size, self.sq_size), py.SRCALPHA, 32)
        py.draw.circle(self.show_moves_surf, (0, 200, 0, 100), (self.sq_size // 2, self.sq_size // 2), 25, 0)

        self.boardlayout_init()
        self.update(self.board)

    def boardlayout_init(self):
    
        for x in range(8):
            for y in range(8):
              
                pos_x = x * self.sq_size + self.offset_x
                pos_y = self.offset_y - (y * self.sq_size)
                
                self.boardPos[str(chr(97 + x) + str(y + 1))] = [pos_x, pos_y]
                self.boardLayout[str(chr(97 + x) + str(y + 1))] = None

    def update(self, board):
        for x in range(8):
            for y in range(8):
                self.boardLayout[str(chr(97 + x) + str(y + 1))] = None

        self.board = board
        self.fen = board.fen()

        boardString = str(self.fen)[0:str(self.fen).find(' ')]
        boardString = boardString + '/'

        for y in range(8, 0, -1):
            dash = boardString.find('/')
            rawCode = boardString[0:dash]
            boardString = boardString[dash + 1:len(boardString)]

            alphabetCounter = 97
            for char in rawCode:
                if char.isdigit():
                    alphabetCounter += int(char)
                else:
                    self.boardLayout[str(chr(alphabetCounter)) + str(y)] = self.pieceData(char)
                    alphabetCounter +=1
        self.update_screen()

    def update_screen(self):
        self.win.blit(self.chessBoard, (0, 0))
        for num in self.boardLayout:
            if self.boardLayout[num] != None:
                self.win.blit(self.boardLayout[num].render(), (self.boardPos[num][0], self.boardPos[num][1]))
        
        if self.show_moves_surf_list != []:
            for num in self.show_moves_surf_list:
                self.win.blit(self.show_moves_surf, (num[0], num[1]))

        py.display.update()
        self.clock.tick(15)

    def update_possible_moves(self):
        if self.selected_square != None:
            self.show_moves_surf_list.clear()
            lg = self.board.legal_moves
            for pos in lg:
                if str(pos)[0:2] == self.selected_square:
                    self.show_moves_surf_list.append((self.boardPos[str(pos)[2:4]][0], self.boardPos[str(pos)[2:4]][1]))

    def pieceData(self, piece):
        pieces = {
            'p': ("Pawn", "B"), 'r': ("Rook", "B"), 'n': ("Knight", "B"),
            'b': ("Bishop", "B"), 'k': ("King", "B"), 'q': ("Queen", "B"),
            'P': ("Pawn", "W"), 'R': ("Rook", "W"), 'N': ("Knight", "W"),
            'B': ("Bishop", "W"), 'K': ("King", "W"), 'Q': ("Queen", "W")
        }
        name, color = pieces[piece]
        return Piece(name, color)

    def square_select(self, pos):
      
        x_board_pos = int((pos[0] - self.offset_x) // self.sq_size)
        y_board_pos = int(-((pos[1] - self.offset_y) // self.sq_size) + 1)
        
     
        if not (0 <= x_board_pos <= 7 and 1 <= y_board_pos <= 8):
            self.remove_square_select()
            return None

        current_square = str(chr(97 + x_board_pos) + str(y_board_pos))

        if self.selected_square == None:
            self.square_to_move_too = None
            self.selected_square = current_square
            self.update_possible_moves()
            return None
        else:
            self.square_to_move_too = current_square
            result = str(self.selected_square + self.square_to_move_too)
            
            for move in self.board.legal_moves:
                if str(move) == str(result + "q"):
                    self.remove_square_select()
                    return str(result + "q")
                elif str(move) == result:
                    self.remove_square_select()
                    return result

           
            if self.boardLayout[current_square] != None:
                self.square_to_move_too = None
                self.selected_square = current_square
                self.update_possible_moves()
                return None

    def remove_square_select(self):
        self.selected_square = None
        self.square_to_move_too = None
        self.show_moves_surf_list = []

   
    def main_menu(self):
        while self.intro:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()

            self.win.fill((179,222,245))
            largeText = py.font.SysFont("comicsansms", 80)
            TextSurf, TextRect = self.text_objects("Chess Game", largeText)
            TextRect.center = ((self.dim / 2), (self.dim / 2 - 150))
            self.win.blit(TextSurf, TextRect)

            self.button("WHITE", 150, 350, 150, 60, (0, 200, 0), (0, 255, 0), 1)
            self.button("BLACK", 400, 350, 150, 60, (0, 200, 0), (0, 255, 0), 2)
            self.button("Quit", 275, 450, 150, 60, (200, 0, 0), (255, 0, 0), 3)

            py.display.update()
            self.clock.tick(15)

    def game_over_menu(self):
        while self.game_over:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    exit()

            self.win.fill((245, 245, 220)) 
            largeText = py.font.SysFont("comicsansms", 70)
            mediumText = py.font.SysFont("comicsansms", 40)
            
            TextSurfMian, TextRectMain = self.text_objects("Checkmate!", largeText)
            TextRectMain.center = ((self.dim / 2), (self.dim / 2 - 100))
            self.win.blit(TextSurfMian, TextRectMain)

            winner = "Black Won" if self.board.turn == chess.WHITE else "White Won"
            TextSurf, TextRect = self.text_objects(winner, mediumText)
            TextRect.center = ((self.dim / 2), (self.dim / 2))
            self.win.blit(TextSurf, TextRect)

            self.button("Play Again", 150, 450, 150, 60, (0, 200, 0), (0, 255, 0), 4)
            self.button("Quit", 400, 450, 150, 60, (200, 0, 0), (255, 0, 0), 3)

            py.display.update()
            self.clock.tick(15)

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = py.mouse.get_pos()
        click = py.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            py.draw.rect(self.win, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                if action == 1: self.player_color, self.run, self.intro = "W", True, False
                elif action == 2: self.player_color, self.run, self.intro = "B", True, False
                elif action == 3: py.quit(); exit()
                elif action == 4: self.run, self.intro, self.game_over = False, True, False
        else:
            py.draw.rect(self.win, ic, (x, y, w, h))

        smallText = py.font.SysFont("comicsansms", 25)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.win.blit(textSurf, textRect)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

class Piece():
    def __init__(self, name, color):
        self.name = name
        self.color = color
       
        self.dim = 65 

       
        char_code = self.name.lower()[0] if self.name != "Knight" else "n"
        color_code = "l" if self.color == "W" else "d"
        path = f"Image/Chess_{char_code}{color_code}t60.png"
        
        try:
            self.pieceSurface = py.image.load(path).convert_alpha()
        except:
            
            self.pieceSurface = py.Surface((self.dim, self.dim))
            self.pieceSurface.fill((255, 0, 0) if color == "W" else (0, 0, 0))

        self.pieceSurface = py.transform.scale(self.pieceSurface, (self.dim, self.dim))

    def render(self):
        return self.pieceSurface
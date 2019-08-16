from pandac.PandaModules import loadPrcFileData
loadPrcFileData('', 'win-size 640 480') # Window size
loadPrcFileData('', 'win-fixed-size #t') # The window is a fixed size
loadPrcFileData('', 'textures-auto-power-2 1')
loadPrcFileData('', 'textures-power-2 up')
loadPrcFileData('', 'load-file-type p3assimp')

from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay, TransparencyAttrib
from panda3d.core import AmbientLight, DirectionalLight, Vec4, Vec3, Point2
from panda3d.core import CardMaker, Texture, PTAUchar, CPTAUchar, BitMask32
from panda3d.vision import ARToolKit
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from direct.stdpy import threading

from pieces import create_piece
from config import *
import Ray

import multiprocessing
import numpy as np
import sys
import cv2

import time

class ChessboardDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Setting up webcam image
        self.webcam = Webcam()
        self.ar2 = ARToolKit.make(self.cam, "data/camera_para.dat", 1)
        self.cam.node().getDisplayRegion(0).setSort(20)

        # Creating the anchor to the marker
        self.anchor = self.render.attachNewNode("Anchor node")
        self.anchor.reparent_to(render)
        self.ar2.attachPattern("data/marker.patt", self.anchor)

        # Setting up lighting
        alight = AmbientLight('ambientLight')
        alight.setColor(Vec4(0.4, 0.4, 0.4, 1))
        alightNP = render.attachNewNode(alight)
        dlight = DirectionalLight('directionalLight')
        dlight.setDirection(Vec3(-1, 1, -1))
        alight.setColor(Vec4(0.4, 0.4, 0.4, 1))
        dlightNP = render.attachNewNode(dlight)
        render.setLightOff()
        render.setLight(alightNP)
        render.setLight(dlightNP)

        # Setting up players
        self.humans = HUMANS
        self.ais = AIS
        self.ai_queue = multiprocessing.Queue()
        # 1 = white, -1 = black
        self.turn = 1
        # 0 = no check, 1 = white, -1 = black
        self.check = 0
        self.can_move = True
        self.gameover = False

        self.texture_black = self.loader.loadTexture(TEXTURE_BLACK)
        self.texture_white = self.loader.loadTexture(TEXTURE_WHITE)
        
        self.setup_collision()
        self.create_board()
        self.moves = self.get_valid_moves()

        # Currently highlighted square (list [x,y,z])
        self.hiSq = False
        # Piece we are currently selecting
        self.dragging = False

        # Events
        taskMgr.add(self.update_webcam, 'cam')
        taskMgr.add(self.ai_move, 'ai')
        taskMgr.add(self.mouseover, 'mouseover')
        self.accept("mouse1", self.left_click)
        self.accept("mouse3", self.right_click)
        self.accept('escape', sys.exit)     # Escape closes the window

    def create_board(self):
        # C++ object containing the actual chessboard
        self.board = Ray.Chess_AI(np.ascontiguousarray(np.array(BOARD)), self.turn, PAWN_2STEP)

        # Array containing the piece objects we are going to draw
        self.board_array = np.transpose(np.array(BOARD))
        self.draw_pieces = np.full_like(self.board_array, None, dtype=np.object)
        self.draw_squares = np.zeros_like(self.board_array, dtype=np.object)
        max_x, max_y, max_z = BOARD_SIZE

        # Creates the 3D objects (from the file pieces.py) and the squares
        for z in range(max_z):
            for y in range(max_y):
                for x in range(max_x):
                    if self.board_array[x,y,z] != 0:
                        self.draw_pieces[x,y,z] = create_piece(self.board_array[x,y,z], [x,y,z], self)

                    # Load, parent, color, and position the model (a single square polygon)
                    self.draw_squares[x,y,z] = loader.loadModel("models/square")
                    self.draw_squares[x,y,z].reparentTo(self.anchor)
                    self.draw_squares[x,y,z].setScale(SCALE)
                    self.draw_squares[x,y,z].setPos(square_position(x,y,z, BOARD_SIZE))
                    self.draw_squares[x,y,z].setColor(square_color(x,y,z))

                    # The bottom one is solid, the rest are a little translucid
                    if z > 0:
                        self.draw_squares[x,y,z].setTransparency(TransparencyAttrib.MAlpha)
                        self.draw_squares[x,y,z].setAlphaScale(0.75)
                    # Set the model itself to be collideable with the ray.
                    self.draw_squares[x,y,z].find("**/polygon").node().setIntoCollideMask(BitMask32.bit(1))
                    # Set a tag on the square's node so we can look up what square this
                    self.draw_squares[x,y,z].find("**/polygon").node().setTag('square', ','.join([str(dim) for dim in (x,y,z)]))

    def setup_collision(self):
        self.picker = CollisionTraverser()  # Make a traverser
        self.pq = CollisionHandlerQueue()  # Make a handler
        # Make a collision node for our picker ray
        self.pickerNode = CollisionNode('mouseRay')
        # Attach that node to the camera since the ray will need to be positioned
        # relative to it
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        # Everything to be picked will use bit 1. This way if we were doing other
        # collision we could separate it
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()
        # Add it to the collision node
        self.pickerNode.addSolid(self.pickerRay)
        # Register the ray as something that can cause collisions
        self.picker.addCollider(self.pickerNP, self.pq)

    def ai_move(self, task):
        if self.turn in self.ais and not self.gameover:
            if self.can_move is True:
                # Start the thinking process
                self.can_move = False
                recursions = 1
                if len(self.moves) < 30:
                    recursions = 2
                if len(self.moves) < 12:
                    recursions = 3
                
                if TEST is True:
                    print(f'doing {recursions} recursions')
                    self.start = time.time()

                make_ai_think = multiprocessing.Process(target=ai, args=(self.board, self.ai_queue, recursions))
                make_ai_think.start()
            else:
                # The AI function will put the move in this queue when it figures it out
                if not self.ai_queue.empty():
                    if TEST is True:
                        print(f'Took {time.time()-self.start}.')
                    piece, move = self.ai_queue.get()
                    self.can_move = False

                    self.move_pieces(piece, move)
                    self.turn = 1 if self.turn == -1 else -1

                    new_array = np.ascontiguousarray(np.transpose(self.board_array))
                    self.board.set_board(new_array, self.turn)
                    # This hides the check on the player's king if there was one
                    self.hide_possible_moves()
                    self.moves = self.get_valid_moves()
                    self.can_move = True

                    if TEST is True:
                        print('AI moved')

        return Task.cont

    def update_webcam(self, task):
        self.can_get_image = False
        self.webcam_texture = self.webcam.step()
        self.ar2.analyze(self.webcam_texture)
        self.can_get_image = True
        return Task.cont

    def move_pieces(self, a, b, move_model=True):
        # Move the 3D model of the piece and update its square variable
        # Also delete the other one...
        if move_model is True:
            # If there is a piece on the new location
            if self.draw_pieces[b[0], b[1], b[2]] is not None:
                # We delete it
                self.draw_pieces[b[0], b[1], b[2]].obj.removeNode()
            # We move the piece to its new location
            self.draw_pieces[b[0], b[1], b[2]] = self.draw_pieces[a[0], a[1], a[2]]
            self.draw_pieces[b[0], b[1], b[2]].move([b[0], b[1], b[2]])
            # Remove the piece from the old location
            self.draw_pieces[a[0], a[1], a[2]] = None
        # Move one to other's position
        self.board_array[b[0], b[1], b[2]] = self.board_array[a[0], a[1], a[2]]
        # Replace one's position with empty
        self.board_array[a[0], a[1], a[2]] = 0

    def mouseover(self, task): 
        # If we have a mouse
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            # Do the actual collision pass
            self.picker.traverse(self.anchor)
            if self.pq.getNumEntries() <= 0:
                if self.hiSq is not False:
                    self.square_default_color(self.hiSq)
                    self.hiSq = False
            else:
                # Sort the hits so the closest is first, and highlight that node
                self.pq.sortEntries()
                dims = self.pq.getEntry(0).getIntoNode().getTag('square').split(',')
                x,y,z = [int(dim) for dim in dims]
                
                # Remove highlight from previous square
                if self.hiSq is not False and self.hiSq != [x,y,z]:
                    # Turn square back to its normal, non highlighted color
                    self.square_default_color(self.hiSq)
                # Set the highlight on the current square
                self.draw_squares[x,y,z].setColor(HIGHLIGHT)
                self.hiSq = [x,y,z]

        return Task.cont

    def right_click(self):
        # Drop the piece
        if self.dragging is not False:
            # Hide the green/red squares showing where we can move
            self.hide_possible_moves()
            tmp = self.dragging
            self.dragging = False
            self.square_default_color(tmp)

    def left_click(self):
        if self.gameover is False and self.turn in self.humans:

            # MOVING SELECTED PIECE
            if self.dragging is not False:
                # If we have a piece selected and we are hovering over a square
                if self.hiSq is not False:
                    # If the square we are clicking is a possible move, we move
                    if (self.dragging, self.hiSq) in self.moves:
                        self.can_move = False
                        self.move_pieces(self.dragging, self.hiSq)
                        self.turn = 1 if self.turn == -1 else -1

                        # Moving the object
                        new_array = np.ascontiguousarray(np.transpose(self.board_array))
                        self.board.set_board(new_array, self.turn)

                        self.hide_possible_moves()

                        self.moves = self.get_valid_moves()
                        self.can_move = True

                # Hide the green/red squares showing where we can move
                self.hide_possible_moves()
                # Drop the piece
                tmp = self.dragging
                self.dragging = False
                self.square_default_color(tmp)

            # SELECTING PIECE
            if self.hiSq is not False:
                # If we pick the piece of the side whose turn it is
                if self.turn * self.board_array[self.hiSq[0],self.hiSq[1],self.hiSq[2]] > 0:
                    # Hide the old green/red squares showing where we could move
                    self.hide_possible_moves()
                    # Select it
                    self.dragging = self.hiSq
                    self.show_possible_moves()

    def get_valid_moves(self):
        moves = self.board.get_moves()
        check_found = self.board.is_in_check()
        
        if check_found is True:
            self.check = self.turn
            kings = np.argwhere(self.board_array == 6*self.turn)
            for king in kings:
                self.draw_squares[king[0], king[1], king[2]].setColor(HIGHLIGHT_ATTACK)

            if not moves:
                print('CHECKMATE')
                self.gameover = True
                for king in kings:
                    self.draw_pieces[king[0], king[1], king[2]].obj.setColor(HIGHLIGHT_ATTACK)
            else:
                print('CHECK')

        else:
            self.check = 0
            if not moves:
                print('DRAW')

        return moves
        
    def square_default_color(self, pos):
        'Colors a specific square'
        # If we have a piece selected
        if self.dragging is not False:
            # If it's a move by a selected piece, it's green or red
            if (self.dragging, pos) in self.moves:
                if self.board_array[pos[0], pos[1], pos[2]] == 0:
                    self.draw_squares[pos[0], pos[1], pos[2]].setColor(HIGHLIGHT_MOVE)
                else:
                    self.draw_squares[pos[0], pos[1], pos[2]].setColor(HIGHLIGHT_ATTACK)
            # If it's a selected piece, it's blue
            elif self.dragging == pos:
                self.draw_squares[pos[0], pos[1], pos[2]].setColor(HIGHLIGHT)
            # If it isn't then it's just black or white
            else:
                self.draw_squares[pos[0], pos[1], pos[2]].setColor(square_color(*pos))
        # If we don't have a piece selected, it's just black or white
        else:
            self.draw_squares[pos[0], pos[1], pos[2]].setColor(square_color(*pos))

        # Mark king in red if in check
        if self.check:
            if self.board_array[pos[0], pos[1], pos[2]]*self.turn == 6 and self.dragging != pos:
                self.draw_squares[pos[0], pos[1], pos[2]].setColor(HIGHLIGHT_ATTACK)

    def show_possible_moves(self):
        # Changes the color of the squares the selected piece can move to
        for piece, move in self.moves:
            if piece == [self.dragging[0],self.dragging[1],self.dragging[2]]:
                if self.board_array[move[0],move[1],move[2]]*self.turn < 0:
                    self.draw_squares[move[0],move[1],move[2]].setColor(HIGHLIGHT_ATTACK)
                else:
                    self.draw_squares[move[0],move[1],move[2]].setColor(HIGHLIGHT_MOVE)

    def hide_possible_moves(self):
        # When we unselect a piece, we remove the coloring from the squares we can move to
        for piece, move in self.moves:
            self.draw_squares[move[0],move[1],move[2]].setColor(square_color(*move))


class Webcam(DirectObject):
    def __init__(self):
        'This object deals with obtaining the image from the webcam and processing it'
        base.setBackgroundColor(0.5,0.5,0.5)
        self.cap = cv2.VideoCapture(0)
        [self.cap.read() for i in range(10)]

        # Show the image on a card
        sm = CardMaker('bg')
        sm.setUvRange(Point2(0, 0), Point2(1, 1))
        sm.setFrame(-1, 1, -1, 1)

        self.test = render2d.attachNewNode(sm.generate(),2)

        webcam_img, webcam_texture = self.get_cv_img()
        self.test.setTexture(webcam_texture)

    def step(self):
        # Update texture
        webcam_img, webcam_texture = self.get_cv_img()
        self.test.setTexture(webcam_texture)

        return webcam_texture

    def get_cv_img(self):
        success, webcam_img = self.cap.read()
        if success:
            shape = webcam_img.shape
            flipped_img = cv2.flip(webcam_img, 0)

            webcam_texture = Texture("detect")
            webcam_texture.setCompression(Texture.CMOff)
            webcam_texture.setup2dTexture(shape[1], shape[0], Texture.TUnsignedByte, Texture.FRgb)

            p = PTAUchar.emptyArray(0)
            p.setData(flipped_img)
            webcam_texture.setRamImage(CPTAUchar(p))

            return webcam_img, webcam_texture


def ai(board, queue, recursions):
    # Get the move from the c++ code
    # In a separate function because it gets multiprocessed by the main function
    piece, move = board.best_move(recursions)
    queue.put((piece, move))

if __name__ == '__main__':    
    demo = ChessboardDemo()
    demo.run()
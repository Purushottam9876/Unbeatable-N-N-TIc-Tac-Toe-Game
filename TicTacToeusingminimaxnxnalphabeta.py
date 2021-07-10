from pade.misc.utility import start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
import random
import math
import time


class Board_state:
    def __init__(self,dim):
        self.dim = dim
        self.board = []
        self.pos={}
        for i in range(dim):
            l1=[]
            for j in range(dim):
                l1.append(' ')
                self.pos[i*dim+j] = [i,j]
            self.board.append(l1)

    def num_empty_space(self):
        count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] != 'X' and self.board[i][j] != 'O':
                    count += 1
        return count

    def print_board(self):
        for i in range(self.dim):
            str1 = ""
            for j in range(self.dim):
                if self.board[i][j] == 'X' or self.board[i][j] == 'O':
                    str1 = str1 + self.board[i][j] + " | "
                else:
                    str1 = str1 + "  | "
            print("| " + str1)

    def print_board_positions(self):
        for i in range(self.dim):
            str1 = ""
            for j in range(self.dim):
                str1 = str1 + str(i * self.dim + j) + " | "
            print("| " + str1)

    def write_symbol(self, symbol, n):
        i = self.pos[n][0]
        j = self.pos[n][1]
        if self.board[i][j] != 'X' and self.board[i][j] != 'O':
            self.board[i][j] = symbol
            return 1
        return -1

    def avlbl_moves(self):
        avlbl = []
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] == ' ':
                    avlbl.append(i * self.dim + j)
        return avlbl

    def iswinner(self, letter):
        for i in range(self.dim):
            if all(self.board[i][j] == letter for j in range(self.dim)):
                return True
            if all(self.board[j][i] == letter for j in range(self.dim)):
                return True
        if all(self.board[i][i] == letter for i in range(self.dim)):
            return True
        if all(self.board[i][self.dim-1-i] == letter for i in range(self.dim)):
            return True
        return False


class Human(Agent):
    def __init__(self, aid, symbol):
        super().__init__(aid)
        self.symbol = symbol

    def make_move(self, gameboard):
        while True:
            position = int(input("Enter the position you want to mark : "))
            if gameboard.write_symbol(self.symbol, position) != -1:
                break


class Computer(Agent):
    def __init__(self, aid, symbol):
        super().__init__(aid)
        self.symbol = symbol

    def make_move(self, gameboard):
        if gameboard.num_empty_space() == gameboard.dim*gameboard.dim:
            k = random.randint(0, gameboard.dim*gameboard.dim-1)
        else:
            start = time.time()
            k = self.minimax(gameboard, self.symbol,-math.inf,math.inf)['pos']
            end = time.time()
            print("Time Elapsed:",(end-start))
        gameboard.write_symbol(self.symbol, k)

    def minimax(self, gameboard, turn,alpha,beta):
        maximizing_player = self.symbol
        prev_turn = 'X'
        if turn == 'X':
            prev_turn = 'O'
        if gameboard.iswinner(prev_turn):
            res = {'pos': None}
            if prev_turn == maximizing_player:
                res['score'] = 1 * (gameboard.num_empty_space()+1)
            else:
                res['score'] = -1 * (gameboard.num_empty_space()+1)
            return res
        elif gameboard.num_empty_space() == 0:
            return {'pos': None, 'score': 0}
        if turn == maximizing_player:
            best_move = {'pos': None, 'score': -math.inf}
        else:
            best_move = {'pos': None, 'score': math.inf}
        for pos_move in gameboard.avlbl_moves():
            gameboard.write_symbol(turn, pos_move)
            ret_res = self.minimax(gameboard, prev_turn,alpha,beta)
            i = gameboard.pos[pos_move][0]
            j = gameboard.pos[pos_move][1]
            gameboard.board[i][j] = ' '
            ret_res['pos'] = pos_move
            if turn == maximizing_player:
                if ret_res['score'] > best_move['score']:
                    best_move = ret_res
                if best_move['score'] >= beta:
                    break
                if best_move['score'] > alpha:
                    alpha = best_move['score']
            else:
                if ret_res['score'] < best_move['score']:
                    best_move = ret_res
                if best_move['score'] <= alpha:
                    break
                if best_move['score'] < beta:
                    beta = best_move['score']
        return best_move


def play_first(gameboard, player1, player2):
    gameboard.print_board_positions()
    while gameboard.num_empty_space() != 0:
        player1.make_move(gameboard)
        gameboard.print_board()
        if gameboard.iswinner(player1.symbol):
            print("Hooray! You won!!!")
            break
        if gameboard.num_empty_space() == 0:
            print("It's a Tie.")
            return
        else:
            print("Computer's Turn")
            player2.make_move(gameboard)
            gameboard.print_board()
            if gameboard.iswinner(player2.symbol):
                print("Oops! You lost. Computer Won!")
                break
    if gameboard.num_empty_space() == 0:
        print("It's a Tie.")


def play(gameboard, player1, player2):
    while gameboard.num_empty_space() != 0:
        print("Computer's Turn")
        player2.make_move(gameboard)
        gameboard.print_board()
        if gameboard.iswinner(player2.symbol):
            print("Oops! You lost. Computer Won!")
            break
        if gameboard.num_empty_space() == 0:
            print("It's a Tie.")
        else:
            player1.make_move(gameboard)
            gameboard.print_board()
            if gameboard.iswinner(player1.symbol):
                print("Hooray! You won!!!")
                break
    if gameboard.num_empty_space() == 0:
        print("It's a Tie.")


if __name__ == "__main__":
    c = 100
    agents = list()
    n = int(input("Enter the dim of board: "))
    gameboard = Board_state(n)
    human_symbol = input("Enter Your Symbol(X or O): ").upper()
    computer_symbol = 'X'
    if human_symbol == 'X':
        computer_symbol = 'O'
    p1 = 'player1@localhost:{}'.format(2000 + c)
    player1 = Human(AID(name=p1), human_symbol)
    agents.append(player1)
    c += 10
    p2 = 'player2@localhost:{}'.format(20000 + c)
    player2 = Computer(AID(name=p2), computer_symbol)
    agents.append(player2)
    ch = 'Y'
    ch = input("Wanna play first?(Y/N): ").upper()
    if ch == 'Y':
        play_first(gameboard, player1, player2)
    else:
        play(gameboard, player1, player2)
    start_loop(agents)

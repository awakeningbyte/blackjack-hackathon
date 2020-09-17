import os,sys,inspect
from random import randint


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(parent_dir,"learntools"))
from learntools.core import binder; binder.bind(globals())
from learntools.python.blackjack import BlackJack

    
class Dealer(BlackJack):
    def __init__(self,strategy,verbose=True):
        super().__init__(strategy, verbose, True)
        
    def face(self):
        c = self.deal()
        self.log('Dealer starts with {}\n'.format(c))
        return c
    
    def deal(self):
        c = super().deal()
        self.dealer_cards.append(c)
        return c

    def play(self):
        self.log('\n__Dealer__play')
        while True:
            c = self.deal()
            self.log('Dealer hits and receives {}. (total = {})'.format(c, self.dealer_total))
            
            if self.dealer_total > 21:
                self.log('Dealer busts!')
                return -1
            # Stand on 17
            elif self.dealer_total >= 17:
                return self.dealer_total
        
class Player(BlackJack):
    def __init__(self,dealer_face_cards,id,name, strategy,verbose=True):
        super().__init__(strategy, verbose, True)
        self.dealer_cards=dealer_face_cards
        self.stack = 0
        self.name=name
     
        if callable(strategy)==False:
            self.attach(strategy)

    def attach(self, code):
        shim = 'player.phit=should_hit'
        func = code +"\n"+shim
        exec(func,{},{"player":self})
        
    def face(self):
        p1, p2 = self.deal(), self.deal()
        self.player_cards = [p1, p2]
        self.log('{}: starts with {} and {} (total = {})'.format(self.name, p1, p2, self.player_total))
    
    def deal(self):
        c = super().deal()
        self.player_cards.append(c)
        return c      
    
    def player_hits(self):
        args = [self.player_total, self.dealer_total, self.player_cards.count('A')]
        hit, bet = self.phit(*args)
        if bet < 0:
            bet=0
        if bet > 10:
            bet=10
        self.stack += bet    
        return hit,bet
    
    def play(self):
        hit, bet = self.player_hits()
        while hit:
            c = self.deal()
            self.log('{} hits, bet {}, receives {}. (total = {})'.format(
                self.name, bet, c, self.player_total))
            if self.player_total > 21:
                #'Player busts!'
                return self.player_total
            hit, bet = self.player_hits()
            
        self.log('{} stays, bet {}'.format(self.name, bet))
        return self.player_total

class simulate():
    def __init__(self,verbose=True):
        self.verbose=verbose
        self.players ={}

    def log(self, msg):
        if self.verbose:
            print(msg)  

    def add(self,id, name, strategy):
        self.players[id]= [name,strategy]

    def one_game(self):
        result = {}
        holds ={}
        dealer = Dealer("",self.verbose)
        dealer_face_card = dealer.face()
        
        for id in self.players:
            name, s = self.players[id]
            player = Player([dealer_face_card], id, name, s, self.verbose)
            player.face()

            p = player.play()
            if p > 21:
                #self.log('{} busts, lost -{}'.format(name, player.stack))
                result[id] = [name, 0, -player.stack,'{} busts, {} lost,  $ -{}'.format(p, name, player.stack)]
            else:
                holds[id] = [p,name, player.stack]
                #return 0, -player.stack
            self.log("\n")

        d =dealer.play()
        if d == -1:
            for id in holds:
                _, name, stack = holds[id]
                #self.log('Dealer busts, {name} won +{}'.format(name, holds[name]))
                result[id] = [name, 1, stack,'Dealer busts, {} won $ +{}'.format(name, stack)]

        # if p > d:
        #     self.log('{} > {}, Player won,  +{}'.format(p, d, player.stack))
        #     return 1,player.stack
        else:
            for id in holds:
                c, name, s = holds[id]
                if c > d:
                    #self.log('{} > {},  simulation.simulate(10000){} won,  +{}'.format(c, d, name, s))
                    result[id] = [name, 1, s, '{} > {}, {} won,  $ +{}'.format(c, d, name, s)]
                else:
                    #self.log('{} =< {}, {} lost,  -{}'.format(p, d, name, player.stack))
                    result[id]= [name, 0,-s, '{} =< {}, {} lost,  $ -{}'.format(c, d, name, player.stack)]
        return result

    def simulate(self, n_games=100):
        result = {}
        for _ in range(n_games):
            r = self.one_game()
            #print("*", r,"\n")
            for n in r:
                name, w,b,_ = r[n]
                
                if n in result:
                    name, x,y = result[n]
                    #print(w,b,x,y, "\n")
                    result[n]=[name, x+w,y+b]
                else:
                    result[n]=[name,w,b]
        output = []
        for id in result:
            name, wins, bankroll= result[id]
            output.append((name, wins/n_games, bankroll))
        return output
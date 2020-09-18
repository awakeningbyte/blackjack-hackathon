# Intro

This coding competition is modified from Kaggle's awesome [Microchallenges](https://www.kaggle.com/learn/microchallenges). Participants are required to implement a gaming strategy and upload it to the judging server. All uploaded strageties will be executed together. A winner will be picked based on the performance of his/her strategy.

# Run
    After cloning the repo, you should pull `learningtools` submodule

```
    git submodule update --recursive --init
```

Then you can run the notebook container with the following commands
```
    docker build -t datomar/hackson-blackjack .
    docker run --rm -p 8888:8888 datomar/hackson-blackjack
```

Open a brower at http://localhost:8888, click `blackjack.ipynb` to get started.

# Blackjack Rules

Ready for a quick test of your logic and programming skills? 

In this challenge, you will write the logic for a blackjack playing program.  Our dealer will test your program by playing 50,000 hands of blackjack. You'll see how frequently your program won, and you can discuss how your approach stacks up against others in the challenge.

![Blackjack](http://www.hightechgambling.com/sites/default/files/styles/large/public/casino/table_games/blackjack.jpg)

We'll use a slightly simplified version of blackjack (aka twenty-one). In this version, there is one player (who you'll control) and a dealer. Play proceeds as follows:

- The player is dealt two face-up cards. The dealer is dealt one face-up card.
- The player may ask to be dealt another card ('hit') as many times as they wish. If the sum of their cards exceeds 21, they lose the round immediately.
- The dealer then deals additional cards to himself until either:
    - The sum of the dealer's cards exceeds 21, in which case the player wins the round, or
    - The sum of the dealer's cards is greater than or equal to 17. If the player's total is greater than the dealer's, the player wins. Otherwise, the dealer wins (even in case of a tie).

When calculating the sum of cards, Jack, Queen, and King count for 10. Aces can count as 1 or 11. (When referring to a player's "total" above, we mean the largest total that can be made without exceeding 21. So A+8 = 19, A+8+8 = 17.)



```python
### Don't change content in this cell
import pandas as pd
from tqdm import tqdm
from game import *

### strategy of NPC player 1 
random_hit = """
def should_hit(player_total, dealer_card_val, player_aces):
    import random
    bet = random.randint(1, 10)
    hit = (bet % 2 ==0)
    return hit,bet
"""

### strategy of NPC player 2
always_no = """
def should_hit(player_total, dealer_card_val, player_aces):
    return False,1
"""
```


# The Blackjack Player
You'll write a function representing the player's decision-making strategy. It returns a tuple of bool & int
The boolean value means decision of `hit` or `stay`. The int value must be within 1..10, it means how much you want to bet on this hand. The above cell contains 2 strategies in string format. You can use them as example


```python
#implement your stragegy here
def should_hit(player_total, dealer_card_val, player_aces):
    return False, 11
```

# Try your strategy out
You can test your strategy against the 2 NPC players.


```python
simulation = simulate(True)
simulation.add(1,"You", strategy=should_hit)
simulation.add(2,"NPC1", strategy=random_hit)
simulation.add(3,"NPC2", strategy=always_no)

result = simulation.one_game()

print("\n\n******* Game Result ********\n\n")
for p in result:
    name,_,_, m = result[p]
    print("*", m)
```

    Dealer starts with K
    
    You: starts with 3 and 5 (total = 8)
    You stays, bet 10
    
    
    NPC1: starts with Q and K (total = 20)
    NPC1 hits, bet 6, receives 3. (total = 23)
    
    
    NPC2: starts with A and Q (total = 21)
    NPC2 stays, bet 1
    
    
    
    __Dealer__play
    Dealer hits and receives J. (total = 20)
    
    
    ******* Game Result ********
    
    
    * 23 busts, NPC1 lost,  $ -6
    * 8 =< 20, You lost,  $ -1
    * 21 > 20, NPC2 won,  $ +1


# Compete with NPC

Once you fell satisfied with your stategy, upload the `should_hit` function to the judge backend. Winnier will be chosen with the player with higest positive bankroll. If all player loss money, then the higest winning rate is the winnipeg.

The following is how the judging function works.


```python
simulation = simulate(False)
simulation.add(1,"You", should_hit)
simulation.add(2,"NPC1", random_hit)
simulation.add(3,"NPC2", always_no)

data = simulation.simulate(n_games=50000)

df = pd.DataFrame(data, columns =['Name', 'Wins', 'Bankroll']) 
  
print(df)

winner = df.loc[df['Bankroll'].idxmax()]
print(f"\n\nThe winner is {winner['Name']}")
```

    100%|██████████| 50000/50000 [00:07<00:00, 6504.78games/s]

       Name     Wins  Bankroll
    0   You  0.38078   -119220
    1  NPC1  0.27934   -173783
    2  NPC2  0.37918    -12082
    
    
    The winner is NPC2


    



```python

```

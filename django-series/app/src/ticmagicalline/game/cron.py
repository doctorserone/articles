from game.models import Game, GameMovement
from django.db.models import Q
from datetime import datetime
from game.tictactoe.tictactoe import TicTacToe
from game.tictactoe.dragonplay import DragonPlay
from game.views import getDragonAI

def do_ia_movements():
    print("Performing pending IA movements...")

    ai = getDragonAI()

    # Get unfinished IA games
    pendingIaGames = Game.objects.filter(Q(user_o=ai) | Q(user_x=ai), Q(winner='')).order_by("-creation")

    for game in pendingIaGames:
        lastMovement = GameMovement.objects.filter(Q(game=game)).order_by("-date").first()
        tictactoe = TicTacToe(game.board)

        if lastMovement.user != ai:
            print(f"Making dragon move on game against {game.user_o}, created on {game.creation}...")
            dragon = DragonPlay(game.board)

            position =- 1
            while position == -1:
                position = dragon.chooseMovement()

                # In these games the AI is always the X player (second player)
                symbol = 'X' 

                if position == -1:
                    print(f"Invalid movement at position {position}! Trying again...")

            # If our turn, make move
            tictactoe.makeMove(symbol, position)
            lastMovement = GameMovement.objects.create(user=ai, game=game, symbol=symbol, movement=position, date=datetime.now())

            # Update game
            game.board = tictactoe.board
            game.last_move = datetime.now()

            # Check if game is over
            if tictactoe.checkGameOver():
                game.winner = tictactoe.winner

            game.save()


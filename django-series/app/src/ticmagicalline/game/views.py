from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from game.models import Game, GameMovement
from game.tictactoe.tictactoe import TicTacToe


# Movement symbols:
# E=empty
# X=Player X movement
# O=Player O movement
# C=Game creation
# J=Join to game

# Winner symbol:
# D=draw
# X=Player X wins
# O=Player O wins


def indexView(request):
    context = {}

    user = request.user
    if user is not None and request.user.username != "":
        numStartPageGames = 10

        # Get real user
        user = User.objects.get(username=request.user.username)

        # About pagination:
        # https://docs.djangoproject.com/en/5.0/topics/pagination/

        openedGames = Game.objects.filter(Q(user_x=None), ~Q(user_o=user)).order_by("-creation")
        paginator1 = Paginator(openedGames, numStartPageGames)
        context['openedGames'] = paginator1.get_page(1)
        context['openedGamesCount'] = paginator1.count

        myGames = Game.objects.filter(Q(user_o=user), Q(winner='')).order_by("-creation")
        paginator2 = Paginator(myGames, numStartPageGames)
        context['myGames'] = paginator2.get_page(1)
        context['myGamesCount'] = paginator2.count

        finalizedGames = Game.objects.filter(Q(user_o=user) | Q(user_x=user), ~Q(winner='')).order_by("-creation")
        paginator3 = Paginator(finalizedGames, numStartPageGames)
        context['finalizedGames'] = paginator3.get_page(1)
        context['finalizedGamesCount'] = paginator3.count

    response = loader.get_template("game/templates/index.html").render(context, request)
    return HttpResponse(response)


def loginView(request):
    if request.POST.get("username", "") == "ai":
        return makeErrorView(request, "Don't mess with the dragons!")

    # Try to log in first
    user = authenticate(username=request.POST.get("username", ""), password=request.POST.get("password", ""))

    if user is not None and user.is_active:
        print("User " + request.POST.get("username", "") + " authenticated!")
        login(request, user)
        return redirect("index")

    # Validate user and password
    if User.objects.filter(username=request.POST.get("username", "")).exists():
        return makeErrorView(request, "Invalid username or password.")

    if (len(request.POST.get("password", "")) < 8 or request.POST.get("password", "").find(request.POST.get("username", "")) != -1):
        return makeErrorView(request, "Password too short or too similar to username.")

    # The user does not exists, create it
    user = User.objects.create_user(username=request.POST.get("username", ""), email="", password=request.POST.get("password", ""))
    login(request, user)
    return redirect("index")


def logoutView(request):
    logout(request)
    return redirect("index")


def createGameView(request):
    user = request.user
    if user is None or request.user.username == "":
        return makeErrorView(request, "Not authenticated!")

    # Get real user
    user = User.objects.get(username=request.user.username)

    # Create game
    if request.POST.get("type", "pvp") == "pvp":
        print("Creating PVP game...")
        game = Game.objects.create(
            user_o=user, user_x=None, board="EEEEEEEEE", winner="", creation=datetime.now()
        )

    else:
        ai = getDragonAI()
        if ai is None:
            return makeErrorView(
                request,
                "Cannot create PVE game! There are no dragons in the lair at this moment...",
            )

        print("Creating PVE game...")
        game = Game.objects.create(
            user_o=user, user_x=ai, board="EEEEEEEEE", winner="", creation=datetime.now()
        )

    print("Creating initial movement (C=creation)...")
    GameMovement.objects.create(user=user, game=game, symbol="C", movement=0, date=datetime.now())
    game.last_move = datetime.now()
    game.save()

    print("Game with ID " + str(game.id) + " created! Redirecting to play...")
    return redirect("play", id=game.id)


def joinGameView(request, id):
    user = request.user
    if user is None or request.user.username == "":
        return makeErrorView(request, "Not authenticated!")

    # Get real user
    user = User.objects.get(username=request.user.username)

    # Get game
    game = Game.objects.get(id=id)
    game.user_x = user

    print("Creating join movement (J=join)...")
    GameMovement.objects.create(user=user, game=game, symbol="J", movement=0, date=datetime.now())
    game.last_move = datetime.now()

    game.save()

    print("Joined to game with ID " + str(game.id) + "! Redirecting to play...")
    return redirect("play", id=game.id)


def playGameView(request, id):
    context = {}
    
    user = request.user
    if user is None or request.user.username == "":
        return makeErrorView(request, "Not authenticated!")

    # Get game
    print("Obtaining game with ID " + str(id) + "...")
    game = Game.objects.get(id=id)

    if game is not None:
        numMovements = 8

        movements = GameMovement.objects.filter(Q(game=game)).order_by("-date")
        paginator = Paginator(movements, numMovements)
        context['movements'] = paginator.get_page(1)
        context['movementsCount'] = paginator.count

        context["id"] = id
        context["game"] = game

        lastPlayer = None
        for mov in movements:
            if mov.symbol != "C" and mov.symbol != "J":
                print(f"Last valid movement: user={mov.user.username}, symbol={mov.symbol}, movement={mov.movement}, date={mov.date}")
                lastPlayer = mov.user
                break
             
        if lastPlayer == None and game.user_o == user:
            context["currentStatus"] = "The game has been created! It's your turn to play."
            context["ommitPlayAction"] = 0

        elif game.winner != "":
            context["ommitPlayAction"] = 1

            if game.winner == "D":
                context["currentStatus"] = "The game has ended in a draw!"
            elif (game.winner == "X" and game.user_x == user) or (game.winner == "O" and game.user_o == user):
                context["currentStatus"] = "The game has ended! You win!"
            else:
                context["currentStatus"] = "The game has ended! Your enemy win!"

        elif lastPlayer == user:
            context["currentStatus"] = "It's the enemy turn to play."
            context["ommitPlayAction"] = 1

        else:
            context["currentStatus"] = "It's your turn to play."
            context["ommitPlayAction"] = 0

        response = loader.get_template("game/templates/game.html").render(context, request)
        return HttpResponse(response)

    else:
        return makeErrorView(request, "Cannot load that game!")


def makeMoveView(request, id, position):
    context = {}
    
    user = request.user
    if user is None or request.user.username == "":
        return makeErrorView(request, "Not authenticated!")

    # Get game
    print("Obtaining game with ID " + str(id) + "...")
    game = Game.objects.get(id=id)

    if game is not None:
        if game.winner != "":
            return redirect("play", id=game.id)
        
        if game.board[position] != "E":
            return makeErrorView(request, "Invalid movement, position not available!", "/play/"+str(game.id))
        
        tictactoe = TicTacToe(game.board)

        # Check latest movement, maybe is not our turn
        movements = GameMovement.objects.filter(Q(game=game)).order_by("-date")

        lastPlayer = None
        for mov in movements:
            if mov.symbol != "C" and mov.symbol != "J":
                print(f"Last valid movement: user={mov.user.username}, symbol={mov.symbol}, movement={mov.movement}, date={mov.date}")
                lastPlayer = mov.user
                break
             
        if lastPlayer == None or lastPlayer != user:
            if game.user_o == user:
                symbol = 'O'
            else:
                symbol = 'X'

            print(f"Making {symbol} movement at position {position}...")

            # If our turn, make move
            tictactoe.makeMove(symbol, position)
            lastMovement = GameMovement.objects.create(user=user, game=game, symbol=symbol, movement=position, date=datetime.now())

            # Update game
            game.board = tictactoe.board
            game.last_move = datetime.now()

            # Check if game is over
            if tictactoe.checkGameOver():
                game.winner = tictactoe.winner

            game.save()

        return redirect("play", id=game.id)

    else:
        return makeErrorView(request, "Cannot load that game!")

def makeErrorView(request, message, returnUrl = '/'):
    context = {}
    
    print(message)
    context["message"] = message
    context["returnUrl"] = returnUrl

    response = loader.get_template("game/templates/error.html").render(context, request)
    return HttpResponse(response)


def getDragonAI():
    dragon = None

    try:
        print("Getting dragon...")
        dragon = User.objects.get(username="ai")

    except User.DoesNotExist:
        print("Nobody is in the lair! Creating dragon now...")
        dragon = User.objects.create_user(username="ai", email="ai@tic.fake", password="drag0n")

    return dragon

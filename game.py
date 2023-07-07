import turtle as tt
import random as rd
import time

# Global variables

# set rate and delay
rate = 5
delay = 0.05

winsize = 700
fs = winsize/2 - 100  # frame size
vps = fs - 15  # valid position for food and snake snake
style = ('Segoe UI', 20)
titlefont = 'Comic sans ms'


# Direction changing functions
def goUp():
    if snake.direction != 'down':
        snake.direction = 'up'

def goDown():
    if snake.direction != 'up':
        snake.direction = 'down'

def goRight():
    if snake.direction != 'left':
        snake.direction = 'right'

def goLeft():
    if snake.direction != 'right':
        snake.direction = 'left'


# Control speed
def fast():
    global rate
    if (rate >= 30): return
    rate += 0.5

def slow():
    global rate
    if (rate <= 5): return
    rate -= 0.5


# Function to control the snake's moves
def move(rate):
    if snake.direction == 'up':
        y = snake.ycor()
        snake.sety(y + rate)
    if snake.direction == 'down':
        y = snake.ycor()
        snake.sety(y - rate)
    if snake.direction == 'right':
        x = snake.xcor()
        snake.setx(x + rate)
    if snake.direction == 'left':
        x = snake.xcor()
        snake.setx(x - rate)


# Function for welcome
def welcomeScreen():
    pen = tt.Turtle()
    pen.speed(0)
    pen.hideturtle()
    pen.pensize(7)
    r = 250

    pen.up()
    pen.goto(0, -r)
    pen.down()
    # Total angle = 10 * 4 * 9 = 360 degree
    for i in range(10):
        for j in range(4):
            if j % 2 == 0:
                pen.up()
                pen.circle(r, 9)
                pen.down()
            if j % 4 == 1:
                pen.color('red')
                pen.circle(r, 9)
            if j % 4 == 3:
                pen.color('blue')
                pen.circle(r, 9)
    pen.up()

    pen.goto(0, 100)
    pen.color('white')
    pen.write('WELCOME TO', font = ('Arial', 20), align = 'center')

    pen.goto(0, 0)
    pen.color('orange')
    pen.write('H\'s Hungry ', font = (titlefont, 50, 'bold', 'italic'), align = 'center')
    
    pen.color('red')
    pen.goto(0, -80)
    pen.write('Snake ', font = (titlefont, 60, 'bold', 'italic'), align = 'center')

    pen.goto(0, -170)
    pen.color('yellow')
    pen.write('Please wait...\n', font = ('Arial', 20, 'italic'), align = 'center')

    pen.write(' ')
    
    time.sleep(2)
    win.clearscreen()


# To display scores
def scoreboard(score, highScore):
    board.clear()
    board.color('lime')
    board.goto(-fs + 100, fs + 30)
    board.write(f"Score : {score}", align = 'center', font = style)

    board.color('orange')
    board.goto(fs - 120, fs + 30)
    board.write(f"High Score : {highScore}", align = 'center', font = style)


# Reset game bsed on conditions
def gameReset(type):
    global rate, delay

    board.clear()
    board.color('white')
    board.goto(0, fs + 30)
    if (type == 'boundary'):
        board.write("Oops, boundary collision", align = 'center', font = style)
    if (type == 'body'):
        board.write("Oops, self collision", align = 'center', font = style)
    win.update()
    time.sleep(2)
    board.clear()
    board.color('red')
    board.write("GAME OVER", align = 'center', font = style)
    win.update()
    time.sleep(2)

    # Increase speed for next game
    rate += 0.5

    # Reset snake & score
    snake.goto(0, 0)
    snake.direction = 'stop'
    score = 0
    delay = 0.05

    # Remove snake body
    for body in snakebody:
        body.goto(1000, 1000)  # Move body parts off the screen
    snakebody.clear()
    
    # Move food at random position
    food.goto(rd.randint(-vps, vps), rd.randint(-vps, vps))

    # Update scoreboard
    scoreboard(score, highScore)


# Main function
if __name__ == '__main__':
    # set scores
    score = 0
    highScore = 0

    # set up screen
    win = tt.Screen()
    win.title("H's Hungry snake")
    win.setup(width = winsize, height = winsize)
    win.bgpic("welcome.png")
    win.tracer(2)

    # welcome player
    welcomeScreen()

    # set up game screen
    win.bgpic("welcome.png")
    win.tracer(0)

    # set up boundary and space for snake to move
    frame = tt.Turtle()
    frame.pensize(4)
    frame.hideturtle()
    frame.up()
    frame.goto(fs, -fs)
    frame.down()
    frame.fillcolor('black')
    frame.begin_fill()
    for i in range(4):
        frame.left(90)
        # total length = 10 * (0.1 + 0.1) * fs = 2 * fs
        for j in range(20):
            frame.pencolor('dodgerblue')
            frame.forward(0.05 * fs)
            frame.pencolor('black')
            frame.forward(0.05 * fs)
    frame.end_fill()

    # set up scoreboard
    board = tt.Turtle()
    board.hideturtle()
    board.up()
    scoreboard(score, highScore)

    # set up snake head
    snake = tt.Turtle()
    snake.shape('circle')
    snake.shapesize(1)
    snake.color('yellow')
    snake.speed(0)
    snake.up()
    snake.direction = "stop"  # initially snake is at rest

    snakebody = []  # to grow as food is consumed

    # set up food
    food = snake.clone()
    food.shapesize(0.7)
    food.color('red')
    food.up()
    food.goto(rd.randint(-vps, vps), rd.randint(-vps, vps))

    # keyboard controls for snake
    win.listen()
    win.onkeypress(goUp, 'Up')
    win.onkeypress(goDown, 'Down')
    win.onkeypress(goRight, 'Right')
    win.onkeypress(goLeft, 'Left')
    win.onkeypress(fast, '+')
    win.onkeypress(slow, '-')

    # Main game loop
    while True:
        win.update()

        # if snake collides with boundary
        if (abs(snake.xcor()) > vps) or (abs(snake.ycor()) > vps):
            gameReset('boundary')

        # if snakebody collides with its head
        for cell in snakebody:
            if cell.distance(snake) < 5:
                gameReset('body')

        # if snake collides with food
        if snake.distance(food) < 15:
            # Move food at random position
            food.goto(rd.randint(-vps, vps), rd.randint(-vps, vps))

            # Grow snake body
            newPart = snake.clone()
            newPart.color('orange')
            snakebody.append(newPart)
            delay -= 0.001

            # Update score
            score += 50
            highScore = max(highScore, score)

            # Update scoreboard
            scoreboard(score, highScore)

        # Move the snake body
        if len(snakebody) > 0:
            # Move the last body part to the position of the second-to-last body part
            for i in range(len(snakebody) - 1, 0, -1):
                x = snakebody[i - 1].xcor()
                y = snakebody[i - 1].ycor()
                snakebody[i].goto(x, y)

            # Move the first body part to the position of the snake's head
            x = snake.xcor()
            y = snake.ycor()
            snakebody[0].goto(x, y)

        move(rate)
        time.sleep(delay)
import turtle as tt
import random as rd
import time

# GLOBAL VARIABLES
WINSIZE = 700
FS = WINSIZE/2 - 100  # Frame size
VPS = FS - 15  # Valid position for food and snake snake
STYLE = ('Comic Sans MS', 20)
TITLEFONT = 'Comic sans ms'
BGPIC = 'images/bg.png'
SNAKE_HEAD_COLOR = 'yellow'
SNAKE_BODY_COLOR = 'orange'
FOOD_COLOR = 'red'

# Stats
SCORE = 0
HIGHSCORE = 0

# Set rate and delay
RATE = 5
DELAY = 0.05

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
    global RATE
    if RATE >= 30:
        return
    RATE += 0.5

def slow():
    global RATE
    if RATE <= 5:
        return
    RATE -= 0.5

# Function to control the snake's moves
def moveSnake():
    global RATE

    # Move the body
    if len(snake_body) > 0:
        # Move the last body part to the position of the second-to-last body part
        for i in range(len(snake_body) - 1, 0, -1):
            x = snake_body[i - 1].xcor()
            y = snake_body[i - 1].ycor()
            snake_body[i].goto(x, y)

        # Move the first body part to the position of the snake's head
        x = snake.xcor()
        y = snake.ycor()
        snake_body[0].goto(x, y)

    # move the head
    if snake.direction == 'up':
        y = snake.ycor()
        snake.sety(y + RATE)
    if snake.direction == 'down':
        y = snake.ycor()
        snake.sety(y - RATE)
    if snake.direction == 'right':
        x = snake.xcor()
        snake.setx(x + RATE)
    if snake.direction == 'left':
        x = snake.xcor()
        snake.setx(x - RATE)

    # to control the speed of snake
    time.sleep(DELAY)

# Function to call key bindings
def keyBindings():
    win.listen()
    win.onkeypress(goUp, 'Up')
    win.onkeypress(goDown, 'Down')
    win.onkeypress(goRight, 'Right')
    win.onkeypress(goLeft, 'Left')
    win.onkeypress(fast, '+')
    win.onkeypress(slow, '-')


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
    # Total angle = 10 * 4 * 9 = 360 degrees
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
    pen.write('WELCOME TO', font=('Arial', 20), align='center')

    pen.goto(0, 0)
    pen.color('orange')
    pen.write('H\'s Hungry ', font=(TITLEFONT, 50, 'bold', 'italic'), align='center')

    pen.color('red')
    pen.goto(0, -80)
    pen.write('Snake ', font=(TITLEFONT, 60, 'bold', 'italic'), align='center')

    pen.goto(0, -170)
    pen.color('yellow')
    pen.write('Please wait...\n', font=('Arial', 20, 'italic'), align='center')

    pen.write(' ')

    time.sleep(2)
    win.clearscreen()

# Function to draw boundary
def drawBoundary():
    frame = tt.Turtle()
    frame.pensize(4)
    frame.hideturtle()
    frame.up()
    frame.goto(FS, -FS)
    frame.down()
    frame.fillcolor('black')
    frame.begin_fill()
    for i in range(4):
        frame.left(90)
        # Total length = 10 * (0.1 + 0.1) * FS = 2 * FS
        for j in range(20):
            frame.pencolor('dodgerblue')
            frame.forward(0.05 * FS)
            frame.pencolor('black')
            frame.forward(0.05 * FS)
    frame.end_fill()

# Function to display scores
def scoreBoard():
    global SCORE, HIGHSCORE
    board.clear()
    board.color('lime')
    board.goto(-FS + 100, FS + 30)
    board.write(f"Score : {SCORE}", align='center', font=STYLE)

    board.color('orange')
    board.goto(FS - 120, FS + 30)
    board.write(f"High Score : {HIGHSCORE}", align='center', font=STYLE)

# Function to check for collisions
def checkCollisions():
    # If snake collides with the boundary
    if abs(snake.xcor()) > VPS or abs(snake.ycor()) > VPS:
        gameReset('boundary')

    # If snake body collides with its head
    for cell in snake_body:
        if cell.distance(snake) < 5:
            gameReset('body')

# Function to call when snake eats food
def eatFood():
    global DELAY, SCORE, HIGHSCORE
    # Move food to a random position
    food.goto(rd.randint(-VPS, VPS), rd.randint(-VPS, VPS))

    # Grow snake body
    new_part = snake.clone()
    new_part.color(SNAKE_BODY_COLOR)
    snake_body.append(new_part)
    DELAY -= 0.001

    # Update score
    SCORE += 50
    HIGHSCORE = max(HIGHSCORE, SCORE)

    # Update scoreBoard
    scoreBoard()

# Reset game based on conditions
def gameReset(type):
    global RATE, DELAY, SCORE

    board.clear()
    board.color('white')
    board.goto(0, FS + 30)
    if type == 'boundary':
        board.write("Oops, boundary collision", align='center', font=STYLE)
    if type == 'body':
        board.write("Oops, self collision", align='center', font=STYLE)
    win.update()
    time.sleep(2)
    board.clear()
    board.color('red')
    board.write("GAME OVER", align='center', font=STYLE)
    win.update()
    time.sleep(2)

    # Increase speed for the next game
    RATE += 0.5

    # Reset snake and score
    snake.goto(0, 0)
    snake.direction = 'stop'
    SCORE = 0
    DELAY = 0.05

    # Remove snake body
    for body in snake_body:
        body.goto(1000, 1000)  # Move body parts off the screen
    snake_body.clear()

    # Move food to a random position
    food.goto(rd.randint(-VPS, VPS), rd.randint(-VPS, VPS))

    # Update scoreBoard
    scoreBoard()


# Main function
if __name__ == '__main__':

    # Set up screen
    win = tt.Screen()
    win.title("H's Hungry snake")
    win.setup(width=WINSIZE, height=WINSIZE)
    win.bgpic(BGPIC)
    win.tracer(2)

    # Welcome player
    welcomeScreen()

    # Set up game screen
    win.bgpic(BGPIC)
    win.tracer(0)

    # Set up boundary and space for the snake to move
    drawBoundary()

    # Set up scoreBoard
    board = tt.Turtle()
    board.hideturtle()
    board.up()
    scoreBoard()

    # Set up snake head
    snake = tt.Turtle()
    snake.shape('circle')
    snake.shapesize(1)
    snake.color(SNAKE_HEAD_COLOR)
    snake.speed(0)
    snake.up()
    snake.direction = "stop"  # Initially, snake is at rest

    snake_body = []  # To grow as food is consumed

    # Set up food
    food = snake.clone()
    food.shapesize(0.7)
    food.color(FOOD_COLOR)
    food.up()
    food.goto(rd.randint(-VPS, VPS), rd.randint(-VPS, VPS))

    # Keyboard controls for the snake
    keyBindings()

    # Main game loop
    while True:
        win.update()

        # Check for collisions
        checkCollisions()

        # If snake collides with food    
        if snake.distance(food) < 15:
            eatFood()

        # Move the snake body
        moveSnake()

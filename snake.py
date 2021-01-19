import curses
import time
import random
from curses import textpad


def create_food(snake ,box):
    food = None

    while food is None:
        food = [random.randint(box[0][0] + 1 , box[1][0] -1) ,
                random.randint(box[0][1] + 1 , box[1][1] -1) ]

        if food in snake:
            food = None
    return food


def print_score(stdcr,score):
    sh , sw = stdcr.getmaxyx()
    score_text = "Score : "+str(score)
    stdcr.addstr(1 , sw//2 - len(score_text) , score_text)
    stdcr.refresh()



def main(stdcr):
    # for making the cursor invisible
    curses.curs_set(0)

    # for making no delays and waithing for userinput for 150ms
    # it is used for making snake move automatically
    stdcr.nodelay(1)
    stdcr.timeout(150)
    
    # for getting the height and width of the screen
    # the (0,0) position is at the top left in curses 
    sh , sw = stdcr.getmaxyx()


    box = [[3,3] , [sh-3,sw-3]]

    # for drawing a rectangle area
    textpad.rectangle(stdcr , box[0][0] , box[0][1] , box[1][0] , box[1][1])
    
    # initializing a screen
    snake = [
        [sh//2 , sw//2+1],
        [sh//2 , sw//2],
        [sh//2 , sw//2-1]
    ]

    # setting the snake direction to right
    direction = curses.KEY_RIGHT

    # printing the snake
    for y , x in snake:
        stdcr.addstr(y,x,'#')
        #stdcr.refresh()

    # printing the food
    food = create_food(snake , box)
    stdcr.addstr(food[0] , food[1] , '*')

    # for printing the score
    score = 0
    print_score(stdcr ,score)

    # for personal signature
    sig_text = "Made By Naheed Rayan @2021"
    stdcr.addstr(sh-1 , sw//2 - len(sig_text)//2 , sig_text) 

    while 1:
        key = stdcr.getch()

        if key in [curses.KEY_RIGHT , curses.KEY_LEFT , curses.KEY_UP ,curses.KEY_DOWN]:
            direction = key
        

        head = snake[0]

        if direction == curses.KEY_RIGHT:
            new_head = [head[0] , head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0] , head[1] -1 ]
        elif direction == curses.KEY_UP:
            new_head = [head[0] -1 , head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] +1 , head[1]]

        # inserting the new head
        snake.insert(0 , new_head)
        stdcr.addstr(new_head[0] , new_head[1] , '#')


        # if the snake eats the food
        if snake[0] == food:
            # for updating the score
            score += 1
            print_score(stdcr ,score)

            # for creating the food
            food = create_food(snake , box)
            stdcr.addstr( food[0] ,food[1] , '*')

        else:
            # making the last element black and poping them out
            # in this way the snake moves
            stdcr.addstr(snake[-1][0] , snake[-1][1] , ' ')
            snake.pop()
            
        # for ending the game
        if (snake[0][0] in [box[0][0] , box[1][0]] or
            snake[0][1] in [box[0][1] , box[1][1]] or
            snake[0] in snake[1:]) :

            # for initializing color
            curses.init_pair(1 ,curses.COLOR_RED ,curses.COLOR_YELLOW)
            
            msg = "Game Over!"

            # printing the message with color
            stdcr.attron(curses.color_pair(1))
            stdcr.addstr(sh//2, sw//2 - len(msg) , msg)
            stdcr.attroff(curses.color_pair(1))

            # for making infinite delay
            stdcr.nodelay(0)
            stdcr.getch()
            break


        # for refreshing the screen
        stdcr.refresh()


    
# using the wrapper class.Read the doc for more info
curses.wrapper(main)
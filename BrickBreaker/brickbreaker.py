import tkinter as tk
import login

g_high_score=0
u_score=0
username=''

class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10
        item = canvas.create_oval(x-self.radius, y-self.radius,
                                  x+self.radius, y+self.radius,
                                  fill='white')
        super().__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='yellow')
        super().__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        # get width of the info
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)


class Brick(GameObject):
    COLORS = {1: "#e74c3c", 2: "#3498db"}
    game=None
    def __init__(self, gamee, canvas, x, y, hits):
        Brick.game=gamee
        self.width = 75
        self.height = 20
        self.hits = hits
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super().__init__(canvas, item)

    def hit(self):
        self.hits -= 1
        if self.hits == 0:
            # print('inside brick class:',Brick.game.score)
            # on breaking the brick update score
            Brick.game.score+=10
            Brick.game.update_score()
            # destroy brick from canvas
            self.delete()
        else:
            self.canvas.itemconfig(self.item,
                                   fill=Brick.COLORS[self.hits])


class Game(tk.Frame):
    global g_high_score
    def __init__(self, master):
        # inherit the frame class to place the canvas objects
        super().__init__(master)
        self.lives = 3
        self.highscore = g_high_score
        self.score=0
        self.width = 610
        self.height = 400
        self.canvas = tk.Canvas(self, bg='#aaaaff',
                                width=self.width,
                                height=self.height,)
        self.canvas.pack()
        self.pack()

        self.items = {}
        self.ball = None
        # creae paddle object
        self.paddle = Paddle(self.canvas, self.width/2, 326)
        self.items[self.paddle.item] = self.paddle

        # create bricks
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)


        self.lives_text = None
        self.score_text=None
        self.highscore_text=None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                         lambda _: self.paddle.move(10))

    def setup_game(self):
           self.add_ball()
           self.update_lives_text()
           self.update_score()
           self.update_highscore()
           self.text = self.draw_text(300, 200,
                                      'Press Space to start')
           self.canvas.bind('<space>', lambda _: self.start_game())

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        # place ball on middle of paddle
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        # make ball object
        self.ball = Ball(self.canvas, x, 310)
        # set ball on paddle
        self.paddle.set_ball(self.ball)

    def add_brick(self, x, y, hits):
        # create brick object
        brick = Brick(self,self.canvas, x, y, hits)
        self.items[brick.item] = brick

    # to display text
    def draw_text(self, x, y, text, size='40'):
        font = ('Forte', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)

    def update_lives_text(self):
        text = 'Lives: %s' % self.lives
        if self.lives_text is None:
            self.lives_text = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.lives_text, text=text)

    def update_score(self):
        print("Update_scores: ",self.score)
        text = 'Score: %d' % self.score
        if self.score_text is None:
            self.score_text = self.draw_text(300, 20, text, 15)
        else:
            self.canvas.itemconfig(self.score_text, text=text)

    def update_highscore(self):
        global g_high_score
        text = 'Highscore: %s' % g_high_score
        if self.highscore_text==None:
            self.highscore_text = self.draw_text(540, 20, text, 15)
        self.canvas.itemconfig(self.highscore_text, text=text)


    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        global g_high_score
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))

        if num_bricks == 0: 
            self.ball.speed = None
            self.draw_text(300, 200, 'You win!')
            self.display_highscore_after_gameover()

        elif self.ball.get_position()[3] >= self.height: 
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'You Lose!!! Game Over!')
                self.display_highscore_after_gameover()
            else:
                self.after(1000, self.setup_game)

        else:
            self.ball.update()
            self.after(50, self.game_loop)


    def display_highscore_after_gameover(self):
        global g_high_score
        if self.score>g_high_score:
            print("updating highscore")
            g_high_score=self.score
            self.draw_text(300, 240, 'New Highscore: '+str(g_high_score)+'!',size='20')
            login.upd(g_high_score,username)


    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self.ball.collide(objects)


def opengame(U,H):
    global g_high_score, username
    # Load user data here
    g_high_score=int(H)
    username=U
    # Create interface object
    root = tk.Tk()
    root.title('Hello,'+ username + "!")
    # Load game assets -- line 113
    game = Game(root)
    # Run game
    game.mainloop()

opengame("mihir",'140')
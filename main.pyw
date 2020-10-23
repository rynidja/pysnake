import pyglet
import random
from pyglet.window import key


WIDTH = 400
ROWS = 20

SPEED = 10 # also fps
BLOCK = WIDTH // ROWS


class Snake:
    def __init__(self):
        self.block = BLOCK
        self.speed = SPEED
        self.border = WIDTH
        self.is_alive = True

        self.lenght = 1
        self.body = []

        self.x_dir = 0
        self.y_dir = 0

        self.x = self.border // 2
        self.y = self.border // 2

    def draw(self):
        if self.body:
            for i in self.body:
                pyglet.shapes.Rectangle(i[0], i[1] , self.block, self.block, (255, 0, 0)).draw()
            pyglet.shapes.Circle(self.body[-1][0]+self.block/2, self.body[-1][1]+self.block/2 , 8, color=(0,0,0)).draw()

    def update(self, dt, keys):
        if self.is_alive:
            if keys[key.A] and (not self.x_dir or self.lenght==1):
                self.x_dir = -self.block
                self.y_dir = 0
            elif keys[key.D] and (not self.x_dir or self.lenght==1):
                self.x_dir = self.block
                self.y_dir = 0
            elif keys[key.W] and (not self.y_dir or self.lenght==1):
                self.x_dir = 0
                self.y_dir = self.block
            elif keys[key.S] and (not self.y_dir or self.lenght==1):
                self.x_dir = 0
                self.y_dir = -self.block

            self.x += self.x_dir
            self.y += self.y_dir

            if self.x >= self.border:
                self.x -= self.border + self.block
            elif self.y >= self.border:
                self.y -= self.border + self.block
            elif self.x < 0:
                self.x += self.border
            elif self.y < 0:
                self.y += self.border

            snake_head =[self.x, self.y]

            self.body.append(snake_head)
            del self.body[:len(self.body)-self.lenght]

            if snake_head in self.body[:-1]:
                self.is_alive = False


class Food:
    def __init__(self):
        self.block = BLOCK
        self.rows = ROWS

        self.gen()

    def draw(self):
        pyglet.shapes.Rectangle(self.x, self.y, self.block, self.block, (0, 255, 0)).draw()

    def gen(self):
        self.x = random.randrange(self.rows) * self.block
        self.y = random.randrange(self.rows) * self.block


class Grid:
    def __init__(self):
        self.rows = ROWS
        self.wind = WIDTH

        self.Space = BLOCK

    def draw(self):
        x, y = 0,0
        for i in range(self.rows):
            x += self.Space
            y += self.Space
            
            pyglet.shapes.Line(x, 0, x, self.wind, width=1, color=(255, 255, 255)).draw()
            pyglet.shapes.Line(0, y, self.wind, y, width=1, color=(255, 255, 255)).draw()

            


class Window(pyglet.window.Window):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.grid = Grid()
        self.snake = Snake()
        self.food = Food()

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        pyglet.clock.schedule_interval(self.update, 1/self.snake.speed)

    def update(self, dt):
        if self.snake.is_alive:
            self.snake.update(dt, self.keys)
        if [self.food.x, self.food.y] == self.snake.body[-1]:
            self.snake.lenght += 1
            self.food.gen()

    def on_draw(self):
        self.clear()
        if self.snake.is_alive:
            self.food.draw()
            self.snake.draw()
            self.grid.draw()
        else:
            pyglet.text.Label(f'Your Score : {self.snake.lenght-1}',
                          font_size=36,
                          x=self.width-(self.width-40), y=self.width-40).draw()

            pyglet.text.Label(f'-Press "R" to restart-',
                          font_size=24,
                          x=38, y=38).draw()

    def on_key_press(self, Key, mod):
        if not self.snake.is_alive:
            if Key == key.R:
                del self.snake
                self.snake = Snake()


if __name__ == "__main__":
    win = Window(caption="PySnake", width=WIDTH, height=WIDTH)
    pyglet.app.run()

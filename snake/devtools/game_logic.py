import random

class GameLogic:
    def __init__(self):
        # Initialize game state
        self.game_speed = 200
        self.board_size = 11

        self.setup_game()

    def setup_game(self):
        self.game_score = 0
        self.snake_alive = True
        
        # Snake start position
        snake_start_length = 3
        x_start = self.board_size // 2
        self.snakeX = [x_start]*snake_start_length  # Snake x-coords
        self.snakeY = [-1]*snake_start_length       # Snake y-coords

        # Snake start direction
        self.direction = 'Down'         # Start direction
        self.vertical_direction = 1      # Start going down
        self.horisontal_direction = 0    # Not moving horisontally

        # Get fruit position
        self.fruitX = random.randint(0, self.board_size-1)
        self.fruitY = random.randint(0, self.board_size-1)

    def get_snake_coords(self):
        return self.snakeX, self.snakeY
    
    def get_fruit_coords(self):
        return self.fruitX, self.fruitY
    
    def set_new_direction(self, new_direction: str):
        self.direction = new_direction

        match new_direction:
            case 'Up':
                if self.direction != 'Down':
                    self.direction = new_direction
            case 'Down':
                if self.direction != 'Up':
                    self.direction = new_direction
            case 'Right':
                if self.direction != 'Left':
                    self.direction = new_direction
            case 'Left':
                if self.direction != 'Right':
                    self.direction = new_direction

    
    def move_snake(self):
        # get new direction and head location
        self._update_directions()
        newY = self.snakeY[0] + self.vertical_direction
        newX = self.snakeX[0] + self.horisontal_direction

        # Check if new position is valid
        validPosition = self._check_valid_position(newY, newX)
        self.snake_alive = validPosition

        # Check if eaten fruit
        ateFruit = self._check_fruit(newY, newX)

        # Add new head and remove old tail if it did not eat a fruit
        if validPosition:
            self.snakeY.insert(0, newY)
            self.snakeX.insert(0, newX)

            # self.board[self.snakeY[0]][self.snakeX[0]].configure(background=self.snake_color)
            if not ateFruit:
                # Remove tail of snake if valid position
                # self.board[self.snakeY[-1]][self.snakeX[-1]].configure(background=self.bg_color)
                oldY = self.snakeY.pop()
                oldX = self.snakeX.pop()

            # Move again
            self.parent.after(self.game_speed, self._move_snake)
        else:
            self._game_lost()


    def is_alive(self):
        return self.snake_alive


    def _move_snake(self):
        # get new direction and head location
        self._update_directions()
        newY = self.snakeY[0] + self.vertical_direction
        newX = self.snakeX[0] + self.horisontal_direction

        # Check if new position is valid
        validPosition = self._check_valid_position(newY, newX)

        # Check if eaten fruit
        self.ateFruit = self._check_fruit(newY, newX)

        # Draw new head and add to list
        if validPosition:
            self.snakeY.insert(0, newY)
            self.snakeX.insert(0, newX)

            self.board[self.snakeY[0]][self.snakeX[0]].configure(background=self.snake_color)
            if not ateFruit:
                # Remove tail of snake if valid position
                self.board[self.snakeY[-1]][self.snakeX[-1]].configure(background=self.bg_color)
                self.snakeY.pop()
                self.snakeX.pop()

            # Move again
            self.parent.after(self.game_speed, self._move_snake)
        else:
            self._game_lost()

    def remove_tail(self):
        return not self.ateFruit


    def _update_directions(self): # TODO controlls are still a bit slow to update. Should have this check when pressing buttons instead
        """Sets direction of snake. Snake is not allowed to turn 180 degrees and
            if the player tries, nothing will happen.
        """
        match self.direction:
            case 'Up':
                self.vertical_direction = -1
                self.horisontal_direction = 0
            case 'Down': 
                self.vertical_direction = 1
                self.horisontal_direction = 0
            case 'Left':
                self.horisontal_direction = -1
                self.vertical_direction = 0
            case 'Right':
                self.horisontal_direction = 1
                self.vertical_direction = 0

        # match self.direction:
        #     case 'Up':
        #         if self.vertical_direction != 1:
        #             self.vertical_direction = -1
        #             self.horisontal_direction = 0
        #     case 'Down': 
        #         if self.vertical_direction != -1:
        #             self.vertical_direction = 1
        #             self.horisontal_direction = 0
        #     case 'Left':
        #         if self.horisontal_direction != 1:
        #             self.horisontal_direction = -1
        #             self.vertical_direction = 0
        #     case 'Right':
        #         if self.horisontal_direction != -1:
        #             self.horisontal_direction = 1
        #             self.vertical_direction = 0

    def _check_valid_position(self, newY, newX):
        # Snake is not allowed outside of game board
        if newY >= self.board_size or newX >= self.board_size or newY < 0 or newX < 0:
            return False
        
        # Snake is not allowed to overlap with itself
        for i in range(len(self.snakeX)):
            if newX == self.snakeX[i] and newY == self.snakeY[i]:
                return False
        return True

    def _check_fruit(self, newY, newX):
        if newY == self.fruitY and newX == self.fruitX:
            self.game_score += 1

            # New Fruit is not allowed to be created inside the snake
            make_fruit = True
            while make_fruit:
                self.fruitX = random.randint(0, self.board_size-1)
                self.fruitY = random.randint(0, self.board_size-1)
                make_fruit = False
                for i in range(len(self.snakeX)):
                    if self.fruitX == self.snakeX[i] and self.fruitY == self.snakeY[i]:
                        make_fruit = True
            # self.board[self.fruitY][self.fruitX].configure(background=self.fruit_color)
            return True
        return False

    # TODO osäker på exakt vad jag har kvar men:
    # Fixa en main script som kör game logic och gui 
    # Fixa funktionerna med TODO i game_gui
    # Det kanske är allt
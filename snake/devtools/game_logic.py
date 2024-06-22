import random
import json

class GameLogic:
    def __init__(self):
        # Initialize game state
        self.game_speed = self._get_speed_settings()
        self.board_size = 11

        self.setup_game()

    def setup_game(self):
        self.game_score = 0
        self.snake_alive = True
        self.ate_fruit = False
        
        # Snake start position
        snake_start_length = 3
        x_start = self.board_size // 2
        self.snakeX = [x_start]*snake_start_length  # Snake x-coords
        self.snakeY = [-1]*snake_start_length       # Snake y-coords

        # Snake start direction
        self.direction = 'Down'          # Start direction
        self.vertical_direction = 1      # Start going down
        self.horisontal_direction = 0    # Not moving horisontally

        # Get fruit position
        self.fruitX = random.randint(0, self.board_size-1)
        self.fruitY = random.randint(0, self.board_size-1)

    def _get_speed_settings(self): # TODO get settings from functions from a separate file
            with open('../settings/settings.json', 'r') as file:
                data = json.load(file)
                return data['speed']

    def get_snake_coords(self):
        return self.snakeX, self.snakeY
    
    def get_fruit_coords(self):
        return self.fruitX, self.fruitY
    
    def set_new_direction(self, new_direction: str):

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
        self.ate_fruit = self._check_fruit(newY, newX)

        # Add new head and remove old tail if it did not eat a fruit
        if validPosition:
            self.snakeY.insert(0, newY)
            self.snakeX.insert(0, newX)

            if not self.ate_fruit:

                # Remove tail of snake if valid position
                self.old_tailY = self.snakeY.pop()
                self.old_tailX = self.snakeX.pop()


    def get_old_tail_coords(self):
        return self.old_tailX, self.old_tailY


    def is_alive(self):
        return self.snake_alive


    def check_ate_fruit(self):
        return self.ate_fruit


    def get_game_score(self):
        return self.game_score


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
            return True
        return False

import arcade 
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

SCREEN_TITLE = "Moving Sprite"


PLAYER_SPEED = 5 
COIN_COUNT = 10
ENEMY_COUNT = 5

class Enemy(arcade.Sprite):
    def  __init__(self, image, scale):
        super().__init__(image, scale)
        self.enemy_change_x = 0
        self.enemy_change_y = 0


class CoinCollector(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_over = False
        self.game_lost = False
        self.score = 0
        self.lives = 5
        self.player = None
        self.coins = None
        self.enemy = None
        self.background = None
        self.change_x = 0
        self.change_y = 0


        self.score_text = arcade.Text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20)
        lives_str = f"Lives: {self.lives}"
        self.lives_text = arcade.Text(
        lives_str,10,  # Temporary x position
        SCREEN_HEIGHT - 30,
        arcade.color.BLACK, 20)

        # Now adjust x to align it to the right
        self.lives_text.x = SCREEN_WIDTH - self.lives_text.content_width - 20
        



        self.coin_sound = arcade.load_sound("coin_sound.mp3")
        self.player = arcade.Sprite("puppy_pic.png", 0.4)
        self.background = arcade.Sprite("background.png", 0.8)


        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()

        
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.background.center_x = SCREEN_WIDTH // 2
        self.background.center_y = SCREEN_HEIGHT // 2 

        self.player_list.append(self.player)
        self.background_list.append(self.background)


        #load the coins
        for _ in range(COIN_COUNT):
            coin = arcade.Sprite("cookie.png", 0.08)
            coin.center_x = random.randint(20, SCREEN_WIDTH - 20)
            coin.center_y = random.randint(20, SCREEN_HEIGHT - 20)
            self.coin_list.append(coin)
        
        #load the cookie monster enemies 
        for _ in range(ENEMY_COUNT):
            enemy = Enemy("cookie_monster.png", 0.3)
            enemy.center_x = random.randint(20, SCREEN_WIDTH - 20)
            enemy.center_y = random.randint(20, SCREEN_HEIGHT - 20)
            enemy.enemy_change_x = random.choice([-2, -1, 1, 2])
            enemy.enemy_change_y = random.choice([-2, -1, 1, 2])
            self.enemy_list.append(enemy)


    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.score_text.draw()
        self.lives_text.draw()
        #arcade.draw_lbwh_rectangle_filled(self.rect_left, self.rect_bottom, RECT_WIDTH, RECT_HEIGHT, arcade.color.PINK)
         
        if self.game_over:
            arcade.draw_text("You win!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.RED, 50, anchor_x="center")
        elif self.game_lost:
            arcade.draw_text("You lose!", SCREEN_WIDTH//2, SCREEN_HEIGHT//2, arcade.color.RED, 50, anchor_x="center")
    def on_update(self, delta_time): #put things that change the square
        if self.game_over or self.game_lost:
            return
        self.score_text.text = f"Score: {self.score}"
        self.lives_text.text = f"Lives: {self.lives}"

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.coin_sound)

        self.player.center_x += self.change_x
        self.player.center_y += self.change_y

        for enemy in self.enemy_list:
            enemy.center_x += enemy.enemy_change_x 
            enemy.center_y += enemy.enemy_change_y

            if enemy.left <= 0 or enemy.right  >= SCREEN_WIDTH:
                enemy.enemy_change_x *= -1
            if enemy.bottom <= 0 or enemy.top >= SCREEN_HEIGHT:
                enemy.enemy_change_y *= -1

             

        enemys_hit = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for enemy in enemys_hit:
           enemy.remove_from_sprite_lists()
           self.lives -= 1

        if self.score >= 10:
            self.game_over = True 
        if self.lives <= 0:
            self.game_lost = True
        #if self.lives == 0:
            #self.game_over = True
            
        #keep the square on the screen
        
        if self.player.left < 0:
            self.player.left = 0 
        if self.player.right > SCREEN_WIDTH:
            self.player.right = SCREEN_WIDTH 
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.top > SCREEN_HEIGHT:
            self.player.top = SCREEN_HEIGHT 

    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.change_x = PLAYER_SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -PLAYER_SPEED
        elif key == arcade.key.UP:
            self.change_y = PLAYER_SPEED
        elif key == arcade.key.DOWN:
            self.change_y = -PLAYER_SPEED
            

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.RIGHT, arcade.key.LEFT):
            self.change_x = 0
        elif key in (arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0 


if __name__ == "__main__":
    game = CoinCollector()
    arcade.run()
    

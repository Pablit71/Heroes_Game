from typing import Dict

from function_unit.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player: BaseUnit
    enemy: BaseUnit
    game: bool = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game = True

    def _check_players_hp(self):
        if self.player.hp > 0 and self.enemy.hp > 0:
            return True

        if self.player.hp <= 0 <= self.enemy.hp:
            self.battle_result = f'{self.player.name} проиграл {self.enemy.name}'

        if self.player.hp >= 0 >= self.enemy.hp:
            self.battle_result = f'{self.player.name} победил {self.enemy.name}'

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = f'Ничья между {self.player.name} и {self.enemy.name}!'

        self._end_game()

        return False

    def _stamina_regeneration(self):
        
        player_stamina_recovery = self.STAMINA_PER_ROUND * self.player.unit_class.stamina
        enemy_stamina_recovery = self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina
        self.player.stamina_points_ += round(player_stamina_recovery, 1)
        self.enemy.stamina_points_ += round(enemy_stamina_recovery, 1)

        # Ensure stamina points don't exceed maximum for the class
        if self.player.stamina_points_ > self.player.unit_class.max_stamina:
            self.player.stamina_points_ = self.player.unit_class.max_stamina
        if self.enemy.stamina_points_ > self.enemy.unit_class.max_stamina:
            self.enemy.stamina_points_ = self.enemy.unit_class.max_stamina

    def next_turn(self):
        if self._check_players_hp():
            self._stamina_regeneration()
            enemy_result = self.enemy.hit(target=self.player)
            self._stamina_regeneration()
            return enemy_result
        return self.battle_result

    def _end_game(self):
        self._instances: Dict = {}
        self.game = False

    def player_hit(self):
        player_result = self.player.hit(target=self.enemy)
        return player_result + " " + self.next_turn()

    def player_use_skill(self):
        player_result = self.player.use_skill(target=self.enemy)
        return player_result + " " + self.next_turn()

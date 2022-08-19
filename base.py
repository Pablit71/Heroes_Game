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
    STAMINA_RECOVERY_PER_TURN: float = 1
    game_on: bool = False
    battle_result: str = ""
    player: BaseUnit
    enemy: BaseUnit

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_on = True

    def player_attack(self) -> str:
        player_result = self.player.attack(target=self.enemy)
        return player_result + " " + self.next_turn()

    def player_use_skill(self) -> str:
        player_result = self.player.use_skill(target=self.enemy)
        return player_result + " " + self.next_turn()

    def next_turn(self) -> str:
        if self._check_health():
            self._regenerate_stamina()
            enemy_result = self.enemy.attack(target=self.player)
            self._regenerate_stamina()
            return enemy_result
        return self.battle_result

    def _regenerate_stamina(self) -> None:
        player_stamina_recovery = self.STAMINA_RECOVERY_PER_TURN * self.player.unit_class.stamina_modifier
        enemy_stamina_recovery = self.STAMINA_RECOVERY_PER_TURN * self.enemy.unit_class.stamina_modifier
        self.player.stamina_points_ += round(player_stamina_recovery, 1)
        self.enemy.stamina_points_ += round(enemy_stamina_recovery, 1)

        if self.player.stamina_points_ > self.player.unit_class.max_stamina:
            self.player.stamina_points_ = self.player.unit_class.max_stamina
        if self.enemy.stamina_points_ > self.enemy.unit_class.max_stamina:
            self.enemy.stamina_points_ = self.enemy.unit_class.max_stamina

    def _check_health(self) -> bool:

        if self.player.health_points_ > 0 and self.enemy.health_points_ > 0:
            return True

        if self.player.health_points_ <= 0 <= self.enemy.health_points_:
            self.battle_result = f'{self.player.name} проиграл {self.enemy.name}'

        if self.player.health_points_ >= 0 >= self.enemy.health_points_:
            self.battle_result = f'{self.player.name} победил {self.enemy.name}'

        if self.player.health_points_ <= 0 and self.enemy.health_points_ <= 0:
            self.battle_result = f'Ничья между {self.player.name} и {self.enemy.name}!'

        self._finish_game()

        return False

    def _finish_game(self) -> None:
        self._instances: Dict = {}
        self.game_on = False

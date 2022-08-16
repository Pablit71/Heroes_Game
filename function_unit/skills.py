from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from marshmallow_dataclass import dataclass

if TYPE_CHECKING:
    from function_unit.unit import BaseUnit


class Skill(ABC):
    user: BaseUnit
    target: BaseUnit
    name: str = ""
    damage: float = 0
    stamina_required: float = 0

    # @property
    # @abstractmethod
    # def name(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def stamina(self):
    #     pass
    #
    # @property
    # @abstractmethod
    # def damage(self):
    #     pass

    @abstractmethod
    def _skill_effect(self):
        pass

    # def _is_stamina_enough(self):
    #     return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit):
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self.user.stamina < self.stamina_required:
            return self._skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill, ABC):
    name: str = 'Свирепый пинок'
    damage: float = 12.0
    stamina_required: float = 6.0

    def _skill_effect(self):
        self.target.hp -= self.damage
        self.user.stamina -= self.stamina_required
        return f'{self.user.name} использует {self.user.unit_class.skill.name} и наносит {self.damage} урона сопернику.'


class HardShot(Skill, ABC):
    name: str = 'Мощный укол'
    damage: float = 15.0
    stamina_required: float = 5.0

    def _skill_effect(self) -> str:
        self.target.hp -= self.damage
        self.user.stamina -= self.stamina_required
        return f'{self.user.name} использует {self.user.unit_class.skill.name} и наносит {self.damage} урона сопернику.'

from __future__ import annotations
from abc import ABC
from random import randint

from equipment import Weapon, Armor
from function_unit.classes import UnitClass


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Weapon
        self.armor = Armor
        self._is_skill_used = False

    @property
    def health_points(self):
        if self.hp < 0:
            return 0
        return self.hp

    @property
    def stamina_points(self):
        return self.stamina

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        return f"{self.name} экипирован броней {self.weapon.name}"

    def hit(self, target: BaseUnit) -> str:
        if self.stamina >= self.weapon.stamina_per_hit:

            damage_inflicted = self._count_damage(target)
            target.get_damage(damage_inflicted)

            self.stamina -= self.weapon.stamina_per_hit
            target.stamina -= target.armor.stamina_per_turn

            if target.stamina < 0:
                target.stamina = 0

            if damage_inflicted > 0:
                return (f"{self.name}, используя {self.weapon.name}, "
                        f"пробивает {target.armor.name} соперника и наносит {damage_inflicted} урона.")
            return (f"{self.name}, используя {self.weapon.name}, "
                    f"наносит удар, но {target.armor.name} соперника его останавливает.")

        return (f"{self.name} попытался использовать {self.weapon.name}, "
                f"но у него не хватило выносливости.")

    def _count_damage(self, target: BaseUnit) -> int:
        damage = self.weapon.count_damage() * self.unit_class.attack
        defence = target.armor.defence if target.stamina >= target.armor.stamina_per_turn else 0
        if damage <= defence:
            damage_inflicted = 0
        else:
            damage_inflicted = damage - defence

        return round(damage_inflicted, 1)

    def get_damage(self, damage_inflicted: int):
        self.hp -= damage_inflicted

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        pass


class PlayerUnit(BaseUnit):
    pass


class EnemyUnit(BaseUnit):

    def __init__(self, name: str, unit_class: UnitClass):
        super().__init__(name, unit_class)
        self.skill_used = None

    def hit(self, target: BaseUnit) -> str:
        if not self.skill_used:
            use_skill = randint(0, 9)
            if use_skill == 0:
                return self.use_skill(target)

        return super().hit(target)

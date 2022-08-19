from abc import ABC
from dataclasses import dataclass

from function_unit.skills import FuryPunch, HardShot, BaseSkill


@dataclass
class UnitClass(ABC):
    name: str
    max_health: float
    max_stamina: float
    attack_modifier: float
    stamina_modifier: float
    armor_modifier: float
    skill: BaseSkill


WarriorClass = UnitClass(name='Воин', max_health=50, max_stamina=30, attack_modifier=0.8,
                         stamina_modifier=0.9, armor_modifier=1.2, skill=FuryPunch())

ThiefClass = UnitClass(name='Воh', max_health=45, max_stamina=25, attack_modifier=1.2,
                       stamina_modifier=1.0, armor_modifier=1.0, skill=HardShot())

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass
}

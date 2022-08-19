import os

from flask import Flask, render_template, request, redirect, url_for

from base import Arena
from config import BaseConfig
from equipment import Equipment
from function_unit.classes import unit_classes
from function_unit.unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)
BASEDIR = os.path.dirname(os.path.realpath(__file__))
equipment = Equipment(BaseConfig.EQUIPMENT_PATH)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'],
                     enemy=heroes['enemy'])

    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_on:
        result = arena.player_attack()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_on:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_on:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    return render_template('fight.html', heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    return render_template("index.html")


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    if request.method == 'GET':
        result = {
            "header": 'Выбор героя для игрока',
            "classes": unit_classes,
            "weapons": equipment.get_weapon_names(),
            "armors": equipment.get_armor_names()
        }
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        user_name = request.form.get('name')
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon = equipment.get_weapon(request.form.get('weapon'))
        armor = equipment.get_armor(request.form.get('armor'))

        # Create hero
        player_unit = PlayerUnit(name=user_name, unit_class=unit_class, weapon=weapon, armor=armor)
        heroes['player'] = player_unit

        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == 'GET':
        result = {
            "header": 'Выбор для ИИ',
            "classes": unit_classes,
            "weapons": equipment.get_weapon_names(),
            "armors": equipment.get_armor_names()
        }
        return render_template('hero_choosing.html', result=result)
    if request.method == 'POST':
        user_name = request.form.get('name')
        unit_class = unit_classes[request.form.get('unit_class')]
        weapon = equipment.get_weapon(request.form.get('weapon'))
        armor = equipment.get_armor(request.form.get('armor'))
        enemy_unit = EnemyUnit(name=user_name, unit_class=unit_class, weapon=weapon, armor=armor)
        heroes['enemy'] = enemy_unit

        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(debug=True)

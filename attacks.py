import random

class Attack:
    def __init__(self, name, speed, damage, accuracy):
        self.name = name
        self.speed = speed
        self.damage = damage
        self.accuracy = accuracy
    
    def use(self, offender, defender):
        str_tot = self.damage + offender.get_stat(5)
        spd_tot = self.speed + offender.get_stat(6)
        acc_tot = self.accuracy + offender.get_stat(7)
        hit_chance = min((acc_tot / defender.get_stat(8)), 1) #TODO: Add temp stat bonus support + armor support
        hit_roll = random.uniform(0.0, 1.0)
        if hit_roll > hit_chance:
            dmg = random.randint(0, str_tot)
            defender.change_stat(3, -dmg)

    def get_speed(self, offender):
        return self.speed + offender.get_stat(6)

class SpecialAttack(Attack):
    def __init__(self, name, speed, damage, accuracy, uses):
        super().__init__(name, speed, damage, accuracy)
        self.uses = uses
    
    def use(self):
        self.uses -= 1

quick_attack1   = Attack("Punch", 10, 1, 1)
power_attack1   = Attack("Kick", -10, 2, 1)
special_attack1 = SpecialAttack("Dropkick", -20, 10, 0.5, 2)
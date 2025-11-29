import json
import os
import hashlib
import time
import random
from .cortex import NeuroCortex

class Holon:
    def __init__(self, sender, receiver, amount, parents):
        self.timestamp = time.time()
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.parents = parents
        # إحداثيات ثلاثية الأبعاد
        self.coordinates = {"x": random.random()*100, "y": random.random()*100, "z": random.random()*100}
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        payload = f"{self.sender}{self.receiver}{self.amount}{self.parents}{self.coordinates}"
        return hashlib.blake2b(payload.encode()).hexdigest()
    
    def to_dict(self): return self.__dict__

class HolographicFabric:
    def __init__(self, port=5000):
        # كل عقدة لها ملف نسيج خاص
        self.filename = f"fabric_data_{port}.json"
        self.cortex = NeuroCortex()
        self.holons = {}
        self.balances = {}
        self.tips = [] 
        self.load_fabric()

    def load_fabric(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.holons = data.get("holons", {})
                self.balances = data.get("balances", {})
                self.tips = data.get("tips", [])
        else:
            self.save_fabric()

    def save_fabric(self):
        data = {"holons": self.holons, "balances": self.balances, "tips": self.tips}
        with open(self.filename, "w") as f: json.dump(data, f, indent=4)

    def get_balance(self, address):
        return self.balances.get(address, 0.0)

    def transfer_funds(self, sender, receiver, amount):
        valid, msg = self.cortex.analyze_intent(sender, amount)
        if not valid: return False, msg

        if self.get_balance(sender) < amount: return False, "رصيد غير كافٍ"

        parents = random.sample(self.tips, min(2, len(self.tips))) if self.tips else ["GENESIS"]
        new_holon = Holon(sender, receiver, amount, parents)
        
        self.holons[new_holon.hash] = new_holon.to_dict()
        self.balances[sender] -= amount
        self.balances[receiver] = self.balances.get(receiver, 0.0) + amount
        
        self.tips.append(new_holon.hash)
        if len(self.tips) > 10: self.tips = self.tips[-10:] 
        
        self.save_fabric()
        return True, "تمت الحياكة بنجاح"

    def deduct_funds(self, address, amount):
        if self.get_balance(address) >= amount:
            self.balances[address] -= amount
            self.save_fabric()
            return True
        return False

    def add_mining_reward(self, miner, amount):
        self.balances[miner] = self.balances.get(miner, 0.0) + amount
        self.save_fabric()
        return amount
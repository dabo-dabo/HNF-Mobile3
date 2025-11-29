import time

class NeuroCortex:
    def __init__(self):
        self.behavior_memory = {} 

    def analyze_intent(self, sender, amount):
        current_time = time.time()
        # حماية ضد الروبوتات (Spam)
        if sender in self.behavior_memory:
            last_tx_time = self.behavior_memory[sender]
            if current_time - last_tx_time < 0.5:
                return False, "⚠️ تم الرفض: تردد عالي (سلوك روبوت)"
        
        if amount <= 0: return False, "❌ المبلغ يجب أن يكون موجباً"
        
        self.behavior_memory[sender] = current_time
        return True, "COHERENT"
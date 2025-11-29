import psutil
import multiprocessing

class DeviceScanner:
    def __init__(self):
        self.device_score = 0
        self.specs = {}

    def scan_device(self):
        cpu_count = multiprocessing.cpu_count()
        try:
            ram_gb = round(psutil.virtual_memory().total / (1024.0 ** 3), 2)
        except: ram_gb = 4.0
        
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else 100
        
        self.specs = {"cores": cpu_count, "ram": ram_gb, "battery": battery_percent}
        
        score = (cpu_count * 10) + (ram_gb * 5)
        if battery_percent < 20: score *= 0.5
        self.device_score = round(score, 2)

    def get_reward_multiplier(self):
        base = self.device_score / 80.0
        return max(0.5, min(base, 3.0))
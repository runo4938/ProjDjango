import math
import matplotlib.pyplot as plt

class ClockMarks:
    def __init__(self, radius=100, mark_length=12):
        self.R = radius
        self.MARK_LENGTH = mark_length
        self.PI = math.pi
    
    def get_minute_mark(self, minute):
        """Получить координаты минутного деления по его номеру (0-59)"""
        # Угол для данного деления (в радианах)
        # 0 минут = 12 часов = -90 градусов
        angle = (minute * 6.0 - 90.0) * self.PI / 180.0
        
        # Координаты начала деления (ближе к центру)
        inner_radius = self.R - self.MARK_LENGTH
        x1 = inner_radius * math.cos(angle)
        y1 = inner_radius * math.sin(angle)
        
        # Координаты конца деления (на внешнем круге)
        x2 = self.R * math.cos(angle)
        y2 = self.R * math.sin(angle)
        
        return (x1, y1, x2, y2)
    
    def get_all_minute_marks(self):
        """Получить все 60 минутных делений"""
        marks = []
        for minute in range(60):
            marks.append(self.get_minute_mark(minute))
        return marks
    
    def print_marks(self):
        """Вывести координаты всех делений"""
        marks = self.get_all_minute_marks()
        print("Minute marks coordinates (center at 0,0):")
        print("=" * 60)
        
        for i, (x1, y1, x2, y2) in enumerate(marks):
            print(f"Minute {i:2d}: ({x1:7.2f}, {y1:7.2f}) -> ({x2:7.2f}, {y2:7.2f})")
        
        # Примеры для ключевых позиций
        print("\nKey positions:")
        key_minutes = [0, 15, 30, 45]
        for minute in key_minutes:
            x1, y1, x2, y2 = marks[minute]
            print(f"Minute {minute:2d}: ({x1:7.2f}, {y1:7.2f}) -> ({x2:7.2f}, {y2:7.2f})")

# Использование
if __name__ == "__main__":
    clock = ClockMarks()
    clock.print_marks()
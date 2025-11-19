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


def visualize_clock_marks():
    """Визуализировать минутные деления на графике"""
    clock = ClockMarks()
    marks = clock.get_all_minute_marks()
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Рисуем минутные деления
    for i, (x1, y1, x2, y2) in enumerate(marks):
        # Более длинные деления для каждых 5 минут
        if i % 5 == 0:
            ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2.5, label='5-minute marks' if i == 0 else "")
            # Добавляем цифры для часов
            hour = i // 5 if i > 0 else 12
            text_radius = clock.R - 20
            text_angle = (i * 6.0 - 90.0) * math.pi / 180.0
            text_x = text_radius * math.cos(text_angle)
            text_y = text_radius * math.sin(text_angle)
            ax.text(text_x, text_y, str(hour), fontsize=12, ha='center', va='center')
        else:
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1, label='minute marks' if i == 1 else "")
    
    # Рисуем окружность циферблата
    circle = plt.Circle((0, 0), clock.R, fill=False, linewidth=2)
    ax.add_artist(circle)
    
    # Настройки графика
    ax.set_aspect('equal')
    ax.set_xlim(-clock.R - 10, clock.R + 10)
    ax.set_ylim(-clock.R - 10, clock.R + 10)
    ax.set_title('Clock Minute Marks (Center at 0,0)')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.show()

# Запуск визуализации




# Использование
if __name__ == "__main__":
    clock = ClockMarks()
    clock.print_marks()
    visualize_clock_marks()
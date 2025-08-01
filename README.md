# Игра "Змейка" 🐍

## Особенности игры

🎮 **Классическая змейка с новыми возможностями:**
- Обычные красные яблоки (+1 к длине)
- **Золотые яблоки** (+3 к длине, появляются на 6 секунд)
- Таймер игры и счетчик яблок
- Победа при заполнении всего поля

## 🚀 Как запустить
1. Клонируйте репозиторий 
```bash
git clone git@github.com:Serieznee-nekuda17/my_snake.git
```

2. Создайте виртуальное окружение
```bash
python -m venv venv
```

3. Активируйте виртуальное окружение
```bash
source venv/Script/activate
```

4. Установите зависимость
```bash
pip install -r requirements.txt
```

5. Запустите игру
```bash
python the_snake.py
```


## 🕹 Управление
- Стрелки ← ↑ → ↓ - движение змейки

- R - рестарт после проигрыша/победы

- ESC или закрытие окна - выход из игры

## 🍎 Особенности золотых яблок
- Появляются случайно (∼каждые 15 сек с 10% шансом)

- Мерцают перед исчезновением (последние 2 секунды)

- Дают +3 к длине змейки

- Отображается таймер до исчезновения

## 🏆 Условия победы и проигрыша
✅ Победа: заполнить всё поле змейкой

❌ Проигрыш: столкновение с собой

После окончания игры показывается:

- Количество собранных яблок

- Затраченное время

- Возможность рестарта (клавиша R)

### 🛠 Технические детали
- Размер поля: 32×24 клетки (640×480 пикселей)

- Скорость игры: 20 FPS

- Цветовая схема:

    Змейка: зеленый

    Обычные яблоки: красные

    Золотые яблоки: желтые
    
    Фон: черный



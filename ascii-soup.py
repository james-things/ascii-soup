import curses
from curses import wrapper
import time
import random
import string

class TextString:
    def __init__(self, text, x, y, speed, z_index, side, color_pair):
        self.text = text
        self.x = x
        self.y = y
        self.speed = speed
        self.z_index = z_index
        self.side = side
        self.color_pair = color_pair
        self.timer = 0

def load_words():
    with open('words.txt', 'r') as f:
        words = [word.strip() for word in f.readlines()]
    return words

english_words = load_words()

def generate_random_text(length):
    same_length_words = [word for word in english_words if len(word) == length]
    return random.choice(same_length_words)

def generate_text_strings(num_strings, max_y, color_pairs):
    text_strings = []
    for _ in range(num_strings):
        side = random.choice(['left', 'right'])
        y = random.randint(0, max_y - 1)
        length = random.randint(1, 10)
        speed = random.uniform(0.001, 0.5)
        z_index = random.randint(1, 5)
        text = generate_random_text(length)
        x = 0 if side == 'left' else curses.COLS - length
        color_pair = random.choice(color_pairs)
        text_strings.append(TextString(text, x, y, speed, z_index, side, color_pair))
    return text_strings

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(5)
    
    # Initialize color pairs
    curses.start_color()
    color_pairs = []
    for i in range(1, 8):
        curses.init_pair(i, i, 0)  # Foreground color i, background color black
        color_pairs.append(i)

    text_strings = []
    max_y, max_x = stdscr.getmaxyx()
    prev_time = time.time()

    while True:
        text_strings.extend(generate_text_strings(5, max_y, color_pairs))

        for ts in text_strings:
            ts.timer += time.time() - prev_time
            if ts.timer >= ts.speed:
                if (ts.side == 'left' and ts.x + len(ts.text) < max_x) or (ts.side == 'right' and ts.x > 0):
                    ts.x += 1 if ts.side == 'left' else -1
                else:
                    text_strings.remove(ts)
                ts.timer = 0

        prev_time = time.time()

        stdscr.clear()

        sorted_text_strings = sorted(text_strings, key=lambda x: x.z_index)

        for ts in sorted_text_strings:
            max_chars = max_x - ts.x - 1
            if max_chars > 0:
                truncated_text = ts.text[:max_chars]
                stdscr.addstr(ts.y, ts.x, truncated_text, curses.color_pair(ts.color_pair))

        stdscr.refresh()
        time.sleep(0.025)

if __name__ == "__main__":
    curses.wrapper(main)

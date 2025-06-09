import random
import threading
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_correct_input(user_input, answer):
    return user_input == answer[:len(user_input)]


def countdown_and_display(user_input, answer, start_time, stop_event):
    while not stop_event.is_set():
        now = time.time()
        time_elapsed = now - start_time
        time_left = max(0, 10 - time_elapsed)
        clear_screen()
        print(f"⏳ Time Left: {time_left:.1f} seconds")  # 顯示到小數點一位
        print(f"📝 Your Input: {' '.join(map(str, user_input))}")
        print(f"⏰ 系統還有 {(time_left - int(time_left)):.1f} 秒鐘就會讀取您的輸入")  # 固定間隔顯示
        if time_left <= 0:
            stop_event.set()
        time.sleep(0.1)  # 更頻繁更新畫面

def show_question_with_countdown(answer, seconds=3):
    for i in range(seconds, 0, -1):
        clear_screen()
        print("🧠 記住這 5 個數字（順序很重要）:")
        print(' '.join(map(str, answer)))
        print(f"📢 還有 {i} 秒後開始作答...")
        time.sleep(1)

def memory_game():
    answer = [random.randint(1, 5) for _ in range(5)]

    # 顯示題目與倒數
    show_question_with_countdown(answer, seconds=3)

    clear_screen()
    print("✅ 開始作答！請輸入數字順序（1~5）")

    user_input = []
    start_time = time.time()
    stop_event = threading.Event()
    input_interval = 1  # 每秒讀取一次輸入

    # 啟動背景倒數與輪詢顯示
    timer_thread = threading.Thread(target=countdown_and_display, args=(user_input, answer, start_time, stop_event))
    timer_thread.start()

    while not stop_event.is_set():
        try:
            entry = input("👉 請輸入下一個數字（1~5）: ").strip()
            if not entry.isdigit() or not (1 <= int(entry) <= 5):
                print("⚠️ 請輸入 1~5 的整數")
                continue
            user_input.append(int(entry))

            if not is_correct_input(user_input, answer):
                print("❌ 輸入錯誤，請重新輸入！")
                user_input.clear()

            elif len(user_input) == len(answer):
                stop_event.set()
                clear_screen()
                print("🎉 恭喜你答對了！")
                break

        except EOFError:
            break

    if user_input != answer:
        print("⌛ 時間到！你輸錯了或來不及完成。")
        print(f"✅ 正確答案是：{' '.join(map(str, answer))}")

    timer_thread.join()

if __name__ == "__main__":
    memory_game()

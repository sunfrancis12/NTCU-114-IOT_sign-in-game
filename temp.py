# main.py
import cv2
import time
from memory_game import MemoryGame

game = MemoryGame()
game.start()

cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    if not ret:
        break

    game.update()

    if game.status == 'showing':
        cv2.putText(frame, "remember this five number:", (50, 50), font, 0.9, (0, 255, 255), 2)
        cv2.putText(frame, ' '.join(map(str, game.answer)), (50, 100), font, 1.2, (0, 255, 0), 3)
        sec = 3 - int(time.time() - game.display_start)
        cv2.putText(frame, f"You still have {sec} second to remember...", (50, 150), font, 0.8, (255, 0, 0), 2)

    elif game.status == 'playing':
        cv2.putText(frame, f"Time left: {game.time_left():.1f}s", (50, 50), font, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, f"Your input: {' '.join(map(str, game.user_input))}", (50, 100), font, 0.9, (255, 255, 0), 2)
        cv2.putText(frame, f"Next input comes in:{(game.time_left() - int(game.time_left())):.1f}", (50, 150), font, 0.9, (200, 200, 255), 2)
        if abs(game.time_left() - int(game.time_left())) <= 0.1:
            game.read_input = True

    elif game.status == 'win':
        cv2.putText(frame, "You win", (100, 100), font, 1.0, (0, 255, 0), 3)

    elif game.status == 'fail':
        cv2.putText(frame, "You lose", (50, 100), font, 1.0, (0, 0, 255), 3)
        cv2.putText(frame, f"Answer: {' '.join(map(str, game.answer))}", (50, 150), font, 0.8, (0, 255, 255), 2)

    cv2.imshow("Memory Game", frame)

    key = cv2.waitKey(30) & 0xFF
    if key == ord('q'):
        break
    elif game.status == 'playing' and game.read_input:
        if ord('1') <= key <= ord('5'):
            game.handle_input(key - ord('0'))
    
    game.read_input = False
    
    # if game.status in ['win', 'fail']:
    #     cv2.waitKey(3000)
    #     break

cap.release()
cv2.destroyAllWindows()

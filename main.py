import threading
from agent.agent import chat_loop, run_display
import agent.events as events

if __name__ == "__main__":
    events.start_event_loop(interval_seconds=20)
    
    chat_thread = threading.Thread(target=chat_loop, daemon=True)
    chat_thread.start()

    run_display()
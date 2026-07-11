import time
import threading
from datetime import timedelta

class Timer:
    """A versatile Python timer class with countdown, stopwatch, and alert features."""
    
    def __init__(self):
        self.is_running = False
        self.is_paused = False
        self.elapsed_time = 0
        self.start_time = None
        self.paused_time = 0
        self.thread = None
    
    def start_countdown(self, seconds):
        """Start a countdown timer for the specified number of seconds."""
        if self.is_running:
            print("Timer is already running!")
            return
        
        print(f"Starting countdown: {self._format_time(seconds)}")
        self.is_running = True
        self.elapsed_time = seconds
        
        self.thread = threading.Thread(target=self._countdown_loop, args=(seconds,), daemon=True)
        self.thread.start()
    
    def start_stopwatch(self):
        """Start a stopwatch that counts up from 0."""
        if self.is_running:
            print("Timer is already running!")
            return
        
        print("Stopwatch started!")
        self.is_running = True
        self.start_time = time.time()
        self.paused_time = 0
        
        self.thread = threading.Thread(target=self._stopwatch_loop, daemon=True)
        self.thread.start()
    
    def pause(self):
        """Pause the running timer."""
        if not self.is_running or self.is_paused:
            print("Timer is not running or already paused!")
            return
        
        self.is_paused = True
        self.paused_time = time.time()
        print(f"Timer paused at {self._format_time(self.elapsed_time)}")
    
    def resume(self):
        """Resume a paused timer."""
        if not self.is_paused:
            print("Timer is not paused!")
            return
        
        self.is_paused = False
        pause_duration = time.time() - self.paused_time
        self.start_time += pause_duration
        print(f"Timer resumed!")
    
    def stop(self):
        """Stop the timer and display final time."""
        if not self.is_running:
            print("Timer is not running!")
            return
        
        self.is_running = False
        self.is_paused = False
        print(f"Timer stopped. Final time: {self._format_time(self.elapsed_time)}")
    
    def _countdown_loop(self, seconds):
        """Internal loop for countdown timer."""
        for remaining in range(seconds, -1, -1):
            if not self.is_running:
                break
            
            while self.is_paused:
                time.sleep(0.1)
            
            self.elapsed_time = remaining
            self._display_time(remaining, is_countdown=True)
            time.sleep(1)
        
        if self.is_running:
            self.is_running = False
            self._alert("⏰ Time's up!")
    
    def _stopwatch_loop(self):
        """Internal loop for stopwatch timer."""
        while self.is_running:
            if not self.is_paused:
                elapsed = time.time() - self.start_time
                self.elapsed_time = int(elapsed)
                self._display_time(self.elapsed_time, is_countdown=False)
            time.sleep(1)
    
    def _display_time(self, seconds, is_countdown=True):
        """Display the timer on screen."""
        formatted = self._format_time(seconds)
        timer_type = "⏱️  Countdown" if is_countdown else "⏲️  Stopwatch"
        print(f"\r{timer_type}: {formatted}    ", end="", flush=True)
    
    @staticmethod
    def _format_time(seconds):
        """Format seconds into HH:MM:SS format."""
        return str(timedelta(seconds=int(seconds)))
    
    @staticmethod
    def _alert(message):
        """Alert the user when timer ends."""
        print(f"\n{message}")
        print("\a" * 3)  # Bell sound


# Example usage
if __name__ == "__main__":
    timer = Timer()
    
    print("=== Python Timer Demo ===\n")
    
    # Example 1: Countdown timer
    print("1. Starting 5-second countdown...")
    timer.start_countdown(5)
    time.sleep(6)  # Wait for countdown to finish
    
    print("\n" + "="*40 + "\n")
    
    # Example 2: Stopwatch
    print("2. Starting stopwatch for 5 seconds...")
    timer.start_stopwatch()
    time.sleep(3)
    
    print("\n   Pausing stopwatch...")
    timer.pause()
    time.sleep(2)
    
    print("\n   Resuming stopwatch...")
    timer.resume()
    time.sleep(2)
    
    timer.stop()
    
    print("\n" + "="*40)
    print("✅ Timer demo complete!")

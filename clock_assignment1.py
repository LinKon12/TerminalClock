import time
import threading
from datetime import datetime, timedelta
import sys

# Global time format (12 or 24 hour)
time_format = 24

def clock_mode():
    import sys
    
    global running
    running = True

    def wait_for_quit():
        input()  # No prompt inside thread
        global running
        running = False

    print("Clock Mode started. Press Enter to quit...\n")
    threading.Thread(target=wait_for_quit, daemon=True).start()

    while running:
        now = datetime.now()
        if time_format == 12:
            sys.stdout.write("\r" + now.strftime("%I:%M:%S %p"))
        else:
            sys.stdout.write("\r" + now.strftime("%H:%M:%S"))
        sys.stdout.flush()
        time.sleep(1)

    print()


def alarm_mode():
    global time_format

    if time_format == 12:
        alarm_input = input("Set alarm time (hh:mm AM/PM): ")
        alarm_time = datetime.strptime(alarm_input, "%I:%M %p").time()
    else:
        alarm_input = input("Set alarm time (HH:MM): ")
        alarm_time = datetime.strptime(alarm_input, "%H:%M").time()

    formatted_alarm = alarm_time.strftime('%I:%M %p' if time_format == 12 else '%H:%M')
    print(f"\nAlarm set for {formatted_alarm}. Waiting...")

    def cancel_alarm():
        input("\nPress Enter to cancel the alarm...\n")
        global alarm_running
        alarm_running = False

    global alarm_running
    alarm_running = True
    threading.Thread(target=cancel_alarm).start()

    while alarm_running:
        now = datetime.now().time()
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            print("\n Alarm ringing!")
            break
        time.sleep(1)

    alarm_running = False


def countdown_mode():
    target_input = input("Enter target time (HH:MM): ")
    now = datetime.now()
    target = datetime.strptime(target_input, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )

    if target < now:
        target += timedelta(days=1)

    while True:
        remaining = target - datetime.now()
        seconds = int(remaining.total_seconds())

        if seconds <= 0:
            print("\nCountdown finished!")
            break

        print(f"Time left: {seconds} seconds", end="\r")
        time.sleep(1)


def settings_mode():
    global time_format
    print("\nChoose time format:")
    print("1. 12-hour")
    print("2. 24-hour")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        time_format = 12
        print("Time format set to 12-hour.")
    elif choice == "2":
        time_format = 24
        print("Time format set to 24-hour.")
    else:
        print("Invalid choice. Format unchanged.")


def menu():
    while True:
        print("\n=== Digital Clock Menu ===")
        print("1. Clock Mode")
        print("2. Alarm Mode")
        print("3. Countdown Mode")
        print("4. Settings (12/24 hour format)")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            clock_mode()
        elif choice == "2":
            alarm_mode()
        elif choice == "3":
            countdown_mode()
        elif choice == "4":
            settings_mode()
        elif choice == "5":
            print("Exiting..")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()

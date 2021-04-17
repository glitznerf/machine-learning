# We assume that sleep goes in regular cycles. Therefore, we aim to wake up as
# close to the end of a sleep cycle as possible.

import datetime

# Define your average sleep cycle. Can be measured by sleep tracker apps.
cycle_time = 1.5                                                    # in hours

# Use user input to define latest wake up time
latest_wake_up_time = float(input("Latest wake up time (in h): "))  # in hours

# Calculate current time metrics
time = datetime.datetime.now()                                      # as object
current_time = time.hour + time.minute/60                           # in hours
sleep_time = latest_wake_up_time - cycle_time

# Print possible wake up times with respect to sleep cycle times
while current_time < sleep_time:
    sleep_time_hours = int(sleep_time)
    sleep_time_minutes = int((sleep_time - sleep_time_hours)*60)
    sleep = latest_wake_up_time - sleep_time
    if sleep_time_minutes < 10:
        sleep_time_minutes = str(sleep_time_minutes)+"0"
    print(f"\nYou could go to sleep at {sleep_time_hours}:{sleep_time_minutes}.")
    print(f"\tYou will get {sleep:.2f} hours of sleep")
    sleep_time -= cycle_time

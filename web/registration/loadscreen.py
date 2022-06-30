import sys
import time
print("please wait", end ="")
loading = True
loading_speed = 4
loading_string = "." * 6
while loading:
    for index, char in enumerate(loading_string):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(1.0 / loading_speed)
    index += 1
    sys.stdout.write("\b" * index + " " * index + "\b" * index)
    sys.stdout.flush()
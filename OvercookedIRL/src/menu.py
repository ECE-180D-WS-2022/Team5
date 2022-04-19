from threading import Thread
import subprocess

t1 = Thread(target=subprocess.run, args=(["python", "pub.py"],))
t2 = Thread(target=subprocess.run, args=(["python", "color.py"],))
t3 = Thread(target=subprocess.run, args=(["python", "main.py"],))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
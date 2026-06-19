import os

logs_dir = r"C:\Users\junxi\.gemini\antigravity-ide\brain\45fa12e0-5442-4e8b-99bc-427d93665aaf\.system_generated\logs"
if os.path.exists(logs_dir):
    print("Logs dir files:")
    for file in os.listdir(logs_dir):
        print(file)
else:
    print("Logs dir does not exist")

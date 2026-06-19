import os

log_dir = r"C:\Users\junxi\.gemini\antigravity-ide\brain\57f46918-4819-485d-a3dd-5d807b5ebcf7\.system_generated\tasks"
# Find the latest log file starting with task-1210
log_file = None
for f in os.listdir(log_dir):
    if f.startswith("task-1210"):
        log_file = os.path.join(log_dir, f)
        break

if log_file:
    print(f"Reading log file: {log_file}")
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    print("Content:")
    # print first 1000 and last 1000 chars
    if len(content) > 2000:
        print(content[:1000])
        print("\n... [TRUNCATED] ...\n")
        print(content[-1000:])
    else:
        print(content)
else:
    print("Log file not found.")

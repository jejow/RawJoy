import os

log_dir = r"C:\Users\junxi\.gemini\antigravity-ide\brain\57f46918-4819-485d-a3dd-5d807b5ebcf7\.system_generated\tasks"
log_file = None
for f in os.listdir(log_dir):
    if f.startswith("task-1210"):
        log_file = os.path.join(log_dir, f)
        break

if log_file:
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    idx = content.find("Checkout Page Text:")
    if idx != -1:
        print(content[idx:idx+800])
    else:
        print("Checkout Page Text not found in log.")
else:
    print("Log file not found.")

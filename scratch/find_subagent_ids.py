import json

transcript_path = r"C:\Users\junxi\.gemini\antigravity-ide\brain\45fa12e0-5442-4e8b-99bc-427d93665aaf\.system_generated\logs\transcript.jsonl"

print("Searching for subagent conversation IDs...")
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'browser_subagent' in line:
            try:
                data = json.loads(line)
                # Check if it contains the subagent id
                # Usually it's in the response tool_calls or output or content
                print("Line details:", str(data)[:300])
            except Exception:
                pass

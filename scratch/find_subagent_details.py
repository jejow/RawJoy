import json

transcript_path = r"C:\Users\junxi\.gemini\antigravity-ide\brain\45fa12e0-5442-4e8b-99bc-427d93665aaf\.system_generated\logs\transcript.jsonl"

print("Searching for subagent details in transcript...")
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if 'execute_browser_javascript' in line:
            # Parse and print
            try:
                data = json.loads(line)
                print("TYPE:", data.get("type"), "STATUS:", data.get("status"))
                # Print any tool calls or content
                if "tool_calls" in data:
                    print("  Tool Calls:")
                    for tc in data["tool_calls"]:
                        print(f"    {tc.get('name')}: {str(tc.get('arguments'))[:200]}")
                if "content" in data and data["content"]:
                    print("  Content:", str(data["content"])[:300])
            except Exception:
                pass

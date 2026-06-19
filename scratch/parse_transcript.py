import json

transcript_path = r"C:\Users\junxi\.gemini\antigravity-ide\brain\45fa12e0-5442-4e8b-99bc-427d93665aaf\.system_generated\logs\transcript.jsonl"

print("Reading transcript...")
subagent_steps = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            step = json.loads(line)
            # Check if this is a subagent step or a tool call response
            if 'browser_subagent' in str(step) or 'execute_browser_javascript' in str(step):
                subagent_steps.append(step)
        except Exception as e:
            pass

print(f"Found {len(subagent_steps)} matching steps.")
# Let's print the last few steps in detail
for step in subagent_steps[-10:]:
    print("STEP TYPE:", step.get("type"), "STATUS:", step.get("status"))
    if "tool_calls" in step:
        for tc in step["tool_calls"]:
            print("  TOOL CALL:", tc.get("name"))
    if "content" in step and step["content"]:
        # Print first 200 chars of content
        print("  CONTENT:", str(step["content"])[:300])
    print("-" * 50)

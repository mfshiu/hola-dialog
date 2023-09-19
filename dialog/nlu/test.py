
import json
import re

# Your text
text = '''Sure, I can help you categorize the instruction you provided. Here is the output in JSON format:
{
"primary": "go somewhere",
"secondary": [
{
"category": "go to a toilet"
},
{
"category": "go to a restaurant"
}
]
}'''

try:
    json_text_match = re.search(r'{.*}', text, re.DOTALL)
    json_text = json_text_match.group(0)
    # print(f"\n{json_text}\n")
    primary, secondary = json.loads(json_text).values()
    # print(f"primary: {primary}")
    # print(f"secondary: {secondary[0]}")
    _classification = (primary, list(secondary[0].values())[0])
except Exception:
    _classification = ('unsupported', 'unsupported')

print(_classification)



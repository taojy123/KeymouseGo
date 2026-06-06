"""
Define a script formatter
Ensure the output recorded script is in the form of
{
  scripts: [
    { delay: 2345, event_type: "EM", action_type: "mouse move", action: [ "0.490234375%", "0.405%"], type: "event"}
  ]
}
instead of
{
  scripts: [
    {
      delay: 2345,
      event_type: "EM",
      action_type: "mouse move",
      action: [
        "0.490234375%",
        "0.405%",
      ],
      type: "event",
    },
  ],
}
The record events consist of simple mouse/keyboard event, we don't need to consider formatting workflow event
"""
from typing import List

import json5


class ScriptWriter:
    @staticmethod
    def dump_to_path(script_path: str, event_list: List):
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write("{\n")
            f.write('  "scripts": [\n')

            for i, event_str in enumerate(event_list):
                line = json5.dumps(event_str, ensure_ascii=False, fp=f, trailing_commas=False, quote_keys=True)
                comma = "," if i < len(event_list) - 1 else ""
                f.write(f'    {line}{comma}\n')

            f.write('  ]\n')
            f.write("}")

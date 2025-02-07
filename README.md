# table
table
http://digistump.com/package_digistump_index.json


https://github.com/digistump/DigistumpArduino/releases/download/1.6.7/Digistump.Drivers.zip
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);


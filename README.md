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










بله، من از طریق API هم قابل دسترسی هستم. OpenAI API به شما این امکان را می‌دهد که از مدل‌های مختلف مثل GPT-3 و GPT-4 برای ساخت برنامه‌ها و پروژه‌های مختلف استفاده کنید.

برای استفاده از API من، شما باید ابتدا در وب‌سایت OpenAI ثبت‌نام کنید و کلید API دریافت کنید. سپس می‌توانید از این کلید برای ارسال درخواست‌ها به مدل‌های زبان OpenAI استفاده کنید.

در اینجا یک نمونه از کد پایتون برای استفاده از OpenAI API آورده شده:

import openai

# کلید API خود را اینجا قرار دهید
openai.api_key = "your-api-key"

# ارسال درخواست به مدل GPT-3
response = openai.Completion.create(
  engine="text-davinci-003",  # می‌توانید مدل‌های دیگر را هم انتخاب کنید
  prompt="سلام، چطور می‌توانم به شما کمک کنم؟",
  max_tokens=100
)

# نمایش پاسخ مدل
print(response.choices[0].text.strip())

مراحل استفاده:

1. به OpenAI بروید و ثبت‌نام کنید.


2. یک پروژه بسازید و کلید API دریافت کنید.


3. از این کلید در کد خود استفاده کنید.



اگر به کد بیشتری نیاز دارید یا سوالی داشتید، من اینجام که کمک کنم!





import openai

# Replace with your API key
openai.api_key = "your-api-key"

# Send a request to the GPT-3 model
response = openai.Completion.create(
  engine="text-davinci-003",  # You can use other models as well
  prompt="Hello, how can I assist you today?",
  max_tokens=100
)

# Print the model's response
print(response.choices[0].text.strip())




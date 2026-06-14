import csv
import random

phishing_templates = [
    "Urgent: Your account has been suspended. Click here to verify your identity.",
    "You have won a $1000 Walmart gift card! Claim your prize now at this link.",
    "Security Alert: We detected unusual login activity on your account. Reset your password immediately.",
    "Your PayPal account is restricted. Please update your billing information within 24 hours.",
    "Final Notice: Your invoice #{} is overdue. Download the attached PDF to view details.",
    "Congratulations! You are our lucky winner today. Click here to claim your reward.",
    "Action Required: Verify your email address to avoid service interruption.",
    "Dear customer, your package could not be delivered. Pay the shipping fee here.",
    "Warning: Your mailbox is almost full. Upgrade your storage by clicking the link.",
    "Please review the attached secure document from HR regarding your salary update.",
    "Your Netflix subscription has expired. Update your payment details to continue watching.",
    "Alert: Someone tried to access your bank account from a new device. Secure it now.",
    "Exclusive offer! Buy cheap medications online without prescription.",
    "You have a pending tax refund. Click here to fill out the form and claim your money.",
    "Your Apple ID has been locked for security reasons. Verify your account at the link below."
]

legitimate_templates = [
    "Hi team, just a reminder about our meeting at 2 PM today. See you there.",
    "Attached is the report you requested for Q3. Let me know if you need any changes.",
    "Hey, are we still on for lunch tomorrow? Let me know what time works for you.",
    "Your Amazon order #{} has shipped and will arrive by tomorrow.",
    "Thank you for your recent purchase. Your receipt is attached.",
    "Don't forget to submit your timesheets by Friday afternoon.",
    "Can you please review this code PR when you have a moment?",
    "Happy Birthday! Hope you have a wonderful day celebrating.",
    "The server maintenance is scheduled for tonight at midnight. Expect brief downtime.",
    "Please find the meeting minutes attached for your review.",
    "I'll be out of the office next week on vacation. Please contact Sarah for urgent issues.",
    "Are you available for a quick sync later today?",
    "Your flight to Chicago is confirmed. Here is your itinerary.",
    "Just checking in to see how the project is going. Let me know if you need help.",
    "Thanks for reaching out! I'll get back to you as soon as possible."
]

data = []

# Generate 500 Phishing
for _ in range(500):
    text = random.choice(phishing_templates).format(random.randint(1000, 9999))
    # Add some random noise or variations to make it more realistic
    words = text.split()
    if random.random() > 0.8:
        words.insert(random.randint(0, len(words)), "urgent")
    data.append(["phishing", " ".join(words)])

# Generate 500 Legitimate
for _ in range(500):
    text = random.choice(legitimate_templates).format(random.randint(1000, 9999))
    data.append(["legitimate", text])

# Shuffle the dataset
random.shuffle(data)

with open('phishing_dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["label", "text"])
    writer.writerows(data)

print("Generated phishing_dataset.csv with 1000 examples.")

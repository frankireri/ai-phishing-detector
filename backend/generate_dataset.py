import csv
import random
import os

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
    "Your Apple ID has been locked for security reasons. Verify your account at the link below.",
    # Local Kenyan Phishing Tactics
    "URGENT: Your M-Pesa account has been suspended. Click here to verify your identity http://mpesa-verify.duckdns.org/verify?id={}",
    "Dear Customer, your Equity Bank account will be blocked today due to lack of KYC update. Click here to update: http://equity-update.com",
    "Safaricom: Congratulations! You have won KES 50,000 in the Shinda Mawe promotion. Call 0722000000 to claim.",
    "KRA Alert: You have a pending tax penalty of KES 5,000. Pay immediately via this link to avoid prosecution: http://kra-penalties.org",
    "Dear Parent, this is your child's teacher. Please send 2000 bob for an urgent school trip to this number: 0712345678",
    "Helb Loan disbursement delayed! Kindly click http://helb-portal-login.com to update your bank details immediately.",
    "Warning! M-Shwari loan limit decreased. Click here to increase your limit back to KES 30,000.",
    "Hustler Fund Alert: Your loan of KES 10,000 has been approved. Pay a registration fee of KES 200 to this till number to receive it.",
    "Your KPLC prepaid meter will be disconnected today. Pay outstanding balance here: http://kplc-payment.net",
    "Fuliza Limit Warning: Your Fuliza limit will be reduced to 0. Reply with your PIN to prevent this."
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
    "Thanks for reaching out! I'll get back to you as soon as possible.",
    # Local Kenyan Legitimate Messages
    "Safaricom: You have received KES 5,000 from John Doe. New M-PESA balance is KES 15,200.",
    "Hi, I have sent the 2k via M-Pesa. Let me know if you receive it.",
    "Equity Bank: Your salary of KES 45,000 has been deposited to account ending in 4521.",
    "KRA: Your tax returns for the year have been filed successfully.",
    "Hello! Let's meet at Java House Kimathi Street at 4 PM for the interview.",
    "Kindly remember to pay the caretaker the water bill before the 5th of this month.",
    "Your KPLC Token is 1234 5678 9012 3456 7890. Amount: KES 1000. Units: 45.2",
    "Safaricom: Your data bundle is below 10MB. Dial *544# to buy another bundle.",
    "Hi mum, I arrived safely in Nairobi. I'll call you later in the evening.",
    "Reminder: The tech meetup at iHub starts at 9:00 AM on Saturday."
]

data = []

# Generate 1500 Phishing
for _ in range(1500):
    text = random.choice(phishing_templates).format(random.randint(1000, 9999))
    # Add some random noise or variations to make it more realistic
    words = text.split()
    if random.random() > 0.8:
        words.insert(random.randint(0, len(words)), "urgent")
    data.append(["phishing", " ".join(words)])

# Generate 1500 Legitimate
for _ in range(1500):
    text = random.choice(legitimate_templates).format(random.randint(1000, 9999))
    data.append(["legitimate", text])

# Shuffle the dataset
random.shuffle(data)

# Save to data/phishing_dataset.csv
data_path = os.path.join(os.path.dirname(__file__), 'data', 'phishing_dataset.csv')
os.makedirs(os.path.dirname(data_path), exist_ok=True)

with open(data_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["label", "text"])
    writer.writerows(data)

print(f"Generated {data_path} with 3000 examples (including Kenyan context).")

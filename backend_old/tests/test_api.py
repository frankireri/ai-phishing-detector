"""Test all major endpoints."""
import json
from app import create_app

app = create_app()
client = app.test_client()

# Register a user
r = client.post('/api/auth/register', json={
    'email': 'test@cuea.ac.ke',
    'username': 'tester',
    'password': 'TestPass123',
    'full_name': 'Test User',
})
print('Register:', r.status_code)
data = r.json
print(json.dumps({k: v for k, v in data.items() if k != 'user'}, indent=2))
token = data.get('token')

# Login
r = client.post('/api/auth/login', json={
    'email': 'tester',
    'password': 'TestPass123',
})
print('\nLogin:', r.status_code, 'token received:', bool(r.json.get('token')))

# Me
r = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})
print('\nMe:', r.status_code)
print(json.dumps(r.json, indent=2))

# Logged predict
r = client.post('/api/predict/logged', json={
    'text': 'URGENT: Your KCB account is locked. Click http://kcb-verify.tk',
    'type': 'email',
}, headers={'Authorization': f'Bearer {token}'})
print('\nLogged predict:', r.status_code, r.json['result']['prediction'],
      f"{r.json['result']['confidence']:.2%}")

# Dashboard
r = client.get('/api/analytics/dashboard', headers={'Authorization': f'Bearer {token}'})
print('\nDashboard:', r.status_code)
print(json.dumps(r.json, indent=2)[:500])

# Batch predict
r = client.post('/api/predict/batch', json={
    'messages': [
        {'text': 'Your account has been suspended. Verify now at http://fake.com', 'type': 'sms'},
        {'text': 'Thanks for the meeting yesterday. Let me know your thoughts on the proposal.', 'type': 'email'},
    ]
})
print('\nBatch predict:', r.status_code)
print(json.dumps(r.json, indent=2))

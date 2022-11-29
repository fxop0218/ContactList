from user_api_contact import check_user

print(f"Correct: {check_user('admin', 'admin')}")
print(f"InCorrect: {check_user('admin', 'ad1min')}")
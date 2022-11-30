from user_api_contact import check_user
from helpful_functions import encript_pwd

print(f"Correct: {check_user('admin', encript_pwd('admin'))}")
print(f"InCorrect: {check_user('admin', encript_pwd('ad1min'))}")

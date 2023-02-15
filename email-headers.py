import sys

# Read email file path from command line arguments
if len(sys.argv) < 2:
    print("Please provide an email file path as a command line argument.")
    sys.exit()

email_file = sys.argv[1]

# Parse email headers and body
with open(email_file, 'r') as f:
    email = f.read()

# Split email into headers and body
email_parts = email.split('\n\n', 1)
headers = email_parts[0]

# Print raw headers
print(headers)

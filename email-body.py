import sys

# Read email file path from command line arguments
if len(sys.argv) < 2:
    print("Please provide the path to the .eml file as an argument.")
    sys.exit()

email_file = sys.argv[1]

# Parse email headers and body
with open(email_file, 'r') as f:
    email = f.read()

# Split email into headers and body
email_parts = email.split('\n\n', 1)
headers = email_parts[0].split('\n')

# Get Delivered-To, To, CC, References, From, and Body headers
delivered_to = None
to = None
cc = None
body = None
frm = None

for header in headers:
    if header.startswith("Delivered-To:"):
        delivered_to = header.split(":")[1].strip()
    elif header.startswith("To:"):
        to = header.split(":")[1].strip()
    elif header.startswith("CC:"):
        cc = header.split(":")[1].strip()
    elif header.startswith("From:"):
        frm = header.split(":")[1].strip()
        
# If "CC" header does not exist, set cc to an empty string
if cc is None:
    cc = ""

# Get email body
if len(email_parts) > 1:
    body = email_parts[1].strip()

# Print results
print("From: ", frm)
print("Delivered-To: ", delivered_to)
print("To: ", to)
print("CC: ", cc)
print("Body: ", body)

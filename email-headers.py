import email
import argparse

# Set up the command line arguments
parser = argparse.ArgumentParser(description="Parse an .eml file and return the headers.")
parser.add_argument("filename", help="Path to the .eml file.")

# Parse the command line arguments
args = parser.parse_args()

with open(args.filename, "r") as f:
    msg = email.message_from_file(f)

# Print out the headers
for header in msg.keys():
    print(f"{header}: {msg[header]}")

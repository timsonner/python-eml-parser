import sys
import email
import quopri

def get_first_text_block(msg):
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            try:
                text = part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
                return text.strip()
            except:
                pass
    return None

if len(sys.argv) < 2:
    print("Usage: python eml_parser.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    msg = email.message_from_file(f)

    # Parse the From, To, Cc, Subject, Delivered-To, and Date headers
    sender = msg['From']
    recipient = msg['To']
    cc = msg['Cc']
    subject = msg['Subject']
    delivered_to = msg['Delivered-To']
    date = msg['Date']

    # Parse the main body of the email
    body = get_first_text_block(msg)

    # Parse the received headers to get the email path
    received = msg.get_all('Received')
    path = []
    if received:
        for r in received:
            # Extract the IP address of the sender
            ip = r.split('[')[-1].split(']')[0]
            # Add the hop to the path
            path.append((r, ip))

    # Print out the results
    print("From: {}".format(sender))
    print("To: {}".format(recipient))
    print("Cc: {}".format(cc))
    print("Subject: {}".format(subject))
    print("Delivered-To: {}".format(delivered_to))
    print("Date: {}".format(date))
    #print("Body: {}".format(body))
    if path:
        print("\nEmail path:")
        for i, (hop, ip) in enumerate(path):
            hop_desc = "Hop {}".format(i+1)
            if i == 0:
                hop_desc = "First hop (sender)"
            elif i == len(path)-1:
                hop_desc = "Final destination"
            print("{} - {} - IP: {}".format(hop_desc, hop, ip))
    else:
        print("\nEmail path: No Received headers found.")

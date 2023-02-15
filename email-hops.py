import sys
import re
import subprocess

# function to get the abuse email from WHOIS
def get_abuse_email(domain):
    try:
        whois_output = subprocess.check_output(['whois', domain]).decode('utf-8')
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        abuse_regex = r'abuse@' + domain
        match = re.search(abuse_regex, whois_output, re.IGNORECASE)
        if match:
            return match.group(0)
        else:
            match = re.search(email_regex, whois_output)
            if match:
                return match.group(0)
            else:
                return None
    except Exception as e:
        print(f"Failed to get abuse email for {domain}: {e}")
        return None

# function to extract headers and body from .eml file
def parse_eml_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # use regex to extract headers and body
    header_regex = r"((?:.+\n)*)(?:\r?\n)"
    headers = re.match(header_regex, content).group(1)

    body = re.sub(header_regex, "", content)

    return headers, body

# function to extract email addresses from headers
def extract_emails_from_headers(headers):
    hops = re.findall(r"Received: from ([a-zA-Z0-9._%+-]+\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", headers, re.IGNORECASE)
    
    return hops

if __name__ == '__main__':
    # check if file path is provided
    if len(sys.argv) < 2:
        print("Please provide the path to the .eml file as an argument.")
        sys.exit(1)

    # get the file path from command line arguments
    file_path = sys.argv[1]

    # extract headers and body from .eml file
    headers, body = parse_eml_file(file_path)

    # extract email addresses from headers
    hops = extract_emails_from_headers(headers)

    # print the extracted information
    print("Hops: ", hops)

    # get abuse email for last hop
    if hops:
        last_hop = hops[-1]
        abuse_email = get_abuse_email(last_hop)
        if abuse_email:
            print(f"Abuse email for {last_hop}: {abuse_email}")
        else:
            print(f"No abuse email found for {last_hop}")
    else:
        print("No hops found in headers")
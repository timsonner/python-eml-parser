import sys
import re
import subprocess

# function to get the abuse email from WHOIS
def get_abuse_email(domain):
    # make sure domain only contains the domain name and its tld extension
    match = re.search(r"\b([a-zA-Z0-9]+\.[a-zA-Z]{2,})\b", domain)
    if match:
        domain = match.group(1)
    else:
        print(f"Invalid domain name: {domain}")
        return None

    process = subprocess.run(["whois", domain], capture_output=True, text=True)
    output = process.stdout
    match = re.search(r"Registrar Abuse Contact Email: (.+)", output)
    if match:
        abuse_contact_email = match.group(1)
        print(f"\nAbuse contact email for {domain}: {abuse_contact_email}")
    else:
        print(f"Couldn't find the Registrar Abuse Contact Email field for {domain}")
        print(f"Try running 'whois {domain}' to see if an alternate whois database exists")
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
    # trim subdomain from last hop
    if hops:
        last_hop = hops[-1].rsplit('.', 2)[-2] + "." + hops[-1].rsplit('.', 2)[-1]
        hops[-1] = last_hop
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
        get_abuse_email(last_hop)
    else:
        print("No hops found in headers")

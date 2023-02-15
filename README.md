# python-eml-parser
Display info from an email .eml file such as delevered-to, cc, to, from, body, received headers (hops).

## Usage
Print To, CC, Delivered-To, and Body.
    
    python email-body.py <filename>
  
Print the path (hops) the email took from sender to receiver.
    
    python email-hops.py <filename>

Print the headers of the email.

    python email-headers.py <filename>

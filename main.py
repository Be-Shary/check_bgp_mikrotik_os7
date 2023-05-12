import requests
import sys, argparse
from argparse import RawTextHelpFormatter

# NOTE: This is to suppress the insecure connection warning for certificate verification.
from requests.packages.urllib3.exceptions import InsecureRequestWarning # Turn off request warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_data(url, username, password):
    try:
        response = requests.get(url, auth=(username, password), verify=False, timeout=15)
        code = (response.status_code)
        if code == 206 or code == 200:
            data = response.json()
            return data
        else:
            print("UNKNOWN - Authorization failed - code: " + str(code))
            sys.exit(3)
    except requests.exceptions.ConnectTimeout:
        print('UNKNOWN - Connection has timed out')
        sys.exit(3)
    except requests.exceptions.ConnectionError:
        print("UNKNOWN - Connection failed: " + str(sys.exc_info()[1]))
        sys.exit(3)
    except:
        print("Unexpected error: " + sys.exc_info()[0])
        sys.exit(3)


def check_bgp(bgp_address, data):
    global exit_code
    for item in data:
        if item["remote.address"] == str(bgp_address):
            if (item["established"]) == "true":
                exit_code = 0
                return "OK - " + str(bgp_session) + " state is established. Established for " + str(item["uptime"])
    exit_code = 2
    return "CRITICAL - BGP not found or other problem!"


if __name__ == "__main__":
    hostname = ""
    username = ""
    password = ""
    bgp_session = ""
    temp = {}
    output = ""
    exit_code = 3  # set nagios status to unknown as default

    help_message = ("""Check BGP sessions in Mikrotik OS7 routers through API""")

    parser = argparse.ArgumentParser(description=help_message, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-H', '--hostname', metavar='<HOSTNAME>', required=True)
    parser.add_argument('-u', '--api_username', metavar='<USERNAME>', required=True)
    parser.add_argument('-p', '--api_password', metavar='<PASSWORD>', required=True)
    parser.add_argument('-b', '--bgp_ip', metavar='<BGP_IP>', required=True)

    args = parser.parse_args()

    # Assign parsed arguments to variables
    hostname = args.hostname
    username = args.api_username
    password = args.api_password
    bgp_session = args.bgp_ip
    url = "https://" + str(hostname) + "/rest/routing/bgp/session"

    temp = get_data(url, username, password)
    output = check_bgp(bgp_session, temp)

    print(output)
    sys.exit(exit_code)

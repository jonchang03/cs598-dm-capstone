import requests
import sys

SUBMISSION_URL = 'http://capstone-leaderboard.centralus.cloudapp.azure.com'

if len(sys.argv) != 3:
    print("Usage: {} netid outputfile\n")
    print("\tnetid: your UIUC NetID\n")
    print("\toutputfile: newline separated file")
    print("\t\tThe first line is your desired alias on the leaderboard")
    print("\t\tThe remaining lines are binary labels (0 or 1) for each")
    print("\t\tdocument in the test set.\n")
    sys.exit(1)

netid = sys.argv[1]
with open(sys.argv[2], 'r') as inputfile:
    alias = inputfile.readline().strip()
    labels = [lbl.strip() for lbl in inputfile]

req = {
    'netid': netid,
    'alias': alias,
    'results': [{
        'error': None,
        'dataset': 'hygiene',
        'results': labels
    }]
}
response = requests.post(SUBMISSION_URL + '/api', json=req)
jdata = response.json()
if jdata['submission_success'] is not True:
    print("An error occurred during submission!")
    print("See the below JSON response for more information.")
    print()
    print(jdata)
else:
    print("Submission completed successfully!")
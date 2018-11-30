import argparse
import time
import calendar

parser = argparse.ArgumentParser()
parser.add_argument('--search', type=str)
#parser.add_argument('--orcid_client_id', type=str)
#parser.add_argument('--orcid_client_secret', type=str)
parser.add_argument('--file', type=str)
args = parser.parse_args()
search = args.search
outputFile = args.file
#client_id = args.orcid_client_id
#client_secret = args.orcid_client_secret
#token_endpoint = args.token_endpoint
search_endpoint='https://pub.orcid.org/v2.1/search/?'
api_endpoint='https://pub.orcid.org/v2.1/'

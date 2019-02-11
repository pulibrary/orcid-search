import argparse
import io
from io import BytesIO
import sys
import config
import string
import pycurl
import unicodecsv as csv
import urllib
import json


def csv_to_file(output):
    with open(config.outputFile, "w") as outputFile:
        wr = csv.writer(outputFile, lineterminator='\n')
        wr.writerows(output)

#not used yet
def get_orcid_token():
    #set request variables
    client_id = config.orcid_client_id
    client_secret = config.orcid_client_secret
    token_endpoint = config.token_endpoint
    data = BytesIO()
    #create post data
    post_data = {'client_id': client_id, 'client_secret': client_secret, 'scope': '/read-public', 'grant_type': 'client_credentials'}
    #url encode post data
    postfields = urllib.urlencode(post_data)
    #create and send http request
    c = pycurl.Curl()
    c.setopt(c.URL, token_endpoint)
    c.setopt(c.HTTPHEADER, ['Accept: application/json'])
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    #get request response
    json_object = json.loads(data.getvalue())
    token = json_object['access_token']
    return token

def getName(orcid):
    base_url = config.api_endpoint
    data = BytesIO()
    #create request string
    request_string = base_url + orcid + '/person'
    #create and send http request
    c = pycurl.Curl()
    c.setopt(c.URL, request_string)
    c.setopt(c.HTTPHEADER, ['Content-Type: application/orcid+xml', 'Accept: application/json'])
    c.setopt(c.POST, 0)
    c.setopt(c.WRITEFUNCTION, data.write)
    c.perform()
    c.close()
    #get request response
    json_object = json.loads(data.getvalue())
    return json_object

def search_affiliations(search):
    startRow = 0
    numRows = 100
    output = []
    #set request variables
    base_url = config.search_endpoint
    query = {'defType' : 'edismax', 'q' : 'affiliation-org-name:' + '"' + search + '"'}
    #url encode query
    encoded_query = urllib.urlencode(query)
    
    while(True):
        data = BytesIO()
        #create request string
        request_string = base_url + encoded_query + '&start=' + str(startRow)
        request_string = request_string + '&rows=' + str(numRows)
        print request_string
        #create and send http request
        c = pycurl.Curl()
        c.setopt(c.URL, request_string)
        c.setopt(c.HTTPHEADER, ['Content-Type: application/orcid+xml', 'Accept: application/json'])
        c.setopt(c.POST, 0)
        c.setopt(c.WRITEFUNCTION, data.write)
        c.perform()
        c.close()
        #get request response
        json_object = json.loads(data.getvalue())
        new_results = json_object['result']
        num_results = json_object['num-found']
        #return num_results
        if len(new_results) == 0:
            break
        print "Getting " + str(startRow + numRows) + " out of " + str(num_results)
        for result in new_results:
            temp_row = []
            temp_row.append(result['orcid-identifier']['path'])
            names = getName(result['orcid-identifier']['path'])
            if names['name']:
                if names['name']['given-names']:
                    temp_row.append(names['name']['given-names']['value'])
                else:
                    temp_row.append('')
                if names['name']['family-name']:
                    temp_row.append(names['name']['family-name']['value'])
                else:
                    temp_row.append('')
            else:
                temp_row.append('')
                temp_row.append('')
    
            output.append(temp_row)
        #print output
        startRow += numRows
    csv_to_file(output)

def main():
    search_affiliations(config.search)

if __name__ == '__main__':
  main()

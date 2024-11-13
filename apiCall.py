#Api Call Functions

import requests
import json

requests.packages.urllib3.disable_warnings()

def postApiCall(url, authKey):

    data = {"entities":[]}
    os = 0
    leng = 500
  
    payload = json.dumps({
      "length": leng,
      "offset": os
      })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Basic {authKey}',
      }
  
    response = requests.request("POST", url, headers=headers, data=payload, verify = False)

    if response.status_code ==  200:

        output = response.json()

    else:

        print("Invalid Credentials, please try again")
        return 0
    
        
    while os < output['metadata']['total_matches']:
        payload = json.dumps({
        "length": leng,
        "offset": os
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {authKey}',
        }

        try:

            response = requests.request("POST", url, headers=headers, data=payload, verify = False)
            requests.packages.urllib3.disable_warnings()
            output = response.json()
            data['entities'].extend(output['entities'])
            os = os + leng


        
        except requests.exceptions.RequestException as err:

            print("Error getting Cluster Lists")

            return None
            
    return data


def getApiCall(url, authKey, clus_uuid):

    data = {"entities":[], "metadata":{}}
    os = 0
    leng = 500
  
    payload = json.dumps({
      "length": leng,
      "offset": os
      })

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {authKey}',
    }
       
  
    response = requests.request("GET", url, headers=headers, data=payload, verify = False)

    if response.status_code ==  200:

        output = response.json()

    else:

        print("Invalid Credentials, please try again")
        return "-"

    if "v2.0" in url:
        if 'metadata' in output:
            entryCount = output['metadata']['grand_total_entities']
        else:
          return output
    elif "v2.a1" in url:
        
        return output
    else:
        if 'metadata' in output:
          entryCount = output['metadata']['grandTotalEntities']
        else:
          return output

    while os < entryCount:
        payload = json.dumps({
        "length": leng,
        "offset": os
        })
        if 'virtual-switches' in url:
          headers = {
        'Content-Type': 'application/json',
        'X-Cluster-Id': f'{clus_uuid}',
        'Authorization': f'Basic {authKey}'
        }
        else:
          headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {authKey}',
        }

        try:

            response = requests.request("GET", url, headers=headers, data=payload, verify = False)
            requests.packages.urllib3.disable_warnings()
            output = response.json()
            if "v4.0.b1" in url:
                data['entities'].extend(output['data'])
            else:
                data['entities'].extend(output['entities'])
            os = os + leng

        
        except requests.exceptions.RequestException as err:

            print("Error getting Cluster Lists")

            return None
    data['metadata'] = output['metadata']
    return data
    
def apiV4(mainUrl, authKey):

    data = {"entities":[]}
    page = 0
    limit = 100

    
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {authKey}'
      }
    
    response = requests.request("GET", mainUrl, headers=headers, data=payload, verify = False)

    if response.status_code ==  200:

      output = response.json()

    else:

      print("Invalid Credentials, please try again")
      return 0
    

    count = 0

    
    while count < output['metadata']['totalAvailableResults']:


        try:

          url = f"{mainUrl}?$page={page}&$limit={limit}"
          response = requests.request("GET", url, headers=headers, data=payload, verify = False)
          requests.packages.urllib3.disable_warnings()
          output = response.json()
          data["entities"].extend(output["data"])
          count = count + limit
          page = page + 1

        
        except requests.exceptions.RequestException as err:

          print("Error getting Cluster Lists")

          return None

    return data

def apiV4Conf(url, authKey):

    page = 0
    limit = 100
    
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {authKey}'
      }

    try:

        url = f"{url}?$page={page}&$limit={limit}"
        response = requests.request("GET", url, headers=headers, data=payload, verify = False)
        requests.packages.urllib3.disable_warnings()
        output = response.json()
        return output

        
    except requests.exceptions.RequestException as err:

        print("Error getting Cluster Lists")

        return None
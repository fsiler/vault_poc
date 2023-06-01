#!/usr/bin/env python3
from json     import loads, dumps
from os       import environ as env
from pprint   import pprint
from requests import get, post

if __name__ == '__main__':
  body = {'role_id':   'cmdb28550_nonprod',
          'secret_id': env['VAULT_SECRET_ID']}

  # use approle to get a key
  d = post('https://vault-enterprise-test.ssnc-corp.cloud/v1/auth/approle/login',
           data=dumps(body))

  response = loads(d.text)

  token = response['auth']['client_token']

  # access a secret using the namespace and path, plus token derived above
  secret_path = 'CMDB28550/test'
  headers = { 'X-Vault-Token': token,
              'X-Vault-Namespace': 'kv-v1/application/nonprod/'}

  fetch = get('https://vault-enterprise-test.ssnc-corp.cloud/v1/' + secret_path,
              headers=headers)

  pprint(loads(fetch.text))

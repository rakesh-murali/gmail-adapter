import os, os.path
import configparser

from constant import EMAIL_TABLE_FIELDS
from GmailAdapter import GmailAdapter
from SQLClient import SQLClient
from creds.rule import rule

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

cfg = configparser.ConfigParser()
cfg.read('config-dev.cfg')

def main():
    adapter = GmailAdapter(SCOPES, 'me')
    action = input("""
      Click below option for process email:
      Choose 1 to fetch email form API and store in local DB :
      Choose 2 to search email and do action based on json rule :
      """)

    if (action == '1'):
      data = adapter.fetch_emails()
      sql_client = SQLClient(
        cfg.get('database', 'host'), 
        cfg.get('database', 'user'), 
        cfg.get('database', 'password'), 
        cfg.get('database', 'name')
      )
      sql_client.insert('inbox', EMAIL_TABLE_FIELDS, data)
    elif (action == '2'):
      messages = adapter.search_email(rule)
      adapter.do_action(rule.get('actions'), messages)
    else:
        print('Invalid Option, Enter 1 or 2 and submit')
        main()

if __name__ == '__main__':
    main()




            

    


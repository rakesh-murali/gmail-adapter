import os, os.path
import configparser

from constant import EMAIL_TABLE_FIELDS
from clients.GmailClient import GmailClient
from clients.YahooClient import YahooClient
from Adapter import Adapter
from helpers.SQLHelper import SQLClient
from creds.rule import rules

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

cfg = configparser.ConfigParser()
cfg.read('config-dev.cfg')


def main():
    """
        We can have n number of clients, 
        We can pass different client methods with static adapter keys,
        Separate client functions can be added
    """
    gmail_client = GmailClient(SCOPES, 'me')
    yahoo_client = YahooClient([], 'me')

    adapters = [
        Adapter(gmail_client, 
            authenticate='get_authenticated', 
            initialize_service ='initialize_service', 
            do_action_based_on='do_action_based_on', 
            fetch_emails='fetch_emails'),
        Adapter(yahoo_client, 
            authenticate='authenticate_yahoo', 
            initialize_service ='create_service', 
            do_action_based_on='do_action_based_on', 
            fetch_emails='get_emails'),
    ]

    for adapter in adapters:
        action = input("""
                          Click below option for process email:
                          Choose 1 to fetch email form API and store in local DB :
                          Choose 2 to search email and do action based on json rule :
                      """
                      )

        adapter.authenticate()
        adapter.initialize_service()
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
            adapter.do_action_based_on(rules)
        else:
            print('Invalid Option, Enter 1 or 2 and submit')
            main()

if __name__ == '__main__':
    main()




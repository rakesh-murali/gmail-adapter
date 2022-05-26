import base64
import datetime as dt
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup

from clients.GmailBaseClient import GmailBaseClient
from constant import QUERY_KEYWORD_MAPPER, FIELD_MAPPER


class GmailClient(GmailBaseClient):

    def __init__(self, scopes, user_id):
        super().__init__(scopes, user_id)


    def do_action_based_on(self, rules):
        """
            Gets the email based on id and process the returned raw mail

            Params:
                list of rules inside filter constrains and action items
        """
        for rule in rules:
            filters = rule.get('rules')
            actions = rule.get('actions')
            predicate = rule.get('predicate')
            mails = self.search_email(filters, predicate)
            self.do_action(actions, mails)


    def search_email(self, rules, predicate):
        """
            Generates search query and get mails based on the query and returns

            Params:
                rules - list of objects contains field, constraint, value and type
                predicate - overall constraint (OR/AND)
            
            Return:
                Returns the filtered emails
        """
        for index, a in enumerate(rules):
            if (a['type'] == 'date'):     
                del rules[index]
                rules += GmailClient.get_date_search_keywords(a)
                break

        try:
            query = self.generate_search_query(rules, predicate)
            print(query)
            txt = self.get_user_mails(q=query)
            return txt['messages']
        except Exception as error:
            print(f'An error occurred: {error}')


    def do_action(self, actions, mails):
        """
            Removes and adds mail labels based ont he given action

            Params:
                actions - object contains list of labels to be added and removes
                mails - action required mails
        """
        add_label = actions.get('add-labels')
        remove_label = actions.get('remove-labels')

        for mail in mails:
            self.modify_email(
                id = mail.get('id', ''), body = {
                'removeLabelIds': remove_label, 
                'addLabelIds': add_label
                }
            )
            print(f'Mails is being moved from {remove_label} to {add_label}')


    def fetch_emails(self):
        """
            Gets the email based on id and process the returned raw mail

            Returns:
                Object contains mail fields will be returned
        """
        insert_data = []
        mail_details = self.get_user_mails()
        mails = mail_details.get('messages')

        for mail in mails:
            body, id = '', mail.get('id')
            mail_obj = self.get_user_mail(id)
            payload = mail_obj['payload']
            headers = payload['headers']
            headers = GmailClient.pickup_required_headers(headers)

            try:
                mail_body = GmailClient.get_mail_body(payload)
                decoded_data = base64.b64decode(mail_body)
                soup = BeautifulSoup(decoded_data , 'lxml')
                body = str(soup.body())
            except Exception as error:
                print(f'An error occurred: {error}')

            date = headers.get('date')
            mail_from = headers.get('from')
            subject = headers.get('subject')
            insert_data.append((subject, date, body, mail_from))

        return insert_data


    @classmethod
    def generate_search_query(cls, rules, predicate):
        """
            This will converts given rules into gmail search query

            Params:
                rules - list of objects contains field, constraint, value and type
                predicate - overall constraint (OR/AND)
            
            Return:
                Return the query that needs to pass email api
        """
        query = ''
        predicate = QUERY_KEYWORD_MAPPER.get(predicate, '')

        for rule in rules:
            constraint = QUERY_KEYWORD_MAPPER.get(rule['constraint'], '')
            value = rule['value']
            field = FIELD_MAPPER.get(rule['field'], '')
            query += f'{constraint}{field}:{value} {predicate} '

        return query


    @classmethod
    def get_date_search_keywords (cls, rule):
        """
            This will converts given date rule to compatable processing rule

            Params:
                rule - objects contains field, constraint, value and type
            
            Return:
                Return aligned date rule
        """
        today = date.today()
        days = dt.timedelta(int(rule['value']))

        if rule['constraint'] == 'less-than':
            before = today - days
            after = today
        else:
            after = today + days
            before = today

        date_rule = [{
            'constraint': '',
            'value': before,
            'field': 'before'
          },
          {
            'constraint': '',
            'value': after,
            'field': 'after'
          }]
        return date_rule


    @staticmethod
    def pickup_required_headers(headers):
        """
            Will receive the overall header and returns only required headers

            Params:
                headers - object contains subject, from, delivered_date, labels etc..
            
            Return:
                Returns required headers to be stored
        """
        required_headers = {}

        for d in headers:
            name = d['name'].lower()
            if name in ['subject', 'from']:
              required_headers.update({name: d['value']})
            elif name == 'date':
              date = d['value']
              received_date = datetime.strptime(date[5:16], '%d %b %Y')
              date = received_date.strftime('%Y-%m-%d')
              required_headers.update({name: date})
        return required_headers


    @staticmethod
    def get_mail_body(payload):
        """
            Will get the raw mail body and retuired the processed mail body

            Params:
                payload - raw mail body
            
            Return:
                Returns readable mail body
        """
        mail_parts = payload.get('body')
        mail_parts = mail_parts[0] if mail_parts  else ''
        mail_body = payload['body']['data']
        mail_body = mail_body.replace('-','+').replace('_','/')
        return mail_body
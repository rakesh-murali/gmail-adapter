from datetime import datetime
from bs4 import BeautifulSoup
from datetime import date
import datetime as dt
import base64

from GmailBaseAdapter import GmailBaseAdapter
from constant import QUERY_KEYWORD_MAPPER


class GmailAdapter(GmailBaseAdapter):

  def __init__(self, scopes, user_id):
    # initializing query generator methods
    GmailAdapter.query_generators = {
      'date': GmailAdapter.get_date_search_keywords,
      'string': GmailAdapter.get_string_search_keywords
    }
    super().__init__(scopes, user_id)


  @staticmethod
  def get_date_filter_value(date_received):
    # function gets the date for Gmail api query
    today = date.today()
    days = dt.timedelta(int(date_received))
    filter_date = today - days
    return filter_date.strftime('%Y/%m/%d')

  def fetch_emails(self):
    ''' This Function fetches the emails based on user id from gmail and 
    split the mail parts and return the email parts '''

    mail_details = self.service.users().messages().list(userId=self.user_id).execute()
    mails = mail_details.get('messages')
    insert_data = []

    for index, mail in enumerate(mails):
      id = mail.get('id')
      mail_obj = self.service.users().messages().get(userId=self.user_id, id=id).execute()

      try:
        payload = mail_obj['payload']
        headers = payload['headers']

        for d in headers:
          if d['name'] == 'Subject':
            subject = d['value']
          if d['name'] == 'From':
            mail_from = d['value']
          if d['name'] == 'Date':
            date = d['value']
            received_date = datetime.strptime(date[5:16], '%d %b %Y')
            date = received_date.strftime('%Y-%m-%d')

        mail_parts = payload.get('parts')
        mail_parts = mail_parts[0] if len(mail_parts) > 0  else ''
        mail_body = mail_parts['body']['data']
        mail_body = mail_body.replace('-','+').replace('_','/')

        decoded_data = base64.b64decode(mail_body)
        soup = BeautifulSoup(decoded_data , 'lxml')
        body = soup.body()
        insert_data.append((subject, date, str(body), mail_from))
        if (index == 9):
          break
      except Exception as error:
        print(f'An error occurred: {error}')
    return insert_data

  def search_email(self, rule):
    # function to make search call to gmail API
    filters, overall_predicate = rule.get('filters'), rule.get('predicate', '')
    try:
      import pdb;pdb.set_trace()
      query = self.generate_search_query(filters, overall_predicate)
      txt = self.service.users().messages().list(userId=self.user_id, q=query).execute()
      return txt['messages']
    except Exception as error:
       print(f'An error occurred: {error}')


  def do_action(self, actions, messages):
    #function to make action through gmail API
    add_label = actions.get('add-labels')
    remove_label = actions.get('remove-labels')
    for msg in messages:
        txt = self.service.users().messages().modify(userId=self.user_id, id=msg.get('id', ''), body={
          'removeLabelIds': remove_label, 
          'addLabelIds': add_label
        }).execute()

  @classmethod
  def generate_search_query(cls, filters, overall_predicate):
    # This fuction acceps the rule filter and return the query which needs to send Gmail API
    query = ''
    for field, filter_obj in filters.items():
      field_type = filter_obj['type']
      overall_prediate_keyword = QUERY_KEYWORD_MAPPER.get(overall_predicate, '')
      query_generator = cls.query_generators[field_type]
      field, filter_keyword, filter_input = query_generator(filter_obj, field)
      
      query += '%s:%s%s %s ' % (field, filter_keyword, filter_input, overall_prediate_keyword)
    return query

  @classmethod
  def get_string_search_keywords (cls, filter_obj, field):
    # to generate gmail api search keyword for string fields    
    filter_keyword = QUERY_KEYWORD_MAPPER.get(filter_obj['constraint'], '')
    filter_input = filter_obj['value']
    return field, filter_keyword, filter_input

  @classmethod
  def get_date_search_keywords (cls, filter_obj, field):
    # to generate gmail api search keyword for date fields
    field = QUERY_KEYWORD_MAPPER.get(filter_obj['constraint'], '')
    filter_input = cls.get_date_filter_value(filter_obj['value'])
    return field, '', filter_input
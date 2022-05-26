
QUERY_KEYWORD_MAPPER = {
    # string keywords
    'contains': '',
    'equals': '+',
    'not-equals': '-',
    'not-contains': '-',
    'in': '+',
    'not-in': '-',
    # action keywords
    'read': 'removeLabelIds',
    'unread': 'addLabelIds',
    # date filter keywords
    'less-than': 'before',
    'greater-than': 'after',
    # overall predicate
    'any': 'OR',
    'all': 'AND',
  }

FIELD_MAPPER = {
  'subject': 'subject',
  'from': 'from',
  'to': 'to',
  'have': '',
  'not-have': '',
  'in': 'in',
  'not-in': 'in',
  'has': 'has',
  'not-has': 'has',
  'before': 'before',
  'after': 'after'
}

EMAIL_TABLE_FIELDS = ('subject', 'delivered_at', 'body', 'mail_from')
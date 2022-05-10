
QUERY_KEYWORD_MAPPER = {
    # string keywords
    'contains': '',
    'equals': '+',
    'not-equals': '-',
    'not-contains': '-',
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

EMAIL_TABLE_FIELDS = ('subject', 'delivered_at', 'body', 'mail_from')
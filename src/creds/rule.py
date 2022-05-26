rules = [{
  'predicate': 'any',
  'rules': [
     {
      'value': 'Please confirm your email',
      'constraint': 'contains',
      'field': 'subject',
      'type': 'string'
    },
     {
      'value': 'test',
      'constraint': 'not-contains',
      'field': 'subject',
      'type': 'string'
    },
    {
      'value': 'confirm@account.pinterest.com',
      'constraint': 'equals',
      'field': 'from',
      'type': 'string'
    },
    {
      'value': '3',
      'constraint': 'less-than',
      'field': 'received-date',
      'type': 'date'
    },
    {
      'value': 'drafts',
      'constraint': 'not-in',
      'field': 'in',
      'type': 'string'
    },
  ],
  'actions': {
    'add-labels': ['Label_8755948405532946904'],
    'remove-labels': ['UNREAD']
  }
},
# Can have more rules and actions
]
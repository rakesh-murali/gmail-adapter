rule = {
  'predicate': 'any',
  'filters': {
    "subject": {
      'value': 'Please confirm your email',
      'constraint': 'contains',
      'type': 'string'
    },
    "from": {
      'value': 'confirm@account.pinterest.com',
      'constraint': 'equals',
      'type': 'string'
    },
    "to": {
      'value': 'rakesh.trade2020@gmail.com',
      'constraint': 'equals',
      'type': 'string'
    },
    "delivered_at": {
      'value': '4',
      'constraint': 'less-than',
      'type': 'date'
    }
  },
  'actions': {
    'add-labels': ['Label_8755948405532946904'],
    'remove-labels': ['UNREAD']
  }
}
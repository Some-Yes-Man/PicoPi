def parse(request: str):
  r = {
       'request_str': request,
       'request': request.split('\\r\\n'),
       'header': {},
       'GET': [],
       'POST': [],
       'parameter': {},
      }

  for field in r['request'][1:]:
    if field.find(': ') > 0:
      key,value = field.split(': ')#split each line by http field name and value
      r['header'][key] = value

  r['GET'] = r['request'][0]
  if r['GET'].find('/?') > 0:
    r['GET'] = r['GET'][r['GET'].find('/?') + 2:]
    r['GET'] = r['GET'][:r['GET'].find(' ')]
    r['GET'] = r['GET'].split('&')

    for p in r['GET']:
      if p.find('=') > 0:
        key,value = p.split('=')
        r['parameter'][key] = value
      else:
        r['parameter'][p] = ''

  return r
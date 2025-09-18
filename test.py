def function(s=''):
    return s.split('/')[-1].split('?')[0]

print(function(s='https://999.md/ro/list/transport/cars?page=1'))
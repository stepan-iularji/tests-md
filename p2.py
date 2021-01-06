data = None

with open('tests/t.txt', encoding='Windows-1251') as fh:
    data = fh.read()

with open('tests/t.txt', 'wb') as fh:
    fh.write(data.encode('utf-8'))
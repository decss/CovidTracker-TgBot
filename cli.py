from CovidTracker import CovidTracker


name = None
while not name:
    name = input('Введите название страны: ')
    tracker = CovidTracker()

    if not name:
        name = 'world'

    # World data
    if name == 'world':
        print('Данные по миру')
        data = tracker.getData('world', 'text')
        print('------------------------------')
        print(data)

    # Country data
    elif name:
        country = tracker.processCountryName(name)

        if not country:
            print('Страна "' + name + '" не найдена\n')
            name = None
        else:
            print('Данные по стране "' + country['name'] + '":')
            data = tracker.getData(country['code'], 'text')
            print('------------------------------')
            print(data)

    else:
        print('Вы не ввели название\n')
        name = None


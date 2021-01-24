from CovidTracker import CovidTracker


name = None
while not name:
    name = input('Введите название страны: ')
    tracker = CovidTracker()

    # World data
    if name == 'world':
        data = tracker.getData('world', 'text')
        print('Данные по миру')
        print('------------------------------')
        print(data)

    # Country data
    elif name:
        country = tracker.processCountryName(name)

        if not country:
            print('Страна "' + name + '" не найдена\n')
            name = None
        else:
            data = tracker.getData(country['code'], 'text')
            print('Данные по стране "' + country['name'] + '":')
            print('------------------------------')
            print(data)

    else:
        print('Вы не ввели название\n')
        name = None


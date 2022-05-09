import _import as imp


def features(_id, _data):
    print('---------------')
    print(_id, _data.pop(0))
    for i in _data:
        print(i.date, i.eye, i.e_type, i.flash, i.adaptation)
        """
        print(i.recorded_waveform)
        print(i.raw_waveform)
        print(i.pupil_waveform)
        """


def intra_distance(data):
    date = data.pop(0)
    print(date)
    dist = []
    for i in range(6):
        if i != 2 or i != 3:
            re = data[i].recorded_waveform
            le = data[i+2].recorded_waveform
            l = min(re.shape[0], le.shape[0])
            print(l)
            print(re.dtypes)
            #print(int(re.loc[:10, ['uV']].subtract(le.loc[:10, ['uV']]))
            #dist.append()
    print([i.eye for i in data])
    print('distance: ')


def main():
    path = r'C:\Users\Mirdir\PycharmProjects\data_btt'
    data = imp.read_data(path)
    for key in data.keys():
        print(key)
        #features(key, data[key])
        intra_distance(data[key])

    print(data.keys())
    print(data['CB07'])

    print(data['CB07'][1])

    mes_vals = data['CB07'][1].__dict__.keys()
    print(mes_vals)

    print(vars(data['CB07'][1]))
    print(data['CB07'][1].eye, data['CB07'][1].e_type, )

    print('hi')


if __name__ == '__main__':
    main()

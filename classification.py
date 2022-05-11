import _import as imp
import math
import matplotlib.pyplot as plt
import numpy as np


def features(_id, _data):   # get familiar with data format
    print('---------------')
    print(_id, _data.pop(0))
    for i in _data:
        print(i.date, i.eye, i.e_type, i.flash, i.adaptation)
        """
        print(i.recorded_waveform)
        print(i.raw_waveform)
        print(i.pupil_waveform)
        """


def dot_product(a, b):  # dot product of a and b
    return sum([float(i)*float(j) for (i, j) in zip(a, b)])


def dot_distance(a, b): # pontwise distance
    return math.sqrt(sum([ (float(i) - float(j))**2 for (i, j) in zip(a, b)]))


def plot_features(f):   # draw figures and save
    x = [key for key in f]
    y_all = [f[key] for key in f]
    y = np.array(y_all)
    #print(y_all)
    print(y)
    print('--------------------')
    """
    for i in range(8):
        y_ = y[:, i, 0]
        print(y_)

        plt.bar(x, y_.astype('float'))
        plt.title('dot_prod'+str(i))
        plt.show()
        #plt.savefig('img/dot_prod'+str(i)+'.png')
        #plt.close()
    """


def print_metr(metrics, index):     # examine distance and dot product results
    for m in metrics:
        print('\n',m)
        for i in metrics[m]:
            print(i)
        #print(metrics[m][0])


def intra_distance(data):   # calculate intra-subject metrics
    date = data.pop(0)
    #print(date)
    #print('Left-Right comp.', end=' ')
    dist = []
    for i in range(16):
        if i % 4 != 2 and i % 4 != 3:
            re = data[i].recorded_waveform
            le = data[i+2].recorded_waveform

            try:    # replace nan with (0, 0)
                ind = min(re.last_valid_index(), le.last_valid_index(), 0)
            except:
                dist.append([0, 0])
                continue

            re = re.loc[:ind]
            le = le.loc[:ind]

            RE = re['uV'].values.tolist()
            LE = le['uV'].values.tolist()

            dist.append([dot_product(RE, LE), dot_distance(RE, LE)])

    return dist


def print_ab(ab):
    for e in ab:
        print('\n',e)
        for i in range(5):
            print(ab[e][i*2])
            print(ab[e][i*2 + 1])


def ab_waves(data):     # get waveform data
    dist = []
    for i in range(16):
        if i in [0, 2, 5, 7, 13]:
            a_t, a_A = data[i].a_t, data[i].a_A
            b_t, b_A = data[i].b_t, data[i].b_A

            #print(i)
            #print(a_t, a_A)
            #print(b_t, b_A)
            dist.append([a_t, a_A])
            dist.append([b_t, b_A])
    return dist


def classif_wave(ab):   # give back classification of the data... not work yet
    mean = {}
    x = [key for key in ab]
    y_all = [ab[key] for key in ab]
    y = np.array(y_all)
    y = y[:, :8, :].astype('float')
    mean['a_t'] = np.sum(y[:, 0, 0])/len(x)
    mean['a_t'] = np.sum([y[:, i*2, 0] for i in range(2)])/len(x)
    print(y)
    print([y[:, i*2, 0] for i in range(2)])
    print(mean['a_t'])


def main():
    path = r'C:\Users\Mirdir\PycharmProjects\brain-therapy\data'
    data = imp.read_data(path)
    metr = {}
    ab = {}
    print(data.keys())
    print(len(data.keys()))
    for key in data.keys():
        #print(key)
        #features(key, data[key])
        metr[key] = intra_distance(data[key])
        ab[key] = ab_waves(data[key])

    print('hi')
    print_metr(metr, 1)
    #print_ab(ab)
    #plot_features(ab)
    classif_wave(ab)



if __name__ == '__main__':
    main()

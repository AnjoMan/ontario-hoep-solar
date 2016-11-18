#!usr/bin/python3.5

import pandas
import numpy as np
import matplotlib.pyplot as plt



def main():


    hoep_file = pandas.read_csv("hoep_data.csv", parse_dates=['Date'])


    hoep_filtered = hoep_file.copy()
    hoep_filtered['HOEP'] = filter(hoep_filtered['HOEP'])


    # plt.plot(hoep_file['HOEP'])
    # plt.plot(hoep_filtered['HOEP'])
    # plt.show(block=True)


    daily = day_profile(hoep_file)
    daily_filtered = day_profile(hoep_filtered)
    # #
    # print(daily)
    # print(daily_filtered)
    # plt.plot(daily)
    # plt.plot(daily_filtered)

    #make a histogram of the output
    # n, bins, patchs = plt.hist(hoep_file['HOEP'], 100)
    daily = hoep_file.pivot(index='Date', columns='Hour', values='HOEP')

    mask = ((daily > daily.stack().quantile(0.01)) & (daily < daily.stack().quantile(0.99))).all(axis=1)
    print(mask)

    pctTrue = len([i for i in mask if i])/len(mask)
    print("{:.2f}%".format(pctTrue*100))

    # print(daily[mask])

    plt.plot(daily[mask].transpose())
    plt.plot(daily[mask].mean(axis=0), linewidth=3)

    # for profile, toPlot in zip(daily, mask):
    #     if toPlot:
    #         plt.plot(profile)

    plt.show(block=True)



    # mask = (hoep_file['HOEP'] > hoep_file['HOEP'].quantile(0.025)) & (hoep_file['HOEP'] < hoep_file['HOEP'].quantile(0.975))

    # print(mask)

    # plt.show(block=True)
    #








def day_profile(df):
    daily = df.pivot(index='Date', columns='Hour', values='HOEP')
    return daily.mean(axis=0)



def filter(hoep, show=False):
    #sample rate is 1 sample per hour
    T = 1*60*60
    f_samp = 1/(T)
    f_ny = f_samp / 2

    #filter between 3 and 10 days
    short_days, long_days = 3, 30
    f_high=  1/(2           * 24*60*60)/f_samp
    f_low= 1/(30          * 24*60*60)/f_samp
    b =      1/(13          * 24*60*60)/f_samp
    N = int(np.ceil(12/b))
    if not N%2: N+= 1
    n = np.arange(N)


     # Compute a low-pass filter with cutoff frequency fL.
    hlpf = np.sinc(2 * f_low * (n - (N - 1) / 2.))
    hlpf *= np.blackman(N)
    hlpf /= np.sum(hlpf)

    # Compute a high-pass filter with cutoff frequency fH.
    hhpf = np.sinc(2 * f_high * (n - (N - 1) / 2.))
    hhpf *= np.blackman(N)
    hhpf /= np.sum(hhpf)
    hhpf = -hhpf
    hhpf[(N - 1) / 2] += 1

    # Add both filters.
    h = hlpf + hhpf
    # h = hhpf

    hoep_f = np.convolve(hoep, h, mode="same")

    if show:
        orig, = plt.plot(hoep)
        filt, = plt.plot(hoep_f)



        plt.legend([orig, filt], 'HOEP', 'weather-adjusted')
        plt.show(block=True)
    return hoep_f





if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

class impulse:
    def __init__(self):
        self.freq = 0;

    def set_freq(self, Fi):
        self.freq = Fi

class FOFlet:
    def __init__(self):
        self.beta = 0
        self.alpha = 0
        self.BW = 0
        self.k1 = 0
        self.Fc = 0
        self.Fs = 44100
        self.Ts = 1/self.Fs
        self.FOFlet = []

    def set_beta(self, beta_val):
        self.beta = beta_val
    def set_alpha(self, alpha_val):
        self.alpha = alpha_val
    def set_BW(self, BW_val):
        self.BW = BW_val
    def set_k1(self, k1_val):
        self.k1 = k1_val
    def set_Fc(self, Fc_val):
        self.Fc = Fc_val
    def set_Fs(self, Fs_val):
        self.Fs = Fs_val

    def update_FOFlet(self, alpha, BW, k1, Fc, Fs, impulse):
        self.set_Fs(Fs)
        self.set_k1(k1*self.Fs)
        self.set_beta(np.pi/self.k1)
        self.set_alpha(alpha)
        self.set_BW(BW)
        self.set_Fc(Fc)

        tmp = []
        for i in range(0,int(self.k1)):
            attack_env = .5 * ( 1 - np.cos(self.beta*i) )
            exponential = np.exp((-self.BW*np.pi*i)/self.Fs)
            msg = np.sin((2*np.pi*self.Fc*i)/Fs)
            tmp.append( attack_env*exponential*msg )
        for i in range(int(self.k1)+1, int(Fs/impulse.freq)):
            decay_env = np.exp((-self.BW*np.pi*i)/self.Fs)
            msg = np.sin((2*np.pi*self.Fc*i)/Fs)
            tmp.append(decay_env * msg)
        self.FOFlet = np.asarray(tmp)

    def plot_FOFlet(self):
        plt.plot(self.FOFlet)
        plt.draw()

    def synthesize(self, impulse):
        return sp.signal.convolve(impulse, self.FOFlet);

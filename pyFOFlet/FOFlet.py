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
    # initialize class with these values
    def __init__(self, BW=60, k1=0.002, Fc=640, Fs=44100):
        self.beta = np.pi/k1
        self.alpha = BW*np.pi
        self.BW = BW
        self.k1 = k1
        self.Fc = Fc
        self.Fs = Fs
        self.Ts = 1/self.Fs
        self.FOFlet = []

    # functions to set values individually
    def set_beta(self):
        self.beta = np.pi/self.k1
    def set_alpha(self):
        self.alpha = self.BW*np.pi
    def set_BW(self, BW_val):
        self.BW = BW_val
        self.set_alpha()
    def set_k1(self, k1_val):
        self.k1 = k1_val
        self.set_beta()
    def set_Fc(self, Fc_val):
        self.Fc = Fc_val
    def set_Fs(self, Fs_val):
        self.Fs = Fs_val
        self.Ts = 1/Fs_val

    # Generate new FOFlet from each impulse time.
    def update_FOFlet(self, Fs, impulse):
        tmp = []
        for i in range(0,int(self.k1*self.Fs)):
            attack_env = .5 * ( 1 - np.cos(self.beta*i*self.Ts) )
            exponential = np.exp((-self.BW*np.pi*i)/self.Fs)
            msg = np.sin((2*np.pi*self.Fc*i)/Fs)
            tmp.append( attack_env*exponential*msg )
        for i in range(int(self.k1*self.Fs)+1, int(Fs/impulse)+1):
            decay_env = np.exp((-self.BW*np.pi*i)/self.Fs)
            msg = np.sin((2*np.pi*self.Fc*i)/Fs)
            tmp.append(decay_env * msg)
        self.FOFlet = np.asarray(tmp)

    def plot_FOFlet(self):
        plt.plot(self.FOFlet)
        plt.draw()

    def synthesize(self, impulse):
        return sp.signal.convolve(impulse, self.FOFlet);

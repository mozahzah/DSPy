# SPDX-License-Identifier: GPL-2.0-only
# Copyright © mozahzah. All rights reserved.
# Author: mozahzah

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

class filter:

    def __init__(self, sampleRate, filterOrder):
        self.sampleRate = sampleRate
        self.filterOrder = filterOrder

    def get_running_mean_filtered_signal(self, signal):
        numSamples = len(signal)
        filteredSignal = np.zeros(numSamples)

        for i in range(self.filterOrder + 1, numSamples - self.filterOrder - 1):
            window = signal[i - self.filterOrder:i + self.filterOrder + 1]
            filteredSignal[i] = np.mean(window)

        return filteredSignal
    
    def draw_gaussian_distribution(self, fullWidthHalfMaximum):
        gTime = np.arange(-self.filterOrder, self.filterOrder + 1)
        gaussian_kernel = np.exp(-(4 * np.log(2) * (gTime**2)) / (fullWidthHalfMaximum**2))
        gaussian_kernel /= np.sum(gaussian_kernel) 
        plt.figure(figsize=(5, 3))
        plt.plot(gTime, gaussian_kernel, label='Gaussian Kernel')
        plt.title('Gaussian Distribution (Probability Density Function)')
        plt.xlabel('x')
        plt.ylabel('Probability Density')
        plt.grid()
        plt.legend()
        plt.show()

    def get_gaussian_filtered_signal(self, signal, fullWidthHalfMaximum):
        numSamples = len(signal)
        filteredSignal = np.zeros(numSamples)

        gTime = np.arange(-self.filterOrder, self.filterOrder + 1)
        gaussian_kernel = np.exp(-(4 * np.log(2) * (gTime**2)) / (fullWidthHalfMaximum**2))
        gaussian_kernel /= np.sum(gaussian_kernel) 

        for i in range(self.filterOrder + 1, numSamples - self.filterOrder - 1):
            window = signal[i - self.filterOrder:i + self.filterOrder + 1]
            filteredSignal[i] = np.sum(window * gaussian_kernel)
        
        return filteredSignal
    
    def get_median_filtered_signal(self, signal, threshold):
        numSamples = len(signal)
        supraThreshold_indices = np.where(signal > threshold)[0]
        filteredSignal = signal.copy()

        for i in supraThreshold_indices:
            lowbnd = max(0, i - self.filterOrder)
            uppbnd = min(i + self.filterOrder + 1, numSamples)
            filteredSignal[i] = np.median(signal[lowbnd:uppbnd])

        return filteredSignal

    def draw_filtered_signal(self, filteredSignal):
        time = np.arange(0, len(filteredSignal)/self.sampleRate, 1/self.sampleRate)
        plt.plot(time, filteredSignal, label='Filtered Signal', color = 'red')
        plt.legend()
        
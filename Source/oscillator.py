# SPDX-License-Identifier: GPL-2.0-only
# Copyright © Interactive Echoes. All rights reserved.
# Author: mozahzah

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('dark_background')

class oscillator:

    def __init__(self,sampleRate):
        self.sampleRate = sampleRate

    def make_sine_signal(self, frequency, amplitude, phase, timeSecond, addNoise=False):
        numsamples = int(timeSecond * self.sampleRate)
        signal = np.zeros(numsamples) 
        time = np.arange(0, timeSecond, 1/self.sampleRate)

        for i in range(0, numsamples):
            signal[i] = amplitude * np.sin(time[i] * 2*np.pi*frequency + phase)
            if (addNoise):
                signal[i] += np.random.uniform(-1, 1)
        
        return signal
    
    def make_square_signal(self, frequency, amplitude, phase, timeSecond, addNoise=False):
        numsamples = int(timeSecond * self.sampleRate)
        signal = np.zeros(numsamples) 
        signal = amplitude * np.sign(self.make_sine_signal(frequency, amplitude, phase, timeSecond, addNoise))
        return signal
    
    def make_triangle_signal(self, frequency, amplitude, phase, timeSecond, addNoise=False):
        numsamples = int(timeSecond * self.sampleRate)
        signal = np.zeros(numsamples) 
        time = np.arange(0, timeSecond, 1/self.sampleRate)

        for i in range(0, numsamples):
            signal[i] = 2 * amplitude * np.abs((time[i] * frequency + phase) % 1 - 0.5)
            # HINT: %1 to get the fractional part 5.75 % 1 = 0.75
            if (addNoise):
                signal[i] += np.random.uniform(-1, 1)
        
        return signal
    
    def make_sawtooth_signal(self, frequency, amplitude, phase, timeSecond, addNoise=False):
        numsamples = int(timeSecond * self.sampleRate)
        signal = np.zeros(numsamples) 
        time = np.arange(0, timeSecond, 1/self.sampleRate)

        for i in range(0, numsamples):
            signal[i] = 2 * amplitude * (time[i] * frequency - np.floor(0.5 + time[i] * frequency + phase))
            if (addNoise):
                signal[i] += np.random.uniform(-1, 1)
        
        return signal

    def draw_oscillator_signal(self, signal, bufferSize=None):
        if bufferSize is None:
            bufferSize = self.sampleRate
        numBuffers = int(np.ceil(len(signal) / bufferSize))

        buffers = np.zeros((numBuffers, bufferSize))
        for i in range(numBuffers):
            startIdx = i * bufferSize
            endIdx = startIdx + bufferSize
            buffer_data = signal[startIdx:endIdx]
            if len(buffer_data) < bufferSize:
                buffer_data = np.pad(buffer_data, (0, bufferSize - len(buffer_data)), mode='constant', constant_values=0)
            buffers[i] = buffer_data

        time = np.arange(0, len(signal)/self.sampleRate, 1/self.sampleRate)
        for i in range(numBuffers):
            startIdx = i * bufferSize
            endIdx = startIdx + bufferSize
            time_slice = time[startIdx:endIdx]
            if len(time_slice) < bufferSize:
                break
            bufferColor = 'blue'
            if i % 2:
                bufferColor = 'green'
            plt.plot(time_slice, buffers[i], color = bufferColor)

        plt.xlabel("Time (seconds)")
        plt.ylabel("Amplitude")
        plt.title("DSPy")
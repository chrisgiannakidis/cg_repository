# -*- coding: utf-8 -*-
"""

@author: Chris Giannakidis
"""

import time

start_time = time.time()


import pandas as pd
import matplotlib.pyplot as plt
import kkantoutsis427


'''In this example of Recurrent Neural Network - Machine Learning, the input
is a second order transfer function:
    
https://en.wikipedia.org/wiki/Transfer_function
https://en.wikibooks.org/wiki/Signals_and_Systems/Second_Order_Transfer_Function
    '''


xlsx_file = pd.ExcelFile('example.xlsx').parse('Sheet1')
Inputs = xlsx_file['Inputs'].values
Targets = xlsx_file['Targets'].values
Inputs_Test = xlsx_file['InputsTest'].values
Targets_Test = xlsx_file['TargetsTest'].values


''' We construct the Recurrent Neural Network'''
''' It will have 1 input, 2 hidden layers with 2 neurons each and 1 output'''

network = kkantoutsis427.construct_RNN([1,2,2,1],delay_Input=[0],delay_Intern=[1],
                          delay_Output=[1,2])


'''We use the Levenberg–Marquardt Algorithm for training
https://en.wikipedia.org/wiki/Levenberg%E2%80%93Marquardt_algorithm'''

''' Also, the default Performance Function is the Mean Absolute Error'''

print("Recurrent neural network is being trained to be able to predict")
print("It uses Levenberg-Marquardt as Training Algorithm")
print("It uses Mean Absolute Error as Performance Function")

network = kkantoutsis427.lm_Algorithm(Inputs,Targets,network,verbose=True,k_max=100,
                             E_stop=1e-3)

targets = kkantoutsis427.output_RNN_b(Inputs,network)
targets_Test = kkantoutsis427.output_RNN_b(Inputs_Test,network)

fig = plt.figure(figsize=(11,7))
ax0 = fig.add_subplot(211)
ax1 = fig.add_subplot(212)
fs=18

print("Elasped time is ",time.time() - start_time, " seconds")

'''Train Data'''
ax0.set_title('Train Data',fontsize=fs)
ax0.plot(targets,color='g',lw=2,label='RNN Output')
ax0.plot(Targets,color='maroon',marker='None',linestyle=':',lw=4, markersize=7,
         label='Train Data')
ax0.tick_params(labelsize=fs-2)
ax0.legend(fontsize=fs-2,loc='upper left')
ax0.grid()

'''Test Data'''
ax1.set_title('Test Data',fontsize=fs)
ax1.plot(targets_Test,color='steelblue',lw=2,label='RNN Output')
ax1.plot(targets_Test,color='black',marker='None',linestyle=':',lw=4,
         markersize=7,label='Test Data')
ax1.tick_params(labelsize=fs-2)
ax1.legend(fontsize=fs-2,loc='upper left')
ax1.grid()

fig.tight_layout()
plt.show()

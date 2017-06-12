from flask import Flask, jsonify, request
import RNNcodeexample  # import ML code sample
import numpy as np
import copy

app = Flask(__name__)

# resource name is RNNaddition. Used to be a noun.
# Method POST.
@app.route('/RNNaddition', methods = ['POST'])
def calculate():
    num1 = request.args.get('number1')
    num2 = request.args.get('number2')

    if isinstance(num1,basestring):
        num1 = int(num1)
        num2 = int(num2)

    num1_bin = RNNcodeexample.int2binary[num1]
    num2_bin = RNNcodeexample.int2binary[num2]

    c = num1+num2
    c_bin = RNNcodeexample.int2binary[c]

    d = np.zeros_like(num2_bin)
    overallError = 0  # initial error

    binary_dim = RNNcodeexample.binary_dim

    # to store hidden value at each timestamp
    layer_1_values = list()
    #initial values are 0 
    layer_1_values.append(np.zeros(RNNcodeexample.hidden_dim))  

    synapse_0 = RNNcodeexample.synapse_0
    synapse_h = RNNcodeexample.synapse_h
    synapse_1 = RNNcodeexample.synapse_1

	# use the trained model to predict each binary value of the adding result.
    for position in range(binary_dim):
        X = np.array([[num1_bin[binary_dim - position - 1], num2_bin[binary_dim - position - 1]]]) 
        layer_1 = RNNcodeexample.sigmoid(np.dot(X, synapse_0) + np.dot(layer_1_values[-1], synapse_h))  
        layer_2 = RNNcodeexample.sigmoid(np.dot(layer_1, synapse_1))  

        d[binary_dim - position - 1] = np.round(layer_2[0][0])  
        layer_1_values.append(copy.deepcopy(layer_1)) 
        
    out = 0
    for index,x in enumerate(reversed(d)):
        out += x*pow(2,index)

    return_result = {'num1':num1, 'num2':num2, 'pred_bin':str(d), 'pred_num':out, 'true_bin':str(c_bin), 'true_num':c}

    return jsonify(return_result)

if __name__ == '__main__':
    app.run(debug=True)

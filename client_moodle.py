import json
import requests
import numpy as np
import ast
f = open("./output.txt", "a")
with open("./output.json", "r") as fp:
    input_str = json.load(fp)
# list_old = ast.literal_eval(input_str)
# input_str = []
list_old = input_str

######### DO NOT CHANGE,"" ANYTHING IN THIS FILE ##################
API_ENDPOINT = 'http://10.4.21.147'
PORT = 3000
MAX_DEG = 11
overfit_original = [0.0, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 8.132366097133624e-05, -6.018769160916912e-05, -1.251585565299179e-07, 3.484096383229681e-08, 4.1614924993407104e-11, -6.732420176902565e-12]
# overfit_original = [4.1614924993407104e-11, 0.1240317450077846, -6.211941063144333, 0.04933903144709126, 0.03810848157715883, 3.484096383229681e-08, -6.018769160916912e-05, -1.251585565299179e-07, 0.0, 8.132366097133624e-05, -6.732420176902565e-12]


#### functions that you can call
def get_errors(id, vector):
    """
    returns python array of length 2 
    (train error and validation error)
    """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG

    return json.loads(send_request(id, vector, 'geterrors'))

def submit(id, vector):
    """
    used to make official submission of your weight vector
    returns string "successfully submitted" if properly submitted.
    # """
    for i in vector: assert -10<=abs(i)<=10
    assert len(vector) == MAX_DEG
    return send_request(id, vector, 'submit')

#### utility functions
def urljoin(root, port, path=''):
    root = root + ':' + str(port)
    if path: root = '/'.join([root.rstrip('/'), path.rstrip('/')])
    return root

def send_request(id, vector, path):
    api = urljoin(API_ENDPOINT, PORT, path)
    vector = json.dumps(vector)
    response = requests.post(api, data={'id':id, 'vector':vector}).text
    if "reported" in response:
        print(response)
        exit()

    return response


if __name__ == "__main__":
    """
    Replace "test" with your secret ID and just run this file 
    to verify that the server is working for your ID.
    """
    size_of_population = 4932
    pop_size = (size_of_population, MAX_DEG)
    new_pop_1 = np.array([overfit_original])
    # new_pop_1 = np.empty([1,11],dtype=float)
    # new_pop_1 = np.vstack((new_pop_1, overfit_original))
    # print(new_pop_1)
    # print("\n")
    for i in range(1, size_of_population):
        l = []
        # temp = list(new_pop_1[i])
        temp = new_pop_1.tolist()
        # print(temp)
        for j in range(MAX_DEG):
            a = np.random.uniform(-1e-15, 1e-15)
            # a = overfit_original[j] + a
            a = a + temp[i-1][j]
            l.append(a)
        new_pop_1 = np.vstack((new_pop_1, l))

    # print(new_pop_1)
# *********************************************************************************************
    # new_pop = np.random.uniform(low=-10, high=10, size=pop_size)
    # new_pop_1 = new_pop_1.tolist()
    # final = []
    # for i in range(size_of_population):
    #     # new_pop[i]=new_pop[i].tolist()
    #     err = get_errors('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', new_pop_1[i])
    #     temp_list = [new_pop_1[i], err]
    #     # final.append(temp_list)
    #     list_old.append(temp_list)
    #     assert len(err) == 2
    #     # print("err")
    #     # print(err)
    #     str1 = ""
    #     str1 = str(err[0]) + " , " + str(err[1]) # [ [[array], err], [[]]]
    #     f.write(str1)
    #     f.write("\n")
# ***********************************************************************************************      
    for i in range(len(list_old)):
        e = list_old[i][1][1] - list_old[i][1][0]
        list_old[i].append(e)

     
        
    # submit_status = submit('JtabQSXoKd2CihU78SWRmmvFUqe7N2yFho55eMMQbplTwMGxus', vector)
    # assert "submitted" in submit_status
    # print("sumbit status")
    # print(submit_status)
    f.close()
    list_old = sorted(list_old, key=lambda x: (x[2]))  ## sorting according to first error
    # temp_3 = []
    # for i in range(1):
    #     temp_3.append(list_old[i][0])
    # print(temp_3)
    
    
    
    
    
    
    
    
    with open("./output.json", 'w') as fp_3:
        json.dump(list_old, fp_3, indent=2)
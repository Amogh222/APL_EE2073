import numpy as np


def evalSpice(filename):
    try:
        f = open(filename, 'r')
    except FileNotFoundError:
        raise FileNotFoundError('Please give the name of a valid SPICE file as input')
    data = f.readlines()

    # Filtering the Text File
    end_i = None
    start_i = None
    data_refined = []
    for line in range(0, len(data)):
        data_refined.append(data[line].strip("\n"))
        if data[line] == ".circuit\n":
            start_i = line
        if data[line] == ".end\n":
            end_i = line
    if start_i is None or end_i is None:
        raise ValueError("Malformed circuit file")

    # Data_refined stores the data between the .circuit and .end in form of list of strings
    data_refined = list(filter(None, data_refined[start_i+1:end_i]))

    # data_list will keep the data in 3 nested lists of voltage, resistance and current and raise error if anything else
    # is input in the file like Inductor
    data_list = [[], [], []]
    for line in data_refined:
        if line[0] == "V" or line[0] == 'v':
            data_list[0].append(line)
        elif line[0] == "I" or line[0] == 'i':
            data_list[2].append(line)
        elif line[0] == "R" or line[0] == 'r':
            data_list[1].append(line)
        else:
            raise ValueError("Only V, I, R elements are permitted")

    # data_dic is a list that will store 3 dictionary of the 3 circuit elements  with the format
    # {name:[node1, node2, dc or ac, value]}
    # node_list stores the total unique nodes except GND
    data_dic = [{}, {}, {}]
    node_list = []

    # Parsed data being added to data_dic
    for i in range(3):
        data_dic[i] = parse(data_list[i])
        put_node(data_dic[i], node_list)
    node_list = sorted(set(node_list))

    # Ensuring GND is present if not then name a node as GND
    if "GND" not in node_list:
        gnd_node = node_list[-1]
        node_list[-1] = "GND"
        # Changing the last node to GND code here
        for dic in data_dic:
            for key in dic:
                if dic[key][0] == gnd_node:
                    dic[key][0] = "GND"
                if dic[key][1] == gnd_node:
                    dic[key][1] = "GND"

    node_list.remove("GND")
    total_nodes = len(node_list)

    # Unknowns is the total nodes + no. of voltage sources
    unknowns = total_nodes + len(data_dic[0])

    # The two matrix to be solved are created here and the value will be filled by the functions down below
    admittance_matrix = np.zeros(shape=(unknowns, unknowns), dtype=float)
    ind_matrix = np.zeros(shape=(unknowns, 1), dtype=float)

    # The 3 functions that put the respective circuit elements in effect in both the matrices
    current_matrix(data_dic[2], ind_matrix, node_list)
    resist_matrix(data_dic[1], admittance_matrix, node_list)
    voltage_matrix(data_dic[0], admittance_matrix, node_list, ind_matrix)

    # gauss elimination function which gives me all the unknowns that we have to find
    gauss(admittance_matrix, ind_matrix)

    # Formatting the result list
    final_list = [{}, {}]
    for line in range(total_nodes):
        final_list[0][node_list[line]] = ind_matrix[line][0]
    for line in data_dic[0]:
        j = 0
        final_list[1][line] = ind_matrix[total_nodes + j][0]
        j += 1
    final_list[0].update({"GND": 0})

    return final_list[0], final_list[1]


def gauss(a, b):
    # Raises an error if the matrix is singular that is when circuit is insolvable
    for row in range(len(a)):
        norm = a[row][row]
        if norm == 0:
            raise ValueError("Circuit error: no solution")
        a[row] = a[row] / norm
        b[row] = b[row] / norm
        for i in range(len(a)):
            if i != row:
                norm = a[i][row]
                a[i] = a[i] - a[row] * norm
                b[i] = b[i] - b[row] * norm
    return b


def current_matrix(i_dic, independent_matrix, nodes):
    for i_name in i_dic:
        if i_dic[i_name][0] != "GND":
            independent_matrix[nodes.index(i_dic[i_name][0])] -= float(i_dic[i_name][-1])
        if i_dic[i_name][1] != "GND":
            independent_matrix[nodes.index(i_dic[i_name][1])] += float(i_dic[i_name][-1])


def resist_matrix(r_dic, admittance_matrix, nodes):
    # To handle the case of R = 0 I have added the resistance as 1e-10 which gives me accurate value upto .0000001
    for res_name in r_dic:
        if "GND" not in r_dic[res_name]:
            if r_dic[res_name][-1] != '0':
                admittance_matrix[nodes.index(r_dic[res_name][0])][nodes.index(r_dic[res_name][0])] += float(1 / float(r_dic[res_name][-1]))
                admittance_matrix[nodes.index(r_dic[res_name][0])][nodes.index(r_dic[res_name][1])] -= float(1 / float(r_dic[res_name][-1]))
                admittance_matrix[nodes.index(r_dic[res_name][1])][nodes.index(r_dic[res_name][1])] += float(1 / float(r_dic[res_name][-1]))
                admittance_matrix[nodes.index(r_dic[res_name][1])][nodes.index(r_dic[res_name][0])] -= float(1 / float(r_dic[res_name][-1]))
            else:
                admittance_matrix[nodes.index(r_dic[res_name][0])][nodes.index(r_dic[res_name][0])] += 1e10
                admittance_matrix[nodes.index(r_dic[res_name][0])][nodes.index(r_dic[res_name][1])] -= 1e10
                admittance_matrix[nodes.index(r_dic[res_name][1])][nodes.index(r_dic[res_name][1])] += 1e10
                admittance_matrix[nodes.index(r_dic[res_name][1])][nodes.index(r_dic[res_name][0])] -= 1e10
        if r_dic[res_name][0] == "GND":
            if r_dic[res_name][-1] != '0':
                admittance_matrix[nodes.index(r_dic[res_name][1])][nodes.index(r_dic[res_name][1])] += float(1 / float(r_dic[res_name][-1]))
            else:
                admittance_matrix[nodes.index(r_dic[res_name][1])][nodes.index(r_dic[res_name][1])] += 1e10
        if r_dic[res_name][1] == "GND":
            if r_dic[res_name][-1] != '0':
                admittance_matrix[nodes.index(r_dic[res_name][0])][nodes.index(r_dic[res_name][0])] += float(1 / float(r_dic[res_name][-1]))
            else:
                admittance_matrix[nodes.index(r_dic[res_name][0])][nodes.index(r_dic[res_name][0])] += 1e10


def voltage_matrix(v_dic, admittance_matrix, node_list, out_mat):
    # This unknown node keeps the track of the position of current thru sources in the matrix
    unknown_index = len(node_list)
    for v_name in v_dic:
        if "GND" not in v_dic[v_name]:
            admittance_matrix[node_list.index(v_dic[v_name][0])][unknown_index] += 1
            admittance_matrix[node_list.index(v_dic[v_name][1])][unknown_index] += -1
            admittance_matrix[unknown_index][node_list.index(v_dic[v_name][0])] += 1
            admittance_matrix[unknown_index][node_list.index(v_dic[v_name][1])] += -1
            out_mat[unknown_index] += float(v_dic[v_name][-1])
            unknown_index += 1
        else:
            if v_dic[v_name][0] == "GND":
                admittance_matrix[node_list.index(v_dic[v_name][1])][unknown_index] += -1
                admittance_matrix[unknown_index][node_list.index(v_dic[v_name][1])] += -1
            else:
                admittance_matrix[node_list.index(v_dic[v_name][0])][unknown_index] += 1
                admittance_matrix[unknown_index][node_list.index(v_dic[v_name][0])] += 1
            out_mat[unknown_index] += float(v_dic[v_name][-1])
            unknown_index += 1


def parse(data_list):
    # Here all the handled errors will be written in the md/pdf file
    result = {}
    for i in range(len(data_list)):
        # dummy stores the string of each circuit element
        dummy = (data_list[i]).split("#")
        dummy = dummy[0].split()
        if len(dummy) > 5:
            raise ValueError("Malformed circuit file")
        try:
            float(dummy[-1])
        except ValueError:
            raise ValueError("Malformed circuit file")
        if dummy[0] in result:
            raise ValueError("Malformed circuit file")
        if dummy[0][0] == "R" or dummy[0][0] == "r":
            if len(dummy) > 4:
                raise ValueError("Malformed circuit file")
            if float(dummy[3]) < 0:
                raise ValueError("Malformed circuit file")
        else:
            if dummy[-2] == "ac":
                raise ValueError("Malformed circuit file")
        result.update({dummy[0]: dummy[1:]})

    return result


def put_node(dic, node_list):
    for key in dic:
        node_list.append(dic[key][0])
        node_list.append(dic[key][1])

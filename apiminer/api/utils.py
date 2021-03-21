import socket


def get_inform_gpu(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((host, port))
    except socket.error as e:
        return [e]

    # count gpu
    sock.send(b'config')
    count_gpu = int(sock.recv(1048).decode().split(',')[5].split('=')[1])
    print(count_gpu)
    sock.close()
    data_list = []
    for gpu in range(count_gpu):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((host, port))
        except socket.error as e:
            return [e]
        command = f'gpu|{gpu}'
        sock.send(command.encode())
        data = sock.recv(1048).decode().split(',')
        sock.close()

        gpu_dict = {
            'Msg': data[3],
            'Enabled': data[5],
            'Temperature': data[7],
            'Fan_Speed': data[8],
            'Fan_Percent': data[9],
            'GPU_Clock': data[10],
            'Memory_Clock': data[11],
            'GPU_Voltage': data[12],
            'GPU_Activity': data[13],
            'MHS': data[15],
            'MHS_30s': data[16],
            'Accepted': data[19],
            'Rejected': data[20],
            'Hardware_Errors': data[21],
        }
        data_list.append(gpu_dict)
    return data_list

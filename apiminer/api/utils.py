import socket


def _get_value_from_string(string: str) -> str:
    return string.split('=')[-1]


def _sending_server(host, port, command) -> list:

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        sock.send(command.encode())
        request = sock.recv(1048).decode().split(',')
        sock.close()
    except socket.error as e:
        return [False, e]
    return request


def get_inform_gpu(host, port):
    data = _sending_server(host, port, 'config')
    if not data[0]:
        return False
    count_gpu = int(_sending_server(host, port, 'config')[5].split('=')[1])
    data_list = []
    for gpu in range(count_gpu):
        command = f'gpu|{gpu}'
        data = _sending_server(host, port, command)
        if not data[0]:
            return False
        if list(data) == 1:
            return ['connect error']
        gpu_dict = {
            'Msg': _get_value_from_string(data[3]),
            'Enabled': _get_value_from_string(data[5]),
            'Temperature': _get_value_from_string(data[7]),
            'Fan_Speed': _get_value_from_string(data[8]),
            'Fan_Percent': _get_value_from_string(data[9]),
            'GPU_Clock': _get_value_from_string(data[10]),
            'Memory_Clock': _get_value_from_string(data[11]),
            'GPU_Voltage': _get_value_from_string(data[12]),
            'GPU_Activity': _get_value_from_string(data[13]),
            'MHS': _get_value_from_string(data[15]),
            'MHS_30s': _get_value_from_string(data[16]),
            'Accepted': _get_value_from_string(data[19]),
            'Rejected': _get_value_from_string(data[20]),
            'Hardware_Errors': _get_value_from_string(data[21]),
        }
        data_list.append(gpu_dict)
    return data_list


if __name__ == '__main__':
    host = 'abrep.ddns.net'
    port = 7776
    print(get_inform_gpu(host, port))

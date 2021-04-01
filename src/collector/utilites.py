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
        print(e)
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
            'msg': _get_value_from_string(data[3]),
            'enabled': _get_value_from_string(data[5]),
            'temperature': _get_value_from_string(data[7]),
            'fan_speed': _get_value_from_string(data[8]),
            'fan_percent': _get_value_from_string(data[9]),
            'gpu_clock': _get_value_from_string(data[10]),
            'memory_clock': _get_value_from_string(data[11]),
            'gpu_voltage': _get_value_from_string(data[12]),
            'gpu_activity': _get_value_from_string(data[13]),
            'mhs': _get_value_from_string(data[15]),
            'mhs_30s': _get_value_from_string(data[16]),
            'accepted': _get_value_from_string(data[19]),
            'rejected': _get_value_from_string(data[20]),
            'error': _get_value_from_string(data[21]),
        }
        data_list.append(gpu_dict)
    return data_list


if __name__ == '__main__':
    host = 'abrep.ddns.net'
    port = 26541
    informer_data = get_inform_gpu(host, port)

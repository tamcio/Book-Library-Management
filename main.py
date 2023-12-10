from multiprocessing import Process
from interface import server_function, interface_function

if __name__ == '__main__':
    server_process = Process(target=server_function)
    interface_process = Process(target=interface_function)

    server_process.start()
    interface_process.start()
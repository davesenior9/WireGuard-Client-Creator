#!/usr/bin/python3
import os

def key_generate(client_number):
    cmd = os.system(f'mkdir /etc/wireguard/clients/client{client_number}')
    cmd = os.system(f'umask 077; wg genkey | tee /etc/wireguard/clients/client{client_number}/privatekey | wg pubkey > /etc/wireguard/clients/client{client_number}/publickey')

def user_generate(client_number, description):
    with open(f'/etc/wireguard/clients/client{client_number}/privatekey', 'r') as f:
        private_key = f.read()
        private_key = str(private_key)
    default_data = [(f'#Client{client_number} = {description}\n'),'[Interface]\n', (f'PrivateKey = {private_key}'), (f'Address = 192.168.100.{client_number}/32\n'), 'DNS = 1.1.1.1\n', '\n'>
    with open(f'/etc/wireguard/clients/client{client_number}/client.conf', 'w') as f:
        f.writelines(default_data)
        f.close

def server_side(client_number,description):
    with open(f'/etc/wireguard/clients/client{client_number}/publickey', 'r') as f:
        public_key = f.read()
        public_key = str(public_key)

    default_data = ['\n','[Peer]\n', (f'#{description}\n'), (f'AllowedIPs = 192.168.100.{client_number}/32\n'), (f'PublicKey = {public_key}\n')]
    with open(f'/etc/wireguard/wg0.conf', 'a') as f:
        f.writelines(default_data)
        f.close
    cmd = os.system('systemctl restart wg-quick@wg0')

def qr_code_generate():
    cmd = os.system(f'qrencode -t ansiutf8 < /etc/wireguard/clients/client{client_number}/client.conf')


while True:
    try:
        print ('\n')
        cmd = os.system('ls /etc/wireguard/clients')
        print ('\n')
        client_number = input('What is the Client Number?\n')
        description = input('What is the Description of the Client?\n')
        key_generate(client_number)
        user_generate(client_number, description)
        server_side(client_number, description)
        while True:
            qr_code = input('Do you want to generate a QR Code?(y/n)\n')
            if qr_code == 'y':
                qr_code_generate()
                break
            elif qr_code == 'n':
                break
            else:
                print (f'You entered {qr_code}. Enter "y" or "n"\n')
        restart = input('Do you want to make another Client?(y/n)\n')
        if restart == 'y':
            pass
        else:
            break
    except KeyboardInterrupt:
        print ('\nKeyboard Break')
        break


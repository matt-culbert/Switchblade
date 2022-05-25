From Switchblade to Swiss Army Knife. This is a Python based Beacon/C2 combo that is designed for Linux systems. It can open a shell back to the C2 communicating either with headers or with websockets.

# To Use #
Set the Nginx sites-enabled default listen to 8081 and use either of the Nginx configs for what you're aiming to do

Setup:

Drop c2.py in your /var/www/html folder and start it.

Inside /etc/nginx/conf.d/nginx.conf, copy one of the premade config files. For testing, the standard nginx.conf will be sufficient. 

When using mTLS:

Generate certs with the following

```
openssl genrsa -out ca.key 2048 

openssl req -new -x509 -days 365 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt

openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=_*.example.com" -out server.csr 

openssl x509 -req -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com") -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt 
```
Ensure required ports are open.

Compile the beacon.py into an executable using auto-py-to-exe and send it to the target.

 - Sending the beacon.py can typically be done with a staged dropper powershell script that will retrieve it and run it in the proper context.


# ToDo #

- [ ] Add base64 encoding for back and forth beacon/c2 communication
- [ ] Create DLL for communication alternative
- [x] Add shellcode injection
- [ ] Combine our two python beacon scipts into one, make sure there is a dynamic switch between the two modes

From Switchblade to Swiss Army Knife. This is a Python based Beacon/C2 combo that is designed for Linux systems. It can open a shell back to the C2 communicating either with headers or with websockets.

# To Use #
Set the Nginx sites-enabled default listen to 8081 and use either of the Nginx configs for what you're aiming to do

When using mTLS:

Generate certs with the following

```
openssl genrsa -out ca.key 2048 

openssl req -new -x509 -days 365 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt

openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=_*.example.com" -out server.csr 

openssl x509 -req -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com") -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt 
```

ToDo

- [ ] Add base64 encoding for back and forth beacon/c2 communication
- [ ] Add setting for OTP communication
- [ ] Combine our two python beacon scipts into one, make sure there is a dynamic switch between the two modes

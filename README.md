# LIA CAR
## OS
* user: pi
* hostname: liacar
* password: raspberry

### Config auto-launch
#### Setup service
```sh
cp lia_car.service /etc/systemd/system/lia_car.service
systemctl enable lia_car
```
#### Stop service
```sh
systemctl stop lia_car
```

#### Get logs
```sh
systemctl status lia_car
```

## Network
* SSID: carrinho_lia
* password: emclia2023
* host: 192.168.13.1

## How to run
```sh
systemctl stop lia_car
python3 run.py
```


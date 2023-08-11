# LIA CAR
## OS
user: pi
hostname: liacar
password: raspberry

### Config auto-launch
#### Setup service
```sh
cp lia_car.service /etc/systemd/system/lia_car.service
systemctl enable lia_car
```
#### Stop service
systemctl stop lia_car

#### Get logs
systemctl status lia_car

## Network
SSID: carrinho_lia
password: emclia2023
host: 192.168.13.1

## Train HAAR
1. Prepare negatives
2. Prepare positives
3. Train

## How to run
```sh
python3 run.py
```


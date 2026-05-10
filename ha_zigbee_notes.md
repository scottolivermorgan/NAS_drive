# SLZB-MR1U setup
- plug in
- terminal `ip addr`
- find local network - in this case 192.168.2.154/24 
- terminal nmap local network to find device so `nmap 192.168.2.154/24`
- device exposes webserver so try - in this case is `http://192.168.2.137`
- update firmware via GUI -> settings & Tools -> firmware update.
- not tcp port - usually 6638
- go to home assitant GUI -> Devices & Services -> should have auto discovered.
- click add device

# zha
- got to settings & devices -> add integration
- search zha and click it
  - for radio type select `EZSP`
  - in serial device path `socket://192.168.2.137:6638`
  - select auto configure
  


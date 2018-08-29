# Work in progress!
#home_assistant_gardena

Custom component to support Gardena smart devices.

It supports the devices:

## Sileno smart mower
It auto discovers mowers and adds them as a vacum cleaner.
The vacum cleaner is the closest thing to a lawn mower, it has characteristics like a base station, being a robot, supports simular command (stop, start, dock) and has battery status.

![alt screenshot](https://raw.githubusercontent.com/wijnandtop/home_assistant_gardena/master/doc/screenshot1.png)

## Usage

Just copy the content of this repo to

```
[your home-assistant-path]/config/custom_components
```

Add these lines in your configuration.yml

```
gardena:
  username : !secret gardena_user
  password : !secret gardena_password
```

Of course you need to make sure you have the secrets available.

##TODO

* Create separate pypi module for pygardena
* submit component to home-assistant
    * Validate if all requirements are met 
* support smart sensor https://www.gardena.com/int/products/smart/smart-system/gardena-smart-sensor/967044801/
* support smart water control https://www.gardena.com/int/products/smart/smart-system/gardena-smart-water-control/967045101/
* fetch garden image
* nice lovelace display for a garden / location

## tested with:
 
 * Mower: Sileno smart (the one with a working capacity of 1000m2)
 
## not planned yet
Since I do not own the devices.

* Smart pressure pump
* smart power adapter
* smart battery
* smart irrigation control (is on my wishlist)




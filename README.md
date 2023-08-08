# ryu-slicing
this repository contains the ryu code for the 5G-network slicing, using the application based slicing


## About the code
- In this code which server will respond will be based on the port number.
- If the port number is 9999, it will go to our server.
- If it is any other port it will go to the router.


## Dependencies
* python3
```
apt install python3
```
* ryu
```
pip install ryu
```

## To run the code
```
ryu-manager --observe-links <file_name>
```

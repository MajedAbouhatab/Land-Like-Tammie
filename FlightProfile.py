import requests as REST
import json

GatewayURL='https://ns01-api.brainium.com/api/v1/gateways/1285-2872-9190-3985'
DeviceURL='https://ns01-api.brainium.com/api/v1/devices/TO136-0202100001000901'
headers={'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJuczAxIiwic3ViIjoiMjUxNCIsInVzZXJfbmFtZSI6ImFib3VoYXRhYkB5YWhvby5jb20iLCJzY29wZSI6WyJyZWFkLW9ubHkiXSwiZXhwIjoxNjIwNDA5MTE4LCJhdXRob3JpdGllcyI6WyJST0xFX1VTRVIiXSwianRpIjoiZjA0MzIzN2ItZDg3Ny00ZDNjLWExZmYtYWY0NWE3MmJiMDE5IiwiY2xpZW50X2lkIjoicmVhZC1vbmx5In0.u7LcGXSm_cGKWPec7bJOK_7f0fFCe7SLyjcwAx8dbRk'}

def IsConnected(x):
    return eval(str(json.loads(REST.request('GET',x,headers=headers).text)['connected']))
    
while True:
    # Wait for Gateway to connect
    if IsConnected(GatewayURL):
        # Wait for Device to connect
        if IsConnected(DeviceURL):
            # Start logging
            import CoreFP
        else:
            print('Connect your Device')
    else:
        print('Connect your GW')
            

import bluetooth
import sys
from bluetooth.btcommon import BluetoothError
import time
import re

def finddevice():

    print("Performing inquiry...")
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
    print("Found {} devices".format(len(nearby_devices)))
    for addr, name in nearby_devices:
        try:
            print("   {} - {}".format(addr, name))
        except UnicodeEncodeError:
            print("   {} - {}".format(addr, name.encode("utf-8", "replace")))
    # for addr, name in nearby_devices:
    #     print("  %s - %s" % (addr, name))
    #
    #     services = bluetooth.find_service(address=addr)
    #     for svc in services:
    #         print("Service Name: %s" % svc["name"])
    #         print("    Host:        %s" % svc["host"])
    #         print("    Description: %s" % svc["description"])
    #         print("    Provided By: %s" % svc["provider"])
    #         print("    Protocol:    %s" % svc["protocol"])
    #         print("    channel/PSM: %s" % svc["port"])
    #         print("    svc classes: %s " % svc["service-classes"])
    #         print("    profiles:    %s " % svc["profiles"])
    #         print("    service id:  %s " % svc["service-id"])
    #         print("")

    return nearby_devices
def connect(nearby_devices):
    for addr, name in nearby_devices:
        addr_target='7C:9E:BD:6D:C5:2E'
        if addr_target=='7C:9E:BD:6D:C5:2E':
            #addr_target=addr
            print(addr_target)
            sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            try:
                sock.connect((addr_target,1))
                print("Connection successful. Now ready to get the data")
                count=0
                encoder_A = []
                encoder_B = []
                encoder_C = []
                encoder_D = []
                angel_x = []
                angel_y = []
                while(1):
                    data_send='5'
                    sock.send(data_send)
                    data = sock.recv(1024)
                    data = str(data, 'utf-8')
                    print(data)



                    start_time=time.time()
                    #print("开始时间：",start_time)

                    count+=1
                    end_time=time.time()
                    #print("结束时间：",end_time)
                    #print("接受数据用时：",end_time-start_time)
            except BluetoothError as e:
                print("fail\n")


if __name__ == '__main__':
    nearby_devices = finddevice()
    connect(nearby_devices)
    #rec()
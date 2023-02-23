from pymodbus.client import ModbusTcpClient

class client:

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.modbusConnect()  

    def modbusConnect(self):
        self.connection = ModbusTcpClient(self.ip,self.port)
        self.connection.connect()

    def isAlive(self):
        return self.connection.is_socket_open()

    def modbusDisconnet(self):
        self.connection.close()
        return self.connection.is_socket_open()

    def readFromTextRegister(self,regStart,regCount,slaveID):
        try:
            registers = self.connection.read_holding_registers(regStart,regCount,slaveID).registers
            value=""
            for i in registers:
                if(i!=0):
                    registerValue= bytes.fromhex((hex(i))[2:]).decode("ASCII")
                    value=value+registerValue
            return registers,value
        except:
            print("Could not properly read registers")
            
    def writeToTextResigter(self,regStart,regCount,slaveID,payload):
        regBefore,valueBefore=self.readFromTextRegister(regStart,regCount,slaveID)
        returns=self.connection.write_registers(regStart,payload,slaveID) 
        if(str(returns).startswith("Exception")):
            raise Exception
        else:
            print("Values before changes:\n{}\n{}".format(regBefore,valueBefore))
            regAfter,valueAfter=self.readFromTextRegister(regStart,regCount,slaveID)
            print("Values after changes:\n{}\n{}".format(regAfter,valueAfter))
           
    def __del__(self):
        print("destructor called, object destroyed") 
    
    
def main():
    modbusDevice = client("192.168.1.1",502)
    if modbusDevice.isAlive():
        try:
            payload=[21077, 21592, 20037, 22272]
            modbusDevice.writeToTextResigter(71,16,1,payload)
        except:
            print("Modbus write error")
        if modbusDevice.modbusDisconnet():
            print("Connection did not close")
        else:
            print("Client disconnected")
    else:
        print("Connection with slave device was not established")
    del modbusDevice

if __name__ == "__main__":
    main()
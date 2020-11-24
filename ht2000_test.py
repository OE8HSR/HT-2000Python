import time
import datetime
import array, fcntl, struct, termios, os, sys

# constant for linux portability
_IOC_NRBITS = 8
_IOC_TYPEBITS = 8

# architecture specific
_IOC_SIZEBITS = 14
_IOC_DIRBITS = 2

_IOC_NRMASK = (1 << _IOC_NRBITS) - 1
_IOC_TYPEMASK = (1 << _IOC_TYPEBITS) - 1
_IOC_SIZEMASK = (1 << _IOC_SIZEBITS) - 1
_IOC_DIRMASK = (1 << _IOC_DIRBITS) - 1

_IOC_NRSHIFT = 0
_IOC_TYPESHIFT = _IOC_NRSHIFT + _IOC_NRBITS
_IOC_SIZESHIFT = _IOC_TYPESHIFT + _IOC_TYPEBITS
_IOC_DIRSHIFT = _IOC_SIZESHIFT + _IOC_SIZEBITS

_IOC_NONE = 0
_IOC_WRITE = 1
_IOC_READ = 2


def _IOC(dir, type, nr, size):
    if isinstance(size, str):
        size = struct.calcsize(size)
    return dir  << _IOC_DIRSHIFT  | \
            type << _IOC_TYPESHIFT | \
            nr   << _IOC_NRSHIFT   | \
        size << _IOC_SIZESHIFT


def _IO(type, nr): return _IOC(_IOC_NONE, type, nr, 0)
def _IOR(type, nr, size): return _IOC(_IOC_READ, type, nr, size)
def _IOW(type, nr, size): return _IOC(_IOC_WRITE, type, nr, size)
def _IOWR(type, nr, size): return _IOC(_IOC_READ | _IOC_WRITE, type, nr, size)




def readHT():
    fd= open("/dev/hidraw0", "r+")
    buf = bytearray(256)
    buf[0] = 0x05
    buf[1] = 0xff
    buf[2] = 0xff
    buf[3] = 0xff
    res = fcntl.ioctl(fd, _IOC(_IOC_READ | _IOC_WRITE, 0x48, 0x06, 4), buf, 1)
    buf = bytearray(256)
    buf[0] = 0x05
    res = fcntl.ioctl(fd, _IOC(_IOC_READ | _IOC_WRITE, 0x48, 0x07, 256), buf, 1)
    fd.close()
    return(buf)

"""seconds = int(buf[1]) * 16777216 + int(buf[2]) * 65536 + int(buf[3]) * 256 + int(buf[4])
seconds = seconds - 2004450700
print(seconds)"""

def decodeHT(buf):
    temp = int(buf[7]) * 256 + int(buf[8])
    temp = temp - 400
    temp = temp / 10
    #print("Temp.: ", temp, "°C")

    rh = int(buf[9]) * 256 + int(buf[10])
    rh = rh / 10
    #print("Relative Humidity: ", rh, "%")

    co = int(buf[24]) * 256 + int(buf[25])
    #print("CO2: " , co, "ppm")
    return([temp, rh, co])



while True:
    liste = decodeHT(readHT())
    print(liste)
    datei = open("env.log", "a")
    datei.write(str(datetime.datetime.now()))
    datei.write(" ")
    datei.write("Temp.: ")
    datei.write(str(liste[0]))
    datei.write(" ")
    datei.write("Humidity: ")
    datei.write(str(liste[1]))
    datei.write(" ")
    datei.write("CO2.: ")
    datei.write(str(liste[2]))
    datei.write("\n")
    datei.close()
    time.sleep(5)


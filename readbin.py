import struct
import os

LSB = "LSB"
MSB = "MSB"

class BinFile:

  def __init__(self, filename=None):
    self.fp = None
    self.length = None
    if filename:
      self.open(filename)

  def open(self, filename):
    self.length = os.path.getsize(filename)
    self.fp = open(filename, 'rb')

  def close(self):
    self.fp.close()
    self.fp = None
    self.length = 0

  def goto(self, pos=0):
    self.fp.seek(pos, 0)

  def move(self, off=0):
    self.fp.seek(off, 1)

  def offset(self):
    return self.fp.tell()

  def _readContent(self, count=1):
    leftCount = self.length - self.offset() - 1
    if count > leftCount: count = leftCount
    if count <= 0: return None
    content = (count, self.fp.read(count))
    return content

  def readType(self, fmt, unitSize, count=1, byteSeq=LSB, forceList=False):
    us = unitSize
    content = self._readContent(count*us)
    if content is None: return None
    count = content[0]/us
    content = content[1][0:(count*us)]
    if byteSeq == MSB:
      newContent = ""
      for i in range(0,count):
        subcontent = content[(i*us):((i+1)*us)]
        for u in range(0, us):
          newContent += subcontent[us-u-1]
      content = newContent
    result = struct.unpack("%d%s" % (count, fmt), content)
    if (not forceList) and (len(result) == 1):
      result = result[0]
    return result

  def readChar(self, count=1, forceList=False):
    return self.readType(fmt='c', unitSize=1, count=count, forceList=forceList)

  def readByte(self, count=1, forceList=False):
    return self.readType(fmt='b', unitSize=1, count=count, forceList=forceList)

  def readUByte(self, count=1, forceList=False):
    return self.readType(fmt='B', unitSize=1, count=count, forceList=forceList)

  def readShort(self, count=1, byteSeq=LSB, forceList=False):
    return self.readType(fmt='h', unitSize=2, count=count, byteSeq=byteSeq, forceList=forceList)

  def readUShort(self, count=1, byteSeq=LSB, forceList=False):
    return self.readType(fmt='H', unitSize=2, count=count, byteSeq=byteSeq, forceList=forceList)

  def readInt(self, count=1, byteSeq=LSB, forceList=False):
    return self.readType(fmt='i', unitSize=4, count=count, byteSeq=byteSeq, forceList=forceList)

  def readUInt(self, count=1, byteSeq=LSB, forceList=False):
    return self.readType(fmt='I', unitSize=4, count=count, byteSeq=byteSeq, forceList=forceList)

if __name__ == "__main__":
  f = BinFile("ds")
  f.goto(4)
  imCount = f.readInt(1, MSB)
  imSize = f.readInt(2, MSB)
  print imCount, imSize

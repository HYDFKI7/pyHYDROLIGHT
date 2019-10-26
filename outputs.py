import numpy as np


class OUTPUTS(object):
    def __init__(self, resroot, filename):
        self.rrs = RRS(resroot, filename)


class RRS(object): # 这个类的名字要改，因为包含不仅仅有遥感反射率
    def __init__(self, resroot, filename):
        with open(resroot + filename) as file:
            self.fulltext = file.readlines()
        # Get the total length of the file
        filelength = len(self.fulltext)
        # Get header length to skip it
        skipheader = [idx for idx, text in enumerate(self.fulltext)
                      if '" " "in air" "Rrs" "Ed" "Lw" "Lu"' in text][0]
        skipfooter = [idx for idx, text in enumerate(self.fulltext)
                      if '"R" "R = Eu/Ed"' in text][0]
        self.wa, self.Rrs, self.Ed, self.Lw, self.Lu = np.genfromtxt(
            resroot + filename,
            skip_header=skipheader + 1,
            skip_footer=filelength - skipfooter,
            unpack=True)



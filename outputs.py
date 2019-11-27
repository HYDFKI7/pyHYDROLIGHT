import numpy as np


class OUTPUTS(object):
    def __init__(self, resroot, filename):
        self.rrs = RRS(resroot, filename)
        self.bb = BB(resroot, filename)
        self.a = A(resroot, filename)


class RRS(object):
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


class BB(object):
    def __init__(self, resroot, filename):
        with open(resroot + filename) as file:
            self.fulltext = file.readlines()
        # Total lenght of the file
        filelength = len(self.fulltext)
        # Get header lenght to skip it
        skipheader = [idx for idx, text in enumerate(self.fulltext)
                      if '"bb" "backscat coef b (1/m)"      87       3' in text][0]
        skipfooter = [idx for idx, text in enumerate(self.fulltext)
                      if '" " "bb (1/m) for component  1"' in text][0]
        self.wa, self.bb_0, self.bb_10 = np.genfromtxt(
            resroot + filename,
            skip_header=skipheader + 3,
            skip_footer=filelength - skipfooter + 1,
            unpack=True)


class A(object):
    def __init__(self, resroot, filename):
        with open(resroot + filename) as file:
            self.fulltext = file.readlines()
        # Total lenght of the file
        filelength = len(self.fulltext)
        # Get header lenght to skip it
        skipheader = [idx for idx, text in enumerate(self.fulltext)
                      if '"a" "abs coef a (1/m)"      87       3' in text][0]
        skipfooter = [idx for idx, text in enumerate(self.fulltext)
                      if '" " "a (1/m) for component  1"' in text][0]
        self.wa, self.a_0, self.a_10 = np.genfromtxt(
            resroot + filename,
            skip_header=skipheader + 3,
            skip_footer=filelength - skipfooter + 1,
            unpack=True)

import os
import matplotlib.pyplot as plt
from outputs import OUTPUTS
import numpy as np


class RunIdentification(object):
    def __init__(
            self,
            rootname="Results",
            descriptive="Replace the rootname and title"):
        """
        :param rootname: to be used in generating the names of the various input and output file associat with this run (max 32 characters)
        :param descriptive: descriptive title for this run (max 120 characters)
        """
        self.rootname = rootname
        self.descriptive = descriptive


class InherentOpticalPropertySpecification(object):
    """
    a model for the absorption a and scattering b coefficients and scattering phase functions that describe the water body
    """

    def __init__(self, ioptmodel=2):
        """
        iOptmodel indicates which IOP model has been selected in the GUI
        :param  iOptmodel = 0: for constant IOPs (IOP routine abconst.f will be called)
                iOptmodel = 1 for the classic Case 1 IOP model (IOP routine abcase1.f)
                iOptmodel = 2 for the Case 2 IOP model (IOP routine abcase2.f)
                iOptmodel = 3 for the IOP data model (IOP routine abacbb.f)
                iOptmodel = 4 for the new Case 1 IOP model (IOP routine abcase1new.f)
                iOptmodel = -1 for a user-written IOP model (the user’s named IOP routine in HE5/code/users will be used)
        """
        self.ioptmodel = ioptmodel


class PureWater(object):
    def __init__(self, case=1):
        """
        :param case1: Pope and Fry’s data
               case2: Smith and Baker’s data
               case3: select your own data file
        """
        self.case = case
        self.concentration = ConcentrationProfile.CONSTANT()
        self.abs = SpectifyAbsorption(usersupport=r"..\data\H2OabDefaults.txt")
        self.phasefunction = PhaseFunction(bbb=0.005)


class ConcentrationProfile(object):
    class CONSTANT(object):
        def __init__(self, value=0):
            self.value = value

    class UserSupport(object):
        def __init__(self, usersupport):
            self.usersupport = usersupport


class Wavelength(object):
    def __init__(self, startwa=400, endwa=800, interval=10):
        self.startwa = startwa
        self.endwa = endwa
        self.interval = interval
        self.wavelengths = np.arange(
            start=self.startwa,
            stop=self.endwa,
            step=interval)
        self.length = len(self.wavelengths)


class SpectifyAbsorption(object):
    def __init__(self, usersupport=r"..\data\Examples\astarchl.txt"):
        self.usersupport = usersupport


class SpectifyScattering(object):
    def __init__(self, usersupport=r"..\data\defaults\bstarmin_redclay.txt"):
        self.usersupport = usersupport


class PhaseFunction(object):
    def __init__(self, bbb=0.005, name="pureh2o.dpf"):
        """
        :param bbb:
        :param name: the names of the files  containing the discretized phase functions to be used with each component of the IOP model
        """
        self.bbb = bbb
        self.name = name


class Chlorophyll(object):
    def __init__(self, concentration=30, ichl=2):
        self.constant = ConcentrationProfile.CONSTANT(concentration)
        self.abs = SpectifyAbsorption()
        self.sca = SpectifyScattering()
        self.phasefunction = PhaseFunction(bbb=0.005, name="isotrop.dpf")
        self.ichl = ichl


class CDOM(object):
    def __init__(self, concentration=0.3, icdom=3):
        self.constant = ConcentrationProfile.CONSTANT(concentration)
        self.abs = SpectifyAbsorption(usersupport="dummyastar.txt")
        self.phasefunction = PhaseFunction(bbb=0.005, name="isotrop.dpf")
        self.icdom = icdom


class Minerals(object):
    def __init__(self, concentration=30):
        self.constant = ConcentrationProfile.CONSTANT(concentration)
        self.abs = SpectifyAbsorption(
            usersupport=r"..\data\defaults\astarmin_redclay.txt")
        self.sca = SpectifyScattering()
        self.phasefunction = PhaseFunction(bbb=0.028, name="isotrop.dpf")


class OutputOptions:
    def __init__(
            self,
            ioptprnt=0,
            ioptdigital=0,
            ioptexcelS=2,
            ioptexcelm=1,
            ioptrad=0,
            nwskip=1):
        """
        :param ioptprnt: is a flag for the specification of the amount of printout
                         if iOptPrnt =-1, Proot.txt will contain only “minimal” runtime output.if iOptPrnt = 0,
                         Proot.txt will contain the “standard” output, including component IOPs and selected radiances
                         and irradiances.
                         if iOptPrnt = 1, Proot.txt will contain “extensive” output including all radiance arrays and
                         some “intermediate” values. WARNING: this option is not recommended as it can produce a
                         substantial amount of output.
        :param ioptdigital: is a flag for the inclusion/omission of the digital output file
                            if iOptDigital = 0, Droot.txt will not be generated for this run. if iOptDigital = 1,
                            Droot.txt will be generated for this run.
        :param ioptexcelS: a flag for the inclusion/omission of the Excel Single-wavelength output file
                           if iOptExcelS = 0, Sroot.txt will not be generated for this run. if iOptExcelS = 2,
                           Sroot.txt will be generated for this run.
        :param ioptexcelm: is a flag for the inclusion/omission of the Excel Multi-wavelength output file
                           if iOptExcelM = 0, Mroot.txt will not be generated for this run. if iOptExcelM = 1,
                           Mroot.txt will be generated for this run.
        :param ioptrad: is a flag for the inclusion/omission of the full radiance printout file
                        if iOptRad = 0, Lroot.txt will not be generated for this run. if iOptRad = 1, Lroot.txt will be
                        generated for this run.
        :param nwskip: sets whether to skip alternating wave bands and then interpolate to fill skipped bands (nwskip=1
                       solves all wavelengths; nwskip=2 solves every other wavelength, etc)
        """
        self.ioptprnt = ioptprnt
        self.ioptdigital = ioptdigital
        self.ioptexcelS = ioptexcelS
        self.ioptexcelm = ioptexcelm
        self.ioptrad = ioptrad
        self.nwskip = nwskip


class AirWaterSurfaceBoundaryConditions(object):

    class SkyModel(object):
        def __init__(self, iskyradmodel=1, iskyirradmodel=0):
            """
            :param iskyradmodel: iSkyRadmodel indicates which sky radiance model has been selected in the GUI
                                 iSkyRadmodel = 0 for the analytical sky radiance model (single-wavelength runs only)
                                 iSkyRadmodel = 1 for the semi-empirical skyradiance model of Harrison and Coombes(1988;
                                 routine hcnrad will be used)
                                 iSkyRadmodel = 2 to call a user-defined sky radiance model (the user’s named sky
                                 radiance routine in HE5/code/users will be used)
            :param iskyirradmodel: iSkyIrradmodel indicates how the sky irradiances are to be obtained
                                   iSkyIrradmodel = 0 for the analytical sky irradiance model (single-wavelength runs
                                   only; available only when iSkyRadmodel = 0)
                                   iSkyIrradmodel = 1 to call RADTRANX to obtain the irradiances (available when
                                   iSkyRadmodel = 1 or 2)
                                   iSkyIrradmodel = 2 to read a user-defined data file with the total irradiances
                                   (RADTRANX will still be used to partition the total into direct and diffuse
                                   contributions; available when iSkyRadmodel = 1 or 2)
            """
            self.iskyradmodel = iskyradmodel
            self.iskyirradmodel = iskyirradmodel


class HYDROLIGHT(object):
    def __init__(
            self,
            icompile=0,
            phichl=.02,
            raman0=488,
            ramanxs=.00026,
            idynz=1,
            batch=False):
        """
        :param icompile: is the flag that tells the RUN utility whether to use the STANDARD (icompile=0, no compiling
                         necessary) or USER (icompile=1, code must be ecompiled) executable.
        :param phichl: is the chlorophyll fluorescence efficiency
        :param raman0: is the Raman reference wavelength
        :param ramanxs: is the Raman scattering coefficient at the reference
        :param idynz: is the flag that tells HE5 whether to use the Dynamic depth option if an infinitely-deep bottom
                      boundary is selected when inelastic sources are present. If iDynZ=1, inelastic sources are present
                      and an infintely-deep bottom is  selected, HE5 will compute the light field to a greater depth
                      (roughly 20 opticaldepths at the clearest wavelength).
                      This helps guarantee a good solution at all depths
        """
        self.icompile = icompile
        self.batch = batch
        self.phichl = phichl
        self.raman0 = raman0
        self.ramanxs = ramanxs
        self.idynz = idynz
        self.outputoptions = OutputOptions()
        self.root = os.getenv("HYDROLIGHT")
        self.resroot = self.root + "/output/Hydrolight/excel/"
        self.runidentification = RunIdentification()
        self.inherentopticalpropertyspecification = InherentOpticalPropertySpecification()
        self.skymodel = AirWaterSurfaceBoundaryConditions.SkyModel()
        self.chl = Chlorophyll()
        self.cdom = CDOM()
        self.purewater = PureWater()
        self.minerals = Minerals()
        self.wavelength = Wavelength()

    def run(self):
        # icompile, Parmin, Parmax, PhiChl, Raman0, RamanXS, iDynZ
        sc = "{},400,700,{},{},{},{}".format(
            self.icompile, self.phichl, self.raman0, self.ramanxs, self.idynz)
        sc = sc + "\n" + "{}".format(self.runidentification.descriptive)
        sc = sc + "\n" + "{}".format(self.runidentification.rootname)
        # iOptPrnt, iOptDigital, iOptExcelS, iOptExcelM, iOptRad , nwskip
        sc = sc + "\n" + "{},{},{},{},{},{}".format(
            self.outputoptions.ioptprnt,
            self.outputoptions.ioptdigital,
            self.outputoptions.ioptexcelS,
            self.outputoptions.ioptexcelm,
            self.outputoptions.ioptrad,
            self.outputoptions.nwskip)
        # iIOPmodel, iSkyRadModel, iSkyIrradModel, iChl, iCDOM
        sc = sc + "\n" + "{},{},{},{},{}".format(
            self.inherentopticalpropertyspecification.ioptmodel,
            self.skymodel.iskyradmodel,
            self.skymodel.iskyirradmodel,
            self.chl.ichl,
            self.cdom.icdom)
        sc = sc + "\n" + "4,4"
        sc = sc + "\n" + "{},{},{},{}".format(
            self.purewater.concentration.value,
            self.chl.constant.value,
            self.cdom.constant.value,
            self.minerals.constant.value)
        sc = sc + "\n" + "0,1,440,.1,.014"
        sc = sc + "\n" + "0,0,440,.1,.014"
        sc = sc + "\n" + "0,4,440,1,.014"
        sc = sc + "\n" + "0,0,440,.1,.014"
        sc = sc + "\n" + "{}".format(self.purewater.abs.usersupport)
        sc = sc + "\n" + "{}".format(self.chl.abs.usersupport)
        sc = sc + "\n" + "{}".format(self.cdom.abs.usersupport)
        sc = sc + "\n" + "{}".format(self.minerals.abs.usersupport)
        sc = sc + "\n" + "0,-999,-999,-999,-999,-999"
        sc = sc + "\n" + "4,550,.3,1,.62,-999"
        sc = sc + "\n" + "-1,-999,0,-999,-999,-999"
        sc = sc + "\n" + "0,-999,-999,-999,-999,-999"
        sc = sc + "\n" + "bstarDummy.txt"
        sc = sc + "\n" + "dummybstar.txt"
        sc = sc + "\n" + "dummybstar.txt"
        sc = sc + "\n" + "{}".format(self.minerals.sca.usersupport)
        sc = sc + "\n" + "0,0,550,.01,0"
        sc = sc + "\n" + "1,.005,0,0,0"
        sc = sc + "\n" + "-1,0,0,0,0"
        sc = sc + "\n" + "1,.028,0,0,0"
        sc = sc + "\n" + "{}".format(self.purewater.phasefunction.name)
        sc = sc + "\n" + "{}".format(self.chl.phasefunction.name)
        sc = sc + "\n" + "{}".format(self.cdom.phasefunction.name)
        sc = sc + "\n" + "{}".format(self.minerals.phasefunction.name)
        sc = sc + "\n" + "{}".format(self.wavelength.length)
        [rows, cols] = self.wavelength.wavelengths.reshape(-1, 10).shape
        for row in range(rows):
            sc = sc + "\n" + "{}".format(str(self.wavelength.wavelengths.reshape(-1, 10)[
                                         row, :]).replace(" ", ",").replace("[", "").replace("]", ""))
        sc = sc + "\n" + "{}".format(self.wavelength.endwa)
        sc = sc + "\n" + "0,0,0,0,2"
        sc = sc + "\n" + "2,3,30,0,0"
        sc = sc + "\n" + "-1,0,0,29.92,1,80,2.5,15,4.99746,300"
        sc = sc + "\n" + "2.99937,1.34,20,35"
        sc = sc + "\n" + "0,0"
        sc = sc + "\n" + "0,2,0,10,"
        sc = sc + "\n" + "{}".format(self.purewater.abs.usersupport)
        sc = sc + "\n" + "1"
        sc = sc + "\n" + "dummyac9.txt"
        sc = sc + "\n" + "dummyFilteredAc9.txt"
        sc = sc + "\n" + "dummyHscat.txt"
        sc = sc + "\n" + "dummyComp.txt"
        sc = sc + "\n" + "dummyComp.txt"
        sc = sc + "\n" + "dummyR.bot"
        sc = sc + "\n" + "dummydata.txt"
        sc = sc + "\n" + "dummyComp.txt"
        sc = sc + "\n" + "dummyComp.txt"
        sc = sc + "\n" + "dummyComp.txt"
        sc = sc + "\n" + "DummyIrrad.txt"
        sc = sc + "\n" + r"..\data\MyBiolumData.txt"
        with open("{}/run/batch/I{}.txt".format(self.root, self.runidentification.rootname), 'w') as file:
            file.write(sc)
        with open("{}/run/runlist.txt".format(self.root), 'wt') as file:
            file.write("I{}.txt".format(self.runidentification.rootname))
        # Change directory
        #old_dir = os.getcwd()
        os.chdir(self.root + "/run")
        os.system("runHL.exe")
        self.result = "M{}.txt".format(self.runidentification.rootname)
        # read OUTPUTS
        self.outputs = OUTPUTS(self.resroot, self.result)


if __name__ == '__main__':
    hydrolight = HYDROLIGHT()
    # Input file name
    hydrolight.runidentification.rootname = "test"
    hydrolight.wavelength.startwa = 400
    hydrolight.wavelength.endwa = 900
    chls = np.array([5, 10, 30, 50, 80, 100, 120, 140])
    tsss = np.array([5, 10, 30, 50, 80, 100, 120, 140])
    cdoms = np.array([0.4, 0.6, 0.8, 1.2, 1.6, 2, 2.4, 2.6])
    for cdom in cdoms:
        hydrolight.chl.constant.value = 20
        hydrolight.cdom.constant.value = cdom
        hydrolight.minerals.constant.value = 20
        hydrolight.run()
        plt.plot(
            hydrolight.outputs.rrs.wa,
            hydrolight.outputs.rrs.Rrs,
            label=cdom)
    plt.legend()
    plt.xlabel("wavelengths/nm")
    plt.ylabel(r"$R_{rs}/sr^{-1}$")
    plt.show()

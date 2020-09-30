# Subject data (unchanging)
class Subject:
    def __init__(self, subnumber, bday, gender, rundate):
        self.__subnumber = subnumber
        self.__bday = bday
        self.__gender = gender
        self.__rundate = rundate

    def get_subnumber(self):
        return self.__subnumber

    def get_bday(self):
        return self.__bday

    def get_gender(self):
        return self.__gender

    def get_rundate(self):
        return self.__rundate


class Experiment:
    """contains subject AND trials"""
    def __init__(self, subject):
        self.__subject = subject
        self.__triallist = []

    def get_subject(self):
        return self.__subject

    def add_trial(self, trial):
        self.__triallist.append(trial)

    def get_trial(self, trialnum):
        return self.__triallist[trialnum]

    def get_triallist(self):
        return self.__triallist

class Trial:
    """trial object"""

    def __init__(self, blocknum, trialnum, attendtype, stimtype, practice = 'True'):
        self.__blocknum = blocknum
        self.__trialnum = trialnum
        self.__attendtype = attendtype
        self.__stimtype = stimtype
        self.__stimlist = []  # lists are in the format [[#,#,#...],[#,#,#...],...]
        """to navigate through list:
            for probe in obj.get_stimlist():
                for i in probe:
                    if probe.len = 3 ->add blankspace
                     i.foo(bar)
                    """
        self.__responselist = []
        self.__errorlist = []
        self.__responsetimelist = []
        self.__stimorderlist = []
        self.__practice = practice

    def get_blocknum(self):
        return self.__blocknum

    def get_trialnum(self):
        return self.__trialnum

    def get_attendtype(self):
        return self.__attendtype

    def get_stimtype(self):
        return self.__stimtype

    def get_stimlist(self):
        return self.__stimlist

    def get_responselist(self):
        return self.__responselist

    def get_errorlist(self):
        return self.__errorlist

    def get_responsetimelist(self):
        return self.__responsetimelist

    def get_stimorderlist(self):
        return self.__stimorderlist

    def get_practice(self):
        return self.__practice

# orglist[].add_stim([1,2,3])-> orglist[[1,2,3]]: variable leng list [[1,2,3,4,5,6], [1,2,3], ]
    def add_stim(self, stim):  #stim is a list of any length [most likely 3 or 6] that will be added to the stimlist attribute
        self.__stimlist.append(stim)

    def add_response(self, response):
        self.__responselist.append(response)

    def add_error(self, error):
        self.__errorlist.append(error)

    def add_responsetime(self, responsetime):
        self.__responsetimelist.append(responsetime)

    def add_stimorder(self, stimorder):
        self.__stimorderlist.append(stimorder)

    def set_practice(self, practice):
        self.__practice = practice

class Data:
    def __init__(self):
        self.__explist =[]

    def add_exp(self, exp):
        self.__explist.append(exp)

    def get_explist(self):
        return self.__explist

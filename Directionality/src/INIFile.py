class INIFile:

    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, file):
        self.parse = {}
        self.file = file
        self.open = open(file, "r")
        self.f_read = self.open.read()
        split_content = self.f_read.split("\n")

        section = ""

        for i in range(len(split_content)):
            if split_content[i].find("[") != -1:
                section = split_content[i]
                section = section[section.find("[") + 1:section.rfind("]")]
                self.parse.update({section: {}})
            elif split_content[i].find("[") == -1 and split_content[i].find("=") != -1:
                pairs = split_content[i]
                split_pairs = pairs.split("=")
                key = split_pairs[0].strip()
                value = split_pairs[1].strip()
                self.parse[section].update({key: value})

    # ************************************************************************
    # Return a String or Default from section/key
    # ************************************************************************
    def getStr(self, section, key, default):
        try:
            return self.parse[section][key]
        except:
            return default

    # ************************************************************************
    # Return a Integer or Default from section/key
    # ************************************************************************
    def getInt(self, section, key, default):
        try:
            return int(self.parse[section][key])
        except:
            return default

    # ************************************************************************
    # Return a Float or Default from section/key
    # ************************************************************************
    def getFloat(self, section, key, default):
        try:
            return float(self.parse[section][key])
        except:
            return default

    # ************************************************************************
    # Return a Boolean or Default from section/key
    # ************************************************************************
    def getBool(self, section, key, default):
        try:
            v = self.parse[section][key]
            if v[0] == "T" or v[0] == "t":
                return True
            else:
                return False
        except:
            return default

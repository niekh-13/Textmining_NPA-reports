##############################################################
#                                                            #
#    Niek Huijsmans (2021)                                   #
#    Textmining medical notes for cognition                  #
#    ParseDataset                                            #
#                                                            #
##############################################################
# Import the relevant packages
import pandas as pd

class ParseDataset:

    def __init__(self, filename, file, i):
        self.file = file
        self.i = i
        self.filename = filename

    def create_dataset(self):
        ID, re =  self.get_ID()
        self.data_table = pd.DataFrame({'ID':ID, 're':re}, index=[self.i])

    def get_ID(self):
        id = str(self.filename.split('/')[-1].split('.')[0])
        return self.check_id(id)

    def check_id(self, id):
        ids = id.split('-')
        if ids[-1] == 're':
            re = True
        else:
            re = False
        id = ids[0].split('_')[-1]
        return id, re

    def pre_parser(self):
        """
        parsing basic variables of files in to dict
        """
        # make dict from items in file
        items = {}
        # parse each line in the file
        for line in self.file.splitlines():
            # remove whitespace at the end of the line
            line = line.strip()
            line = re.sub(r"\s+", " ", line)
            if line.startswith('Verhage:'):
                line = line.split(':')
                items['verhage'] = line[-1]
            elif line.startswith('Opleiding:'):
                line = line.split(':')
                items['opleiding'] = line[-1]
            elif line.startswith('Aantal jaren:'):
                line = line.split(':')
                items['jaren'] = line[-1]
            elif line.startswith('handvoorkeur'):
                line = line.split(':')
                items['hand'] = line[-1]
            elif line.startswith('Partner'):
                line = line.split(':')
                items['partner'] = line[-1]
            elif line.startswith('Woonsituatie'):
                line = line.split(':')
                items['woon'] = line[-1]
            elif line.startswith('Roker'):
                line = line.split(':')
                items['roker'] = line[-1]
            elif line.startswith('Alcohol'):
                line = line.split(':')
                items['alcohol'] = line[-1]
            elif line.startswith('Kleurenblind'):
                line = line.split(':')
                items['kleur'] = line[-1]
            elif line.startswith('Epilepsie:'):
                line = line.split(':')
                items['epil'] = line[-1]
            elif line.startswith('Computergebruik:'):
                line = line.split(':')
                items['com'] = line[-1]
                break
            else:
                continue
        data = pd.DataFrame(items, index=[self.i])
        self.data_table = self.data_table.join(data)

    def T0_parser(self):
        """
        parsing basic pre measurements and questions variables of files in to dict format for T0
        """
        try:
            file = self.file.split('PRE-meting')[1:]
            file = "\n".join(file).split('POST-meting')[0].replace('3 maanden', '').replace('12 maanden', '')
        except:
            file = ''

        lines = file.splitlines()

        items = self.test_parser(lines)
        items = {'T0_' + str(key): val for key, val in items.items()}
        data = pd.DataFrame(items, index=[self.i])
        self.data_table = self.data_table.join(data)

        items_obs = self.obs_parser(file)
        items_obs = {'T0_' + str(key): val for key, val in items_obs.items()}
        data = pd.DataFrame(items_obs, index=[self.i])
        self.data_table = self.data_table.join(data)


    def T3_parser(self):
        """
        parsing basic pre measurements and questions variables of files in to dict format for T3
        """
        # make dict from items in file
        check = self.check_format()
        if check == 3:
            months = self.check_6months()
            if months:
                file = self.file.split('3 maanden POST-meting')[1].split('6 maanden POST-meting')[0]
                lines = file.splitlines()
                items = self.test_parser(lines)
                items_obs = self.obs_parser(file)
            else:
                file = self.file.split('3 maanden POST-meting')[1].split('12 maanden POST-meting')[0]
                lines = file.splitlines()
                items = self.test_parser(lines)
                items_obs = self.obs_parser(file)
        elif check == 0:
            file = re.sub('POST-meting', '3 maanden POST-meting', self.file, 1)
            months = self.check_6months()
            if months:
                file = file.split('3 maanden POST-meting')[1].split('6 maanden POST-meting')[0]
                lines = file.splitlines()
                items = self.test_parser(lines)
                items_obs = self.obs_parser(file)
            else:
                file = file.split('3 maanden POST-meting')[1].split('12 maanden POST-meting')[0]
                lines = file.splitlines()
                items = self.test_parser(lines)
                items_obs = self.obs_parser(file)
        else:
            items ={}
            items_obs={}

        items = {'T3_' + str(key): val for key, val in items.items()}
        data = pd.DataFrame(items, index=[self.i])
        self.data_table = self.data_table.join(data)

        items_obs = {'T3_' + str(key): val for key, val in items_obs.items()}
        data = pd.DataFrame(items_obs, index=[self.i])
        self.data_table = self.data_table.join(data)

    def T12_parser(self):
        """
          parsing T3 measurements variables of files in to objects
          """
        check = self.check_T12()
        # make dict from items in file
        if check:
            file = self.file.split('12 maanden POST-meting')[1].split('24 maanden POST-meting')[0]
            lines = file.splitlines()
            items = self.test_parser(lines)
            items_obs = self.obs_parser(file)
        else:
            items = {}
            items_obs = {}

        items = {'T12_' + str(key): val for key, val in items.items()}
        data = pd.DataFrame(items, index=[self.i])
        self.data_table = self.data_table.join(data)

        items_obs = {'T12_' + str(key): val for key, val in items_obs.items()}
        data = pd.DataFrame(items_obs, index=[self.i])
        self.data_table = self.data_table.join(data)

    def test_parser(self, lines):
        """
        parsing basic test measurements and questions of time in file in to dict format
        """
        items = {}
        for i, line in enumerate(lines):
            line = line.strip()
            line = re.sub(r"\s+", " ", line)
            if line.startswith('Algemene observatie:'):
                break
            elif line.startswith('Volledig getest:'):
                line = line.split(':')
                items['tested'] = line[-1]
            elif line.startswith('Getest door:'):
                line = line.split(':')
                items['tester'] = line[-1]
            elif line.startswith('Medicatiepre:'):
                line = line.split(':')
                items['medication'] = line[-1]
            elif line.startswith('Datum:'):
                line = line.split(':')
                items['date'] = line[-1]
            elif line.startswith('Angst'):
                items['angst'] = lines[i + 1]
            elif line.startswith('Depressie'):
                items['depres'] = lines[i + 1]
            elif line.replace(' ', '') == 'D':
                items['WF_D'] = lines[i + 1]
            elif line.replace(' ', '') == 'A':
                items['WF_A'] = lines[i + 1]
            elif line.replace(' ', '') == 'T':
                items['WF_T'] = lines[i + 1]
            elif line.replace(' ', '') == 'K':
                items['WF_K'] = lines[i + 1]
            elif line.replace(' ', '') == 'O':
                items['WF_O'] = lines[i + 1]
            elif line.replace(' ', '') == 'M':
                items['WF_M'] = lines[i + 1]
            elif line.replace(' ', '') == 'Voorwaarts':
                items['ds_voor'] = lines[i + 1]
            elif line.replace(' ', '') == 'Achterwaarts':
                items['ds_achter'] = lines[i + 1]
                continue
        return items

    def obs_parser(self, file):
        '''
        Parse the observation of the medical notes in the file
        '''
        items = {}
        file = file + 'POST-meting'
        format_note = self.identify_format(file)
        if format_note == 0:
            # this is old format
            items['obs_truth'], items['ptnt_obs'], items['lich'], items['cog'] = self.old_obs_parser(file)
        else:
            items['obs'], items['obs_truth'], items['ptnt_obs'], items['lich'], items['cog'], items['pres'],\
            items['v-g'], items['motor'], items['taal'], items['aan'], items['werkh'], items['werkz'], items['stem'],\
            items['ptnt'], items['klacht'], items['other'] = self.new_obs_parser(file, format_note)
        return items


    def old_obs_parser(self, file):
        '''
        Parse the observation of the medical notes in the file when the medical note is written old way
        '''
        lich = ''
        cog = ''
        try:
            obs_truth = file.split('Algemene observatie:')[1].split('Gerapporteerde klachten door patient:')[
                    0].replace('POST-meting', '').strip()
            obs_truth = re.sub(r"\s+", " ", obs_truth)
        except:
            obs_truth = ''
        # described by patient
        try:
            ptnt_obs = \
                    file.split('Gerapporteerde klachten door patient:')[1].split('POST-meting')[0].strip()
            ptnt_obs = re.sub(r"\s+", " ", ptnt_obs)
        except:
            ptnt_obs = ''
        # check what kind of format the patient obs are written down are correct if necessary
        check = self.obs_check(ptnt_obs)
        if check == True:
            lich, cog = self.ptnt_obs_split(ptnt_obs)
            ptnt_obs = re.sub(r"\s+", " ", ptnt_obs.strip())
        else:
            ptnt_obs =  re.sub(r"\s+", " ", ptnt_obs.strip())
        return obs_truth, ptnt_obs, lich, cog

    def new_obs_parser(self, file, format_note):
        lich = ''
        cog = ''
        pres = ''
        vg = ''
        motor = ''
        taal = ''
        aan = ''
        werkh = ''
        werkz = ''
        stem = ''
        ptnt = ''
        klacht = ''
        other = ''
        # this is the new format
        if format_note == 1:
            obs = file.split('Algemene observatie:')[1].split('Presentatie:')[0].strip()
        elif format_note == 2:
            obs = file.split('Algemene observatie:')[1].split('Visus ')[0].strip()
        elif format_note == 3:
            obs = file.split('Algemene observatie:')[1].split('Motoriek:')[0].strip()
        elif format_note == 4:
            obs = file.split('Algemene observatie:')[1].split('Taal:')[0].strip()
        elif format_note == 5:
            obs = file.split('Algemene observatie:')[1].split('Aandacht:')[0].strip()
        elif format_note == 6:
            obs = file.split('Algemene observatie:')[1].split('Werkhouding:')[0].strip()
        elif format_note == 7:
            obs = file.split('Algemene observatie:')[1].split('Werkwijze:')[0].strip()
        elif format_note == 8:
            obs = file.split('observatie:')[1].split('Stemming:')[0].strip()
        elif format_note == 9:
            obs = file.split('Algemene observatie:')[1].split('Beleving onderzoek door patient:')[0].strip()
        elif format_note == 10:
            obs = file.split('Algemene observatie:')[1].split('Klachtenpresentatie:')[0].strip()
        elif format_note == 11:
            obs = file.split('Algemene observatie:')[1].split('Overige opvallende kenmerken:')[0].strip()
        else:
            obs = file.split('Algemene observatie:')[1].split('Gerapporteerde klachten door patient:')[0].strip()
        # described by patient
        try:
            ptnt_obs = file.split('Gerapporteerde klachten door patient:')[1].split('POST-meting')[0].strip()
        except:
            ptnt_obs = ''
        # check what kind of format the patient obs are written down are correct if necessary
        check = self.obs_check(ptnt_obs)
        if check == True:
            ptnt_obs = re.sub(r"\s+", " ", ptnt_obs.strip())
            lich, cog = self.ptnt_obs_split(ptnt_obs)
        else:
            ptnt_obs =  re.sub(r"\s+", " ", ptnt_obs.strip())
        # more detail obs
        for line in file.splitlines():
            if line.startswith("Presentatie:"):
                pres = line.strip().split(':')[-1]
            elif line.startswith("Visus en gehoor:"):
                vg = line.strip().split(':')[-1]
            elif line.startswith("Motoriek:"):
                motor = line.strip().split(':')[-1]
            elif line.startswith("Taal:"):
                taal = line.strip().split(':')[-1]
            elif line.startswith("Aandacht:"):
                aan = line.strip().split(':')[-1]
            elif line.startswith("Werkhouding:"):
                werkh = line.strip().split(':')[-1]
            elif line.startswith("Werkwijze:"):
                werkz = line.strip().split(':')[-1]
            elif line.startswith("Stemming:"):
                stem = line.strip().split(':')[-1]
            elif line.startswith("Beleving onderzoek door patient:"):
                ptnt = line.strip().split(':')[-1]
            elif line.startswith("Klachtenpresentatie:"):
                klacht = line.strip().split(':')[-1]
            elif line.startswith("Overige opvallende kenmerken:"):
                other = line.strip().split(':')[-1]
            else:
                continue
        try:
            obs_truth = file.split('Algemene observatie:')[1].split('Gerapporteerde klachten door patient:')[
                0].replace('POST-meting', '').strip()
            obs_truth = re.sub(r"\s+", " ", obs_truth)
        except:
            obs_truth = ''
        return obs, obs_truth, ptnt_obs, lich, cog, pres, vg, motor, taal, aan, werkh, werkz, stem, ptnt, klacht, other


    def identify_format(self, file):
        '''
        Help to identify whether the file has new format for observation ornot
        '''
        # parse each line in the file
        for line in file.splitlines():
            if line.startswith("Presentatie:"):
                return 1
            elif line.startswith("Visus en gehoor:") or line.startswith('Visus + gehoor:'):
                return 2
            elif line.startswith("Motoriek:"):
                return 3
            elif line.startswith("Taal:"):
                return 4
            elif line.startswith("Aandacht:"):
                return 5
            elif line.startswith("Werkhouding:"):
                return 6
            elif line.startswith("Werkwijze:"):
                return 7
            elif line.startswith("Stemming:"):
                return 8
            elif line.startswith("Beleving onderzoek door patient:"):
                return 9
            elif line.startswith("Klachtenpresentatie:"):
                return 10
            elif line.startswith("Overige opvallende kenmerken:"):
                return 11
            else:
                continue
        return 0

    def obs_check(self, file):
        '''
        Check what the format is in the file for patients observations
        '''
        for line in file.splitlines():
            if line.startswith('Lichamelijk:') or line.startswith('lichamelijk:'):
                return True
            elif line.startswith("Cognitief:") or line.startswith("cognitief:"):
                return True
            else:
                continue
        return False

    def ptnt_obs_split(self, file):
        '''
        Split the ptnt observations in to main complaints
        '''
        lich = ''
        cog = ''
        for line in file.splitlines():
            if line.startswith('Lichamelijk:') or line.startswith('lichamelijk:'):
                lich = line.split(':')[-1].strip()
            elif line.startswith('Cognitief:') or line.startswith("cognitief:"):
                cog = line.split(':')[-1].strip()
            else:
                continue
        return lich, cog

    def check_6months(self):
        '''
        Check whether the file has 6 months time point to taken in to account
        '''
        for line in self.file.splitlines():
            if line.startswith('6 maanden POST-meting'):
                return True
            else:
                continue
        return False

    def check_format(self):
        '''
        Check whether the file has new format for time points (T3)
        '''
        # parse each line in the file
        for line in self.file.splitlines():
            if line.startswith("3 maanden POST-meting"):
                return 3
            elif line.startswith('POST-meting'):
                return 0
            else:
                continue
        return 9999

    def check_T12(self):
        '''
        Check whether the file has new format for time points (post or T3 and T12)
        '''
        # parse each line in the file
        for line in self.file.splitlines():
            if line.startswith('12 maanden POST-meting'):
                return True
            else:
                continue
        return False
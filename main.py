#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from prettytable import PrettyTable as pt

def calculate_age(birthday):
    """ Calculate the induviduals date and DOB """

    current = datetime.today()
    return current.year - birthday.year - ((current.month, current.day) < (birthday.month, birthday.day))

class Gedcom(object):
    """Define all the valid tags"""
    valid = {
    '0':(['INDI','FAM'],'HEAD','TRLR','NOTE'),
    '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
    '2':('DATE'),
    }

    def __init__(self, path):
        self.path = path
        file = self.parse_file()
        self.fam = file['fam']
        self.indi = file['indi']


    def parse_file(self):
        """Reads the file from the path and stores all the information in a dictionary. Uses Pretty table to print out further information about the family.
        """
        try:
            gp = open(self.path, 'r', encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError('%s not exist' % (self.path))
        else:
            with gp:
                isValid = 'N'
                IsIND = True
                indi = {}
                fam = {}
                currentDate = ''                        
                currentInd = ''
                currentFam = ''
                
                for line in gp:    
                    family = line.strip().split()
                    arguments = ''.join(family[2:])
                    tag = 'NA'
                    level = 'NA'

                    if len(family) == 1:
                        level = family[0]
                    elif len(family) > 1:
                        level = family[0]
                        tag = family[1]

                    if len(family) == 3 and family[0] == '0' and family[2] in ('INDI', 'FAM'):
                        isValid = 'Y'
                        tag = family[2]
                    elif len(family) > 1 and level in Gedcom.valid and tag in Gedcom.valid[level]:
                        isValid = 'Y'
                    
                    if isValid == 'Y':
                        if level== '0' and tag == 'INDI':
                            currentInd = family[1]
                            IsIND = True

                            ''' Implement the unique key identifier'''
                            
                            indi[currentInd] = {'id':family[1]}

                        if IsIND:
                            if level == '1' and tag == 'NAME':
                                indi[currentInd]['name'] = arguments
                            if level == '1' and tag == 'BIRT' or tag == 'DEAT':
                                currentDate = tag 
                            if level == '2' and currentDate != '' and tag == 'DATE':
                                indi[currentInd][currentDate] = datetime.strptime(arguments,'%d%b%Y')   

                            if level == '1' and tag == 'SEX':
                                indi[currentInd]['sex'] = arguments   
                            if level == '1' and tag in ('FAMC','FAMS'):
                                if tag in indi[currentInd]:
                                    indi[currentInd][tag].add(arguments)
                                else:
                                    indi[currentInd][tag] = {arguments}  
        
                        if level=='0' and tag == 'FAM':
                            IsIND = False
                            currentFam = family[1]
                            fam[currentFam] = {'fam':currentFam}
                            
                        if IsIND == False:
                            if level == '1' and family[1] == 'MARR' or family[1] == 'DIV':
                                currentDate = tag
                            if level == '2' and tag == 'DATE':
                                fam[currentFam][currentDate] =datetime.strptime(arguments,'%d%b%Y')
                            if level == '1' and tag in ('HUSB','WIFE'):
                                fam[currentFam][tag] = arguments
                            if level == '1' and tag == 'CHIL':
                                if tag in fam[currentFam]:
                                    fam[currentFam][tag].add(arguments)
                                else:
                                    fam[currentFam][tag] = {arguments}

        return {'fam':fam, 'indi':indi}

class Individual:
    """Defining a class to hold individual tags"""
    """ID, name, gender, alive, dead, child, spouse are present here"""
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.gender = ''
        self.age = ''
        self.alive = 'TRUE' # set this to true to compare and evaluate metrics on death 
        self.death = 'NA'   # Death is set to NA 
        self.child = dict() # store as dictionary or team's preferred choice of action
        self.spouse = dict()      # same as above, choose any data structure. Vote of dict or set??

    def print_table(self):
        """Pretty Table info for induvidual"""

        indiTable = pt(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
        
        for key in self.indi.keys():
            # print birth date
            birth_str = self.indi[key]['BIRT'].strftime('%Y-%m-%d')
            
            """Condition for alive"""
            if 'DEAT' in self.indi[key]:
                death = self.indi[key]['DEAT']
                death_str = 'False'
            else:
                death_str ='True'

            """Condition for Death column"""  #Note that I am using same "deat" keyword for alive and dead
            if 'DEAT' in self.indi[key]:
                alive = self.indi[key]['DEAT']
                alive_str = death.strftime('%Y-%m-%d')
            else:
                alive_str ='NA'

            """Condition for Children"""
            if 'FAMC' in self.indi[key]:
                child = self.indi[key]['FAMC']
            else:
                child = None
            
            """Spouse Situation LOL"""
            if 'FAMS' in self.indi[key]:
                spouse = self.indi[key]['FAMS']
            else:
                spouse = 'NA'

            age = calculate_age(self.indi[key]['BIRT'])
            indiTable.add_row([self.indi[key]['id'],self.indi[key]['name'],self.indi[key]['sex'], birth_str, age, death_str, alive_str, child, spouse])
        
        """Pretty table info for family relations"""

        famTable =pt(['ID','Married','Divorced','Husband ID','Husband Name','Wife ID','Wife name','Children'])
        for key in self.fam.keys():
            if 'DIV' in self.fam[key]:
                div_str = self.fam[key]['DIV'].strftime('%Y-%m-%d')

            else: 
                div_str = "NA"

            if "HUSB" in self.fam[key]:
                hubID = self.fam[key]['HUSB']
                hubName = self.indi[hubID]['name']
            else:
                hubID = "NA"
                hubName = "NA"

            if "WIFE" in self.fam[key]:
                wifeID = self.fam[key]['WIFE']
                wifeName = self.indi[wifeID]['name']
            else:
                wifeID = "NA"
                wifeName = "NA"

            if 'CHIL' in self.fam[key] :
                chil = self.fam[key]['CHIL']
            else:
                chil = "NA"

            if 'MARR' in self.fam[key]:
                marr_str = self.fam[key]['MARR'].strftime('%Y-%m-%d')
            else:
                marr_str = "NA"

            famTable.add_row([key, marr_str, div_str, hubID, hubName, wifeID, wifeName, chil])
        
        print(indiTable)
        print(famTable)
    
    def US01(self): #  US01 - Dates before current date - By Vignesh Mohan
        
        #getting todays date 
        today = datetime.today().strftime('%Y-%m-%d')

        error = list()

        for i in self.indi:

            individual = self.indi[i]
            if 'BIRT' in self.indi[i].keys():
                birt_dt = self.indi[i]['BIRT'].date()
            if 'DEAT' in self.indi[i].keys():
                death_dt = self.indi[i]['DEAT'].date()
        
            if 'BIRT' in individual.keys():
                Bdate = birt_dt.strftime('%Y-%m-%d')
                if Bdate > today:
                    error.append(['ERROR US01', self.indi[i]['id']])
                    print("Error US01:-Birthdate ",Bdate,"is after current date")
            
            if 'DEAT' in individual.keys():
                Ddate = death_dt.strftime('%Y-%m-%d')
                if Ddate > today:
                    error.append(['ERROR US01', self.indi[i]['id']])
                    print("Error US01:- Deathdate ",Ddate,"is after current date")
    
            for i in self.fam:
                family = self.fam[i]

                if "FAMC" in self.fam[i].keys():
                    fam_id = ''.join(self.indi[i]['FAMC'])
                    
                    if 'MARR'in self.fam[i].keys():
                        marry_date = self.fam[fam_id]['MARR']

                    if 'DIV' in self.fam[i].keys():
                        div_date = self.fam[fam_id]['DIV']
                            
                        self.fam_id = i

                        husb_id = self.fam[i]['HUSB']
                        wife_id = self.fam[i]['WIFE']
                    
                        if family not in ['HUSB']: husb_id = family['HUSB']
                        if family not in ['WIFE']: wife_id = family['WIFE']
                        if family not in ['MARR']: marry_date = family['MARR']
                        if family not in ['DIV']: div_date = family['DIV']
            
                        if marry_date:
                            WD = marry_date.strftime('%Y-%m-%d')
                            if WD > today:
                                error.append(['ERROR US01', self.indi[i]['id']])
                                print("Error US01:- marriageDate ",WD,"is after current date")
                        
                        if div_date:
                            DD = div_date.strftime('%Y-%m-%d')
                            if DD > today:
                                error.append(['ERROR US01', self.indi[i]['id']])
                                print("Error US01:- marriageDate ",DD,"is after current date")
        return error
    
    def US02(self): #  US02 - Birth before marriage of an individual - By Vignesh Mohan
        error = list()
        for i in self.indi:
            if "FAMC" in self.indi[i].keys():
                child_birt = self.indi[i]['BIRT']
                fam_id = ''.join(self.indi[i]['FAMC'])
                if 'MARR' in self.fam[fam_id].keys():
                    marry_date = self.fam[fam_id]['MARR']
                    if marry_date > child_birt:
                        error.append(['ANOMALY US02', self.indi[i]['id']])
                        print('ANOMALY: FAMILY: US02: ' + self.fam[fam_id]['fam'] + ' individual ' + self.indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' before marriage on ' + marry_date.strftime('%Y-%m-%d'))
        return error

    def US03(self): #  US 03 - Birth before death of individual - Anirudh
        error = list()
        for i in self.indi:
            if 'BIRT' in self.indi.keys():
                child_birt = self.indi[i]['BIRT']
                if self.indi[i]['BIRT'] < self.indi[i]['DEAT']:
                    print('ERROR: INDIVIDUAL: US03:' + self.indi[i]['id'] + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + 'was born before' + self.indi[i]['DEAT'].strftime('%Y-%m-%d'))
        
    def US04(self): #  US 04 - Marriage before Divorce of Parents by Anirudh
        for i in self.fam:
            if 'MARR'in self.fam[i].keys():
                marry_date = self.fam[i]['MARR']
                if 'DIV' in self.fam[i].keys():
                    div_date = self.fam[i]['DIV']
                    if marry_date < div_date:
                        j = print('ERROR: FAMILY: US04: ' + self.fam[i]['fam']  +  'Married before'  + self.fam[i]['MARR'].strftime('%Y-%m-%d') +  'Divorce'  + self.fam[i]['DIV'].strftime('%Y-%m-%d'))
        return j

    def US05(self): #  US05 Marriage before death - By Tanvi
        for i in self.indi:
            if 'DEAT' in self.indi[i].keys():
                death_dt = self.indi[i]['DEAT']
            if "FAMC" in self.indi[i].keys():
                fam_id = ''.join(self.indi[i]['FAMC'])
                
                if 'MARR' in self.fam[fam_id].keys():
                    marriage_dt = self.fam[fam_id]['MARR']
                    if  death_dt > marriage_dt:
                        print('ANOMALY: FAMILY: US05: ' + self.fam[fam_id]['fam'] + ' Person ' + self.indi[i]['id'] + ' Marriage ' + marriage_dt.strftime('%Y-%m-%d') + ' before death on ' + death_dt.strftime('%Y-%m-%d'))

    def US06(self): #  US06 Divorce before death - By Tanvi
        for i in self.indi:
            if 'DEAT' in self.indi[i].keys():
                death_dt = self.indi[i]['DEAT']
            if "FAMC" in self.indi[i].keys():
                fam_id = ''.join(self.indi[i]['FAMC'])
                
                if 'DIV' in self.fam[fam_id].keys():
                    div_dt = self.fam[fam_id]['MARR']
                    marriage_dt = self.fam[fam_id]['MARR']
                    if  death_dt > marriage_dt:
                        print('ANOMALY: FAMILY: US06: ' + self.fam[fam_id]['fam'] + ' Person ' + self.indi[i]['id'] + ' Marriage ' + div_dt.strftime('%Y-%m-%d') + ' before death on ' + death_dt.strftime('%Y-%m-%d'))



    def US07(self): #  US07 Less then 150 years old - By Lifu
        error = list()
        for i in self.indi:
            if 'DEAT' in self.indi[i].keys():
                if self.indi[i]['DEAT'] - self.indi[i]['BIRT'] > timedelta(days = 54750):
                    error.append(['ERROR US07', self.indi[i]['id']])
                    print('ERROR: INDIVIDUAL: US07: ' + self.indi[i]['id'] + ' More than 150 years old at death - Birth ' + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + ' Death ' + self.indi[i]['DEAT'].strftime('%Y-%m-%d'))
            else:
                if datetime.today() - self.indi[i]['BIRT'] > timedelta(days = 54750):
                    print('ERROR: INDIVIDUAL: US07: ' + self.indi[i]['id'] + ' More than 150 years old - Birth '  + self.indi[i]['BIRT'].strftime('%Y-%m-%d'))
                    error.append(['ERROR US07', self.indi[i]['id']])
        return error

    def US08(self): #  US08 Birth before marriage of parents - By Lifu
        for i in self.indi:
            if "FAMC" in self.indi[i].keys():
                child_birt = self.indi[i]['BIRT']
                fam_id = ''.join(self.indi[i]['FAMC'])
                if 'MARR' in self.fam[fam_id].keys():
                    marry_date = self.fam[fam_id]['MARR']
                    if marry_date > child_birt:
                        print('ANOMALY: FAMILY: US08: ' + self.fam[fam_id]['fam'] + ' Child ' + self.indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' before marriage on ' + marry_date.strftime('%Y-%m-%d'))
                if 'DIV' in self.fam[fam_id].keys():
                    div_date = self.fam[fam_id]['DIV']
                    if div_date < child_birt:
                        print('ANOMALY: FAMILY: US08: ' + self.fam[fam_id]['fam'] + ' Child ' + self.indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' after divorce on ' + div_date.strftime('%Y-%m-%d'))

    def US09(self): #  US09 Birth before death of parents - by Yuan
        for i in self.indi:
            if 'FAMC' in self.indi[i].keys():
                child_birt = self.indi[i]['BIRT']
                fam_id = ''.join(self.indi[i]['FAMC'])
                mom_id = self.fam[fam_id]['WIFE']
                dad_id = self.fam[fam_id]['HUSB']
                if 'DEAT' in self.indi[mom_id].keys():
                    mom_deat = self.indi[mom_id]['DEAT']
                    if child_birt > mom_deat:
                        print('ERROR: FAMILY: US09: ' + fam_id + ' Child ' + self.indi[i]['id'] + ' born ' + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + " after mother's death on " + mom_deat.strftime('%Y-%m-%d'))
                if 'DEAT' in self.indi[dad_id].keys():
                    dad_deat = self.indi[dad_id]['DEAT']
                    if dad_deat - child_birt < timedelta(days = 270):
                        print('ERROR: FAMILY: US09: ' + fam_id + ' Child ' + self.indi[i]['id'] + ' born ' + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + " after nine months after father's death on " + dad_deat.strftime('%Y-%m-%d'))
        
    def US10(self): #  US10 Marriage after 14 - by Yuan
        for i in self.fam:
            if 'MARR'in self.fam[i].keys():
                marry_date = self.fam[i]['MARR']
                self.fam_id = i
                husb_id = self.fam[i]['HUSB']
                wife_id = self.fam[i]['WIFE']
                husb_birt = self.indi[husb_id]['BIRT']
                wife_birt = self.indi[wife_id]['BIRT']
                if marry_date - husb_birt < timedelta(days = 5110): # 365days/yr * 14yr = 5110
                    print('ERROR: FAMILY: US10: ' + self.fam_id + ' Husband ' + self.indi[husb_id]['id'] + ' married on ' + marry_date.strftime('%Y-%m-%d') + ' before 14 years old (born on ' + husb_birt.strftime('%Y-%m-%d') + ')')
                if marry_date - wife_birt < timedelta(days = 5110): # 365days/yr * 14yr = 5110:
                    print('ERROR: FAMILY: US10: ' + self.fam_id + ' Wife ' + self.indi[wife_id]['id'] + ' married on ' + marry_date.strftime('%Y-%m-%d') + ' before 14 years old (born on ' + wife_birt.strftime('%Y-%m-%d') + ')')

def main():
    my_family = Gedcom('My-Family-7-Oct-2019-205.ged')
    my_family.print_table()

    my_family.US01()
    my_family.US02()
    my_family.US03()
    my_family.US04()
    my_family.US05()
    my_family.US06()
    my_family.US07()
    my_family.US08()
    my_family.US09()
    my_family.US10()

if __name__ == '__main__':
    main()

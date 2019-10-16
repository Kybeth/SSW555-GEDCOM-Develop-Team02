#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Project           : GEDCOM SSW 555 
#Program name      : main.py
#Author            : Tanvi Hanamshet, Anirudh Bezzam, Yuan Zhang, Vignesh Mohan, Lifu Xiao
#Purpose           : User story Implementation of US11, US12, US13, US14, US15, US16, US17, US18, US19, US20
# US11:  No Bigamy
# US12:  Parents not too old
# US13:  Siblings spacing
# US14:  Multiple Births <= 5
# US15:  Fewer than 15 siblings
# US16:  Male last name
# US17:  No marriages to children
# US18:  Siblings should not marry
# US19:  First cousins should not marry
# US20:  Aunts and Uncles

from datetime import date, datetime, timedelta
from collections import defaultdict
from prettytable import PrettyTable as pt

def calculate_age(birthday):
    """ Calculate the induviduals date and DOB """

    current = datetime.today()
    return current.year - birthday.year - ((current.month, current.day) < (birthday.month, birthday.day))

months = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}

def stringToDate(date1):
    date1year = int(date1[-4:])
    date1month = date1[-8:-5].upper()
    date1date = int(date1[:-9])
    return date(date1year,months[date1month],date1date)

def dateDiff(date1,date2):
    # Parse dates
    date1 = stringToDate(date1)
    date2 = stringToDate(date2)

    difference = date2 - date1
    return difference.days

def dates_check(date1,date2,diffYear=0):
    return (dateDiff(date1, date2) - diffYear * 360) >= 0

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

        famTable =pt(['ID','Married','Divorced','hubID ID','hubID Name','Wife ID','Wife name','Children'])
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
                wife_id = self.fam[key]['WIFE']
                wifeName = self.indi[wife_id]['name']
            else:
                wife_id = "NA"
                wifeName = "NA"

            if 'CHIL' in self.fam[key] :
                chil = self.fam[key]['CHIL']
            else:
                chil = "NA"

            if 'MARR' in self.fam[key]:
                marr_str = self.fam[key]['MARR'].strftime('%Y-%m-%d')
            else:
                marr_str = "NA"

            famTable.add_row([key, marr_str, div_str, hubID, hubName, wife_id, wifeName, chil])
        
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

                        hubID = self.fam[i]['HUSB']
                        wife_id = self.fam[i]['WIFE']
                    
                        if family not in ['HUSB']: hubID = family['HUSB']
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
                if self.indi[i]['BIRT'] > self.indi[i]['DEAT']:
                    error.append(['ERROR: INDIVIDUAL: US03:', self.indi[i]['id']])
                    print('ERROR: INDIVIDUAL: US03:' + self.indi[i]['id'] + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + 'was born before' + self.indi[i]['DEAT'].strftime('%Y-%m-%d'))
        return error
        
    def US04(self): #  US 04 - Marriage before Divorce of Parents by Anirudh
        error = list()
        for i in self.fam:
            if 'MARR'in self.fam[i].keys():
                marry_date = self.fam[i]['MARR']
                if 'DIV' in self.fam[i].keys():
                    div_date = self.fam[i]['DIV']
                    if marry_date < div_date:
                        error.append(['ERROR: FAMILY: US04: ', self.fam[i]['fam']])
                        print('ERROR: FAMILY: US04: ' + self.fam[i]['fam']  +  'Married before'  + self.fam[i]['MARR'].strftime('%Y-%m-%d') +  'Divorce'  + self.fam[i]['DIV'].strftime('%Y-%m-%d'))
        return error
    
    def US05(self): #  US05 Marriage before death - By Tanvi
        j = list()
        for i in self.indi:
            if 'DEAT' in self.indi[i].keys():
                death_dt = self.indi[i]['DEAT']
            if "FAMC" in self.indi[i].keys():
                fam_id = ''.join(self.indi[i]['FAMC'])
                if 'MARR' in self.fam[fam_id].keys():
                    marriage_dt = self.fam[fam_id]['MARR']
                    if  death_dt > marriage_dt:
                        j.append(['ANOMALY US05', self.indi[i]['id']])
                        print('ANOMALY: FAMILY: US05: ' + self.fam[fam_id]['fam'] + ' individual ' + self.indi[i]['id'] + ' Marriage ' + marriage_dt.strftime('%Y-%m-%d') + ' before death on ' + death_dt.strftime('%Y-%m-%d'))
        return j

   
    def US06(self): #  US06 Divorce before death - By Tanvi
        error = list()
        for i in self.indi:
            if 'DEAT' in self.indi[i].keys():
                death_dt = self.indi[i]['DEAT']
            if "FAMC" in self.indi[i].keys():
                fam_id = ''.join(self.indi[i]['FAMC'])
                
                if 'DIV' in self.fam[fam_id].keys():
                    div_dt = self.fam[fam_id]['MARR']
                    marriage_dt = self.fam[fam_id]['MARR']
                    if  death_dt > marriage_dt:
                        print('ANOMALY: FAMILY: US06: ' + self.fam[fam_id]['fam'] + ' individual ' + self.indi[i]['id'] + ' Marriage ' + div_dt.strftime('%Y-%m-%d') + ' before death on ' + death_dt.strftime('%Y-%m-%d'))
                        error.append(['ANOMALY US06', self.indi[i]['id']])
        return error


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
        error = list()
        for i in self.indi:
            if "FAMC" in self.indi[i].keys():
                child_birt = self.indi[i]['BIRT']
                fam_id = ''.join(self.indi[i]['FAMC'])
                if 'MARR' in self.fam[fam_id].keys():
                    marry_date = self.fam[fam_id]['MARR']
                    if marry_date > child_birt:
                        error.append(['ANOMALY: FAMILY: US08:', self.indi[i]['id']])
                        print('ANOMALY: FAMILY: US08: ' + self.fam[fam_id]['fam'] + ' Child ' + self.indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' before marriage on ' + marry_date.strftime('%Y-%m-%d'))
                if 'DIV' in self.fam[fam_id].keys():
                    div_date = self.fam[fam_id]['DIV']
                    if div_date < child_birt:
                        error.append(['ANOMALY: FAMILY: US08:', self.indi[i]['id']])
                        print('ANOMALY: FAMILY: US08: ' + self.fam[fam_id]['fam'] + ' Child ' + self.indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' after divorce on ' + div_date.strftime('%Y-%m-%d'))
        return error

    def US09(self): #  US09 Birth before death of parents - by Yuan
        error = list()
        for i in self.indi:
            if 'FAMC' in self.indi[i].keys():
                child_birt = self.indi[i]['BIRT']
                fam_id = ''.join(self.indi[i]['FAMC'])
                wife_id = self.fam[fam_id]['WIFE']
                hubID = self.fam[fam_id]['HUSB']
                if 'DEAT' in self.indi[wife_id].keys():
                    mom_deat = self.indi[wife_id]['DEAT']
                    if child_birt > mom_deat:
                        error.append(['ERROR US09', self.indi[i]['id']])
                        print('ERROR: FAMILY: US09: ' + fam_id + ' Child ' + self.indi[i]['id'] + ' born ' + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + " after mother's death on " + mom_deat.strftime('%Y-%m-%d'))
                if 'DEAT' in self.indi[hubID].keys():
                    dad_deat = self.indi[hubID]['DEAT']
                    if dad_deat - child_birt < timedelta(days = 270):
                        error.append(['ERROR US09', self.indi[i]['id']])
                        print('ERROR: FAMILY: US09: ' + fam_id + ' Child ' + self.indi[i]['id'] + ' born ' + self.indi[i]['BIRT'].strftime('%Y-%m-%d') + " after nine months after father's death on " + dad_deat.strftime('%Y-%m-%d'))
        return error

    def US10(self): #  US10 Marriage after 14 - by Yuan
        error = list()
        for i in self.fam:
            if 'MARR'in self.fam[i].keys():
                marry_date = self.fam[i]['MARR']
                self.fam_id = i
                husb_id = self.fam[i]['HUSB']
                wife_id = self.fam[i]['WIFE']
                husb_birt = self.indi[husb_id]['BIRT']
                wife_birt = self.indi[wife_id]['BIRT']
                if marry_date - husb_birt < timedelta(days = 5110): # 365days/yr * 14yr = 5110
                    error.append(['ANOMALY US10', self.fam_id])
                    print('ANOMALY: FAMILY: US10: ' + self.fam_id + ' Husband ' + self.indi[husb_id]['id'] + ' married on ' + marry_date.strftime('%Y-%m-%d') + ' before 14 years old (born on ' + husb_birt.strftime('%Y-%m-%d') + ')')
                if marry_date - wife_birt < timedelta(days = 5110): # 365days/yr * 14yr = 5110:
                    error.append(['ANOMALY US10', self.fam_id])
                    print('ANOMALY: FAMILY: US10: ' + self.fam_id + ' Wife ' + self.indi[wife_id]['id'] + ' married on ' + marry_date.strftime('%Y-%m-%d') + ' before 14 years old (born on ' + wife_birt.strftime('%Y-%m-%d') + ')')
        return error
    
    def US11(self): # US11 No Bigamy - by Vignesh Mohan
        error = list()
        for f in self.fam: 
            if 'MARR'in self.fam[f].keys():
                bigamy_check = {}
                families = {}
                for parent_id in bigamy_check:
                    family_group = filter(lambda fam: families[fam].has_key("MARR"),bigamy_check[parent_id])
                    if len(family_group) < 2: 
                        continue
                    def sortByMarr(family_id, family_idate2):
                        return dateDiff(families[family_idate2]['MARR'], families[family_id]['MARR'])
                    family_group = sorted(family_group, sortByMarr)

                    for i in range(len(family_group) - 1):
                        if families[family_group[i]].has_key('DIV'):
                            if dates_check(families[family_group[i]]['DIV'], families[family_group[i + 1]]['MARR']): 
                                continue

                            error.append(['ANOMALY: FAMILY: US11:', self.indi[i]['id']])
                            print ("User Story 11 - No bigamy.\n")
                            print ("ANOMALY: The family " + family_group[i] + " does not divorce before the marriage of family " + family_group[i + 1]  + ".")
        return error
        

    def US12(self): #US12 - Parents not too old - By Vignesh Mohan 
        error = list()
        for i in self.indi:
            if 'FAMC' in self.indi[i].keys():
                child_birt = self.indi[i]['BIRT']
                for key in self.fam.keys():
                    fam_id = ''.join(self.indi[i]['FAMC'])
                    if "HUSB" in self.fam[key]:
                        hubID = self.fam[key]['HUSB']
                    if "WIFE" in self.fam[key]:
                        wife_id = self.fam[key]['WIFE']
                    fam_id = ''.join(self.indi[i]['FAMC'])
                    husb_birt = self.indi[hubID]['BIRT']
                    wife_birt = self.indi[wife_id]['BIRT'] 
                    while wife_id:
                        dates_diff = (datetime.strptime(self.indi[child_birt],'%Y-%m-%d')).year - (datetime.strptime(self.indi[wife_birt],'%Y-%m-%d')).year
                        if dates_diff > 60:
                            print("US12 ANOMALY: Fam " + self.fam_id + ": The mother",self.indi[wife_id]['name']," is more than 60 years older than her child," + self.indi[child_birt]['name'],"\n")
                    while hubID:
                        dates_diff = (datetime.strptime(self.indi[child_birt],'%Y-%m-%d')).year - (datetime.strptime(self.indi[husb_birt],'%Y-%m-%d')).year
                        if dates_diff > 80:
                            print("US12 ANOMALY: Fam " + self.fam_id + ": The father", self.indi[hubID]['name']," is more than 60 years older than his child," + self.indi[child_birt]['name'],"\n") 
        return error
    
    def US13(self): # By Anirudh Bezzam
        '''Siblings spacing - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart'''
        result = False
        sibday = []
        sibmonth = []
        for key, family in self.fam.items():
            children_list = list(family.self.fam['CHIL'])
            if self.indi[list(family.self.fam['CHIL'])[0]].id in family.self.fam['CHIL']:
                for each_sibiling in children_list:
                    sib_birthday_month = datetime.today().strptime(self.indi[each_sibiling].birthday, '%Y-%m-%d').month
                    sib_birthday_day = datetime.today().strptime(self.indi[each_sibiling].birthday,  '%Y-%m-%d').day
                    sibday.append(sib_birthday_day)
                    sibmonth.append(sib_birthday_month)
                    for each_month_element in range(len(sibmonth)-1):
                        month_diff = sibmonth[each_month_element+1]-sibmonth[each_month_element]
                        if month_diff > 8:
                            result = True
                    for each_day_element in range(len(sibday)-1):
                        day_diff = sibday[each_day_element+1]-sibday[each_day_element]
                        print(day_diff)
                        if day_diff < 2:
                            result = True
        return result
    
    def US14(self): # By Anirudh Bezzam
        """ US14 Multiple Births <= 5 - No more than five siblings should be born at the same time """
        error = list()
        for i in self.indi:
            if "FAMC" in self.indi[i].keys():
                for key in self.fam.keys():
                    if 'CHIL' in self.fam[key]:
                        chil = self.fam[key]['CHIL']
                        child_birt = self.indi[i]['BIRT']
                        fam_id = ''.join(self.indi[i]['FAMC'])
                        if len(chil) > 5:  # Check logic
                            error.append(['ANOMALY: FAMILY: US14:', self.indi[i]['id']])
            print('ANOMALY: FAMILY: US14: ' + self.fam[fam_id]['fam'] + ' Sibling ' + self.indi[i]['id'] + ' born ' + child_birt.strftime('%Y-%m-%d') + ' at the same time on ' + child_birt.strftime('%Y-%m-%d'))
        return error
    
    def us15(self): # Tanvi - Fewer than 15 siblings
        false = False
        for key in self.fam.keys():
            if 'CHIL' in self.fam[key] :
                chil = self.fam[key]['CHIL']
                if len(chil) < 15:
                    print(f"Error: FAMILY: US15: Family '{key}'  has '{len(chil)}' number of children. No more than fourteen children should be born in each family.")
                    false = True
        return false

    def us16(self): #Tanvi - Male last names
        error = list()
        for i in self.indi:
            if 'FAMC' in self.indi[i].keys():
                fam_id = ''.join(self.indi[i]['FAMC'])
                if self.indi[i]['sex'] == 'M':
                    error.append(['ANOMALY US16', i])
                    last_name_male = self.indi[i]['name'].split('/')[1]
                    print(f" ANOMALY: FAMILY: US16: Male {self.indi[i]['id']} whose last name is {last_name_male}")
                    
        return error

                
    
    def US17(self): # US17: No marriages to children - by Lifu
        error = list()
        for i in self.indi:
            if('FAMS' in self.indi[i].keys()):
                fam_list = list(self.indi[i]['FAMS'])
                for j in fam_list:
                    if('CHIL' in self.fam[j].keys()):
                        if(self.fam[j]['WIFE'] in self.fam[j]['CHIL'] or self.fam[j]['HUSB'] in self.fam[j]['CHIL']):
                            error.append(['ERROR: FAMILY: US17'], j)
                            print('ERROR: FAMILY: US17: Parent ' + i + ' marries with children.')
        return error

    def US18(self): # US18: Siblings should not marry one another - by Lifu
        error = list()
        for i in self.indi:
            if('FAMS' in self.indi[i].keys() and 'FAMC' in self.indi[i].keys()):
                fams_list = list(self.indi[i]['FAMS'])
                famc_list = list(self.indi[i]['FAMC'])
                for j in fams_list:
                    for c in famc_list:
                        if('CHIL' in self.fam[c].keys()):
                            if(self.fam[j]['WIFE'] in self.fam[c]['CHIL'] and self.fam[j]['HUSB'] in self.fam[c]['CHIL']):
                                error.append([['ERROR: US18'], self.fam[j]['HUSB'], self.fam[j]['WIFE']])
                                print('ERROR: US18: Siblings marry Husband: ' + self.fam[j]['HUSB'] + ' Wife: ' + self.fam[j]['WIFE'])
        return error

    def US19(self): # US19 First cousins should not marry - by Yuan
        error = list()
        for f in self.fam: 
            if 'MARR'in self.fam[f].keys():
                # identify the husband and wife
                husb_id = self.fam[f]['HUSB']
                wife_id = self.fam[f]['WIFE']
                if 'FAMC' in self.indi[husb_id].keys() and 'FAMC' in self.indi[wife_id].keys():
                    husb_fam = ''.join(self.indi[husb_id]['FAMC'])
                    wife_fam = ''.join(self.indi[wife_id]['FAMC'])
                    # identify the parents of husband and wife to see if they are siblings
                    husb_parents = self.fam[husb_fam]['HUSB'], self.fam[husb_fam]['WIFE']
                    wife_parents = self.fam[wife_fam]['HUSB'], self.fam[wife_fam]['WIFE']
                    for husb_parent in husb_parents:
                        for wife_parent in wife_parents:
                            if 'FAMC' in self.indi[husb_parent].keys() and 'FAMC' in self.indi[wife_parent].keys() and ''.join(self.indi[husb_parent]['FAMC']) == ''.join(self.indi[wife_parent]['FAMC']):
                                error.append(['ANOMALY US19', f])
                                print('ANOMALY: FAMILY: US19: ' + f + ' Husband ' + self.indi[husb_id]['id'] + ' and wife ' + self.indi[wife_id]['id'] + " are cousins ")
        return error
    
    def US20(self): # US20 Aunts and uncles - by Yuan
        error = list()
        for f in self.fam: 
            if 'MARR'in self.fam[f].keys():
                # identify the husband and wife
                husb_id = self.fam[f]['HUSB']
                wife_id = self.fam[f]['WIFE']
                if 'FAMC' in self.indi[husb_id].keys() and 'FAMC' in self.indi[wife_id].keys():
                    husb_fam = ''.join(self.indi[husb_id]['FAMC'])
                    wife_fam = ''.join(self.indi[wife_id]['FAMC'])
                    # identify husband's parents to see if they're the wife's siblings
                    husb_parents = self.fam[husb_fam]['HUSB'], self.fam[husb_fam]['WIFE']
                    for husb_parent in husb_parents:
                        if 'FAMC' in self.indi[husb_parent].keys() and ''.join(self.indi[husb_parent]['FAMC']) == ''.join(self.indi[wife_id]['FAMC']):
                            error.append(['ANOMALY US20', f])
                            print('ANOMALY: FAMILY: US20: ' + f + ' Wife ' + self.indi[wife_id]['id']  + ' is husband ' + self.indi[husb_id]['id'] + "'s aunt")
                    # identify wife's parents to see if they're the husband's siblings
                    wife_parents = self.fam[wife_fam]['HUSB'], self.fam[wife_fam]['WIFE']
                    for wife_parent in wife_parents:
                        if 'FAMC' in self.indi[wife_parent].keys() and ''.join(self.indi[wife_parent]['FAMC']) == ''.join(self.indi[husb_id]['FAMC']):
                            error.append(['ANOMALY US20', f])
                            print('ANOMALY: FAMILY: US20: ' + f + 'Husband ' + self.indi[husb_id]['id']  + ' is wife ' + self.indi[wife_id]['id'] + "'s uncle")
        return error


def main():
    my_family = Gedcom('My-Family-15-Oct-2019-228.ged')
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
    my_family.US11()
    my_family.US12()
    my_family.US14()
    my_family.us15()
    my_family.us16()
    my_family.US17()
    my_family.US18()
    my_family.US19()
    my_family.US20()

if __name__ == '__main__':
    main()

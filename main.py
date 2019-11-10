from ged import Individual, Family, gedcom_parser
from prettytable import PrettyTable
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict, Counter

months = {"JAN":1,"FEB":2,"MAR":3,"APR":4,"MAY":5,"JUN":6,"JUL":7,"AUG":8,"SEP":9,"OCT":10,"NOV":11,"DEC":12}

def stringToDate(date1):
    date1year = int(date1[-4:])
    date1month = date1[-8:-5].upper()
    date1date = int(date1[:-9])
    return date1(date1year,months[date1month],date1date)

def dateDiff(date1,date2):
    # Parse dates
    date1 = stringToDate(date1)
    date2 = stringToDate(date2)

    difference = date2 - date1
    return difference.days

def dates_check(date1,date2,diffYear=0):
    return (dateDiff(date1, date2) - diffYear * 360) >= 0

class Repo:
    def __init__(self):
        """All information about Individual and Family"""
        self.individual = dict()
        self.family = dict()

    def add_individual(self, level, argument, tag, line_num): ## 
        self.individual[argument] = Individual(argument)
        self.individual[argument].add_line_num(line_num) ## add line number

    def add_family(self, level, argument, tag, line_num): ##
        self.family[argument] = Family(argument)
        self.family[argument].add_line_num(line_num) ## add line number

    def individual_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'partner'])
        for key in sorted(self.individual.keys()):
            pt.add_row(self.individual[key].pt_row())
        print(pt)

    def family_table(self):
        pt = PrettyTable(
            field_names=['ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])
        for key in sorted(self.family.keys()):
            pt.add_row(self.family[key].pt_row())
        print(pt)

    def read_file(self, path):
        for level, tag, argument, line_num in gedcom_parser(path): ##
            # print(level, tag, argument)
            result = list()
            valid_tags = {'NAME': '1', 'SEX': '1', 'MARR': '1',
                          'BIRT': '1', 'DEAT': '1', 'FAMC': '1', 'FAMS': '1',
                          'HUSB': '1', 'WIFE': '1', 'CHIL': '1',
                          'DIV': '1', 'DATE': '2', 'HEAD': '0', 'TRLR': '0', 'NOTE': '0'} # valid gedcom tags except INDI and FAM
            special_valid_tags = {'INDI': '0', 'FAM': '0'} # tags for INDI and FAM

            valid_tag_level = False 
            if argument in ['INDI', 'FAM']: # when the line record is valid with "0 xx INDI" or "0 xx FAM"
                special_tags = True
                for current_tag, current_level in special_valid_tags.items():
                    if level == current_level and argument == current_tag:
                        valid_tag_level = True
                        break
            else: ## other valid tag
                special_tags = False
                for current_tag, current_level in valid_tags.items():
                    if level == current_level and tag == current_tag:
                        valid_tag_level = True
                        break

            if valid_tag_level and special_tags: # if the line is valid top level i.e. "0 xx INDI" or "0 xx FAM"
                result.append(level)
                result.append(argument)
                result.append("Y")
                result.append(tag)
                if argument in ["INDI"]:
                    self.add_individual(level, tag, argument, line_num) # ## initiate a new individual with id and line number
                    current_id = tag
                else:
                    self.add_family(level, tag, argument, line_num) # ## initiate a new family with id and line number
                    current_id = tag
            elif not valid_tag_level and not special_tags: # if not valid
                result.append(level)
                result.append(tag)
                result.append("N")
                result.append(argument)
            elif valid_tag_level and not special_tags: # if valid but not top level
                result.append(level)
                result.append(tag)
                result.append("Y")
                result.append(argument)
                # add the record to the individual/family
                if tag == "NAME":
                    self.individual[current_id].add_name(argument)
                elif tag == "SEX":
                    self.individual[current_id].add_gender(argument)
                elif tag == "FAMC":
                    self.individual[current_id].add_child(argument)
                elif tag == "FAMS":
                    self.individual[current_id].add_partner(argument)
                elif tag in "HUSB":
                    self.family[current_id].add_husband_id(argument)
                    self.family[current_id].add_husband_name(self.individual[argument].name)
                elif tag in "WIFE":
                    self.family[current_id].add_wife_id(argument)
                    self.family[current_id].add_wife_name(self.individual[argument].name)
                elif tag in "CHIL":
                    self.family[current_id].add_children(argument)
                elif tag in ["BIRT", "DEAT", "DIV", "MARR"]:
                    check_date_tag = True
                    previous_tag = tag
                elif tag == "DATE" and check_date_tag is True:
                    argument = datetime.strptime(argument, '%d %b %Y').strftime('%Y-%m-%d')
                    if previous_tag == "BIRT":
                        self.individual[current_id].add_birthday(argument)
                        self.individual[current_id].add_age('Birth', argument)
                    elif previous_tag == "DEAT":
                        self.individual[current_id].add_death(argument)
                        self.individual[current_id].add_alive("False")
                        self.individual[current_id].add_age('Death', argument)
                    elif previous_tag == "MARR":
                        self.family[current_id].add_marriage(argument)
                    elif previous_tag == "DIV":
                        self.family[current_id].add_divorce(argument)

            else:
                result.append(level)
                result.append(argument)
                result.append("N")
                result.append(tag)

    
    """These 2 modules is to convert an integer result for the datetime modules as we were facing attribute errors""" # by Das
    def calculate_abs_date(self, date1, date2, limit, unit):
        """Function to check dates are in given range(limit)"""
        standardunit = {'days': 1, 'months': 30.4, 'year': 365.25}
        return abs((date1 - date2).days / standardunit[unit]) >= limit

    def stringify_date(self, value):
        """Function to convert string to date having format as YYYY-MM-DD"""
        value = datetime.strptime(value, '%Y-%m-%d')
        return value

    """Vignesh Mohan"""

    """US01 Dates before current date"""
    def US01(self):
        #getting todays date 
        today = datetime.today().strftime('%Y-%m-%d')

        result = False
        for key, individual in self.individual.items():
            for key, family in self.family.items():
                if individual.birthday > today:
                    print("Error US01:-Birthdate ", individual.birthday ,"is after current date")
                    result = True
                if individual.death > today:
                    print("Error US01:- Deathdate ", individual.death ,"is after current date")
                    result = True
                if family.marriage > today:
                    print("Error US01:- MarriageDate ", family.marriage ,"is after current date")
                    result = True
                if family.divorced > today:
                    print("Error US01:- DivorceDate ", family.divorced,"is after current date")
                    result = True
        return result

    """US02 Birth before Marriage"""
    def US02(self):
        result = False
        for key, individual in self.individual.items():  #Implementing as a dictionary.
            for key, family in self.family.items():
                if individual.birthday != 'NA' or family.marriage != 'NA':
                    if family.marriage > individual.birthday :
                        print(
                            "ANOMALY: FAMILY: US02: " + str(family.line_num) + " : " + key + " Birth " + individual.birthday + " should not occur before marriage  " + family.marriage)
                        result = True
        return result
    
    """US11 - No Bigamy"""
    def US11(self):
        result = False
        for f, fam in self.family.items(): 
            bigamy_check = {}
            families = {}
            for parent_id in bigamy_check:
                family_group = filter(lambda fam: families[fam].f_key("MARR"),bigamy_check[parent_id])
                if len(family_group) < 2: 
                    continue
                def sortByMarr(family_id, family_idate2):
                    return dateDiff(families[family_idate2]['MARR'], families[fam.id]['MARR'])
                family_group = sorted(family_group, sortByMarr)

                for i in range(len(family_group) - 1):
                    if families[family_group[i]].has_key('DIV'):
                        if dates_check(families[family_group[i]]['DIV'], families[family_group[i + 1]]['MARR']): 
                            continue
                        #error.append(['ANOMALY: FAMILY: US11:', self.indi[i]['id']])
                        print ("User Story 11 - No bigamy.\n")
                        print ("ANOMALY: The family " + family_group[i] + " does not divorce before the marriage of family " + family_group[i + 1]  + ".")
        return result
    


    
    """US21 Correct gender for role"""
    def US21(self):
        result = False
        for individual in self.individual.items():
            for key, fam in self.family.items():
                husband = self.individual["".join(fam.husband_id)]
                wife = self.individual["".join(fam.wife_id)]

                if husband.gender == "F" or husband.gender == "NA":
                    print('ANOMALY: FAMILY: US21: In family: ' + str(fam.line_num) + " : "  + key + ' husband gender is ' + husband.gender)

                elif wife.gender == "M" or wife.gender == "NA":
                    print('ANOMALY: FAMILY: US21: In family: ' + str(fam.line_num) + " : "  + key + ' wife gender is ' + wife.gender)
        return result
    
    """Individual ID and Family ID should be unique"""
    def US22(self):
        result = False

        #Dictionary of the family
        fam ={}
        #Dictionary of the individual
        indi ={}
         
        IndiID = []
        Namelist1 = []
        FamID = []
        famlist1 = []
        for individual_id in indi:
            individual = indi[individual_id]
            IndiID.append(individual_id)
        Namelist1 = set (IndiID)
        print("US22: Number of duplicate Individual IDs:-",len(IndiID)-len(Namelist1),"\n")
        for family_id in fam:
            family = fam[family_id]
            FamID.append(family_id)   
        famlist1 = set (FamID)
        print("US22: Number of duplicate Family IDs:-",len(FamID)-len(famlist1),"\n")
        return result

    """Anirudh Bezzam"""

    """US03 Birth before Death of Individual"""
    def US03(self):
        result = False
        for key, individual in self.individual.items():  #dict implementation
            if individual.birthday != 'NA' or individual.death != 'NA':
                if individual.birthday > individual.death:
                    print(
                        "Error: Individual: US03: " + key + " Birth " + individual.birthday + "should occur before death " + individual.death)
                    result = True
        return result

    """US04	Marriage before divorce"""
    def US04(self):
        result = False
        for key, family in self.family.items():
            if family.marriage < family.divorced:
                print(
                    "Error: FAMILY : US04 : " + key + " Marriage " + family.marriage + " should occur before divorce " + family.divorced)
                result = True
        return result

    """US13 - Birth Dates of Sibilings should be more than 8 months apart or less than 2 days apart"""
    def US13(self):
        result = False
        sibday = []
        sibmonth = []
        for key, family in self.family.items():
            children_list = list(family.children)
            if self.individual[list(family.children)[0]].id in family.children:
                for each_sibiling in children_list:
                    sib_birthday_month = datetime.today().strptime(self.individual[each_sibiling].birthday,
                                                                   '%Y-%m-%d').month
                    sib_birthday_day = datetime.today().strptime(self.individual[each_sibiling].birthday,
                                                                 '%Y-%m-%d').day
                    sibday.append(sib_birthday_day)
                    sibmonth.append(sib_birthday_month)
                    for each_month_element in range(len(sibmonth) - 1):
                        month_diff = sibmonth[each_month_element + 1] - sibmonth[each_month_element]
                        if month_diff > 8:
                            result = True
                        else:
                            print(
                                "Error: FAMILY : US13: Family sibiling spacing should be more than 8 months apart or less than 2 days apart",
                                key)

                    for each_day_element in range(len(sibday) - 1):
                        day_diff = sibday[each_day_element + 1] - sibday[each_day_element]
                        if day_diff < 2:
                            result = True
                        else:
                            print(
                                "Error: FAMILY : US13: Family sibiling spacing should be more than 8 months apart or less than 2 days apart",
                                key)
        return result

    """US14 - Multiple births <= 5"""
    def US14(self):
        result = False
        for key, family in self.family.items():
            birthday_list = list()
            list_of_children = family.children
            for child in list_of_children:
                birthday_list.append(self.individual[child].birthday)
            count_dict = dict((i, birthday_list.count(i)) for i in birthday_list)
            list_birthdays = count_dict.values()
            if max(list_birthdays) <= 5:
                result = True
            else:
                print(
                    "Error: FAMILY : US14: " + key + "Number of children born in a single birth should not be greater than 5")
        return result

    def US23(self): # by Anirudh Bezzam
        """US23 No more than one individual with the same name and birth date should appear in a GEDCOM file"""
        """Using a counter to flush out duplicates"""
        result = False
        count = Counter([individual.name + " " + individual.birthday for individual in self.individual.values()])
        for extra_copy, value in count.items():
            if value > 1:
                print("Error: INDIVIDUAL : US23: Name and age of Person has been repeated: " + extra_copy)
                result = True
        return result
    
    def US24(self): # by Anirudh Bezzam
        """US24 No more than one family with the same spouses by name and the same marriage date should appear in a GEDCOM file"""
        result = False
        duplicate_family = list()
        for key, family in self.family.items():
            wife_name = self.individual[list(family.wife_id)[0]].name
            marriage_date = family.marriage
            current_tuple = (wife_name, marriage_date)
            duplicate_family.append(current_tuple)
        family_dic = {duplicate: duplicate_family.count(duplicate) for duplicate in duplicate_family}
        for family_dic_key, family_dic_value in family_dic.items():
            if family_dic_value > 1:
                print("Error: FAMILY : US24: " + str(family.line_num) + "More than one family with the same spouses by name " + family_dic_key[0] + " and the same marriage date " + family_dic_key[1])
                result = True
        return result


    def US38(self): # by Anirudh Bezzam
        """List upcoming birthdays""" 
        result = False
        list_result = list()
        today_date = datetime.today().strftime('%m-%d');
        today_date_plus30 = datetime.now() + relativedelta(days=30)
        today_date_plus30 = today_date_plus30.strftime('%m-%d')
        for key, individual in self.individual.items():
            if individual.death == 'NA':
                birthday = datetime.strptime(individual.birthday, '%Y-%m-%d')
                birthday = birthday.strftime('%m-%d')
                if today_date < birthday < today_date_plus30:
                    list_result.append("Name: " + individual.name + " Birthday: " + individual.birthday)
                    result = True
        print("List of upcoming birthday :")
        print('\n'.join(str(p) for p in list_result))
        return result
    


    """Tanvi Hanamshet"""
    """unique first name in family"""
    def US25(self):
        result = list()
        for key, individual in self.individual.items():
            unique_names = []
            names = []
            list_of_names = individual.name.split("/")[0]
            names.append(list_of_names)
            for i in names:
                if i not in unique_names:
                    unique_names.append(i)
            for name in unique_names:
                print("ANOMALY: INDIVIDUAL : US25: " + str(individual.line_num) + " : " + key + " Unique name in family: "+ name)
            result.append(unique_names)
        return result
            
        

    """ List all people in a GEDCOM file who were born in the last 30 days.-Tanvi """
    def US35(self):
        result = list()
        for key, individual in self.individual.items():
            d1 = datetime.strptime(individual.birthday, '%Y-%m-%d')
            d2 = (datetime.today().strftime('%Y-%m-%d'))
            d2 = datetime.strptime(d2, '%Y-%m-%d')
            conversion = {'days':1,'months':30.4,'years':365.25}
            diff = abs((d1 - d2).days)
            
            if diff >= 0 and diff <30.4:
                time_typ = 'days'
                diff1 = diff/conversion[time_typ]
                if time_typ == 'days' and diff1 <= 30:
                    print("ANOMALY: INDIVIDUAL: US35: " + str(individual.line_num) + " : " + key +" People who were born in the last 30 days are "+ individual.name + " on "+individual.birthday)
                    result.append(key)
        return result


    """Lifu Xiao"""
    def US07(self): #  US07 Less then 150 years old
        result = list()
        for key, individual in self.individual.items():
            if(individual.age > 150):
                print("ERROR: INDIVIDUAL: US07: " + str(individual.line_num) + key + "  More than 150 years old: Birth date "+ individual.birthday)
                result.append(key)
        return result

    def US08(self): #  US08 Birth before marriage of parents
        result = list()
        for key, individual in self.individual.items():
            if(individual.child != 'NA'):
                for c in individual.child:
                    fam = self.family[c]
                    if(fam.divorced != 'NA'):
                        div_date = datetime.strptime(fam.divorced, '%Y-%m-%d')
                        child_birth_date = datetime.strptime(individual.birthday, '%Y-%m-%d')
                        if(child_birth_date > div_date):
                            print('ANOMALY: FAMILY: US08: ' + c + ' Child ' + key + ' born ' + individual.birthday + ' after divorce on ' + fam.divorced)
                            result.append(key)
                    if(fam.marriage != 'NA'):
                        marr_date = datetime.strptime(fam.marriage, '%Y-%m-%d')
                        child_birth_date = datetime.strptime(individual.birthday, '%Y-%m-%d')
                        if(marr_date > child_birth_date):
                            print('ANOMALY: FAMILY: US08: ' + str(individual.line_num) + c + ' Child ' + key + ' born ' + individual.birthday + ' before marriage on ' + fam.marriage)
                            result.append(key)
        return result

    def US17(self): #  US17: No marriages to children
        result = list()
        for key, individual in self.individual.items():
            if(individual.partner != 'NA'):
                for p in individual.partner:
                    fam = self.family[p]
                    if(fam.children != 'NA'):
                        if (fam.children & set(fam.wife_id) != set() or fam.children & set(fam.husband_id) != set()):
                            print('ERROR: FAMILY: US17: Parent ' + str(individual.line_num) + key + ' marries with children or parents.')
                            result.append(key)
        return result
    
    def US18(self): #  US18: Siblings should not marry one another
        result = list()
        for key, individual in self.individual.items():
            if(individual.partner != 'NA' and individual.child != 'NA'):
                for p in individual.partner:
                    for c in individual.child:
                        famc = self.family[c]
                        fams = self.family[p]
                        if(famc.children != 'NA'):
                            if(famc.children & set(fams.wife_id) != set() and famc.children & set(fams.husband_id) != set()):
                                print('ERROR: US18: ' + str(individual.line_num) + key + ' Siblings marry')
                                result.append(key)
        return result

    def US27(self): #  Include individual ages
        result = list()
        status = True
        for key, individual in self.individual.items():
            if(individual.age == 'NA'):
                status = False
                print('ERROR: US27: ' + str(individual.line_num) + key + ' lacks age information')
                result.append(key)
        if(status):
            print('US27: All peolple include ages!')
        return result
    
    def US28(self): #  Order siblings by age
        result = list()
        for key, family in self.family.items():
            if(family.children != 'NA' and len(family.children) > 1):
                chil = dict()
                for c in family.children:
                    age = self.individual[c].age
                    chil[age] = c
                chil = sorted(chil.items())
                print('Siblings in '+key+':')
                for k,v in chil:
                    print (v+': '+str(k))
                result.append(chil)
        return result

    """Yuan Zhang"""
    def US09(self): # US09 Birth before death of parents - by Yuan
        error = set()
        for key, individual in self.individual.items(): # scan children
            if (individual.child != 'NA'): # if the individual is a child of some family
                for c in individual.child: # each family the individual is a child of
                    fam = self.family[c]
                    father = self.individual[''.join(fam.husband_id)]
                    mother = self.individual[''.join(fam.wife_id)]
                    if father.alive != "TRUE":
                        if individual.birthday > father.death:
                            print('ERROR: FAMILY: US09: ' + str(fam.line_num) + ": " + fam.id + ' Child ' + individual.id + ' born ' + individual.birthday + " after father's death on " + father.death)
                            error.add(key)
                    if mother.alive != "TRUE":
                        if individual.birthday > mother.death:
                            print('ERROR: FAMILY: US09: ' + str(fam.line_num) + ": " + fam.id + ' Child ' + individual.id + ' born ' + individual.birthday + " after mother's death on " + mother.death)
                            error.add(key)
        return error

    def US10(self): # US10 Marriage after 14 - by Yuan
        error = set()
        for key, individual in self.individual.items(): # scan individual
            birt_date = datetime.strptime(individual.birthday, '%Y-%m-%d')
            if individual.partner != 'NA':
                for f in individual.partner:
                    fam = self.family[f]
                    if fam.marriage != 'NA':
                        marr_date = datetime.strptime(fam.marriage, '%Y-%m-%d')
                        if marr_date - birt_date < timedelta(days = 5110): # 365days/yr * 14yr = 5110
                            error.add(key)
                            print('ANOMALY: INDIVIDUAL: US10: ' + str(individual.line_num) + ": " + individual.id + ' married on ' + fam.marriage + ' before 14 years old (born on ' + individual.birthday + ')')
        return error      
    
    def US19(self): # US19 First cousins should not marry - by Yuan
        error = set()
        for key, fam in self.family.items(): # scan families
            # identify the husband and wife
            husb = self.individual["".join(fam.husband_id)]
            wife = self.individual["".join(fam.wife_id)]
            # if the husband/wife is the child of some family
            if husb.child != "NA":
                for h_c in husb.child:
                    if wife.child != "NA": 
                        for w_c in wife.child:
                            husb_fam = self.family[h_c]
                            wife_fam = self.family[w_c]
                            # identify the parents of husband and wife to see if they are siblings
                            husb_parents = self.individual["".join(husb_fam.husband_id)], self.individual["".join(husb_fam.wife_id)]
                            wife_parents = self.individual["".join(wife_fam.husband_id)], self.individual["".join(wife_fam.wife_id)]
                            for husb_parent in husb_parents:
                                for wife_parent in wife_parents:
                                    # if the parents are siblings, the husband and wife are first cousons
                                    if husb_parent.child != "NA" and wife_parent.child != "NA" and "".join(husb_parent.child) == "".join(wife_parent.child): 
                                        error.add(key)
                                        print('ANOMALY: FAMILY: US19: ' + str(fam.line_num) + ": In family " + fam.id + ' husband ' + husb.id + ' and wife ' + wife.id + " are cousins ")
        return error

    def US20(self): # US20 Aunts and uncles - by Yuan
        error = set()
        for key, fam in self.family.items(): # scan families
            # identify the husband and wife
            husb = self.individual["".join(fam.husband_id)]
            wife = self.individual["".join(fam.wife_id)]
            # if the husband/wife is the child of some family
            if husb.child != "NA":
                for h_c in husb.child:
                    if wife.child != "NA": 
                        for w_c in wife.child:
                            husb_fam = self.family[h_c]
                            wife_fam = self.family[w_c]
                            # identify husband's parents to see if they're the wife's siblings
                            husb_parents = self.individual["".join(husb_fam.husband_id)], self.individual["".join(husb_fam.wife_id)]
                            for husb_parent in husb_parents:
                                if husb_parent.child != "NA" and "".join(husb_parent.child) == "".join(wife.child): 
                                    error.add(key)
                                    print('ANOMALY: FAMILY: US20: ' + str(fam.line_num) + ": In family " + fam.id + ' wife ' + wife.id + ' is husband ' + husb.id + "'s aunt")
                            # identify wife's parents to see if they're the husband's siblings
                            wife_parents = self.individual["".join(wife_fam.husband_id)], self.individual["".join(wife_fam.wife_id)]
                            for wife_parent in wife_parents:
                                if wife_parent.child != "NA" and "".join(wife_parent.child) == "".join(husb.child): 
                                    error.add(key)
                                    print('ANOMALY: FAMILY: US20: ' + str(fam.line_num) + ": In family " + fam.id + ' husband ' + husb.id + ' is wife ' + wife.id + "'s uncle")
        return error

    def US29(self): # List all deceased individuals in a GEDCOM file - Yuan Zhang
        error = set()
        print("--- US29: All deceased individuals ---")
        for key, individual in self.individual.items(): # scan individual
            if individual.alive != "TRUE":
                print(individual.id + ": " + individual.name)
                error.add(key)
        print("--- End of all deceased individuals ---")
        return error

    def US30(self): # List all living married people in a GEDCOM file - Yuan Zhang
        error = set()
        print("--- US30: All living married people ---")
        for key, individual in self.individual.items(): # scan individual
            if individual.alive == "TRUE" and individual.partner != "NA":
                print(individual.id + " " + individual.name)
                error.add(key)
        print("--- End of all living married people ---")
        return error

def main():
    # there are several gedcom files
    """ myfamily.ged """
    repo1 = Repo()
    repo1.read_file('ged/myfamily.ged')
    print("\n\nTest file: myfamily.ged")
    print("\n Individual Summary")
    repo1.individual_table()

    print("\n Family Summary")
    repo1.family_table()
    repo1.US01()
    repo1.US02()
    repo1.US07()
    repo1.US08()
    repo1.US11()
    repo1.US18()
    repo1.US27()
    repo1.US28()
    repo1.US25()
    #repo1.US33()
    repo1.US38()
    
    

    """ das.ged """
    repo2 = Repo()
    repo2.read_file('ged/das.ged')
    repo2.US03()
    repo2.US04()
    repo2.US12()
    repo2.US13()
    repo2.US14()
    repo2.US22()
    repo2.US23()
    repo2.US24()
    

    """us17.ged"""
    repo3 = Repo()
    repo3.read_file('ged/us17.ged')

    repo3.US17()

    """Yuan"""
    repo1.US09()
    repo1.US10()
    repo1.US19()
    repo1.US20()
    repo1.US29()
    repo1.US30()
    
    """Ged for US21"""
    repo4 = Repo()
    repo4.read_file('ged/My-Family-28-Oct-2019-667.ged')

    repo4.US21()

    """Ged for US11"""
    repo5 = Repo()
    repo5.read_file('ged/My-Family-29-Oct-2019-620.ged')
    repo5.US11()

    """Ged for US35"""
    repo5 = Repo()
    repo5.read_file('ged/My-Family-29-Oct-2019-793.ged')
    repo5.US35()

if __name__ == '__main__':
    main()
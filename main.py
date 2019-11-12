from ged import Individual, Family, gedcom_parser
from prettytable import PrettyTable
from datetime import date, datetime
from datetime import timedelta
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

    def stringify_dates(self, value):
            """String the instance of the datetime"""
            value = datetime.strptime(value, '%Y-%m-%d')
            return value

    def calc_abs_dates(self, date1, date2, limit, unit):
        """Calculate the absolute values and limit ranges of dates"""
        standardunit = {'days': 1, 'months': 30.4, 'year': 365.25}
        return abs((date1 - date2).days / standardunit[unit]) >= limit
        

    """Vignesh Mohan"""

    """US01 Dates before current date"""
    def US01(self):
        #getting todays date 
        today = str(date.today())

        result = False
        for key, individual in self.individual.items():
            for key, family in self.family.items():
                if individual.birthday != 'NA':
                    if individual.birthday > today:
                        print("Error US01:-" + str(family.line_num) + ": Birthdate" + ": " + individual.birthday + " is after current date")
                        result = True
                if individual.death != 'NA':
                    if individual.death > today:
                        print("Error US01:-"  + str(family.line_num) + ": Deathdate" + ": " + individual.death + " is after current date")
                        result = True
                if family.marriage != 'NA':
                    if family.marriage > today:
                        print("Error US01:-" + str(family.line_num) + ": MarriageDate" + ": " + family.marriage + " is after current date")
                        result = True
                if family.divorced != 'NA':
                    if family.divorced > today:
                        print("Error US01:-" + str(family.line_num) + ": Divorceddate"  + ": " + family.divorced + " is after current date")
                        result = True
        return result

    """US02 Birth before Marriage"""
    def US02(self):
        result = False
        for key, individual in self.individual.items():  #Implementing as a dictionary.
            for key, family in self.family.items():
                if individual.birthday != 'NA' or family.marriage != 'NA':
                    if individual.birthday > family.marriage:
                        print(
                            "ERROR: FAMILY: US02: " + str(family.line_num) + " : " + key + " Birth " + individual.birthday + " should occur after marriage  " + family.marriage + " and not before")
                        result = True
        return result
    
    """No Bigamy"""
    def US11(self):
        result = False
        #today=datetime.date.today()
        for key, family in self.family.items():
            if family.marriage != 'NA':
                currentFamId=family.id
            for key, family2 in self.family.items():
                if currentFamId!=family.id:
                    if family.husband_id==family2.husband_id or family.wife_id==family2.wife_id:
                        if family.marriage<family2.marriage:
                            if family.divorced!='NA' and family.divorced>family2.married:
                                error = "Bigamy detected!"
                                error_loc = [family.id,family2.id]
                            print("\n########  US11  ########")
                            print("ERROR US11: " + str(family.line_num) + ":" +" Marriage should not occur during marriage to another spouse:\n" + family.id)
                            print("")

                        if family.marriage>family2.marriage:
                            if family.divorced!='NA' and family.divorced<family2.marriage:
                                error = "Bigamy detected!"
                                error_loc = [family.uid,family2.id]
                            print("\n########  US11  ########")
                            print("ERROR US11:" + str(family.line_num) +  ":" + " Marriage should not occur during marriage to another spouse:\n" + family.id)
                            print("")
        return result

    def US12(self):
        """US12 - Mother should be less than 60 years older than her children and father should be less than 80 years older than his children"""
        result = False
        for key, family in self.family.items():
            listofchildren = list(family.children)
            mother = list(family.wife_id)[0]
            father = list(family.husband_id)[0]
            for child in listofchildren:
                if self.calc_abs_dates(self.stringify_dates(self.individual[mother].birthday),
                                  self.stringify_dates(self.individual[child].birthday), 60, "year"):
                    print(
                        "Error: FAMILY : US12 : " + key + " : Mother " + mother + " should not be less than 60 years older than her child " + child)
                    result = True
                if self.calc_abs_dates(self.stringify_dates(self.individual[father].birthday),
                                  self.stringify_dates(self.individual[child].birthday), 80, "year"):
                    print(
                        "Error: FAMILY : US12 : " + key + " : Father " + father + " should not be less than 80 years older than his child " + child)
                    result = True
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
    
    """People over 30 who are not married"""
    def US31(self):
        result = False
        people=[]
        currentDate=str(date.today())
        for key, individual in self.individual.items():
            for key, family in self.family.items():
                birthDate = individual.birthday
                spouse = family.marriage
                name = individual.name[0]
                if birthDate!='NA':
                    lifeSpan = datetime.strptime(currentDate, '%Y-%m-%d') - datetime.strptime(birthDate, '%Y-%m-%d')
                    age = datetime.strptime(birthDate, '%Y-%m-%d')
                    if (age > datetime.strptime(currentDate, '%Y-%m-%d')) and datetime.strptime(birthDate, '%Y-%m-%d') > datetime.strptime(currentDate, '%Y-%m-%d'):
                        age = lifeSpan
                    else:
                        age = lifeSpan-timedelta(days=1)
                    if lifeSpan > timedelta(days=30):
                        if spouse:
                            pass
                        else:
                            people.append(name)
            print("ERROR: INDIVIDUAL: US31: " + str(family.line_num) + ':' +" All living people over 30 in family " + family.id + " who have never been married are: " + individual.name)
        return result   

    """List Multiple Births"""
    def US32(self):
        result = False
        for key, family in self.family.items():
            if len(family.children) > 1:
                print('ANOMALY: FAMILY: US32: ' + str(family.line_num) + ':' + ' There are multiple births in the family' + ": " + family.id)
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

    """Tanvi Hanamshet"""
    def US05(self):#  US05 Marriage before death - By Tanvi
        j = list()
        for key, individual in self.individual.items():
            for k, family in self.family.items():
                if individual.death != 'NA' and family.marriage != 'NA':
                    if individual.death > family.marriage:
                        j.append(['ANOMALY US05', key])
                        print('ANOMALY: FAMILY: US05: ' + str(family.line_num) + str(key) + ' individual ' + str(key) + ' Divorced ' + family.marriage + ' before death on ' + individual.death)
        print(j)##test case
        return j

    """US06 Divorce before death - By Tanvi"""
    def US06(self):
        error = list()
        for key, individual in self.individual.items():
            for k, family in self.family.items():
                if individual.death != 'NA' and family.divorced != 'NA':
                    error.append(['ANOMALY US06', key])
                    print('ANOMALY: FAMILY: US06: ' + str(family.line_num) + str(key) + ' individual ' + str(key) + ' Marriage ' + family.divorced + ' before death on ' + individual.death)

        print(error)##test case
        return error


    def US15(self): # Tanvi - Fewer than 15 siblings
        false = False
        for key, individual in self.individual.items():
            if(individual.partner != 'NA' and individual.child != 'NA'):
                for p in individual.partner:
                    for c in individual.child:
                        famc = self.family[c]
                        if(famc.children != 'NA'):
                            if len(famc.children) < 15:
                                print(f"Error: FAMILY: US15: Family '{key}'  has '{len(famc.children)}' number of children. No more than fourteen children should be born in each family.")
                                false = True
        print(false)
        # return false


    """Tanvi - Male last names"""
    def US16(self):
        error = list()
        for key, individual in self.individual.items():
            if individual.gender != 'NA':
                if individual.gender == 'M':
                    error.append(['ANOMALY US16', key])
                    last_name_male = individual.name.split('/')[1]
                    print(f" ANOMALY: FAMILY: US16: Male {key} whose last name is {last_name_male}")
        print(error)           
        return error


    def US26(self):
        invalid_list = list()
        fam_id = list()
        for k, individual in self.individual.items():
            for key, fam in self.family.items(): 
                fam_id.append(key) 
                                
                husband = self.individual["".join(fam.husband_id)]
                wife = self.individual["".join(fam.wife_id)]
                if husband.gender != 'M':
                    invalid_list.append("Misgendered husband in family: " + key)
                else:
                    invalid_list.append("Missing husband: " + husband.id +" in family: " + key)
                if wife.gender != 'M':
                    invalid_list.append("Misgendered husband in family: " + key)
                else:
                    invalid_list.append("Missing wife: " + wife.id + " in family: " + key)
                if(individual.child != 'NA'):
                    for child in individual.child:
                        if child not in fam_id:
                            invalid_list.append("Missing child: " + child + " in family: " + key)

                            
        # print(invalid_list)

    """unique first name in families"""
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

    """ List all people who were death in the last 30 days.-Tanvi """
    def US36(self):
        result = list()
        for key, individual in self.individual.items():
            if individual.death != 'NA':
                d1 = datetime.strptime(individual.death, '%Y-%m-%d')
                d2 = (datetime.today().strftime('%Y-%m-%d'))
                d2 = datetime.strptime(d2, '%Y-%m-%d')
                # print(d1, d2)
                conversion = {'days':1,'months':30.4,'years':365.25}
                diff = abs((d1 - d2).days)
                if diff >= 0 and diff <30.4:
                    time_typ = 'days'
                    diff1 = diff/conversion[time_typ]
                    if time_typ == 'days' and diff1 <= 30:
                        print("ANOMALY: INDIVIDUAL: US35: " + str(individual.line_num) + " : " + key +" People who were dead in the last 30 days are "+ individual.name + " on "+individual.birthday)
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
            if(individual.age == ''):
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
                print('US28: Siblings in '+key+':')
                for k,v in chil:
                    print (v+': '+str(k))
                result.append(chil)
        return result

    def US37(self): #  List recent survivors
        result = list()
        for key, individual in self.individual.items():
            if(individual.death != 'NA'):
                death_date = datetime.today() - datetime.strptime(individual.death, '%Y-%m-%d')
                if(death_date <= timedelta(days=30) and death_date > timedelta(days=0)):
                    if(individual.partner != 'NA'):
                        for family in individual.partner:
                            fam = self.family[family]
                            indi = fam.wife_id | fam.husband_id | fam.children
                            namelist = str()
                            for i in indi:
                                if(self.individual[i].alive == 'TRUE'):
                                    namelist +=(i + ' ')
                            print('US37: living spouses and descendants of ' + individual.id + ' :' + namelist)
                            result.append(individual.id)
        return result
    
    def US38(self): #  List upcoming birthdays
        result = list()
        for key, individual in self.individual.items():
            if(individual.birthday != 'NA'):
                birthday = datetime.strptime(individual.birthday, '%Y-%m-%d')
                today = datetime.today()
                if(birthday.month, birthday.day) >= (today.month, today.day):
                    birthday = birthday.replace(year=today.year)
                else:
                    birthday = birthday.replace(year=today.year + 1)
                if(birthday - today <= timedelta(days=30)):
                    print('US38: upcoming birthdays:' + key)
                    result.append(key)
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
        res = set()
        for key, individual in self.individual.items(): # scan individual
            birt_date = datetime.strptime(individual.birthday, '%Y-%m-%d')
            if individual.partner != 'NA':
                for f in individual.partner:
                    fam = self.family[f]
                    if fam.marriage != 'NA':
                        marr_date = datetime.strptime(fam.marriage, '%Y-%m-%d')
                        if (not(key in res)) and marr_date - birt_date < timedelta(days = 5110): # 365days/yr * 14yr = 5110
                            res.add(key)
                            print('ANOMALY: INDIVIDUAL: US10: ' + str(individual.line_num) + ": " + individual.id + ' married on ' + fam.marriage + ' before 14 years old (born on ' + individual.birthday + ')')
        return res 
        '''
        for key, fam in self.family.items():
            # identify the husband and wife
            husb = self.individual["".join(fam.husband_id)]
            wife = self.individual["".join(fam.wife_id)]
            if fam.marriage != "NA":
                pt.add_row([husb.id, husb.name, husb.alive, fam.id, wife.id])
                pt.add_row([wife.id, wife.name, wife.alive, fam.id, husb.id])
                error.add(husb.id)
                error.add(wife.id)
        print(pt)
        return error   
        '''  
    
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
        print("US29: List all deceased individuals")
        pt = PrettyTable(
            ##field_names=['ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'partner'])
            field_names=['ID', 'Name', 'Alive', 'Birthday', 'Death Date'])
        for key, individual in self.individual.items(): # scan individual
            if individual.alive != "TRUE":
                pt.add_row([individual.id, individual.name, individual.alive, individual.birthday, individual.death])
                ##print(individual.id + ": " + individual.name)
                error.add(key)
        print(pt)
        return error

    def US30(self): # List all living married people in a GEDCOM file - Yuan Zhang
        error = set()
        print("US30: List all living married people")
        pt = PrettyTable(
            field_names=['ID', 'Name', 'Alive',  'Family ID', 'Partner'])
        for key, fam in self.family.items():
            # identify the husband and wife
            husb = self.individual["".join(fam.husband_id)]
            wife = self.individual["".join(fam.wife_id)]
            if fam.divorced == "NA" and husb.alive == "TRUE" and wife.alive == "TRUE":
                pt.add_row([husb.id, husb.name, husb.alive, fam.id, wife.id])
                pt.add_row([wife.id, wife.name, wife.alive, fam.id, husb.id])
                error.add(husb.id)
                error.add(wife.id)
        print(pt)
        return error

    def US39(self): # List all living couples whose marriage anniversaries occur in the next 30 days
        res = set()
        print("US39: List upcoming anniversaries")
        pt = PrettyTable(
            field_names=['Family ID', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Aniversary'])
        for key, fam in self.family.items():
            # identify the husband and wife
            husb = self.individual["".join(fam.husband_id)]
            wife = self.individual["".join(fam.wife_id)]
            if fam.divorced == "NA" and fam.marriage != "NA" and husb.alive == "TRUE" and wife.alive == "TRUE" :
                marr_date = datetime.strptime(fam.marriage, '%Y-%m-%d')
                today_date = datetime.today()
                if (marr_date.month, marr_date.day) > (today_date.month, today_date.day):
                    anniversary = marr_date.replace(year=today_date.year)
                else:
                    anniversary = marr_date.replace(year=today_date.year + 1)
                if  timedelta(days = 0) < anniversary - today_date < timedelta(days = 30): # 
                    pt.add_row([fam.id, husb.id, husb.name, wife.id, wife.name, fam.marriage])
                    res.add(fam.id)
        print(pt)
        return res
    
    def US40(self):
        print("US40: List line numbers from GEDCOM source file when reporting errors")
        print(" - Demostrated in all previous user stories")
        print("   Example: ", end="")
        self.US20()
        return self.family['@F11@'].line_num # for test: the line num of @F11@
        

def main():
    # there are several gedcom files
    """ myfamily.ged """
    repo1 = Repo()
    repo1.read_file('ged/My-Family.ged')
    print("\n\nTest file: myfamily.ged")
    print("\n Individual Summary")
    repo1.individual_table()

    print("\n Family Summary")
    repo1.family_table()
    
    repo1.US01()
    repo1.US02()
    repo1.US07()
    repo1.US08()
    repo1.US18()
    repo1.US21()
    repo1.US28()
    repo1.US25()
    repo1.US31()
    repo1.US32()
    repo1.US37()
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

    """us17&27.ged"""
    repo3 = Repo()
    repo3.read_file('ged/us17.ged')
    repo3.US17()
    repo3.US27()

    """Yuan"""
    repo1.US09()
    repo1.US10()
    repo1.US19()
    repo1.US20()
    repo1.US29()
    repo1.US30()
    repo1.US39()
    repo1.US40()    

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
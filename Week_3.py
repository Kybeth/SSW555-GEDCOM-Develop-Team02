from datetime import datetime
from prettytable import PrettyTable as pt

valid = {
    '0':(['INDI','FAM'],'HEAD','TRLR','NOTE'),
    '1':('NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV'),
    '2':('DATE'),
} # dictionary stores valid tags


def age_cal(birthday): # calculate individual's age
    birthdate = datetime.strptime(birthday, '%d%b%Y')
    current = datetime.today()
    return current.year - birthdate.year - ((current.month, current.day) < (birthdate.month, birthdate.day))

def parse_file(path,encode = 'utf-8'):
    """read the file from the path, based on level and tag scratch the information line by line and store in the dictionary,
       print the summary of individuals and families
    """
    with open(path,'r',encoding=encode) as ged_file:
        isValid = 'N'
        IsIND = True
        indi = {}
        fam = {}
        currentDate = ''
        currentInd = ''
        currentFam = ''
        for line in ged_file:    
            word_list = line.strip().split()
            arguments = ''.join(word_list[2:])
            tag = 'NA'
            level = 'NA'

import pickle, os.path
import expclass
from psychopy import data

def makeExcel():
    with open("data3x3.dat", "rb") as f:
        experiidata = pickle.load(f)

    el=experiidata.get_explist()


    # print(el)
    for i in el:
        fileName = 'Participant_' + i.get_subject().get_subnumber() + '_' + i.get_subject().get_rundate()
        if os.path.isfile(fileName + '.csv'):
            continue
        else:
            dataFile = open(fileName + '.csv', 'w')

        dataCategories = 'Subject number,Birthdate,Gender,Rundate,\
        Practice,\
        Block number,AttendType,\
        Trial number,StimType,StimOrder1,StimOrder2,\
        Stim1,Stim2,Stim3,Stim4,Stim5,Stim6,\
        Response1,Response2,Response3,Response4,Response5,Response6,\
        Error1,Error2,Error3,Error4,Error5,Error6,\
        ResponseTime1,ResponseTime2,ResponseTime3,ResponseTime4,ResponseTime5,ResponseTime6\n'

        dataFile.write(dataCategories)

        sub = i.get_subject()
        tri = i.get_triallist()


        for j in tri:
            index = 0
            attendType = j.get_attendtype()

            dataFile.write(sub.get_subnumber() + ',' + sub.get_bday() + ',' + sub.get_gender() + ',' + sub.get_rundate() + ',' +
            j.get_practice() + ',' + str(j.get_blocknum()) + ',' + attendType + ',' +
            str(j.get_trialnum()) + ',' + str(j.get_stimtype()) + ',')
            stimOrder = str(j.get_stimorderlist()[0]).replace(',', '')
            print(stimOrder)
            dataFile.write(stimOrder + ',')
            if attendType != 'Single':
                stimOrder = str(j.get_stimorderlist()[1]).replace(',', '')
                dataFile.write(stimOrder + ',')
            else:
                dataFile.write('na,')
            for k in j.get_stimlist():
                for l in k:
                    dataFile.write(str(l) + ',')

                index+=1
            index = 0
            if attendType == 'Single':
                dataFile.write('na,na,na,')

            if attendType == 'Second':
                dataFile.write('na,na,na,')
            for k in j.get_responselist():
                for l in k:
                    dataFile.write(str(l) + ',')
                index+=1
            index = 0
            if attendType == 'Single' or attendType == 'First':
                dataFile.write('na,na,na,')

            if attendType == 'Second':
                dataFile.write('na,na,na,')
            for k in j.get_errorlist():
                for l in k:
                    dataFile.write(str(l) + ',')
                index+=1
            index = 0
            if attendType == 'Single' or attendType == 'First':
                dataFile.write('na,na,na,')

            if attendType == 'Second':
                dataFile.write('na,na,na,')
            for k in j.get_responsetimelist():
                for l in k:
                    dataFile.write(str(l) + ',')
                index+=1
            index = 0
            if attendType == 'Single' or attendType == 'First':
                dataFile.write('na,na,na,')
            dataFile.write('\n')

def makeDemoExcel():
    with open("data3x3.dat", "rb") as f:
        experiidata = pickle.load(f)

        dl = experiidata.get_demolist()

        fileName = 'Demographics_3x3_' + data.getDateStr()

        dataFile = open(fileName + '.csv', 'w')

        demoCategories = 'Subject Number, Age, Birthdate,\
        Gender, Class, Ethnicity, Race, First Language,\
        Fluent in English, Medication, Hearing problem,\
        20/20,Glasses/Contacts,Colorblind,Wearing\n'

        dataFile.write(demoCategories)


        for i in dl:
            dataFile.write(str(i.get_subnumber()) + ',' +
            str(i.get_age()) + ',' + str(i.get_bday()) + ',' +
            str(i.get_gender()) + ',' + str(i.get_class()) + ',' +
            str(i.get_ethnicity()) + ',' + str(i.get_race()) + ',' +
            str(i.get_flang()) + ',' + str(i.get_fluent()) + ',' +
            str(i.get_med()) + ',' + str(i.get_hearing()) + ',' +
            str(i.get_vision()) + '\n')

def main():
    makeExcel()
    # makeDemoExcel()

main()
# makeDemoExcel()

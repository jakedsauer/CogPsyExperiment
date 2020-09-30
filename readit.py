import pickle, os.path
import expclass

def makeExcel():
    with open("data.dat", "rb") as f:
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
            attendType = j.get_attendtype()

            dataFile.write(sub.get_subnumber() + ',' + sub.get_bday() + ',' + sub.get_gender() + ',' + sub.get_rundate() + ',' +
            j.get_practice() + ',' + str(j.get_blocknum()) + ',' + attendType + ',' +
            str(j.get_trialnum()) + ',' + str(j.get_stimtype()) + ',')
            dataFile.write(str(j.get_stimorderlist()[0]) + ',')
            if attendType != 'Single':
                dataFile.write(str(j.get_stimorderlist()[1]) + ',')
            else:
                dataFile.write('na,')
            for k in j.get_stimlist():
                for l in k:
                    dataFile.write(str(l) + ',')
            if attendType == 'Single':
                dataFile.write('na,na,na,')
            if attendType == 'Second':
                dataFile.write('na,na,na,')
            for k in j.get_responselist():
                for l in k:
                    dataFile.write(str(l) + ',')
            if attendType == 'Single' or attendType == 'First':
                dataFile.write('na,na,na,')
            if attendType == 'Second':
                dataFile.write('na,na,na,')
            for k in j.get_errorlist():
                for l in k:
                    dataFile.write(str(l) + ',')
            if attendType == 'Single' or attendType == 'First':
                dataFile.write('na,na,na,')
            if attendType == 'Second':
                dataFile.write('na,na,na,')
            for k in j.get_responsetimelist():
                for l in k:
                    dataFile.write(str(l) + ',')
            if attendType == 'Single' or attendType == 'First':
                dataFile.write('na,na,na,')
            dataFile.write('\n')


def main():
    makeExcel()

main()

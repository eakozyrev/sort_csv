import csv
import shutil

index_file = 0;
firstline = []

def index_3(row):
    btv = row[4].split('-')[0].split('  ')[1].rstrip()
    if(len(btv) > 0):
        return float(btv.rstrip().lstrip())
    else:
        return float(row[4].split('-')[0].rstrip().lstrip())

def index_4(row):
    return float(row[4].split('-')[1].rstrip().lstrip())

def index_5(row):
    btv = row[3].split('-')[0].split('  ')[1].rstrip()
    if(len(btv) > 0):
        return float(btv.rstrip().lstrip())
    else:
        return float(row[3].split('-')[0].rstrip().lstrip())

def delete_single(data1):
    i = 0
    lenf = len(data1)
    while i < lenf-1:
        if data1[i][-1] != data1[i+1][-1]:
            if i > 0:
                if data1[i][-1] != data1[i-1][-1]:
                    del(data1[i])
                    lenf = lenf - 1
                    continue
            else:
                del(data1[i])
                lenf = lenf - 1
                continue
        i = i + 1
    if data1[-1][-1] != data1[-2][-1]:
        del(data1[-1])



def delete_only_minos_and_single_plus(data1):
    i = 0
    while i < len(data1)-1:
        allp = 0
        nomers = []
        while data1[i][-1] == data1[i+1][-1]:
            nomers.append(i)
            if data1[i][2] == 'плюс':
                allp += 1
            i = i + 1
            if i == len(data1) - 1:
                break
        nomers.append(i)
        if data1[i][2] == 'плюс':
            allp += 1
        if allp < 2:
            i = i - len(nomers) + 1
            for num in nomers:
                del(data1[i])
        else:
            i = i + 1


def check_fiveth(data1,fpath):
    i = 0
    global firstline
    global index_file
    while i < len(data1)-1:
        arp = []
        arm = []
        while data1[i][-1] == data1[i+1][-1]:
            if data1[i][2] == 'плюс':
                arp.append([i,data1[i][-2]])
            else:
                arm.append([i, data1[i][-2]])
            i +=1
            if i == len(data1)-1:
                break
        if data1[i][2] == 'плюс':
            arp.append([i, data1[i][-2]])
        else:
            arm.append([i, data1[i][-2]])
#        if len(set([x[1] for x in arp])) < len([x[1] for x in arp]):
#            i+=1
#            continue
        sleva = True
        sprava = True
        for ones in arp:
            for twos in arm:
                if ones[1] >= twos[1]:
                    sleva = False
        for ones in arp:
            for twos in arm:
                if ones[1] <= twos[1]:
                    sprava = False
        if sleva == True or sprava == True:
            shutil.rmtree(str(fpath)+str(index_file)+'.csv', ignore_errors=True)
            with open(str(fpath)+str(index_file)+'.csv', mode='w',encoding='cp1251') as filew:
                filew = csv.writer(filew, delimiter=';',lineterminator='\r\n')
                filew.writerow(firstline)
                for row in arp[:-1]:
                    filew.writerow(data1[row[0]][:6])
            with open(str(fpath)+str(index_file)+'.csv', mode='a+',encoding='cp1251') as filew:
                filew = csv.writer(filew, delimiter=';',lineterminator='')
                filew.writerow(data1[arp[-1][0]][:6])
            index_file +=1
        i += 1




def csv_reader(file_obj,fpath,new):
    global index_file
    global firstline
    if new == 0:
        index_file = 0
    reader = csv.reader(file_obj, delimiter=';')
    data = []
    firstline.clear()
    for row in reader:
        for x in row:
            firstline.append(x)
        break
    for row in reader:
        if len(row) < 5:
            continue
        ff = row[5].split('-')
        if len(ff) < 2:
            continue
        row.append(float(ff[0].split('  ')[1].rstrip()))
        row.append(float(ff[1].lstrip()))
        row.append(index_3(row))
        row.append(index_4(row))
        row.append(index_5(row))
        row.append(row[6]*1000000+row[7]*10000+row[8]*100+row[9])
        data.append(row)
    data1 = sorted(data, key=lambda st: st[-1])
    delete_single(data1)
    delete_only_minos_and_single_plus(data1)
    check_fiveth(data1,fpath)


if __name__ == "__main__":

    for i in range(10,11):
        csv_path = "test/" + str(i)+"_G_buy_60_31.csv"
        with open(csv_path, "r",encoding='cp1251', errors='ignore') as f_obj:
            csv_reader(f_obj,fpath)

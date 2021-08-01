import heapq
import math
import operator
import pandas

# Input Data
def data_input():
    df = pandas.read_csv("DATA PROGRAM.csv")
    data = []
    kelas_latih = []
    kelas_data_uji = []
    counter = 0
    for ptf in range(len(df['ID Pasien'])):
        data.append([df['G1'][counter], df['G2'][counter], df['G3'][counter], df['G4'][counter], df['G5'][counter],
                     df['G6'][counter], df['G7'][counter], df['G8'][counter], df['G9'][counter], df['G10'][counter],
                     df['G11'][counter], df['G12'][counter], df['G13'][counter], df['G14'][counter], df['G15'][counter],
                     df['G16'][counter], df['G17'][counter], df['G18'][counter], df['G19'][counter],
                     df['G20'][counter]])
        kelas_latih.append((df['Penyakit'][counter]))
        counter += 1
    data_latih = []
    data_uji = []
    kelas_data_latih = []
    n = 100
    final_data = [data[i:i + n] for i in range(0, len(data), n)]
    for x in final_data:
        latih = x[0:60]
        latih2 = x[80:100]
        jumlah = 0
        for a in latih:
            data_latih.append(a)
            jumlah += 1
        for y in latih2:
            data_latih.append(y)
            jumlah += 1
        uji = x[60:80]
        for b in uji:

            data_uji.append(b)
    final_kelas = [kelas_latih[y:y + n] for y in range(0, len(kelas_latih), n)]
    for c in final_kelas:
        kelas = c[0:60]
        kelas2 = c[80:100]
        for a in kelas:
            kelas_data_latih.append(a)
        for y in kelas2:
            kelas_data_latih.append(y)
    for d in final_kelas:
        kelas_uji = d[60:80]
        for b in kelas_uji:
            kelas_data_uji.append(b)
    return data_uji, data_latih, kelas_data_latih, kelas_data_uji


#Perhitungan Euclidean
def euclidean(data_uji, data_latih, parameter):
    jarak_euclidean = {}
    for x in range(len(data_uji)):
        euclideanlist = []
        for y in range(len(data_latih)):
            euclideandata = 0
            for z in range(len(parameter)):
                euclideandata = euclideandata + ((data_uji[x][z] - data_latih[y][z]) ** 2)
            euclideanlist.append(math.sqrt(euclideandata))
        jarak_euclidean[x] = euclideanlist
    return jarak_euclidean

# Proses KNN
def klasifiaksi(jarak_euclidean, kelas, k):
    semua_kelas = []
    for a in jarak_euclidean.values():
        label = []
        c = heapq.nsmallest(k, enumerate(a), key=operator.itemgetter(1))
        for d in c:
            label.append(kelas[d[0]])
        semua_kelas.append(label)
    counter = 0
    result = {}
    for b in semua_kelas:
        kelas_chf = b.count('CHF')
        kelas_ppok = b.count('PPOK')
        kelas_asma = b.count('Asma')
        dict_kelas = {'CHF': kelas_chf, 'PPOK': kelas_ppok, 'Asma': kelas_asma}
        maksimum = max(dict_kelas.values())
        for nama_kelas, jumlah in dict_kelas.items():
            if jumlah == maksimum:
                result[counter] = nama_kelas
                counter += 1
    return result

# Input CF pakar
def input_CF():
    df = pandas.read_csv('NILAI CF PAKAR.csv')
    nilai_cf_pakar_CHF = []
    nilai_cf_pakar_PPOK = []
    nilai_cf_pakar_asma = []
    counter = 0

    for ptf in range(len(df['no'])):
        if (counter == 0):
            nilai_cf_pakar_CHF.append(
                [df['G1'][counter], df['G2'][counter], df['G3'][counter], df['G4'][counter], df['G5'][counter],
                 df['G6'][counter], df['G7'][counter], df['G8'][counter], df['G9'][counter], df['G10'][counter],
                 df['G11'][counter], df['G12'][counter], df['G13'][counter], df['G14'][counter], df['G15'][counter],
                 df['G16'][counter], df['G17'][counter], df['G18'][counter], df['G19'][counter], df['G20'][counter]])
        elif (counter == 1):
            nilai_cf_pakar_PPOK.append(
                [df['G1'][counter], df['G2'][counter], df['G3'][counter], df['G4'][counter], df['G5'][counter],
                 df['G6'][counter], df['G7'][counter], df['G8'][counter], df['G9'][counter], df['G10'][counter],
                 df['G11'][counter], df['G12'][counter], df['G13'][counter], df['G14'][counter], df['G15'][counter],
                 df['G16'][counter], df['G17'][counter], df['G18'][counter], df['G19'][counter], df['G20'][counter]])
        elif (counter == 2):
            nilai_cf_pakar_asma.append(
                [df['G1'][counter], df['G2'][counter], df['G3'][counter], df['G4'][counter], df['G5'][counter],
                 df['G6'][counter], df['G7'][counter], df['G8'][counter], df['G9'][counter], df['G10'][counter],
                 df['G11'][counter], df['G12'][counter], df['G13'][counter], df['G14'][counter], df['G15'][counter],
                 df['G16'][counter], df['G17'][counter], df['G18'][counter], df['G19'][counter], df['G20'][counter]])
        counter += 1
    return nilai_cf_pakar_CHF,nilai_cf_pakar_PPOK,nilai_cf_pakar_asma

#Perhitungan perkalian certainty Factor
def perkalian_certainty_factor(kelas_data_uji,nilai_cf_user,nilai_cf_pakar_CHF, nilai_cf_pakar_PPOK, nilai_cf_pakar_asma):
    perkalian_cf = []
    counter = 0
    for x in nilai_cf_user:
        CHF = []
        PPOK = []
        Asma = []
        if (kelas_data_uji[counter] == "CHF"):
            for y in nilai_cf_pakar_CHF:
                for x,y in zip (x,y):
                    CHF.append(x*y)
                perkalian_cf.append(CHF)
            counter += 1
        elif (kelas_data_uji[counter] == "PPOK"):
            for y in nilai_cf_pakar_PPOK:
                for x,y in zip (x,y):
                    PPOK.append(x*y)
                perkalian_cf.append(PPOK)
            counter += 1
        elif (kelas_data_uji[counter] == "Asma"):
            for y in nilai_cf_pakar_asma:
                for x,y in zip (x,y):
                    Asma.append(x*y)
                perkalian_cf.append(Asma)
            counter += 1
    return perkalian_cf

#Perhitungan CF Combine
def cf_combine(perkalian_cf):
    cf_combine_list = []
    max_combine_list = []
    for x in perkalian_cf:
        cf_combine_data = []
        for y in range(len(x)):
            if (y == 0):
                cf_combine_data.append(x[0] + x[1] * (1 - x[0]))
            else:
                cf_combine_data.append(cf_combine_data[y-1] + x[y] * (1-cf_combine_data[y-1]))
        cf_combine_list.append(cf_combine_data)
        max_combine = (pandas.Series(cf_combine_data)).max()
        max_combine_list.append(max_combine)
    return cf_combine_list, max_combine_list

#Perhitungan akurasai
def perhitungan_akurasi(hasil_klasifikasi, kelas_uji):
    counter = 0
    chf = 0
    ppok = 0
    asma = 0
    TP_CHF = 0
    FN_CHF = 0
    FP_CHF = 0
    TP_PPOK = 0
    FN_PPOK = 0
    FP_PPOK = 0
    TP_Asma = 0
    FN_Asma = 0
    FP_Asma= 0
    precision_CHF = 0
    recall_chf = 0
    fmeasure_chf = 0
    precision_PPOK = 0
    recall_PPOK = 0
    fmeasure_PPOK = 0
    precision_Asma = 0
    recall_Asma = 0
    fmeasure_Asma = 0
    salah = 0
    data = 1
    for a in range(len(kelas_uji)):
        if (kelas_uji[a]==hasil_klasifikasi[a]):
            counter+=1
            data+=1
        elif(kelas_uji[a]!=hasil_klasifikasi[a]):

            salah+=1
            data+=1
    akurasi = (counter/20) * 100
    for b in range(len(hasil_klasifikasi)):
        if(hasil_klasifikasi[b] == "CHF"):
            chf+=1
        elif(hasil_klasifikasi[b]== "PPOK"):
            ppok+=1
        elif(hasil_klasifikasi[b]=="Asma"):
            asma+=1

    for c in range(len(kelas_uji)):
        if (kelas_uji[c]=='CHF'):
            if (kelas_uji[c] == hasil_klasifikasi[c]):
                TP_CHF += 1
            elif (hasil_klasifikasi[c]!='CHF'):
                FN_CHF += 1
            else:
                TP_CHF += 0
        elif(hasil_klasifikasi[c]=='CHF'):
            if(kelas_uji[c]!='CHF'):
                FP_CHF+=1
    for d in range(len(kelas_uji)):
        if(kelas_uji[d]=='PPOK'):
            if(kelas_uji[d]== hasil_klasifikasi[d]):
                TP_PPOK += 1
            elif (hasil_klasifikasi[d]!='PPOK'):
                FN_PPOK += 1
        elif(hasil_klasifikasi[d]=='PPOK'):
            if(kelas_uji[d]!='PPOK'):
                FP_PPOK += 1
    for e in range(len(kelas_uji)):
        if(kelas_uji[e]=='Asma'):
            if(kelas_uji[e]== hasil_klasifikasi[e]):
                TP_Asma += 1
            elif (hasil_klasifikasi[e]!='Asma'):
                FN_Asma += 1
        elif(hasil_klasifikasi[e]=='Asma'):
            if(kelas_uji[e]!='Asma'):
                FP_Asma += 1

    print("TP_CHF : ",TP_CHF)
    print("FN_CHF : ", FN_CHF)
    print("FP_CHF : ", FP_CHF)

    precision_CHF = TP_CHF/(TP_CHF+FP_CHF)
    recall_chf = TP_CHF/(TP_CHF+FN_CHF)
    fmeasure_chf = (2 * precision_CHF * recall_chf)/(precision_CHF+recall_chf)

    print("Precision CHF : ",precision_CHF)
    print("Recall CHF : ", recall_chf)
    print("F-Measure CHF : ", fmeasure_chf)
    print("=============================")
    print("TP_PPOK : ", TP_PPOK)
    print("FN_PPOK : ", FN_PPOK)
    print("FP_PPOK : ", FP_PPOK)

    precision_PPOK = TP_PPOK / (TP_PPOK + FP_PPOK)
    recall_PPOK = TP_PPOK / (TP_PPOK + FN_PPOK)
    fmeasure_PPOK = (2 * precision_PPOK * recall_PPOK) / (precision_PPOK + recall_PPOK)

    print("Precision PPOK : ", precision_PPOK)
    print("Recall PPOK : ", recall_PPOK)
    print("F-Measure PPOK : ", fmeasure_PPOK)
    print("=============================")
    print("TP_Asma : ", TP_Asma)
    print("FN_Asma : ", FN_Asma)
    print("FP_Asma : ", FP_Asma)

    precision_Asma = TP_Asma / (TP_Asma + FP_Asma)
    recall_Asma = TP_Asma / (TP_Asma + FN_Asma)
    fmeasure_Asma = (2 * precision_Asma * recall_Asma) / (precision_Asma + recall_Asma)

    print("Precision Asma : ", precision_Asma)
    print("Recall Asma : ", recall_Asma)
    print("F-Measure Asma : ", fmeasure_Asma)
    print("================================")
    print("Rata-rata precision : ", (precision_CHF + precision_PPOK + precision_Asma)/3)
    print("Rata-rata Recall : ",(recall_chf + recall_PPOK + recall_Asma)/3)
    print("Rata-rata F-Measure : ",(fmeasure_chf + fmeasure_PPOK + fmeasure_Asma)/3)
    print("")

    return akurasi

gejala = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17',
          'G18', 'G19', 'G20']

def main():
    menu = 0
    while menu < 1 :
        print("Sistem Diagnosa Penyakit Gejaala Sesak")
        print("1. Pengujian")
        print("2. Selesai")
        pilihan = int(input("Masukkan Pilihan : "))
        if (pilihan == 1):
            k = int(input("Masukkan nilai  K : "))
            if(k<1):
                print("Maaf nilai K tidak sesuai ketentuan")
            else:
                data_uji, data_latih, kelas, kelas_uji = data_input()
                jarak_euclidean = euclidean(data_uji, data_latih, gejala)
                hasil_klasifikasi = klasifiaksi(jarak_euclidean, kelas, k)
                nilai_cf_pakar_CHF, nilai_cf_pakar_PPOK, nilai_cf_pakar_asma = input_CF()
                hasil_perkalian_certainty_factor = perkalian_certainty_factor(hasil_klasifikasi, data_uji,nilai_cf_pakar_CHF,nilai_cf_pakar_PPOK, nilai_cf_pakar_asma)
                hasil_cf_combine, max_combine = cf_combine(hasil_perkalian_certainty_factor)
                print()
                counter = 0
                id_pasien = 61
                for a in max_combine:
                    print("Data uji ke", id_pasien, ": ", "\nKelas penyakit = ", hasil_klasifikasi[counter],
                          "\nTingkat keyakinan = ", a * 100, "%")
                    print()
                    counter += 1
                    id_pasien += 1
                Akurasi = perhitungan_akurasi(hasil_klasifikasi, kelas_uji)
                print("Persentase akurasi = ",Akurasi)
                print()

        elif (pilihan == 2):
            print("Anda telah keluar dari sistem ")
            menu += 1
        else:
            print(" Maaf, pilihan yang anda masukkan tidak ada")
            print()

main()


# funktsioon võtab failist iga eraldi retsepti ja väljastab iga retsepti omakorda listina
import ast

def andmed_failist(fail):
    lst_retsept = []
    with open(fail, encoding='UTF-8') as f:
        for rida in f:
            retsept = []
            üks_retsept = rida.strip().split(' | ')
            lst_päris = ast.literal_eval(üks_retsept[0])
            retsept.append(lst_päris)
            retsept.append(üks_retsept[1])
            lst_retsept.append(retsept)

    return lst_retsept


#järjend 1 peab olema retsepti järjend ja jär2 on külmiku jääkide järjend
#funktsioon leiab ühiste sõnade arvu mõlemas järjendis
def andmete_ühilduvus(jär1, jär2):
    ühised_sõnad = []
    for el in jär1:
        if 'Santa' in el:
            continue
        for sõne2 in jär2:
            if sõne2 in el:
                ühised_sõnad.append(sõne2)
    return [len(ühised_sõnad), len(jär1) - len(ühised_sõnad)]


def main():
    külmik = input('Sisesta külmiku jäägid nt(vahukoor pasta): ')
    lst_külmik = külmik.split()
    lst_retsept = andmed_failist('santamaria_koostisosad.txt')
    suurim_sarnasus = 0
    count = 0
    sõnastik = {}
    ## leiab suurima sarnanuse üle kõikide retseptide
    for retsept in lst_retsept:
        ühised = andmete_ühilduvus(retsept[0], lst_külmik)
        if retsept[1] not in sõnastik:
            sõnastik[retsept[1]] = ühised

    for link, v in sõnastik.items():
        if v[0] == max(value[0] for value in sõnastik.values()):
            print(link, v)
            
if __name__ == '__main__':
    main()

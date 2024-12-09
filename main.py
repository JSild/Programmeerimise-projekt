################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Üliõpilaskülmik
#
#
# Autorid: Hardy Reinhold, Jasper Suursild
#
# mõningane eeskuju: Rimi 'Tühjenda oma külmik'
#
# Lisakommentaar (nt käivitusjuhend): terminalist käivitades 'streamlit run main.py'
#
##################################################
import ast
import streamlit as st

# funktsioon võtab failist iga eraldi retsepti ja väljastab iga retsepti omakorda listina
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


#järjend 1 peab olema retsepti järjend ja jär2 on kodus olevate asjade järjend
#funktsioon leiab ühiste sõnade arvu mõlemas järjendis
def andmete_ühilduvus(jär1, jär2):
    ühised_sõnad = []
    for el in jär1:
        if 'Santa' in el:
            continue
        for sõne2 in jär2:
            if sõne2 in el:
                ühised_sõnad.append(sõne2)
    olemas = len(ühised_sõnad)
    puudu = len(jär1) - len(ühised_sõnad)
    return [olemas, puudu]


#
def sobivaimad_retseptid(sõnastik, top_n):
    def skoor(olemas, puudu):
        if olemas == 0:
            return -float('inf')
        return olemas - (puudu ** 1.5)
    
    välistatud_sõnad = ["jaatis", "kteil", "vegan", "taimne", "lihavaba"] 
    filtered_sõnastik = {
        key: value for key, value in sõnastik.items() 
        if not any(exclude_word in key for exclude_word in välistatud_sõnad)
    }
    st.write(filtered_sõnastik["https://www.santamariaworld.com/ee/retseptid/tex-mex-takoburger/"])
    järjestatult = sorted(
        filtered_sõnastik.items(),
        key=lambda x: skoor(x[1][0], x[1][1]),
        reverse=True
        )
    parimad = järjestatult[:top_n]
    return {k: v for k, v in parimad}


def main():
    global sisestatud_sõnad
    st.title('Üliõpilaskülmik')
    sisend = st.text_input('Sisesta külmiku jäägid nt(vahukoor pasta): ')
    if st.button('Leia retseptid'):
        sisestatud_sõnad = sisend.split()
        lst_retsept = andmed_failist('kõik_koostisosad.txt')
        sõnastik = {}
        ## leiab suurima sarnanuse üle kõikide retseptide
        for retsept in lst_retsept:
            ühised = andmete_ühilduvus(retsept[0], sisestatud_sõnad)
            if retsept[1] not in sõnastik:
                sõnastik[retsept[1]] = ühised
        top = sobivaimad_retseptid(sõnastik, 10)
        for k, v in top.items():
            nimetus = k.split('/')[-2].replace('-', ' ')
            with st.expander(nimetus):
                st.write(f'''
                    Olemas koostisosi: {v[0]}\n
                    Juurde vaja osta asju: {v[1]}\n
                    Retsept: {k}
                ''')
            
if __name__ == '__main__':
    main()

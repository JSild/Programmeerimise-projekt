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




def loe_failist(faili_nimi):
    # Loeb failist kõik read, igal real on esimesel kohal koostisosad, teisel kohal retsepti link, 
    # ning eraldab need listi retseptid
    retseptid = []
    with open(faili_nimi, encoding="UTF-8") as fail:
        for rida in fail:
            koostisosad, link = rida.strip().split(" | ")
            retseptid.append([ast.literal_eval(koostisosad), link])
    return retseptid


def leia_ühised(koostisosad, olemasolevad_asjad):
    # Funktsioon võtab argumendiks koostisosad ning kasutaja sisendi,
    # ning tagastab 2 elemendilise enniku kus on esimesel kohal ühiste asjade arv
    # ja teisel kohal puud olevate asjade arv
    ühised = []
    ära_loenda = {'Santa', 'õli', 'sool ', 'pipar', 'äädika', 'maitseaine'}
    uued_koostisosad = koostisosad
    for el in koostisosad:
        if any(keyword in el for keyword in ära_loenda):
            uued_koostisosad.remove(el)

    for el in uued_koostisosad:
        for sõne in olemasolevad_asjad:
            if sõne in el and sõne not in ühised:
                ühised.append(sõne)

    return [len(ühised), (len(koostisosad) - len(ühised))], set(ühised)


def filtreeri_ja_järjesta_retseptid(retseptikogu, top_n, välistatud_sõnad=None):
    """
    Filtreerib retseptide hulgast välja välistatud retseptid, ja hindab neid kasutades funktsiooni skoor.
    Tagastab järjestatult top_n retsepti sõnastikuna.
    """
    välistatud_sõnad = välistatud_sõnad or []

    # Filtreeri retseptid
    filtreeritud_retseptid = {
        link: koostisosad
        for link, koostisosad in retseptikogu.items()
        if not any(sõna in link.lower() for sõna in välistatud_sõnad)
    }

    # Skoorimis funktsioon
    def skoor(olemas, puudu):
        if olemas == 0:
            return -float('inf')
        return 10 * olemas - puudu * 1.5

    # Järjesta retseptid
    järjestatud_retseptid = sorted(
        filtreeritud_retseptid.items(),
        key=lambda x: skoor(x[1][0], x[1][1]),
        reverse=True,
    )
    parimad = järjestatud_retseptid[:top_n]
    return {k: v for k, v in parimad}

# Põhiprogramm
def main():
    st.title("Üliõpilaskülmik")
    kasutaja_sisend = st.text_input("Sisesta koostisosad, eraldatult tühikutega:")

    välistatud_valikud = {
        'Jäätised': "jaatis", 
        'Kokteilid': "kteil", 
        'Vegan toidud': "vegan", 
        'Taimsed toidud': "taimne", 
        'Lihavaba': "lihavaba",
        'Tordid': "tort",
        'Koogid': "kook",
        'Supid': "supp",
        'Kastmed': "kaste"
        }
    
    valikud = st.multiselect(
    label='Mida soovid välistada:',
    placeholder='Tee valik',
    options=list(välistatud_valikud.keys()))
    välistatud = [välistatud_valikud[valik] for valik in valikud]

    if st.button("Leia retseptid"):
        if not kasutaja_sisend.strip():
            st.warning("Palun sisesta vähemalt üks koostisosa.")
            return

        olemasolevad_asjad = kasutaja_sisend.split()
        if 'või' in olemasolevad_asjad:
            i = olemasolevad_asjad.index('või')
            olemasolevad_asjad[i] = 'võid'
        retseptid = loe_failist("kõik_koostisosad.txt")

        # Kontrollib kasutaja sisendi ja koostisosade ühilduvust
        retseptikogu = {}
        ühised_koostisosad = {}
        for retsept in retseptid:
            skoor_andmed, ühised = leia_ühised(retsept[0], olemasolevad_asjad)
            retseptikogu[retsept[1]] = skoor_andmed
            ühised_koostisosad[retsept[1]] = ühised


        # Filtreerib ja järjestab top 10 retsepti
        top_retseptid = filtreeri_ja_järjesta_retseptid(retseptikogu, top_n=10, välistatud_sõnad=välistatud)

        # Näita retsepte
        for link, väärtus in top_retseptid.items():
            if link.startswith('https://nami-nami.ee/'):
                retsepti_nimi = link.split("/")[-1].replace("_", " ")
            else:
                retsepti_nimi = link.split("/")[-2].replace("-", " ")
            with st.expander(retsepti_nimi):
                st.write(
                    f"""
                    **Koostisosi olemas:** {väärtus[0]} [{', '.join(ühised_koostisosad[link])}]\n
                    **Koostisosi vaja:** {väärtus[1]}\n
                    [Retsept]({link})
                    """
                )


if __name__ == "__main__":
    main()

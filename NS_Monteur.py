#Hier wordt een class gemaakt voor de monteurs
class monteur:
    def __init__(self, voornaam, achternaam, adres, beschikbaar, chat_id):
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.vollenaam = voornaam + " " + achternaam
        self.adres = adres
        self.chat_id = chat_id
        self.beschikbaar = beschikbaar

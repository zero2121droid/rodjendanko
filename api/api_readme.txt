Registracija korisnika:
 - url: https://rodjendanko.lenitech.org/api/register/
 - Request body:
    {
        "email": "korisnik@example.com",
        "password": "tajna_lozinka",
        "username": "korisnik",
        "first_name": "Ime",
        "last_name": "Prezime",
        "phone": "+381601234567",
        "city": "Beograd"
    }

Login korisnika:
 - url: https://rodjendanko.lenitech.org/api/token/
 - Request body:
    {
        "email": "korisnik@example.com",
        "password": "P@ssword1"
    }
 - Response:
    {
        "refresh": "jwt-refresh-token",
        "access": "jwt-access-token"
    }

Google login:
 - URL: https://rodjendanko.lenitech.org/api/user/google_login/
 - Request body:
    {
        "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIzZjdhMzU4Mzc5NmY5NzEyOWU1NDE4ZjliMjEzNmZjYzBhOTY0NjIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2MDE3NDIyMjU3NC1zMHU3aGg3bXE2MDR2YzQ5bWJrOW42djY1Z2pqaWFsaC5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjYwMTc0MjIyNTc0LXMwdTdoaDdtcTYwNHZjNDltYms5bjZ2NjVnamppYWxoLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAyNTEzNzczNDk3OTY0OTExNjc2IiwiZW1haWwiOiJ2bGFkYS5nYXNoYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IkxGVEhJWEg1SUl4UEJRd0p3RmE2aVEiLCJuYW1lIjoiVmxhZGltaXIgR2FzZXZpYyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLYXBrWXVJVUx4TWFzaThnRlZEd1g1bzdIZFlXQW5mSFdMNUVhXzZDbGF6eEJUd013PXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IlZsYWRpbWlyIiwiZmFtaWx5X25hbWUiOiJHYXNldmljIiwiaWF0IjoxNzQ1NTIyMDU2LCJleHAiOjE3NDU1MjU2NTZ9.eHEogDdHhWy0SvD5UzHLLUPji7ZnxMGEPemb7NR9zDTgxrMWeI8zjYsuUJtXNKWbGLf-OQx-iZ5yF1taX5DXjkKGyj1Tg7d22dBN2qC0zvmDVEkcFFsNEmDlWZ8djhmllsQFf7EoTW-by30tdkCXFRp_C0vAt9xRaA4fRxscBiaX41sLQgsOwoSkxk5ik3yQiYhtDNZiujUCYd4v5NXw5N56bDGKn7Y5ghaE1VDZJNLXdY92-2dF_STbcfGhJy0fFwT0zyQI24Psk9c9I6SFsqc86ifNvT28Hd8iEnfppfju7N_dDubR7D3CAWh7ExO6hmn3xItQd1VQhJTTS_QSGw"
    }
 - Response:
    {
        "refresh": "jwt-refresh-token",
        "access": "jwt-access-token",
        "email": "korisnik@gmail.com",
        "created": true  // ako je nov korisnik
    }
 - Client ID: 60174222574-s0u7hh7mq604vc49mbk9n6v65gjjialh.apps.googleusercontent.com
 - Client Secret: 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
 - Redirect URI: https://developers.google.com/oauthplayground

Nakon svakog login-a (bilo običnog ili Google), frontend treba da čuva access i refresh tokene (npr. u localStorage).
Svi naredni API pozivi ka backendu treba da imaju Authorization header:
    Authorization: Bearer <access_token>

Pretraga:
  - ?search=neki_tekst

Kada u frontendu Owner kreira lokaciju dovoljno je u request proslediti sledece:
Owner uopšte ne mora ni da zna koji mu je customer_id.
Na backendu sve automatski povezujemo.
Frontend šalje samo:
    {
        "location_name": "Igraonica Sveznalica",
        "location_address": "Ulica Petra Petrovića 12, Beograd",
        "description": "Velika igraonica sa 3 rođendaonice.",
        "location_latitude": 44.7866,
        "location_longitude": 20.4489
    }
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Tekst za uslove koriscenja:

USLOVI KORIŠĆENJA
Datum poslednjeg azuriranja: April 28, 2025.
Dobrodošli na Rodjendanko.rs! Korišćenjem ove platforme pristajete na sledeće uslove korišćenja. Ako se ne slažete sa bilo kojim delom ovih uslova, nemojte koristiti ovaj sajt.
1. Opis usluge
Rodjendanko je platforma koja omogućava korisnicima da rezervišu termine za proslave rođendana u igraonicama i da naruče dodatne usluge kao što su torte, dekoracije, animator i drugo.
2. Registracija korisnika
Da biste koristili platformu, morate se registrovati i uneti tačne informacije. Odgovorni ste za čuvanje poverljivosti svoje lozinke.
3. Obaveze korisnika
Korisnik se obavezuje da:
•	koristi platformu u skladu sa zakonima Republike Srbije;
•	neće zloupotrebljavati sistem za lažne rezervacije;
•	pruža tačne informacije o sebi i detetu.
4. Otkazivanje rezervacija
Otkazivanje rezervacija moguće je u skladu s pravilima igraonice. Rodjendanko ne garantuje povraćaj novca ukoliko rezervacija nije otkazana u roku predviđenom pravilima partnera.
5. Prava i odgovornosti
Rodjendanko zadržava pravo da izmeni ove uslove u bilo kom trenutku. Korisnici će biti obavešteni o izmenama putem sajta.
6. Odricanje od odgovornosti
Rodjendanko ne snosi odgovornost za eventualne nesuglasice između korisnika i igraonice ili za kvalitet dodatnih usluga.
 
POLITIKA PRIVATNOSTI
Datum poslednjeg azuriranja: April 28, 2025.
1. Koje podatke prikupljamo?
•	Ime i prezime korisnika
•	Email adresu
•	Broj telefona
•	Informacije o detetu (ime, datum rođenja)
•	Detalji o rezervacijama
2. Kako koristimo podatke?
Podaci se koriste isključivo za:
•	Omogućavanje rezervacija
•	Slanje obaveštenja i potvrda
•	Unapređenje usluge
3. Deljenje podataka
Podaci se dele samo sa igraonicama i partnerima uključenim u realizaciju rezervacija. Nikada ne prodajemo lične podatke trećim licima.
4. Vaša prava
Korisnici imaju pravo da:
•	zahtevaju pristup, ispravku ili brisanje svojih podataka;
•	se usprotive obradi podataka u marketinške svrhe;
•	podnesu žalbu Povereniku za informacije od javnog značaja i zaštitu podataka o ličnosti.
5. Bezbednost
Podaci se čuvaju na sigurnim serverima i dostupni su samo ovlašćenim licima.
6. Kolačići
Koristimo kolačiće kako bismo poboljšali korisničko iskustvo. Korisnici mogu upravljati kolačićima u svom pregledaču.
Za više informacija, kontaktirajte nas na: admin@rodjendarijum.lenitech.org

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
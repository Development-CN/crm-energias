cd C:\inetpub\wwwroot\Nuevo_crm_Madiautos\crm
call .\newenv\scripts\activate
call daphne -b 201.150.36.240 -p 5022 crm.asgi:application

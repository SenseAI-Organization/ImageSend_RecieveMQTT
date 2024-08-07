#include <pgmspace.h>
 
#define SECRET
#define THINGNAME "device_001"                         //change this
 
const char WIFI_SSID[] = "***************";               //change this
const char WIFI_PASSWORD[] = "***************";           //change this
const char AWS_IOT_ENDPOINT[] = "a320jkm5cscowr-ats.iot.us-west-2.amazonaws.com";       //change this
 
// Amazon Root CA 1
static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
)EOF";
 
// Device Certificate                                               //change this
static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
 MIIDWjCCAkKgAwIBAgIVAK3PlLZyWgE/jshKQWhtKIGeFTBhMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMzEwMDkxNTU1
MTdaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDCOX5Z3gWpJwY9CDYU
Xq1J69yaBRS5lrYsDLSOVAwk1JLGVWv7HMiwnuX2Ohl4ItM91YxFE5zG3o6iYQF4
ySaV8BZzj7rpofmpaXae8XXkulVgnCgH/c4iizYqhoPPestjnuokksHBbZY39962
8jje+eaFSBes+hEsl/gExi2mIKWTch/XAQa7bTnyw9Gmt351YFxf8wC+cSRJuwSk
Mz+P73Zv7fI0rrqYdfZngRwS4ZCuW5ElOlh4E4ky/YdkhOv+ONjRNIMK37Rp5hxj
fctMmQKZHb68kyT+cO/Si1h2olJ6u13qcR25KG3BmVW6bEfzw1K4cdsMKKkuP7xF
5psrAgMBAAGjYDBeMB8GA1UdIwQYMBaAFABKfxgG3KiVEj+/L1mXJmI5FUmFMB0G
A1UdDgQWBBS+jHAwlmWV2/XZG3xCX9q++lHu5TAMBgNVHRMBAf8EAjAAMA4GA1Ud
DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAFofy3uGJbiX/n4JO/LxbtWRD
OsIiog4r+roj/iSS1nUpMulf7FTTZAD2reO7KNHNkKDjA3LiX2aoPD3kHJX1xH5Q
1c6pUn669kw5tLsfzhWwBGVtn8GCEhNSt5TagZ986WRqEsh8tSFrN7u7d/hLtClM
BL9cKJGxzRMks5dwARtbWtQOb9mhNxBQDBVHEvI0A2dsm3LVD009PIkEf8Ksplw+
/2P7ORgt/Ls7M502/92QZKr/p4NjLo5D+v+t/rhVx+7jPpA3v6JWpkhArbiNKg+f
lM3v2LCCbn9SelUpI/n/pB5yFWrgqZju1fR9mWF2pshALqG9IVyGnfRcMMSRiw==
-----END CERTIFICATE-----
 
 
)KEY";
 
// Device Private Key                                               //change this
static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
 MIIEpAIBAAKCAQEAwjl+Wd4FqScGPQg2FF6tSevcmgUUuZa2LAy0jlQMJNSSxlVr
+xzIsJ7l9joZeCLTPdWMRROcxt6OomEBeMkmlfAWc4+66aH5qWl2nvF15LpVYJwo
B/3OIos2KoaDz3rLY57qJJLBwW2WN/fetvI43vnmhUgXrPoRLJf4BMYtpiClk3If
1wEGu2058sPRprd+dWBcX/MAvnEkSbsEpDM/j+92b+3yNK66mHX2Z4EcEuGQrluR
JTpYeBOJMv2HZITr/jjY0TSDCt+0aeYcY33LTJkCmR2+vJMk/nDv0otYdqJSertd
6nEduShtwZlVumxH88NSuHHbDCipLj+8ReabKwIDAQABAoIBAA8tMOtSxvx1uS4R
szAaSc4p6P38AaeS2D9O6tjoRl6mYaWvzRU9JY1vjSaVWaIijoEZa7GGG80KXPjh
PZ0zkplKvmZfR8qzxm9vdz5qPb0Wtk8rRJGDSpU2bZAbHLecr8HkDAW5lfxIVOGg
s7115e2+dz3Y6Uix7Z+fbFjrJ2wApDEofG4l/9PimzqT0oS7qA0K/R0zHwXFGKN9
PxheRTpROsHkVGzV9/4BUAdUPxnkRtze1R8qhoqBwbu/ZaDIVLMftFQnjhttzyLs
d2EdYt7TKyB+88Bt9Z4id+wycAkx/NS1xB8LtBWMoxn1AYcoOC2GYhfD03GlZdKD
dYsrhoECgYEA5s0ioLc7NGxXgZ4yD5kkIPzOZhFf95mp2EOrVZxbfWUNu6jURVj7
MFniMHJ7bi6Ds1Mx+he6Za3+NMydqJ19YxAGFW4TnNwuusFJkqL3jkcAThuBqXw8
+E3Z/tLUk9WV/LThOU0WDo1HykmBAR25WjqiIQZWJTRzVHsXU9ZdXkECgYEA124L
OwF1CdqV/UH4buQ5l+yyDEsQMz2q7pzWamnOLjeOcS+gIhO4f2XatS2lufuX3ZlD
/DuojhuApY8PXf5e5MovZCmyDsZ3Qhub34GZL3bFv6e/XR5B+eUgAwMYYyqewVEl
IwY+dVa7qcnGEoRQ+yIhkCt9FLNSxtT8trBetmsCgYEA1ouQCefqIDQqL/JXRMqt
nACE+LpkBC0Shld5GG7tWSYr2ur4z7IEZhDXwwNYm7afdH38sieGfOh9qqUeVVR4
7zJBBYC6uJCw26e7dZUKHHcB4JmPMXas0oDECS4Ar5/W+f9Gcdanj0Vjm7YyNlBk
MWzZs2tJfvI/1yNJLwTQ7EECgYEA1YUgZG9hTU71cnq8fUx/OPFE16JegCsTDEUu
z3HnBS/TYqPNl3jsWHjfeMuxgtC3CNAr7ghDW/YuX+mXVZYU/7bVmfUpojNbaI5s
w+5zofOatAbTSLwAsGpEfDfJKCDKENkYccpyhWJdxj9Srm+uw/pkQbyY0Lebx666
e2f7t9kCgYA+tZp8Ous6JD4yzipp6xHY/1kShs5eiLTI3kir5xYZpsgy8NGOx2bW
6Xk1snnIRlbvwLrmHTUbG/m25wr6eP0p27NYhzogR3NLjb9k8Qnnlr7vZQwYugvU
6AyZQEkVaV0WlLMGjIiBkJemy1EJKk3/hURt1ONRy2cqcTuhXR4Vkw==
-----END RSA PRIVATE KEY-----
 
 
)KEY";
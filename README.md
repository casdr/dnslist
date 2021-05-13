# DNSlist

ACL's based on TXT records.

Example record:

```
casdr._whitelist.raaw.eu.		900	IN	TXT	"v=dnslist1 ip4:1.3.3.7 ip6:684D:1111:222:3333:4444:5555:6:77 a:home.raaw.eu include:test._whitelist.raaw.eu"
test._whitelist.raaw.eu.		900	IN	TXT	"v=dnslist1 ip4:8.8.8.8"
```

Will result in the following list of IP-addresses:

```
1.3.3.7
684D:1111:222:3333:4444:5555:6:77
31.3.8.7
8.8.8.8
```

# MagistralPython
MagistralPython is a messaging library written in Python.

Features
Requirements
Usage

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - **Intro -** [Prerequisites](#prerequisites), [Key-based access](#key-based-access) 
  - **Connecting -** [Connecting](#connecting)
  - **Resources -** [Topics](#topics)
  - **Publish / Subscribe -** [Publish](#publish), [Subscribe](#subscribe)
  - **History -** [History](#history), [History for Time Interval](#history-for-time-interval)
  - **Access Control -** [Permissions](#permissions), [Grant permissions](#grant-permissions), [Revoke permissions](#revoke-permissions)
  
## Features
- [x] Send / receive data messages
- [x] Replay (Historical data) 
- [x] Resource discovery
- [x] Access Control
- [x] TLS-encrypted communication
- [x] Client-side AES-encryption

## Requirements
- Python 3.5+

## Installation

### Python Package Manager

Just run the following command:
```bash
$ pip install magistral
```

---

## Usage

### Prerequisites

First of all, to stream data over Magistral Network you need to have an Application created.
If you don't have any of them yet, you can easily create one from [Customer Management Panel](https://app.magistral.io) 
(via start page or in [Application Management](https://app.magistral.io/#/apps) section).

Also, you need to have at least one topic created, that you can do from [Topic Management](https://app.magistral.io/#/topics) panel.

### Key-based access

Access to the Magistral Network is key-based. There are three keys required to establish connection:
  - **Publish Key** - Application-specific key to publish messages.
  - **Subscribe Key** - Application-specific key to read messages.
  - **Secret Key** - User-specific key to identify user and his permissions.

You can find both **Publish Key** and **Subscribe Key** in [Application Management](https://app.magistral.io/#/apps) section.
Select your App in the list and click Clipboard icons in App panel header to copy these keys into the Clipboard. 

**Secret Key** - can be found among user permissions in [User Management](https://app.magistral.io/#/usermanagement/) section.
You can copy secret key linked to user permissions into the Clipboard, just clicking right button in the permission list.

### Connecting
To establish connection with Magistral Network you need to create Magistral instance and provide **pub**, **sub** and **secret** keys.

```python
from magistral.client.Magistral import Magistral

magistral = Magistral(
    pubKey = "pub-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    subKey = "sub-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    secretKey = "s-xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx");
```

### Topics

To discover all available topics and channels you can call:

```python
def callback(meta):
  for mi in meta:
    for ch in mi.channels():
      print("%s:%d", mi.topic(), ch);

magistral.topics(lambda meta : callback(meta))
```

In case you know the topic name and want to see information about channels:
```python
def callback(meta):
  for mi in meta:
    for ch in mi.channels():
      print("%s:%d", mi.topic(), ch);

magistral.topic("topic", lambda meta : callback(meta))
```

### Publish

You can send data message to Magistral in this way:
```python
topic = "topic"
channel = 0
msg = "Hello from Python SDK!"

def callback(meta):
  assert(meta != None)

magistral.publish(topic, bytes(msg, 'utf8'), channel, lambda meta : callback(meta))
```
### Subscribe

This is an example how to subscribe and handle incoming data messages:
```python
topic = "topic"
group = "leader"
channel = 0

def listener(message):
  print("Got a message => [%s:%d] index = %d", message.topic(), message.channel(), message.index());
         
def callback(meta, err):
  assert(err is None)
  
magistral.subscribe(topic, group, channel, lambda message : listener(message), lambda meta, err : callback(meta, err))
```
### History

Magistral allows you to replay data  sent via some specific topic and channel. This feature called **History**.
To see last n-messages in the channel:
```python
topic = "topic"
channel = 0
count = 100

def histCallback(h):
  assert(h is not None);
  assert(len(h) == i);

magistral.history(topic, channel, count, lambda h : histCallback(h))
```

You can also provide timestamp to start looking messages from:
```python
topic = "topic"
channel = 0
count = 100
timestamp = 1471099313117

def histCallback(h):
  assert(h is not None);
  assert(len(h) == i);

magistral.history(topic, channel, count, timestamp, lambda h : histCallback(h))
```
### History for Time Interval

Historical data in Magistral can be obtained also for some period of time. You need to specify start and end date:
```python
topic = "topic"
channel = 0
count = 100
start = 1471099313117
end = 1471099313117

def callback(h):
  assert(h is not None);
  assert(len(h) == i);
  
magistral.historyIn(topic, channel, start, end, lambda h : callback(h))
```

### Permissions

This is a part of Access Control functionality. First of all, to see the full list of permissions:

```python
def callback(perms):
  for mi in meta:
    for ch in mi.channels():
      print("%s:%d -> (r:w) .. %r:%r", mi.topic(), ch, mi.readable(ch), mi.writable(ch));

magistral.permissions(None, lambda perms : callback(json));
```

Or if you are interested to get permissions for some specific topic:

```python
def callback(perms):
  for mi in meta:
    for ch in mi.channels():
      print("%s:%d -> (r:w) .. %r:%r", mi.topic(), ch, mi.readable(ch), mi.writable(ch));

magistral.permissions("topic", lambda perms : callback(json));
```

### Grant permissions

You can also grant permissions for other users:
```python
let user = "user"
let topic = "topic"
let channel = 0
let ttl = -1 // permanent permissions
let r = True
let w = True

def callback(perms, err):
  assert(err == None)
                        
magistral.grant(user, topic, r, w, ttl, channel, lambda perms, err : callback(perms, err));
```
> You must have super user priveleges to execute this function.

### Revoke permissions

In similar way you can revoke user permissions:
```python
let user = "user"
let topic = "topic"
let channel = -1 // all channels

def callback(perms, err):
  assert(err == None)
                        
magistral.grant(user, topic, channel, lambda perms, err : callback(perms, err));
```
> You must have super user priveleges to execute this function.

## License
Magistral is released under the MIT license. See LICENSE for details.

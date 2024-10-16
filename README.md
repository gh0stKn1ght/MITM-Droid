# MITM-Droid
A tool to perform man-in-the-middle attacks with ARP-spoofing on rooted Android devices
# Why?
There are a lot of different tools for MITM attacks and ARP-spoofing, but all of those require you to enable net.ipv4.ip_forward setting in your kernel. Why is it bad? It is not a big problem, when you use Kali Linux, for example. But in Android systems it is a way more complicated process(even on rooted devices). After many attempts, I gave up on trying to enable IP forwarding in system kernel and decided to recreate needed functionality with Scapy. So, if you want to perform this sort of attacks with your Android phone, this program is the easiest way to do it.
# Supported platforms
Linux - ✔️ (tested on Kali)<br>
Android<b>[Termux]</b> - ✔️ (rooted)<br>
Windows - ❓ (wasn't tested, but should work)<br>
MacOS - ❓ (wasn't tested)
# Usage
### For all platforms: replace <YOUR_MAC_ADDRESS> in the code with MAC of your attacker device.
## Linux | Android[Termux]
### Warning: you need to be root
```
pip install scapy
curl https://raw.githubusercontent.com/gh0stKn1ght/MITM-Droid/main/mitm.py --output mitm.py
sudo python mitm.py
```
## Other
I didn't test it on Windows and MacOS, so I can't provide step-by-step instructions here. But all you need is to install Python and Scapy and run the script with admin/root permissions.<br>
### When you've completed all previous steps, simply follow instructions in the script and the attack will start. All intercepted packets will be saved into .pcap file with the name entered by you.

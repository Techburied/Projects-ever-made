import wikipedia,datetime,bs4,requests,time,random,os
import serial.tools.list_ports
from GoogleNews import GoogleNews
from speak import speak
import speech_recognition as sr
from pywikihow import search_wikihow
import pyjokes as jo
import threading

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("          ")
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,phrase_time_limit=3)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"boss: {query}")

    except Exception as e: 
        print(e)
        return ""
    return query.lower()

def Time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(time)

def Date():
    date = datetime.date.today()
    speak(date)

def Temp():
        search = "temperature in jaipur"
        url = f"https://www.google.com/search?q={search}"
        r = requests.get(url)
        data = bs4.BeautifulSoup(r.text,"html.parser")
        temperature = data.find("div",class_ = "BNeawe").text
        speak(f"The Temperature Outside Is {temperature} ")

        speak("Do I Have To Tell You Another Place Temperature ?")
        next = takecommand()

        if 'yes' in next:
            speak("Tell Me The name of the place")
            name = takecommand()
            search = f"temperature in {name}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = bs4.BeautifulSoup(r.text,"html.parser")
            temperature = data.find("div",class_ = "BNeawe").text
            speak(f"The Temperature in {name} is {temperature} ")

        else:
            speak("no problem")

def get_random_fun_fact():
    url = "https://useless-facts.sameerkumar.website/api"
    response = requests.get(url)
    if response.status_code == 200:
        fact = response.json()["data"]
        return fact
    else:
        return "Failed to fetch a fun fact"

def joke():
    joke = jo.get_joke(category='neutral')
    speak(joke)

def normalize_time(time_string):
    time_parts = time_string.split()
    hours = 0
    minutes = 0

    for i in range(len(time_parts)):
        if time_parts[i] == 'hour' or time_parts[i] == 'hours':
            hours = int(time_parts[i - 1])
        elif time_parts[i] == 'minute' or time_parts[i] == 'minutes':
            minutes = int(time_parts[i - 1])

    time_str = f"{hours:02d}:{minutes:02d}"
    return time_str

def set_alarm():
    speak("Would you like to set the alarm in AM or PM?")
    am_or_pm = takecommand()

    if am_or_pm and 'am' in am_or_pm.lower():
        period = 'AM'
    elif am_or_pm and 'pm' in am_or_pm.lower():
        period = 'PM'
    else:
        speak("Sorry, I didn't understand. Please try again.")
        return

    speak("What time would you like to set the alarm for?")
    time_string = takecommand()

    try:
        time_string = normalize_time(time_string)
        alarm_time = datetime.datetime.strptime(time_string, "%H:%M")
        current_time = datetime.datetime.now()

        if period == 'PM' and alarm_time < current_time:
            alarm_time += datetime.timedelta(hours=12)  # Add 12 hours if setting PM alarm for the same day

        alarm_time = alarm_time.replace(year=current_time.year,
                                        month=current_time.month,
                                        day=current_time.day)

        if alarm_time < current_time:
            alarm_time += datetime.timedelta(days=1)  # Add 1 day if alarm time is in the past

    except ValueError:
        speak("Sorry, I didn't understand the time format. Please try again.")
        return

    time_diff = alarm_time - current_time
    seconds = time_diff.seconds

    speak(f"Setting the alarm for {alarm_time.strftime('%I:%M %p')}.")
    time.sleep(seconds)

    if period == 'AM':
        speak("Good morning! Wake up!")
    else:
        speak("Good evening! Wake up!")

def battery():
    import psutil
    battery = psutil.sensors_battery()
    per = battery.percent
    plug = battery.power_plugged
    if plug == True: status = "charging"
    else: status = "not charging"
    speak(f"battery is currently {status} with {per} percent")
    if per < 30:
        speak("you should charge your device")

def boot():
    import psutil
    import datetime
    boot_time = psutil.boot_time()
    boot_time_seconds = boot_time // 1
    boot_datetime = datetime.datetime.fromtimestamp(boot_time_seconds)
    boot_time_formatted = boot_datetime.strftime('%I:%M:%S %p')
    speak(f"you are working since {boot_time_formatted}")

def quote():
    response = requests.get("http://api.quotable.io/random")
    data = response.json()
    quote = data["content"]
    speak(f"{quote}")

def NonInputExecution(query):
    query = str(query)

    if "comedy" in query:
        joke()

    elif "time" in query:
        Time()

    elif "date" in query:
        Date()

    elif "facts" in query:
        random_fact = get_random_fun_fact()
        speak(random_fact)

    elif "temperature" in query:
        Temp()
        
    elif "alarm" in query:
        set_alarm()

    elif "battery" in query:
        battery()

    elif "working" in query:
        boot()

    elif "quote" in query:
        quote()

def InputExecution(tag,query):

    if "search" in tag:
        query = str(query).replace("search","").replace("what is","").replace("is","").replace("who is","").replace("query","").replace("can you tell me","").replace("ok","").replace("me","")
        page = wikipedia.summary(query, sentences=3)
        speak(page)

    elif "covid" in tag:
        countries = str(query).replace("corona cases in","").replace("covid cases in","").replace("ok","").replace(" ","").replace("covid","").replace("corona","")
        url = f"https://www.worldometers.info/coronavirus/country/{countries}/"
        result = requests.get(url)
        soups = bs4.BeautifulSoup(result.text,'lxml')
        corona = soups.find_all('div',class_ = 'maincounter-number')
        Data = []
        for case in corona:
            span = case.find('span')
            Data.append(span.string)
        try:
            cases, Death, recovored = Data
            speak(f"Cases : {cases}, Deaths : {Death}, Recovered : {recovored}")

        except:
            speak("no data found")

    elif "forecast" in tag:
        p = str(query).replace("tell me the","").replace("forecast","").replace("weather","").replace("what is the","").replace("can you tell me the","").replace("of","").replace("at","").replace("ok","").replace("in","").replace(" ","")
        api = "https://api.openweathermap.org/data/2.5/weather?q="+p+"&appid=06c921750b9a82d8f5d1294e1586276f"
        
        json_data = requests.get(api).json()
        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
        sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))
        speak(f"it's {condition} outside, today temperature is {temp} degree celcius, minimum temperature is {min_temp} degree celcius, maximum temperature is {max_temp} degree celcius, the pressure is {pressure}, today humidity is {humidity}, wind speed is {wind} percent, sunrise is at {sunrise}, sunset is at {sunset}")

        speak("do you want another place weather forecast")
        city = takecommand()
        if "yes" in city:
            speak("tell me the name of the place")
            place = takecommand()
            api = "https://api.openweathermap.org/data/2.5/weather?q="+place+"&appid=06c921750b9a82d8f5d1294e1586276f"
            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            temp = int(json_data['main']['temp'] - 273.15)
            min_temp = int(json_data['main']['temp_min'] - 273.15)
            max_temp = int(json_data['main']['temp_max'] - 273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']
            sunrise = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunrise'] - 21600))
            sunset = time.strftime('%I:%M:%S', time.gmtime(json_data['sys']['sunset'] - 21600))
            speak(f"it's {condition} outside, today temperature is {temp} degree celcius, minimum temperature is {min_temp} degree celcius, maximum temperature is {max_temp} degree celcius, the pressure is {pressure}, today humidity is {humidity}, wind speed is {wind} percent, sunrise is at {sunrise}, sunset is at {sunset}")
        else: 
            speak("no problem!")

    elif 'news' in tag:
        query = str(query).replace("news of", "").replace("tell me", "").replace("can you", "").replace("the","").replace("what is","").replace("latest","").replace(" ","")
        googlenews = GoogleNews()
        speak(f'Getting news of {query}')
        googlenews.get_news(query)
        googlenews.result()
        a = googlenews.gettext()
        speak(a[1:5])

    elif "rockpaper" in tag:
        while True:
            speak("choose your weapon to play")
            user_action = takecommand()
            if "break" in user_action or "bye" in user_action or "stop" in user_action or "i don't want to play" in user_action:
                break
            if user_action == 'tone':
                user_action = "rock"

            elif user_action == 'lock':
                user_action = "rock"

            elif user_action == 'stone':
                user_action = "rock"

            if user_action != "":
                possible_actions = ["rock", "paper", "scissors"]
                computer_action = random.choice(possible_actions)
                if user_action not in possible_actions:
                    speak("I didn't understand. Please try again with a different weapon.")
                    user_action = takecommand()

                speak(f"\nYou choose {user_action}, and i choose {computer_action}.\n")
                if user_action == computer_action:
                    speak(f"Both players selected {user_action}. It's a tie!")

                elif user_action == "rock":
                    if computer_action == "scissors":
                        speak("Rock smashes scissors! You win!")
                    else:
                        speak("Paper covers rock! You lose.")

                elif user_action == "lock":
                    if computer_action == "scissors":
                        speak("Rock smashes scissors! You win!")
                    else:
                        speak("Paper covers rock! You lose.")

                elif user_action == "stone":
                    if computer_action == "scissors":
                        speak("stone smashes scissors! You win!")
                    else:
                        speak("Paper covers rock! You lose.")

                elif user_action == "tone":
                    if computer_action == "scissors":
                        speak("stone smashes scissors! You win!")
                    else:
                        speak("Paper covers rock! You lose.")
                elif user_action == "paper":
                    if computer_action == "rock":
                        speak("Paper covers rock! You win!")
                    else:
                        speak("Scissors cuts paper! You lose.")
                elif user_action == "scissors":
                    if computer_action == "paper":
                        speak("Scissors cuts paper! You win!")
                    else:
                        speak("Rock smashes scissors! You lose.")
            else:
                InputExecution("rockpaper",'a')

    elif "mod" in tag:
        query = str(query).replace("recipe","").replace("some ","").replace("ideas","").replace("cooking ","").replace("for","").replace("about ","").replace("tell me ","")
        try:
            if "exit" in query or "close" in query:
                speak("ok!")
            else:
                max_results = 1
                how_to = search_wikihow(query, max_results)
                assert len(how_to) == 1
                title = str(how_to[0].title).replace("Make","")
                nstep = how_to[0].n_steps
                summary = str(how_to[0].summary).replace("Make","")
                speak(f"searching for{title}. there are {nstep} steps for making{title}.")
                speak("should i tell you recipe")
                ans = takecommand()
                if "yes" in ans or "sure" in ans:
                    speak(summary)
                else:
                    speak("no problem")
        except Exception as e:
            speak("sorry boss, i am not able to find this")

    elif "volume" in tag:
        import re
        n = int(re.sub(r'\D',"", query))

        if n < 100:
            if n < 10:
                n = f"0.0{n}"
            else:
                n = f"0.{n}"
        if n == "100":
            n = "1"
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 0, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(float(n), None)

        n = str(float(n) * 100).replace(".0", "")
        speak(f"Volume Set to {n} percent")

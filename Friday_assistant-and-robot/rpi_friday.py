from Brain import NeuralNet
from NeuralNetwork import bag_of_words ,tokenize
import datetime,bs4,requests,torch,os,json,random,time
from speak import speak
from Task import InputExecution
from Task import NonInputExecution
import serial.tools.list_ports
from word2number import w2n
import re,threading
import speech_recognition as sr
from gtts import gTTS
import sounddevice as sd
import soundfile as sf

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=3)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"boss: {query}\n")
    except Exception as e:
        print(e)
        return ""
    return query.lower()

def speak(text):
    tts = gTTS(text=text, lang='en',slow=False)
    tts.save('output.mp3')
    data, samplerate = sf.read('output.mp3')
    sd.play(data, samplerate)
    sd.wait()



ports = serial.tools.list_ports.comports()
arduino_port = None
for port in ports:
    if 'Arduino' in port.description:  
        arduino_port = port.device
        break
ser = serial.Serial(arduino_port, 9600)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r') as json_data:
    intents = json.load(json_data)
FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]
model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()
Name = "Friday"


def convert_to_seconds(command):
    words = str(command).split()
    converted_words = []
    for word in words:
        if word.isdigit():
            converted_words.append(word)
        else:
            try:
                converted_number = w2n.word_to_num(word)
                converted_words.append(str(converted_number))
            except ValueError:
                pass
    seconds = int("".join(converted_words))
    return seconds

def wishme(): 
    data = bs4.BeautifulSoup(requests.get("https://www.google.com/search?q=temperature in jaipur").text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    tt = datetime.datetime.now().strftime("%I:%M %p")
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak(f"Good Morning, its {tt}")
        speak(f"current temperature outside is {temp} ")

    elif hour>=12 and hour<18:
        speak(f"Good afternoon, its {tt}")
        speak(f"current temperature outside is {temp} ")

    else:
        speak(f"Good evening, its {tt}")
        speak(f"current temperature outside is {temp} ")

def forward(query):
    ser.write(b'F')
    time.sleep(query)
    ser.write(b'S') 

def backward(query):
    ser.write(b'B')
    time.sleep(query)
    ser.write(b'S') 

def right(query):
    ser.write(b'R')
    time.sleep(query)
    ser.write(b'S') 

def left(query):
    ser.write(b'L')
    time.sleep(query)
    ser.write(b'S') 

def wavehand():
    ser.write(b'q')
    ser.write(b'X')

# wishme()

def TaskexeMain():
    while True:
        # sentence = takecommand()
        sentence = input("type: ")
        result = str(sentence)
        if "okay" in sentence or "ok" in sentence or "friday" in sentence or "buddy" in sentence:
            if result == "":
                pass
            else:
                sentence = sentence.replace("okay", "").replace("friday", "").replace("buddy", "").replace("ok","")
                result = result.replace("okay", "").replace("friday", "").replace("buddy", "").replace("ok","")
                sentence = tokenize(sentence)
                X = bag_of_words(sentence,all_words)
                X = X.reshape(1,X.shape[0])
                X = torch.from_numpy(X).to(device)
                output = model(X)
                _ , predicted = torch.max(output,dim=1)
                tag = tags[predicted.item()]
                probs = torch.softmax(output,dim=1)
                prob = probs[0][predicted.item()]
                if prob.item() > 0.75:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            reply = random.choice(intent["responses"])
                            # print(inten`ts)
                            if "time" in reply:
                                NonInputExecution(reply)

                            elif "date" in reply:
                                NonInputExecution(reply)

                            elif "temperature" in reply:
                                NonInputExecution(reply)

                            elif "mod" in reply:
                                InputExecution(reply, result)

                            elif "search" in reply:
                                InputExecution(reply,result)
                            
                            elif 'repeat' in reply:
                                speak("speak!")
                                jj = takecommand()
                                speak(f"You Said: {jj}")
                            
                            elif 'meet' in reply:
                                result = str(result).replace("ok","").replace("meet","").replace("say hello to","").replace("say hi to","").replace(" to","").replace("greet","")
                                speak(reply+result)
                                wavehand()

                            elif "covid" in reply:
                                InputExecution(reply, result)
                                
                            elif "battery" in reply:
                                NonInputExecution(reply)

                            elif "alarm" in reply:
                                NonInputExecution(reply)

                            elif "heads" in reply or "tails" in reply:
                                ser.write(b'q')
                                ser.write(b'X')
                                os.system("mpg123 coin.wav")
                                speak(reply)
                                ser.write(b'b')
                                ser.write(b'X')

                            elif "working" in reply:
                                NonInputExecution(reply)

                            elif "facts" in reply:
                                NonInputExecution(reply)

                            elif "quote" in reply:
                                NonInputExecution(reply)
                            
                            elif "comedy" in reply:
                                NonInputExecution(reply)

                            elif "forecast" in reply:
                                InputExecution(reply, result)

                            elif "news" in reply:
                                InputExecution(reply, result)
                            
                            elif "coin" in reply:
                                speak(reply,intent)

                            elif "colour" in reply:
                                speak(reply)

                            elif "rockpaper" in reply:
                                InputExecution(reply, result)

                            elif "volume" in reply:
                                InputExecution(reply, result)

                            elif "move" in reply:
                                n = int(re.sub(r'\D',"", result))

                                if "forward" in result:
                                    forward(n)

                                elif "backward" in result:
                                    backward(n)

                                elif "left" in result:
                                    left(n)

                                elif "right" in result:
                                    right(n)
                            
                            elif "dismantle" in reply:
                                speak(random.choice(intents["intents"][36]["responses"]))
                                exit()

                            else:
                                speak(reply)
        else:
            pass

TaskexeMain()
# add port name in line number 42
# add hands down command
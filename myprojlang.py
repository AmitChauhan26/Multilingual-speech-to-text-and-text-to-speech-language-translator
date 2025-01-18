from tkinter import *
from tkinter import ttk
import speech_recognition as s
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

root = Tk()
root.geometry('1200x500')
root.resizable(0,0)
root['bg'] = 'blue'
root.title('Multilingual speech to text and text to speech translator')

Label(root,text='Multilingual speech to text and text to speech Language translator',font='Arial 20 bold').pack()

Label(root,text='Recognized Text',font='arial 14 bold',bg='white smoke').place(x=165,y=90)
Input_text=Entry(root,width=60)
Input_text.place(x=30,y=130)

Label(root,text='Output',font='arial 14 bold',bg='white smoke').place(x=780,y=90)
Output_text=Text(root,font='arial 12',height=6,wrap=WORD,padx=5,pady=5,width=50)
Output_text.place(x=620,y=130)

language=list(LANGUAGES.values())
dest_lang=ttk.Combobox(root,values=language,width=22)
dest_lang.place(x=130,y=180)
dest_lang.set('choose language')

def listen():
    recognizer = s.Recognizer()
    with s.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source)
        try:
            recognized_text=recognizer.recognize_google(audio)
            Input_text.delete(0,END)
            Input_text.insert(END,recognized_text)
        except s.UnknownValueError:
            Input_text.delete(0,END)
            Input_text.insert(END,'Could not understand speech')
        except s.RequestError as r:
            Input_text.delete(0,END)
            Input_text.insert(END,f"Speech recognition error:{r}")

def text_to_speech():
    text=Output_text.get(1.0,END).strip()
    if text:
        try:
            targ_lang=dest_lang.get().lower()
            if targ_lang == 'choose language':
                Output_text.delete(1.0,END)
                Output_text.insert(END,"Please select a language first")
                return

            lang_code=[key for key,value in LANGUAGES.items() if value.lower()==targ_lang]
            if not lang_code:
                    Output_text.delete(1.0,END)
                    Output_text.insert(END,"Language code not found")
                    return

            lang_code=lang_code[0]
            tts=gTTS(text=text,lang=lang_code)
            tts.save("output.mp3")
            os.system("start output.mp3" if os.name=="nt" else "afplay output.mp3")
        except Exception as e:
            Output_text.delete(1.0,END)
            Output_text.insert(END, f"Error in text-to-speech:{e}")

def translate():
    input_text=Input_text.get()
    targ_lang=dest_lang.get().lower()

    if not input_text or targ_lang == 'choose language':
        Output_text.delete(1.0,END)
        Output_text.insert(END,"Please enter text and select a language")
        return

    try:
        translator=Translator()
        translated=translator.translate(text=input_text,dest=targ_lang)
        Output_text.delete(1.0,END)
        Output_text.insert(END,translated.text)
    except Exception as e:
        Output_text.delete(1.0,END)
        Output_text.insert(END,f"Translation error:{e}")

listen_btn=Button(root,text='Start listening',font='arial 12 bold',pady=5,command=listen,bg='lightgreen',activebackground='green')
listen_btn.place(x=130,y=220)

trans_btn=Button(root,text='Transtate',font='arial 12 bold',pady=5,command=translate,bg='red',activebackground='green')
trans_btn.place(x=445,y=220)

tts_btn=Button(root,text='Speak text',font='arial 12 bold',pady=5,command=text_to_speech,bg='purple',activebackground='blue')
tts_btn.place(x=780,y=220)

root.mainloop()
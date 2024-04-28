import pvporcupine
import asyncio
import pyaudio
import os
import signal
from src.speech_to_text import recognize_speech
from src.text_to_speech import text_to_speech
from src.config_example import porcupine_access_key
from src.gpt import ChatGPT

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

async def wake_up_detect():
    #capture SIGINT signal, e.g. ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    #create chatGPT
    chat_gpt = ChatGPT()

    # Wake Word Model Path
    keyword_path = "models/Hey-Ras-Pi_en_raspberry-pi_v2_1_0.ppn"

    #initialize the Porcupine engine
    porcupine = None
    try:

        # porcupine = pvporcupine.create(access_key=porcupine_access_key, keyword_paths=[keyword_path])

        pa = pyaudio.PyAudio()
        print(pa)
        audio_stream = pa.open(
                        rate=16000,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=2048)
        print(audio_stream)

        print("Listening for 'Hey Ras Pi'...")
        os.system(f"wake_up_sound.wav")
        while not interrupt_callback():
            # pcm = audio_stream.read(porcupine.frame_length)
            # pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            # keyword_index = porcupine.process(pcm)
            # if keyword_index >= 0:
                #play wake up sound
            print("Hey Ras Pi detected! Recognizing speech...")
            query, lang = recognize_speech()
            try:
                gpt_result = await asyncio.wait_for(
                    asyncio.gather(chat_gpt.gpt(query, lang)),
                    timeout=45
                )
                if gpt_result[0] is not None:
                    gpt_result = gpt_result[0]['choices'][0]['message']["content"]
                    text_to_speech(gpt_result)
                else:
                    text_to_speech("Sorry i couldnt quite get that speak again")
                print("GPT: ", gpt_result)
            except asyncio.TimeoutError:
                print("Request timed out. Retrying...")
                continue


    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


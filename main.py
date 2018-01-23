#!/usr/bin/python

from CommandRecognizer import recognize
from CommandHandler import CommandHandler
from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer
from logger import log
from os import remove
import wave
import threading


def handle_command(filename):
    log("Recognizing command...")
    command, args = recognize(filename)

    if command != 'NO_MATCH':
        handler.handle(command, args)

    # Delete command file since it is no longer needed
    remove(filename)


def listen_for_commands(data, start, end):
    log("Recorded a command.")
    if 'counter' not in listen_for_commands.__dict__:
            listen_for_commands.counter = 0

    command_name = "command" + str(listen_for_commands.counter) + ".wav"
    save_file(command_name, data)
    threading.Thread(target=handle_command, args=(command_name,)).start()

    log("Waiting for command.")
    listen_for_commands.counter += 1


def save_file(filename, data):
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(asource.get_sample_width())
    wave_file.setframerate(16000)
    wave_file.writeframes(b''.join(data))
    wave_file.close()


if __name__=="__main__":

    # Command utilities:
    handler = CommandHandler()

    # Auditok utilities:
    asource = ADSFactory.ads(sampling_rate=16000, sample_width=2, channels=1, frames_per_buffer=512, record=False, block_dur=0.01)
    validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=50)
    tokenizer = StreamTokenizer(validator=validator, min_length=100, max_length=500, max_continuous_silence=30)

    asource.open()

    # Main program loop
    tokenizer.tokenize(asource, callback=listen_for_commands)



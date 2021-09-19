import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import commands
import json

q = queue.Queue()

Name = ["jerry","jarvi","jeremy","java"]

text = ""
result = ""
test = ""

i = 1
j=1


def cleanCall(x):
    y=json.loads(x)
    z = y["partial"]
    if z==test:
        return z
    else:
        entry = "alternative" + str(i) + ": " cleanCall(call)
        text = text + entry + " "
        return z

def cleanResult(x):
    y=json.loads(x)
    z = y["text"]
    if z==test:
        return z
    else:
        entry = "command" + str(i) + cleanResult(result)
        text = text + entry + " "
        return z

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result = json.loads(result)
                    result = str(result["text"])
                    print(result)
                    text = text + " " + "Command" + str(i) + ": " + result
                    i+= 1
                    for name in Name:
                        if name in result:
                            commands.execute(result, text)
                else:
                    call = rec.PartialResult()
                    call = json.loads(call)
                    call = str(call["partial"])
                    if call == test:
                        continue
                    else:
                        text = text + " " + "Alternative"+ str(i) + ": " + call
                        for name in Name:
                            if name in call:
                                commands.execute(call, text)
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

print(text)
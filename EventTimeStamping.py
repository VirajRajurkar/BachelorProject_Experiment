import time
from pylsl import StreamInfo, StreamOutlet
from pydub import AudioSegment
from pydub.playback import play
import threading
import sys
sys.path.append('/path/to/ffmpeg')

# Set up LSL stream for markers
info = StreamInfo('Markers', 'Markers', 1, 0, 'int32', 'myuidw43536')
outlet = StreamOutlet(info)

# Load audio file (update the path to your actual mp4 file)
audio = AudioSegment.from_file("Experiment Arabic normalized corrected.mp4", format="mp4")

# Duration for each phase in seconds
tone_duration = 1.018
question_duration = 6.018  # Duration of the auditory question
imagined_speech_duration = 8.018
verbal_answer_duration = 2.018
white_noise_duration = 4.018

# Function to send a marker with LSL
def send_marker(marker_value):
    outlet.push_sample([marker_value])
    print(f"Marker {marker_value} sent.")

# Function to play the audio (in parallel)
def play_audio():
    play(audio)

# Function to run the experiment in parallel with audio
def run_experiment():
    # Loop through each trial (assuming you have 20 trials as there are 20 questions)
    for trial in range(20):
        print(f"Starting trial {trial + 1}")
        print()

        # Tone (1 second)
        send_marker(1)  # Marker for tone
        time.sleep(tone_duration)

        # Auditory stimulus (question) (5 seconds)
        # send_marker()  # Marker for auditory stimulus
        time.sleep(question_duration)

        # Tone (1 second)
        send_marker(2)  # Marker for tone before imagined speech
        time.sleep(tone_duration)

        # Imagined speech (8 seconds)
        # send_marker()  # Marker for imagined speech
        time.sleep(imagined_speech_duration)

        # Tone (1 second)
        send_marker(3)  # Marker for tone before verbal answer
        time.sleep(tone_duration)

        # Verbal answer (2 seconds)
        # send_marker(6)  # Marker for verbal answer
        time.sleep(verbal_answer_duration)

        # Tone (1 second)
        send_marker(4)  # Marker for tone before verbal answer
        time.sleep(tone_duration)

        # White noise (4 seconds)
        #send_marker(7)  # Marker for white noise
        time.sleep(white_noise_duration)
        print()

# Start the experiment
print("Starting experiment in 20 seconds...")
time.sleep(20)

# Create a thread to play the audio while the experiment runs
audio_thread = threading.Thread(target=play_audio)
experiment_thread = threading.Thread(target=run_experiment)

# Start both threads
audio_thread.start()
experiment_thread.start()

# Wait for both to finish
audio_thread.join()
experiment_thread.join()

print("Experiment complete!")

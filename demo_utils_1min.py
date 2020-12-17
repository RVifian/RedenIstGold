from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.animation import FuncAnimation
from resemblyzer import sampling_rate
from matplotlib import cm, colors
from time import sleep, perf_counter as timer
from umap import UMAP
from sys import stderr
import matplotlib.pyplot as plt
import numpy as np
import datetime

# speakers
karinTime = 0
sandroTime = 0

# needed to multiply frames by time
timeFrameMultiplier = 0.0625

_default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
_my_colors = np.array([
    [0, 127, 70],
    [255, 0, 0],
    [255, 217, 38],
    [0, 135, 255],
    [165, 0, 165],
    [255, 167, 255],
    [97, 142, 151],
    [0, 255, 255],
    [255, 96, 38],
    [142, 76, 0],
    [33, 0, 127],
    [0, 0, 0],
    [183, 183, 183],
    [76, 255, 0],
], dtype=np.float) / 255 


def play_wav(wav, blocking=True):
    try:
        import sounddevice as sd
        # Small bug with sounddevice.play: the audio is cut 0.5 second too early. We pad it to 
        # make up for that
        wav = np.concatenate((wav, np.zeros(sampling_rate // 2)))
        sd.play(wav, sampling_rate, blocking=blocking)
    except Exception as e:
        print("Failed to play audio: %s" % repr(e))

def interactive_diarization(similarity_dict, wav, wav_splits, x_crop=5, show_time=True):    
    fig, (ax, pie) = plt.subplots(1, 2)
    lines = [ax.plot([], [], label=name)[0] for name in similarity_dict.keys()]
    text = ax.text(0, 0, "", fontsize=10)
    
    def init():
        ax.set_ylim(0.4, 1)
        ax.set_ylabel("Similarity")
        if show_time:
            ax.set_xlabel("Time (seconds)")
        else:
            ax.set_xticks([])
        fig.suptitle("Diarization by Patrik, Dejan & Robin", fontsize=14, fontweight='bold')
        ax.set_title("Speaker Diarization")
        ax.legend(loc="lower right")
        return lines + [text]
        
    
    times = [((s.start + s.stop) / 2) / sampling_rate for s in wav_splits]
    rate = 1 / (times[1] - times[0])
    crop_range = int(np.round(x_crop * rate))
    ticks = np.arange(0, len(wav_splits), rate)
    ref_time = timer()
    
    def update(i):
        global sandroTime
        global karinTime
        labels = 'Sandro Botz, Moderator', 'Karin Keller-Sutter, Bundesrätin'
        nums = [sandroTime, karinTime]
        # Crop plot
        crop = (max(i - crop_range // 2, 0), i + crop_range // 2)
        ax.set_xlim(i - crop_range // 2, crop[1])
        if show_time:
            crop_ticks = ticks[(crop[0] <= ticks) * (ticks <= crop[1])]
            ax.set_xticks(crop_ticks)
            ax.set_xticklabels(np.round(crop_ticks / rate).astype(np.int))

        # Plot the prediction
        similarities = [s[i] for s in similarity_dict.values()]
        best = np.argmax(similarities)
        name, similarity = list(similarity_dict.keys())[best], similarities[best]



        pie
        pie.clear()
        pie.axis('equal')
        pie.pie(nums, autopct='%1.1f%%', shadow=True, startangle=140)
        pie.set_title("Sprechverteilung")
        # Place a legend to the right of this smaller subplot.
        pie.legend(bbox_to_anchor=(0.5, 0.95), loc='upper left', borderaxespad=0., labels=labels)
        pie.text(-1, -1.3, 'Total Talk Time:', fontsize=15)
        pie.text(-1, -1.5, 'Sandro Botz: ' + str(datetime.timedelta(seconds=(sandroTime * timeFrameMultiplier)))[:-4] + " Sekunden", style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        pie.text(-1, -1.7, 'Karin Keller-Sutter: ' + str(datetime.timedelta(seconds=(karinTime * timeFrameMultiplier)))[:-4] + " Sekunden", style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
        
        
        
        if similarity > 0.75:
            message = "Speaker: %s (confident)" % name
            color = _default_colors[best]
            # print name and frametimestamp each update
            if name == "Sandro Botz, Moderator":
                sandroTime += 1
                print(sandroTime)
            if name == "Karin Keller-Sutter, Bundesrätin":
                karinTime += 1
                print(karinTime)
            print(name) # print the name of the speaker every update
        elif similarity > 0.65:
            message = "Speaker: %s (uncertain)" % name
            color = _default_colors[best]
            # print name and frametimestamp each update
            if name == "Sandro Botz, Moderator":
                sandroTime += 1
                print(sandroTime)
            if name == "Karin Keller-Sutter, Bundesrätin":
                karinTime += 1
                print(karinTime)
            print(name) # print the name of the speaker every update
        else:
            message = "Unknown/No speaker"
            color = "black"
        text.set_text(message)
        text.set_c(color)
        text.set_position((i, 0.96))
        
        # Plot data
        for line, (name, similarities) in zip(lines, similarity_dict.items()):
            line.set_data(range(crop[0], i + 1), similarities[crop[0]:i + 1])
        
        # Block to synchronize with the audio (interval is not reliable)
        current_time = timer() - ref_time
        if current_time < times[i]:
            sleep(times[i] - current_time)
        elif current_time - 0.2 > times[i]:
            print("Animation is delayed further than 200ms!", file=stderr)
        return lines + [text]
    
        # #Pie Chart
        

    ani = FuncAnimation(fig, update, frames=len(wav_splits), init_func=init, blit=not show_time,
                        repeat=False, interval=1)
    play_wav(wav, blocking=False)


    plt.show()

    # print total amount of talked seconds each candidate
    global karinTime
    global sandroTime
    print(karinTime * timeFrameMultiplier)
    print(sandroTime * timeFrameMultiplier)
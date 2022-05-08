from bisect import bisect
import sys
from six import string_types
from TJA import TJA

# Const Data
X = 100
Y = 100
sliderMultiplier = 1.4

CIRCLE = 1
SLIDER = 2
SPINNER = 12
SLIDER_END = -2
SPINNER_END = -12

EMPTY = 0
CLAP = 8
FINISH = 4
WHISTLE = 2

debug_mode = False
last_debug = None


def rtassert(b, text=""):
    if not b:
        print(sys.stderr, text)
        exit()


def get_help_str():
    return "HELP STRING"


def tja2osu(filename, difficulty):
    """
    Full explanation of osu file format:
    https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)
    :param filename: tja file path
    :param difficulty: string -> "Edit", "Oni", "Hard", "Normal", "Easy" or others
    :return:
    """
    assert isinstance(filename, string_types)

    tja = TJA(filename, difficulty)
    tja.readFumen()
    tja.calcTimeline()

    result = ""
    result += "osu file format v14" + "\n\n"
    result += "[General]" + \
              "\nAudioFilename: " + tja.wavfile + \
              "\nAudioLeadIn: 0" + \
              "\nPreviewTime: " + str(int(tja.demostart) * 1000) + \
              "\nCountdown: 0" + \
              "\nSampleSet: None" + \
              "\nStackLeniency: 0.7" + \
              "\nMode: 1" + \
              "\nLetterboxInBreaks: 0" + \
              "\nWidescreenStoryboard: 0" + \
              "\n\n"
    result += "[Editor]" + \
              "\nDistanceSpacing: 0.8" + \
              "\nBeatDivisor: 4" + \
              "\nGridSize: 8" + \
              "\nTimelineZoom: 2.2" + \
              "\n\n"
    result += "[Metadata]" + \
              "\nTitle:" + tja.title + \
              "\nArtist:" + \
              "\nCreator:" + \
              "\nVersion:Insane" + \
              "\nSource:" + \
              "\nTags:" + \
              "\nBeatmapID:" + \
              "\nBeatmapSetID:" + \
              "\n\n"
    result += "[Difficulty]" + \
              "\nHPDrainRate:5" + \
              "\nCircleSize:5" + \
              "\nOverallDifficulty:4" + \
              "\nApproachRate:5" + \
              "\nSliderMultiplier:" + str(sliderMultiplier) + \
              "\nSliderTickRate:1" + \
              "\n\n"

    result += "[TimingPoints]\n"
    for timestamp, bpm, measure in tja.timingPoints:
        result += str(timestamp * 1000) + "," + str(60/bpm*1000) + "," + str(measure) + ",1,0,100,1,0\n"

    result += "\n[HitObjects]\n"
    timingPts = [x[0] for x in tja.timingPoints]  # In seconds

    for idx, item in enumerate(tja.timeline):
        note, time = item[0], item[2]
        currBeatLen = 60.0 / tja.timingPoints[bisect(timingPts, time) - 1][1]
        if note != "8":
            result += str(X) + "," + str(Y) + "," + str(time * 1000) + ","
        if note == "1":  # Don
            result += "5,0,0:0:0:0:"
        elif note == "2":  # Ka
            result += "5,8,0:0:0:0:"
        elif note == "3":  # Don(L)
            result += "5,4,0:0:0:65:"
        elif note == "4":  # Ka(L)
            result += "5,12,0:0:0:65:"
        elif note == "5" or note == "6":  # Slider or Large Slider
            endtime = tja.timeline[idx + 1][2]
            lenPixel = (endtime - time) * 1000 / (currBeatLen * 1000) * (sliderMultiplier * 100)
            # print(endtime - time, currBeatLen, lenPixel)
            result += "2,0,L|" + str(X + lenPixel) + ":" + str(Y) + ",1," + str(lenPixel)
        elif note == "7":  # Fusen
            endtime = tja.timeline[idx + 1][2] * 1000
            result += "12,0," + str(endtime) + ",0:0:0:0:"
        result += "\n"

    return result


if __name__ == "__main__":
    rtassert(len(sys.argv) >= 2, "need a filename\n" + get_help_str())
    # global debug_mode
    # debug_mode = (len(sys.argv) >= 3 and ("debug" in sys.argv))
    if not sys.argv[1].lower().endswith(".tja"):
        print("Please use a TJA file")
        sys.exit()
    dif = input("Please enter the difficulty:")
    res = tja2osu(sys.argv[1], dif)

    outFile = open(sys.argv[1] + "." + dif.lower() + ".osu", "w+")
    outFile.write(res)

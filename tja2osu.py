import sys
from six import string_types
from TJA import TJA

# Const Data
X = 256
Y = 192

CIRCLE = 1
SLIDER = 2
SPINNER = 12
SLIDER_END = -2
SPINNER_END = -12

EMPTY = 0
CLAP = 8
FINISH = 4
WHISTLE = 2

has_started = False
curr_time = 0.0
bar_data = []
lasting_note = None


def get_t_unit(tm, tot_note):
    # print tm["bpm"], tot_note
    return tm["measure"] * 60000.0 / (tm["bpm"] * tot_note)


debug_mode = False
last_debug = None


def rtassert(b, text=""):
    if not b:
        print(sys.stderr, text)
        exit()


def get_help_str():
    return "HELP STRING"


def tja2osu(filename):
    """
    Full explanation of osu file format:
    https://osu.ppy.sh/wiki/en/Client/File_formats/Osu_(file_format)
    :param filename:
    :return:
    """
    assert isinstance(filename, string_types)
    # rtassert(filename.endswith(".tja"), "filename should ends with .tja")
    # check_unsupported(filename)
    tja = TJA(filename, "Oni")
    tja.readFumen()
    tja.calcTimeline()
    # print(tja.fumen)
    # tja.exportTimeline("E:/")
    # print(tja.title, tja.wavfile)

    # # real work
    # get_meta_data(filename)
    print("osu file format v14" + "\n")
    print("[General]" +
          "\nAudioFilename: " + tja.wavfile +
          "\nAudioLeadIn: 0" +
          "\nPreviewTime: " + str(int(tja.demostart) * 1000) +
          "\nCountdown: 0" +
          "\nSampleSet: None" +
          "\nStackLeniency: 0.7" +
          "\nMode: 1" +
          "\nLetterboxInBreaks: 0" +
          "\nWidescreenStoryboard: 0" +
          "\n"
          )
    print("[Editor]" +
          "\nDistanceSpacing: 0.8" +
          "\nBeatDivisor: 4" +
          "\nGridSize: 8" +
          "\nTimelineZoom: 2.2" +
          "\n"
          )
    print("[Metadata]" +
          "\nTitle:" + tja.title +
          "\nArtist:" +
          "\nCreator:" +
          "\nVersion:Insane" +
          "\nSource:" +
          "\nTags:" +
          "\nBeatmapID:" +
          "\nBeatmapSetID:" +
          "\n"
          )
    print("[Difficulty]" +
          "\nHPDrainRate:5" +
          "\nCircleSize:5" +
          "\nOverallDifficulty:4" +
          "\nApproachRate:5" +
          "\nSliderMultiplier:1.4" +
          "\nSliderTickRate:1" +
          "\n"
          )
    print("[TimingPoints]\n" +
          str(int(tja.offset * 1000)) + "," + str(tja.oneBeatTime * 1000) + "," + str(tja.measure) +
          ",1,0,100,1,0\n"
          )  # This one needs to be fixed with multiple timelines

    print("[HitObjects]")
    for item in tja.timeline:
        note, time = item[0], item[2]
        print(str(X) + "," + str(Y) + "," + str(time * 1000) + ",", end="")
        if note == "1":  # Don
            print("5,0,0:0:0:0:")
        elif note == "2":  # Ka
            print("5,8,0:0:0:0:")
        elif note == "3":  # Don(L)
            print("5,4,0:0:0:80:")
        elif note == "4":  # Ka(L)
            print("5,12,0:0:0:80:")
        elif note == "5":  # Slider
            # TODO
            print("5,12,0:0:0:0:")
        elif note == "6":  # Large slider
            # TODO
            print("5,12,0:0:0:0:")
        elif note == "7":  # Fusen
            # TODO
            print("5,12,0:0:0:0:")
        elif note == "8":  # End
            # TODO
            print("5,12,0:0:0:0:")
    # get_all(filename)
    # if not debug_mode:
    #     write_TimingPoints()
    #     write_HitObjects()


if __name__ == "__main__":
    rtassert(len(sys.argv) >= 2, "need a filename\n" + get_help_str())
    # global debug_mode
    # debug_mode = (len(sys.argv) >= 3 and ("debug" in sys.argv))
    tja2osu(sys.argv[1])

import keyboard
import os
import re
import sys
import time


class TJA:
    def __init__(self, filePath, difficulty="Oni"):
        self.name = ""

        # Jiro basic info
        self.title = ""
        self.subtitle = ""
        self.bpm = 0.0  # Song BPM
        self.wavfile = ""  # Wav file name
        self.oneBeatTime = 0.0  # How many time does one beat take
        self.offset = 0.0  # The time between song start and first note
        self.demostart = 0.0
        self.measure = 4  # Measure, default 4/4

        # Fumen info
        self.filePath = filePath
        self.difficulty = difficulty
        self.fumen = None
        self.timeline = []
        self.timingPoints = []

    def calcTimeline(self):
        """
        Read the Fumen and calculate time for each notes
        The data will be saved in self.timeline
        :return: None
        """
        overallTime = 0.0
        newTimingPts = False
        idx = 0
        self.timingPoints.append((self.offset, self.bpm, self.measure))

        while idx < len(self.fumen):
            bar = self.fumen[idx]

            # Preprocess each line
            while not bar or "#" in bar:
                # print(bar)
                if not bar or "#GOGOSTART" in bar or "#GOGOEND" in bar or\
                        "#SCROLL" in bar or "#BARLINEON" in bar or "#BARLINEOFF" in bar:
                    idx += 1
                    bar = self.fumen[idx]
                    continue
                if "#MEASURE" in bar:
                    self.measure = int(re.search(r"#MEASURE ([0-9]+)\/[0-9]+", bar).group(1))
                    # print("Measure: " + str(self.measure))
                    newTimingPts = True
                    # continue
                elif "#BPMCHANGE" in bar:
                    self.bpm = int(re.search(r"#BPMCHANGE ([0-9]+)", bar).group(1))
                    self.oneBeatTime = 60.0 / float(self.bpm)
                    # continue
                    newTimingPts = True
                idx += 1
                bar = self.fumen[idx]

            if newTimingPts:
                self.timingPoints.append((overallTime + self.offset, self.bpm, self.measure))
                newTimingPts = False
                # idx += 1
                continue

            # Get bar length
            currBarLength = self.oneBeatTime * self.measure
            # print(currBarLength)
            keys = re.sub(r"(\/\/[0-9]+)", "", bar.strip().replace(",", ""))
            count = len(keys)
            keyDelay = currBarLength / count if count else currBarLength
            # print(keys, count)

            # First note
            if idx == 0:
                self.timeline.append((keys[0], overallTime, overallTime + self.offset))
                overallTime += keyDelay
                keys = keys[1:]

            # Process bar
            if not keys:
                overallTime += currBarLength
            else:
                for note in keys:
                    if note != "0":
                        self.timeline.append((note, overallTime, overallTime + self.offset))
                        overallTime += keyDelay
                    else:  # 0?
                        overallTime += keyDelay
                        continue
            idx += 1
        return

    def exportTimeline(self, outPath):
        """
        For testing purpose
        :param outPath:
        :return:
        """
        try:
            outFile = open(outPath + self.name + ".txt", "w+")
            for item in self.timeline:
                outFile.write(item[0] + " " + str(item[1]) + " " + str(item[2]) + "\n")
            outFile.close()
        except OSError:
            print("Directory error")
            sys.exit()

        return

    def iterTimeline(self, startTime):
        flag = 1  # Left or right
        timestamps = []

        for idx, item in enumerate(self.timeline):
            if idx != 0:
                timestamps.append((item[0], startTime + item[1]))

        for note, absTime in timestamps:
            while time.perf_counter() < absTime:
                pass
            if note == "1" or note == "3":
                if flag:
                    keyboard.press_and_release("j")
                else:
                    keyboard.press_and_release("j")
                flag = 1 - flag
            elif note == "2" or note == "4":
                if flag:
                    keyboard.press_and_release("l")
                else:
                    keyboard.press_and_release("l")
                flag = 1 - flag
        return

    def keyPressedKeyboard(self):
        """
        If "j" (Don) or "k" (Ka) pressed, automatically output rest Fumen
        For testing purpose
        :return: None
        """
        while True:
            if keyboard.read_key() == "j":
                print("D", end="")
                self.iterTimeline(time.perf_counter())
            elif keyboard.read_key() == "k":
                print("K", end="")
                self.iterTimeline(time.perf_counter())
            break

    def readFumen(self):
        """
        Read the TJA file and extract the part with corresponding difficulty
        :return: None
        """
        try:
            TJAFile = open(self.filePath, "r")
            self.name = os.path.basename(self.filePath)

            # Read Meta
            textList = TJAFile.readlines()
            text = "".join(textList)
            for line in textList:
                if "#BRANCH" in line:
                    print("Branch is not supported")
                    sys.exit()

                if "TITLE" in line and "SUBTITLE" not in line:
                    self.title = line.split(":")[1].strip()
                elif "SUBTITLE" in line:
                    self.subtitle = line.split(":")[1]
                elif "BPM" in line:
                    self.bpm = int(line.split(":")[1])
                    self.oneBeatTime = 60.0 / float(self.bpm)
                elif "WAVE" in line:
                    self.wavfile = line.split(":")[1]
                elif "OFFSET" in line:
                    self.offset = 0 - float(line.split(":")[1])
                elif "DEMOSTART" in line:
                    self.demostart = float(line.split(":")[1])

            # Extract Fumen
            for splitResult in text.split("COURSE:"):
                if self.difficulty == splitResult.split("\n")[0].strip():
                    self.fumen = re.search(r"#START\n([\S\s]+)\n#END", splitResult).group(1).split("\n")

        except OSError:
            print("Cannot open the TJA file")
            sys.exit()

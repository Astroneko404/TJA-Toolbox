import keyboard
from pynput.keyboard import Key, Controller
import re
import sys
import time

class TJA:
    def __init__(self, filePath, difficulty="Oni"):
        self.bpm = 0.0  # Song BPM
        self.oneBeatTime = 0.0  # How many time does one beat take
        self.measure = 4  # Measure, default 4/4
        self.offset = 0.0  # The time between song start and first note

        self.filePath = filePath
        self.difficulty = difficulty
        self.fumen = None
        self.timeline = []

        self.kb = Controller()

    def calcTimeline(self):
        """
        Read the Fumen and calculate time for each notes
        The data will be saved in self.timeline
        :return: None
        """
        overallTime = self.offset

        for idx, bar in enumerate(self.fumen):
            # Preprocess each line
            if "#MEASURE" in bar:
                self.measure = int(re.search(r"#MEASURE ([0-9]+)\/[0-9]+", bar).group(1))
                continue
            elif "#GOGOSTART" in bar or "#GOGOEND" in bar:
                continue
            elif "#BARLINEON" in bar or "#BARLINEOFF" in bar:  # Need Verification
                continue
            elif "#SCROLL" in bar:
                continue
            elif "#BPMCHANGE" in bar:
                self.bpm = int(re.search(r"#BPMCHANGE ([0-9]+)", bar).group(1))
                self.oneBeatTime = 60.0 / float(self.bpm)
                continue

            # Get bar length
            currBarLength = self.oneBeatTime * float(self.measure)
            keys = re.sub(r"(\/\/[0-9]+)", "", bar.strip().replace(",", ""))
            count = len(keys)
            keyDelay = currBarLength / count if count else currBarLength
            # print(keys, count)

            # First note
            if idx == 0:
                self.timeline.append((bar[0], overallTime))
                bar = bar[1:]

            # Process bar
            if not bar:
                overallTime += currBarLength
            else:
                for note in bar:
                    overallTime += keyDelay
                    if note == "1" or note == "3":  # Don
                        self.timeline.append((note, overallTime))
                    elif note == "2" or note == "4":  # Ka
                        self.timeline.append((note, overallTime))
                    elif note == "5":  # Start of yellow slider
                        # TODO
                        continue
                    elif note == "6":  # Start of large yellow slider
                        # TODO
                        continue
                    elif note == "7":  # Start of balloon
                        # TODO
                        continue
                    elif note == "8":  # End of yellow slider/balloon
                        # TODO
                        continue
                    else:  # Hmmmmmmm
                        continue
        return

    def iterTimeline(self):
        flag = 1  # Left or right

        for idx, item in enumerate(self.timeline):
            if idx != 0:
                lastItem = self.timeline[idx-1]
                currNote, currTime = item[0], item[1]
                lastNote, lastTime = lastItem[0], lastItem[1]
                deltaTime = currTime - lastTime

                time.sleep(deltaTime)
                if currNote == "1" or currNote == "3":
                    if flag:
                        self.kb.type("j")
                    else:
                        self.kb.type("f")
                    flag = 1 - flag
                elif currNote == "2" or currNote == "4":
                    if flag:
                        self.kb.type("k")
                    else:
                        self.kb.type("d")
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
                self.iterTimeline()
            elif keyboard.read_key() == "k":
                print("K", end="")
                self.iterTimeline()
            break

    def readFumen(self):
        """
        Read the TJA file and extract the part with corresponding difficulty
        :return: None
        """
        try:
            TJAFile = open(self.filePath, "r")

            # Read Meta
            textList = TJAFile.readlines()
            text = "".join(textList)
            for line in textList:
                if "BPM" in line:
                    self.bpm = int(line.split(":")[1])
                    self.oneBeatTime = 60.0 / float(self.bpm)
                elif "OFFSET" in line:
                    self.offset = 0 - int(line.split(":")[1])

            # Extract Fumen
            for splitResult in text.split("COURSE:"):
                if self.difficulty == splitResult.split("\n")[0].strip():
                    self.fumen = re.search(r"#START\n([\S\s]+)\n#END", splitResult).group(1).split("\n")

        except OSError:
            print("Cannot open the TJA file")
            sys.exit()


if __name__ == "__main__":
    assert (len(sys.argv) == 3), "Two args needed: FileName & Difficulty"
    fileName, course = sys.argv[1], sys.argv[2]
    # print("File: " + fileName + "\nDifficulty: " + difficulty)

    newTJA = TJA(fileName, course)
    newTJA.readFumen()
    newTJA.calcTimeline()
    # print(newTJA.bpm, newTJA.measure)
    # print(newTJA.timeline)

    newTJA.keyPressedKeyboard()

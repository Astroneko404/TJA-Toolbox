import keyboard
import re
import sys
import time


def iterateFumen(fumen: list):
    global oneBeatTime, MEASURE, BPM
    overallTime = 0.0
    for idx, bar in enumerate(fumen):
        # Preprocess each line
        if "#MEASURE" in bar:
            MEASURE = int(re.search(r"#MEASURE ([0-9]+)\/[0-9]+", bar).group(1))
            continue
        elif "#GOGOSTART" in bar or "#GOGOEND" in bar:
            continue
        elif "#BARLINEON" in bar or "#BARLINEOFF" in bar:  # Need Verification
            continue
        elif "#SCROLL" in bar:
            continue
        elif "#BPMCHANGE" in bar:
            BPM = int(re.search(r"#BPMCHANGE ([0-9]+)", bar).group(1))
            oneBeatTime = 60.0 / float(BPM)
            continue

        # Get bar length
        currBarLength = oneBeatTime * float(MEASURE)
        keys = re.sub(r"(\/\/[0-9]+)", "", bar.strip().replace(",", ""))
        count = len(keys)
        keyDelay = currBarLength / count if count else currBarLength
        # print(keys, count)
        if idx == 0:
            bar = bar[1:]

        # Process bar
        if not bar:
            # time.sleep(currBarLength)
            overallTime += currBarLength
        else:
            for note in bar:
                # time.sleep(keyDelay)
                overallTime += keyDelay
                if note == "1" or note == "3":
                    print("(D " + str(overallTime) + ")", end="\n")
                elif note == "2" or note == "4":
                    print("(K " + str(overallTime) + ")", end="\n")
                else:
                    print(" ", end="")
        print()


if __name__ == "__main__":
    assert (len(sys.argv) == 3), "Two args needed: FileName & Difficulty"
    fileName, difficulty = sys.argv[1], sys.argv[2]
    # print("File: " + fileName + "\nDifficulty: " + difficulty)
    TJAFile = open(fileName, "r")
    currFumen = None

    BPM = 0.0
    oneBeatTime = 0.0
    MEASURE = 4

    try:
        TJAFile = open(fileName, "r")

        # Read Meta
        textList = TJAFile.readlines()
        text = "".join(textList)
        for line in textList:
            if "BPM" in line:
                BPM = int(line.split(":")[1])
                oneBeatTime = 60.0 / float(BPM)
            elif "OFFSET" in line:
                OFFSET = int(line.split(":")[1])

        # Extract Fumen
        for splitResult in text.split("COURSE:"):
            if difficulty == splitResult.split("\n")[0].strip():
                currFumen = re.search(r"#START\n([\S\s]+)\n#END", splitResult).group(1).split("\n")

        # Key pressed detection
        while True:
            if keyboard.read_key() == "j":
                print("D", end="")
                iterateFumen(currFumen)
            elif keyboard.read_key() == "k":
                print("K", end="")
                iterateFumen(currFumen)
            break

    except OSError:
        print("Cannot open the TJA file")
        sys.exit()

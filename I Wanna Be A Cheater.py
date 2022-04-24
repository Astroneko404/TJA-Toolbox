import sys
from TJA import TJA


if __name__ == "__main__":
    assert (len(sys.argv) == 3), "Two args needed: FileName & Difficulty"
    fileName, course = sys.argv[1], sys.argv[2]

    newTJA = TJA(fileName, course)
    newTJA.readFumen()
    # print(newTJA.fumen)
    newTJA.calcTimeline()
    # print(newTJA.timeline)
    # newTJA.exportTimeline("E:/")

    newTJA.keyPressedKeyboard()

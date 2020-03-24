
def log(line :str):
    f=open("log.txt", "a+")
    f.write(line+"\n")
    print(line)
    f.close()


def clear_log():
    raw = open("log.txt", "r+")
    contents = raw.read().split("\n")
    raw.seek(0)
    raw.truncate()
    raw.close()
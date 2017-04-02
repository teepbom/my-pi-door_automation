def read():
  with open("user2", "r") as ins:
    global array
    array = []
    global id
    id = 0
    for line in ins:
        array.append(line.rstrip('\n'))
        print array[id]
        id += 1

def write_log(n,m):
    log = open("log","a")
    txt = "At: %s -->Name [%s] MAC [%s]  \n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),n,m)
    log.write(txt)
    log.close()


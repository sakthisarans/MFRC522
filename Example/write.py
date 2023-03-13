import mfrc522
import time

def RUN():
    rdr = mfrc522.MFRC522(sck=2, miso=4, mosi=3, cs=1, rst=0)

    print("Place card before reader")

    url='1WvaYJqQCr550LB5y90Iur'
    split=[]
    while len(url)!=0:
        temp=(url[:16])
        url=url[16:]
        while len(temp)<16:
            temp=temp+'*' #here i use * as a dummy character
        split.append(temp)
    #never overwrite segment 0 because it contains manufucturer data
    segment=4  #i start writing data from segment 4 because i corrupted segment 123 in my previous experiment
    ref=0
    try:
        while True and ref<(len(split)):

            (stat, tag_type) = rdr.request(rdr.REQIDL)

            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()

                if stat == rdr.OK:
                    print("CARD DETECTED")
                    print(" -  TAG TYPE : 0x%02x" % tag_type)
                    print(" -  UID      : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                    print("")

                    if rdr.select_tag(raw_uid) == rdr.OK:

                        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                        if rdr.auth(rdr.AUTHENT1A, segment, key, raw_uid) == rdr.OK:
                            stat = rdr.write(segment, split[ref].encode())
                            rdr.stop_crypto1()
                            if stat == rdr.OK:
                                print(f"DATA WRITTEN TO ADDRESS {segment}")
                                ref=ref+1
                                segment=segment+1
                            else:
                                print("FAILED")
                        else:
                            print("AUTH ERR")
                    else:
                        print("Failed to select tag")
        print('remove card')
        time.sleep(20)
    except KeyboardInterrupt:
        print("EXITING PROGRAM")

if __name__=="__main__":
    RUN()

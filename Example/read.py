import mfrc522
import time

def RUN():

    rdr = mfrc522.MFRC522(sck=2, miso=4, mosi=3, cs=1, rst=0)

    print("Place card before reader")

    out=''
    
    segment=4 #read data from segment 4 upto end
    try:
        while True:

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
                            data = rdr.read(segment)
                            datastr = ""
                            hexstr = []
                            for i in data:
                                datastr = datastr + (chr(i))
                                hexstr.append(hex(i))
                            print("DATA: " + str(datastr))
                            print("RAW DATA: " + str(hexstr))
                            out=out+str(datastr)
                            segment=segment+1
                            rdr.stop_crypto1()
                            if(chr(data[len(data)-1])=='*'):
                                print(out.replace('*',""))
                                break
                        else:
                            print("AUTH ERR")
                    else:
                        print("Failed to select tag")
    except KeyboardInterrupt:
        print("EXITING PROGRAM")

if __name__=="__main__":
    RUN()

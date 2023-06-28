# Joshua Liu
# 2023-06-26
# Rover coordinates logger
# This program was created to simulate a program logging the GNSS data.
# This should be replaced with a ROS program or changed to SSH reading

# I am using the average of 3 satellites to use for the path generation, 
# but it should be fine if we change it to just using 1 
# A lot of data is not stored such as 
# the altitude, speeds, direction of the latitude/longitude and other information

import serial

# Opens the serial port connected to the GNSS unit
serialPort = serial.Serial(port = "COM6", baudrate=38400, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)

# This stores the data from the GNGGA sentence that is useful in our case (Lat, Lon, Alt)
gnggaLatitude, gnggaLongitude, gnggaAltitude = 0, 0, 0
# This stores the data from the GNGLL sentence that is useful in our case (Lat, Lon)
gngllLatitude, gngllLongitude = 0, 0
# This stores the data from the GNRMC sentence that is useful in our case (Lat, Lon, Speed: Knots)
gnrmcLatitude, gnrmcLongitude, gnrmcSpeedKnots = 0, 0, 0
# This stores the data from the GNVTG sentence that is useful in our case (Speed: Knots, Speed: Km/h)
gnvtgSpeedKnots, gnvtgSpeedKM = 0, 0

latitudeAverages, longitudeAverages = [], [] # This stores the average lat/lon from 3 satellites

# This function writes the lat/lon coordinates to a txt file
def write_coordinates_to_file(file_name, list_of_coordinates):
    # The coordinates are formated in a way where the DisplayPath.py program can read and parse easily
    string_list_of_coordinates = str(list_of_coordinates)
    string_list_of_coordinates = string_list_of_coordinates.replace(", ", ",")
    string_list_of_coordinates = string_list_of_coordinates.replace("],[", " ")
    string_list_of_coordinates = string_list_of_coordinates.replace("]", "")
    string_list_of_coordinates = string_list_of_coordinates.replace("[", "")

    opened_file = open(file_name, "a")
    opened_file.writelines(string_list_of_coordinates + " ")
    opened_file.close()

while 1:
    if serialPort.in_waiting:
        serialString = serialPort.readline() # This read all the data from the GNSS unit

        #print(serialString.decode('Ascii')) # This line prints all the data from the GNSS unit

        # This splits the data into an array to allow for finding values easier
        splitSerialString = serialString.decode('Ascii').split(",") 

        # Below is the parsed data from the satellites that will be useful for us
        if serialString.__contains__(bytes("GGA", "utf-8")):
            gnggaLatitude, gnggaLongitude, gnggaAltitude = splitSerialString[2], splitSerialString[4], splitSerialString[9]
            #print(f"GNGAA, Lat: {gnggaLatitude}, Lon: {gnggaLongitude}, Alt: {gnggaAltitude}")
        if serialString.__contains__(bytes("RMC", "utf-8")):
            gnrmcLatitude, gnrmcLongitude, gnrmcSpeedKnots = splitSerialString[3], splitSerialString[5], splitSerialString[7]
            #print(f"GNRMC, Lat: {gnrmcLatitude}, Lon: {gnrmcLongitude}, Speed: {gnrmcSpeedKnots}Kn")
        if serialString.__contains__(bytes("VTG", "utf-8")):
            gnvtgSpeedKnots, gnvtgSpeedKM = splitSerialString[5], splitSerialString[7]
            #print(f"GNVTG, Speed: {gnvtgSpeedKnots}Kn, {gnvtgSpeedKM}Km/h")
        if serialString.__contains__(bytes("GLL", "utf-8")):
            gngllLatitude, gngllLongitude = splitSerialString[1], splitSerialString[3]
            #print(f"GNGLL, Lat: {gngllLatitude}, Lon: {gngllLongitude}")

            # The reason why the average is calculated and written to the txt file here 
            # is because putting it outside the if statement will result in 
            # writing the same data over and over until new data is read
            # if this if statement is called that means the previous 2 lat/lon have been stored
            averageLatitude = (float(gnggaLatitude) + float(gngllLatitude) + float(gnrmcLatitude)) / 3
            averageLongitude = (float(gnggaLongitude) + float(gngllLongitude) + float(gnrmcLongitude)) / 3
            write_coordinates_to_file("WalkTest.txt", [averageLatitude, averageLongitude]) # Writes the average lat/lon from the 3 satellites

            speedsKnotsKmHAltitude = [(float(gnrmcSpeedKnots) + float(gnvtgSpeedKnots)) / 2, float(gnvtgSpeedKM), float(gnggaAltitude)]
            write_coordinates_to_file("SpeedsAltitude.txt", speedsKnotsKmHAltitude) # Writes the speeds and altitude to a file

            print(f"Lat: {float(averageLatitude)}, Lon: {float(averageLongitude)}, Alt: {float(gnggaAltitude)}, Speed: {(float(gnrmcSpeedKnots) + float(gnvtgSpeedKnots)) / 2}Kn, {gnvtgSpeedKM}Km/h")
    

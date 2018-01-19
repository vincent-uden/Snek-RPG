new_file = open("tiles.txt", "w")

with open("map3.txt", "r") as f:
    for line in f:
        for character in line:
            if character == "1":
                new_file.write("simple_grass ")
            elif character == "\n":
                new_file.write("\n")
            else:
                new_file.write("sand1 ")

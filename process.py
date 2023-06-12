

def main():
    with open("translation.py", "w") as out_f:
        out_f.write("translations = {\n")
        with open("translation.txt", "r") as file:
            while True:
                ang = file.readline().strip()
                if not ang:
                    break
                pl = file.readline().strip()
                out_f.write(f'    \"{pl}\": \"{ang}\",\n')
        out_f.write("}")


if __name__ == '__main__':
    main()
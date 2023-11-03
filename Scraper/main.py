from scraper import jokes_list
def main():
    jokes = jokes_list()
    for joke in jokes:
        print(joke)

if __name__ == "__main__":
    main()
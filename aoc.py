def main():
    import day1
    day1.main()

    import day2
    day2.main()

    import day3
    day3.main()

    import day4
    day4.main()

    import day5
    day5.main()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))

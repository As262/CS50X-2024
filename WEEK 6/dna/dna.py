import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # Read database file into a variable
    rows = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], encoding="utf-8") as f:
        read_data = f.read()

    # Find longest match of each STR in DNA sequence
    STR_List = reader.fieldnames[1:]  # Skip the first field name, which is 'name'
    DNA_Info = {}
    for STR in STR_List:
        DNA_Info[STR] = longest_match(read_data, STR)

    # Check database for matching profiles
    for person in rows:
        match = True
        for STR in STR_List:
            if int(person[STR]) != DNA_Info[STR]:
                match = False
                break
        if match:
            print(person['name'])
            sys.exit(0)

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in sequence, return longest run found
    return longest_run


main()

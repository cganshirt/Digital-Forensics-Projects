import random

from pprint import pprint

from random_words import RandomEmails, RandomNicknames


def main():
    # create a dictionary of random nicknames
    roster = dict()
    random_nicknames = RandomNicknames()
    random_emails = RandomEmails()
    students = random_nicknames.random_nicks(count=10)
    for name in students:
        roster[name] = {
            "email": random_emails.randomMail(),
            "exam_score": random.randint(1, 100),
            "homework_score": random.randint(1, 100),
        }

    pprint(roster)


if __name__ == "__main__":
    main()

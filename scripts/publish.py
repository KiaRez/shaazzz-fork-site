from argparse import ArgumentParser
from pathlib import Path

from persiantools import digits, jdatetime

from .style import read_file, style, raw_style


def get_now():
    now = jdatetime.JalaliDateTime.now()
    return [now.year, now.month, now.day, now.hour, now.minute]

def write_file(path, content):
    print(f"Writing to {path}")
    with open(path, 'w') as file:
        file.write(content)

def get_title(content):
    content = content.split('\n')
    for i in range(len(content)):
        if content[i][0:2] == '# ':
            _, title = content[i].split(' ', 1)
            return title

def get_filename(content, date):
    title = get_title(content)
    title = title.replace(' ', '-')
    date = list(map(str, date))
    for i in range(1, 3):
        if len(date[i]) < 2:
            date[i] = '0'+date[i]
    return f'{date[0]}-{date[1]}-{date[2]}-{title}.md'

def main(args):
    author, date, content = read_file(args.file)
    author = author or args.author
    date = date or args.date or get_now()

    if not author:
        raise Exception("No author")
    if not date:
        raise Exception("No date")

    filename = get_filename(content, date)
    write_file(f'raw/{filename}', raw_style(content, author, date))

def init(parser: ArgumentParser):
    parser.add_argument(
        '-f','--file',
        type=Path,
        help='Content of blog post in markdown format (required)',
        required=True
    )
    parser.add_argument(
        '-a','--author',
        type=str,
        help='Author of blog post',
    )
    parser.add_argument(
        '-d','--date',
        type=str,
        help='Blog published datetime, in this format: "{year} {month} {day} {hour} {minute} (optional, default is the current time)'
    )
    parser.set_defaults(func=main)

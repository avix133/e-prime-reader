import csv
import codecs
import os


class Stimuli(object):
    def __init__(self, start_onset_time, photo_onset_time, response):
        self.start_onset_time = start_onset_time
        self.photo_onset_time = photo_onset_time
        self.response = response


class Subject(object):
    def __init__(self, id):
        self.id = id
        self.stimuli_list = []

    def append_stimuli(self, start, photo, response):
        if start and photo and response:
            self.stimuli_list.append(Stimuli(int(start), int(photo), int(response)))

    def calculate_offsets(self):
        result = {'low': [], 'high': []}
        for stimuli in self.stimuli_list:
            diff = (stimuli.photo_onset_time - stimuli.start_onset_time) / 1000
            if stimuli.response <= 3:
                result.get('low').append(diff)
            elif stimuli.response >= 4:
                result.get('high').append(diff)
        return result


def csv_to_dict(filename):
    result = {}
    with codecs.open(filename, 'rU', 'utf-16LE') as file:
        reader = csv.DictReader(file, delimiter='\t')
        result = []
        for rows in reader:
            result.append(rows)
    return result

data = csv_to_dict('Food-results.csv')

subjects = {}
for row in data:
    id = int(row.get('Subject'))
    session = row.get('Session')
    start = row.get('start.OnsetTime')
    photo = row.get('Photo.OnsetTime')
    resp = row.get('Question.RESP')
    if int(session) == 2:
        subject = subjects.get(id, Subject(id))
        subject.append_stimuli(start, photo, resp)
        subjects[id] = subject

os.mkdir('output')
sub: Subject
for sub in subjects.values():
    offsets = sub.calculate_offsets()
    for k, v in offsets.items():
        filename = 'output/sb%s.s2.food.f_%s.1D' % (sub.id, k)
        file_content = '\t'.join(map(str, v))
        with open(filename, 'w') as outfile:
            outfile.write(file_content)



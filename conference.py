from datetime import timedelta, datetime



class Track:

    def __init__(self,file_path):
        '''
        This is the constructor class for the Class Track . The file path
        is used to extract the input from.
        '''
        self.morning_start = (datetime.min + timedelta(hours=9)).strftime('%I:%M %p')
        self.lunch = (datetime.min + timedelta(hours=12)).strftime('%I:%M %p')
        self.afternoon_start = (datetime.min + timedelta(hours=13)).strftime('%I:%M %p')
        self.day_end = (datetime.min + timedelta(hours=17)).strftime('%I:%M %p')
        self.id = 1
        self.file_path = file_path
        self.talks = {}
        self.talk_list = self.extract_input()

    def extract_input(self):
        """
        This method is used to get the input from the filepath
        provided in the constructor.
        """
        talks = {}
        lines = []
        try:
            with open(self.file_path) as file:
                lines = [line.strip() for line in file]
        except FileNotFoundError as e:
            print('File Not Found', e)
        for line in lines:
            title, minutes = line.rsplit(maxsplit=1)
            try:
                minutes = int(minutes[:-3])
            # if this fails here that means it's lighting for which value is 5 minutes
            except ValueError:
                minutes = 5
            talks[line] = minutes
        return talks

    def get_talks(self, start_talk, end_talk):
        """
        This method is used to get the talks dictionary between the
        start and end time which are represented as
        start_talk and end_talk respectively.
        """
        start = timedelta(hours=start_talk)
        for talk, minutes in list(self.talk_list.items()):
            prev = start + timedelta(minutes=int(minutes))
            if prev <= timedelta(hours=end_talk):
                self.talks[(datetime.min + start).strftime('%I:%M %p')] = talk
                self.talk_list.popitem()
                start += timedelta(minutes=int(minutes))
        return self.talks

    def show_output(self):
        """
        This method is used to get the output in
        the desired format.
        """
        while self.talk_list:
            print('Track %s' % self.id)
            self.prepare_output(9, 12)
            print('%s - %s' % (self.lunch, 'Lunch'))
            self.prepare_output(13, 17)
            print('%s - %s' % (self.day_end, 'Networking Event'))
            self.id += 1

    def prepare_output(self, start, end):
        """
        This method is used to get the output of the
        talks in the desired format.
        """
        for time, title in sorted(self.get_talks(start, end).items()):
            print(time, '-', title)
        # clear previous entries
        self.talks.clear()


if __name__ == '__main__':
    a = Track('conference.txt')
    a.show_output()
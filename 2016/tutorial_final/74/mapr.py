# This is the mrjob program we will use on Hadoop Mapreduce
from mrjob.job import MRJob
from mrjob.step import MRStep
import string


class MRTopWords(MRJob):
    topdict = {}

    # Clean up the text and assign one count to each word
    def mapper_get_words(self, _, line):
        # Clean up text before further processing
        result = []
        processed = line.lower()
        processed = processed.replace("'s", "")
        processed = processed.replace("'", "")
        remove_punct = string.maketrans(string.punctuation,
                                        " " * len(string.punctuation))
        processed = processed.translate(remove_punct)

        for word in processed.split():
            yield word, 1

    # Sum up the frequency of each word
    def combiner_count_frequency(self, word, counts):
        yield word, sum(counts)

    # Populate the dictionary with word occurances
    def reducer_populate_frequency(self, word, counts):
        frequency = sum(counts)

        # Eliminate words with only one occurance
        if frequency > 1:
            self.topdict[word] = frequency
        dummy = self.topdict
        yield None, dummy

    # Second reducer used to print out
    def reducer_find_top_word(self, _, dummy):
        count = 0
        for key in sorted(self.topdict, key=self.topdict.get, reverse=True):
            yield key, self.topdict[key]
            count += 1
            if count > 99:
                break

    # Steps allow us to flexibly construct the MapReduce processes
    def steps(self):
        return [MRStep(mapper=self.mapper_get_words,
                       combiner=self.combiner_count_frequency,
                       reducer=self.reducer_populate_frequency),
                MRStep(reducer=self.reducer_find_top_word)]

# These two lines are required if we run the program on Hadoop, but not locally.
if __name__ == '__main__':
    MRTopWords.run()
    # job = MRTopWords(args=['-r', 'emr'])
    # with job.make_runner() as runner:
    #     runner.run()
    #     for line in runner.stream_output():
    #         key, value = job.parse_output_line(line)
    #         print key, value

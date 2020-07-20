################################################
# Concatenate entries on a diet analysis       #
# author: PPereira                             #
################################################

import sys


class sample:

    '''sample class takes an id on initiation, the purpose of this class is to hold, for each sample,
    all amplified markers and their correspondent prey items'''

    def __init__(self, id):
        '''On initation of the class define the sample id and create an open dictionary for primers'''

        self.id = id
        self.primers = dict()

    def add_item(self, line):
        '''Add item expects a line of the input file and separates it into primer and the prey_items
        for that particular primer'''

        primer_name = line[0]
        pray_info = line[1:]

        try:
            self.primers[primer_name].add_prey(pray_info)

        except KeyError:
            self.primers[primer_name] = primer(primer_name)
            self.primers[primer_name].add_prey(pray_info)

    def count(self):
        '''Counts the number of entries (preys) added to all primers'''
        return sum([len(x) for x in self.primers.values()])

    def concatenate_primers(self):
        '''This function concatenates all primers found in the sample, it expects no other arguments
        To work the function relies on the __sub__ function that is part of the primer class, it takes
        the first two primers and merges them, all subsquent primers are always compared to the updated
        merged dataset
        '''
        result = primer("concatenated")
        at = 0
        for this_primer in self.primers.keys():

            if at == 0:
                result = self.primers[this_primer]
                at = 1
            else:
                result = result-self.primers[this_primer]

        self.primers["concatenated"] = result

    def make_output(self):
        '''This function prepares a list that can then be written to a file from the main script'''

        to_Write = list()
        for i in self.primers['concatenated'].prey_items:
            o_name = self.id
            o_primer = "concatenated"
            o_classi = "\t".join([str(x) for x in i.classification])
            o_f_id = i.final_id
            o_p_id = i.from_primer
            o_m_b = True if len(i.merged) > 0 else False
            o_m_w = ""
            if o_m_b:
                o_m_w = "\t".join(i.merged)

            strtowrite = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t" % (o_name, o_primer, o_classi, o_f_id, o_p_id, str(o_m_b), o_m_w)
            to_Write.append(strtowrite)

        return to_Write

    def __repr__(self):
        '''A string representation of the data gathered works when class is invoked'''
        return "Sample %s has %s primers with %s entries" % (self.id, len(self.primers.keys()), self.count())


class primer:
    '''This class holds all prey_items for the particular primer (defined by primer name provided on init)'''

    def __init__(self, name):
        self.id = name
        self.prey_items = list()

    def add_prey(self, line):
        ''' Method to add prey_items to a particular primer '''

        self.prey_items.append(prey(self.id, line))

    def __repr__(self):
        ''' Representation of the primer class'''
        return "Primer has found %s items" % (len(self.prey_items))

    def __len__(self):
        ''' Method to retrieve the length of the class '''
        return len(self.prey_items)

    def __sub__(self, other):
        ''' The subtract method was designed to take care of the actual merging of primers '''
        l_this_prey = sorted(self.prey_items,key=lambda x: x.max_level(),reverse=True)
        l_other_prey = sorted(other.prey_items,key=lambda x: x.max_level(),reverse=True)

        def inv_distance(this_prey, other_prey):
            ''' Internal function of the method __sub__ that checks how similar two prey_items are
            from each other. The possible outcomes are 0: Different items; 0.5: one of the primers has
            reached a higher taxonomic resolution; 1: both primers reached the same taxonomic resolution
            and are mergeable. Returns a new primer that is the merge between the two given'''
            result = list()

            for t, o in zip(this_prey, other_prey):

                if t is None and o is None:
                    # If both prey have consumed their respective classifications
                    # return the last valid result
                    return result[-1]

                elif t is None and o is not None or t is not None and o is None:
                    # If one prey has been fully consumed while the other has not
                    # they are marked has mergeable
                    result.append(0.5)

                elif t != o:
                    # If at a certain moment they are both different then they are different
                    # preys
                    result.append(0)
                    return result[-1]

                else:
                    # Otherwise they are the same entrance and marked for merge
                    result.append(1)

            return result[-1]

        this_index = 0

        while this_index < len(l_this_prey):

            other_index = 0

            while other_index < len(l_other_prey):

                inv_dist = inv_distance(l_this_prey[this_index].classification,
                                        l_other_prey[other_index].classification)

                if inv_dist == 0:  # They are different entries just continue to next iteration
                    other_index += 1
                    continue

                elif inv_dist == 0.5:  # One of the primers extends the other consume
                    t_primer = len(
                        [x for x in l_this_prey[this_index].classification if x is not None])
                    o_primer = len(
                        [x for x in l_other_prey[other_index].classification if x is not None])

                    if t_primer > o_primer:
                        l_this_prey[this_index].merged.append(
                            l_other_prey[other_index].from_primer+"\t"+l_other_prey[other_index].final_id)
                        del l_other_prey[other_index]
                        break

                    elif o_primer > t_primer:

                        temp_final_id = l_this_prey[this_index].final_id
                        temp_from_primer = l_this_prey[this_index].from_primer
                        l_this_prey[this_index] = l_other_prey[other_index]
                        l_this_prey[this_index].merged.append(
                            temp_from_primer+"\t"+temp_final_id)

                        del l_other_prey[other_index]
                        break

                    else:
                        assert t_primer != o_primer

                else:  # dist == 0 They are the same consume one
                    l_this_prey[this_index].merged.append(
                        l_other_prey[other_index].from_primer+"\t"+l_other_prey[other_index].final_id)

                    del l_other_prey[other_index]
                    break

            this_index += 1

        final_prey = l_this_prey + l_other_prey
        new_primer = primer("concatenated")

        for i in final_prey:
            new_primer.prey_items.append(i)

        return new_primer


class prey:
    ''' The prey classification is stored here, on init it requires to know from which primer
    this prey is from and the line of prey classifications that must follow the
    Class -> Order -> Family -> Genus -> Species order'''

    def __init__(self, primer, line):
        self.level_classification = ["Kingdom","Class", "Order", "Family", "Genus", "Species"]
        self.from_primer = primer
        self.merged = []
        self.classification = list([None if x == "unk" or x == "" or x == " " or x == "None" or x == "none" else x for x in line[:-1]])
        self.final_id = line[-1].strip("\n")

    def __repr__(self):
        ''' Prints out the max classification level of the prey item '''
        return "This prey higher classification is {} which corresponds to the {}".format(self.classification[self.max_level()],self.level_classification[self.max_level()])

    def max_level(self):
        '''Determines the max classification level of this prey item '''
        max_level = [i for i,x in enumerate(self.classification) if x is None]
        if len(max_level) == 0: # if no entries are None in classificaition it reached species which has index 5
            max_level = 5
        else:
            max_level = max_level[0]-1 # else check whats the index that comes before the first None item is found
        return max_level 

# Main script
if __name__ == "__main__":

    inpfile = sys.argv[1]
    outfile = sys.argv[2]

    all_samples = list()
    old_sample = None
    # If you notice that the first prey item is missing or the sample is duplicated, uncomment the next line and comment the line after
    # with open(inpfile, encoding='utf-8-sig') as diet_table:
    with open(inpfile) as diet_table:
        for line in diet_table:
            info = line.split(";")
            this_sample = info[0].strip()

            if old_sample is None or old_sample != this_sample:
                # if no sample was added so far or a new sample is found

                all_samples.append(sample(this_sample))
                all_samples[-1].add_item(info[1:])
                old_sample = this_sample

            else:
                # keep on adding items to the last found sample
                all_samples[-1].add_item(info[1:])

    with open(outfile, "w") as out:

        for l_sample in all_samples:
            l_sample.concatenate_primers()
            out.write("\n".join(l_sample.make_output()))
            out.write("\n")

from math import ceil
from SkipList import SkipList
from random import randint, shuffle
from bisect import insort

# region Utilities

class Element(object):
    def __init__(self, key):
        self.key = key
        self.next_value = -1

def run_sequence(sequence_file_name):
    # Build initial list
    skiplist = SkipList(3)
    sequence = open(sequence_file_name)
    sequence.readline()
    size = 0
    while True:
        line = sequence.readline().strip().split(':')
        if line[0] != '0':
            break
        if line[1] != 'insert':
            raise Exception('Invalid sequence')

        skiplist.insert(float(line[2]))
        if size % 250 == 0:
            while skiplist.rebalance():
                continue
        size += 1
    while skiplist.rebalance():
                continue

    # Perform experiment
    result = [(0, skiplist.head.s / skiplist.size)]
    while True:
        line = sequence.readline()
        if line == '':
            break
        line = line.strip().split(':')
        i = int(line[0])
        operation = line[1]
        value = float(line[2])
        if operation == 'insert' or operation == 'insert-rebalance':
            skiplist.insert(value)
            size += 1
        elif operation == 'delete':
            skiplist.delete(value)
            size -= 1
        else:
            raise Exception('Invalid operation')
        if i % 10 == 0:
            result.append((i, skiplist.head.s / size))
    sequence.close()
    return result

def run_sequence_standard_mode(sequence_file_name):
    # Build initial list
    skiplist = SkipList(3)
    sequence = open(sequence_file_name)
    sequence.readline()
    size = 0
    while True:
        line = sequence.readline().strip().split(':')
        if line[0] != '0':
            break
        if line[1] != 'insert':
            raise Exception('Invalid sequence')

        skiplist.insert(float(line[2]))
        if size % 250 == 0:
            while skiplist.rebalance():
                continue
        size += 1
    while skiplist.rebalance():
        continue

    # Perform experiment
    rebalances = 0
    result = [(0, skiplist.head.s / skiplist.size, rebalances)]
    while True:
        line = sequence.readline()
        if line == '':
            break
        line = line.strip().split(':')
        i = int(line[0])
        operation = line[1]
        value = float(line[2])
        if operation == 'insert' or operation == 'insert-rebalance':
            skiplist.insert(value)
            size += 1
        elif operation == 'delete':
            skiplist.delete(value)
            size -= 1
        else:
            raise Exception('Invalid operation')
        rebalances += skiplist.full_rebalance()
        if i % 10 == 0:
            result.append((i, skiplist.head.s / size, rebalances))
    sequence.close()
    return result

def run_sequence_threshold(skiplist, sequence_file):
    # Build initial list
    sequence = open(sequence_file)
    sequence.readline()
    size = 0
    while True:
        line = sequence.readline().strip().split(':')
        if line[0] != '0':
            break
        if line[1] != 'insert':
            raise Exception('Invalid sequence')

        skiplist.insert(float(line[2]))
        size += 1
    skiplist.full_rebalance()

    if size == 1000:
        assert(skiplist.head.s / size == 11.149)

    # Perform Experiment
    rebalances = 0
    search_path_averages_sum = skiplist.head.s / skiplist.size
    iterations = 0
    while True:
        line = sequence.readline()
        if line == '':
            break
        line = line.strip().split(':')
        operation = line[1]
        value = float(line[2])
        if operation == 'insert':
            rebalances += skiplist.insert(value)
            size += 1
        elif operation == 'delete':
            rebalances += skiplist.delete(value)
            size -= 1
        else:
            raise Exception('Invalid operation')
        search_path_averages_sum += skiplist.head.s / skiplist.size
        iterations += 1
    sequence.close()
    skiplist.print()
    threshold = ceil(4 * skiplist.height() * skiplist.rebalance_threshold) - 1
    try:
        assert(skiplist.head.longest_search_path <= threshold)
    except AssertionError:
        skiplist.print()
        print('Not Balanced!')
        exit()
    return rebalances, skiplist.head.s / skiplist.size

def run_sequence_ratio(skiplist, ratio, sequence_file):
    # Build initial list
    sequence = open(sequence_file)
    sequence.readline()
    size = 0
    while True:
        line = sequence.readline().strip().split(':')
        if line[0] != '0':
            break
        if line[1] != 'insert':
            raise Exception('Invalid sequence')

        skiplist.insert(float(line[2]))
        size += 1
    skiplist.full_rebalance()
    rebalance_interval = int(size * ratio)

    # Perform Experiment
    rebalances = 0
    rebalance_steps = 0
    search_path_averages_sum = skiplist.head.s / skiplist.size
    worst_case_search_length_avg = 0
    iterations = 0
    while True:
        line = sequence.readline()
        if line == '':
            break
        line = line.strip().split(':')
        operation = line[1]
        value = float(line[2])
        if operation == 'insert':
            skiplist.insert(value)
            size += 1
        elif operation == 'delete':
            skiplist.delete(value)
            size -= 1
        else:
            raise Exception('Invalid operation')
        search_path_averages_sum += skiplist.head.s / skiplist.size
        iterations += 1
        if rebalance_interval == 0 or iterations % rebalance_interval == 0:
            worst_case_search_length_avg += skiplist.head.s / skiplist.size
            rebalances += skiplist.full_rebalance()
            rebalance_steps += 1
    sequence.close()

    worst_case_search_length_avg += skiplist.head.s / skiplist.size
    rebalances += skiplist.full_rebalance()
    rebalance_steps += 1

    print('A:' + str(search_path_averages_sum / iterations))
    print('W:' + str(worst_case_search_length_avg / rebalance_steps))
    print('')

    return rebalances, search_path_averages_sum / iterations, worst_case_search_length_avg / rebalance_steps

def generate_insertions_sequence(size, iterations, sequence_file_name):
    # Build initial list
    skiplist = SkipList(3)
    numbers = list(range(1, size * 5))
    shuffle(numbers)
    numbers = [Element(float(i)) for i in sorted(numbers[:size])]
    deletable_keys = []
    sequence = open(sequence_file_name, 'w')
    sequence.write("initial_list:\n")
    used_keys = []
    for i, element in enumerate(numbers):
        skiplist.insert(element.key)
        used_keys.append(element.key)
        write_sequence_line(sequence, 0, 'insert', element.key)
        if i % 250:
            skiplist.full_rebalance()
    skiplist.full_rebalance()
    numbers[0].next_value = numbers[0].key / 2.0
    for i in range(1, size):
        numbers[i].next_value = (numbers[i].key + numbers[i - 1].key) / 2.0
    append_value = numbers[-1].key + 1.0

    # Generate sequence
    sequence.write("updates:\n")
    for i in range(1, iterations + 1):
        index = randint(0, len(numbers))
        if index == 0:
            element = numbers[0]
            value = element.next_value
            element.next_value = value / 2.0
            assert (value not in used_keys)
        elif index == len(numbers):
            value = append_value
            append_value += 1.0
            assert (value not in used_keys)
        else:
            element = numbers[index]
            value = element.next_value
            element.next_value = (element.next_value + element.key) / 2.0
            assert (value not in used_keys)
        assert (len(numbers) == len(set(numbers)))
        skiplist.insert(value)
        used_keys.append(value)
        write_sequence_line(sequence, i, 'insert', value)
    sequence.close()

def generate_insertions_sequences(size, iterations, repetitions, sequence_file_name):
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]
    for filename in sequence_files:
        generate_insertions_sequence(size, iterations, filename)

def generate_stable_sequence(size, iterations, sequence_file_name):
    # Build initial list
    skiplist = SkipList(3)
    numbers = list(range(1, size * 5))
    shuffle(numbers)
    numbers = [Element(float(i)) for i in sorted(numbers[:size])]
    deletable_keys = []
    sequence = open(sequence_file_name, 'w')
    sequence.write("initial_list:\n")
    used_keys = []
    for i, element in enumerate(numbers):
        skiplist.insert(element.key)
        deletable_keys.append(element.key)
        used_keys.append(element.key)
        write_sequence_line(sequence, 0, 'insert', element.key)
        if i % 250:
            skiplist.full_rebalance()
    skiplist.full_rebalance()
    numbers[0].next_value = numbers[0].key / 2.0
    for i in range(1, size):
        numbers[i].next_value = (numbers[i].key + numbers[i - 1].key) / 2.0
    append_value = numbers[-1].key + 1.0

    # Perform Experiment
    sequence.write("updates:\n")
    for i in range(1, iterations + 1):
        if i % 2 == 0:
            index = randint(0, len(numbers))
            if index == 0:
                element = numbers[0]
                value = element.next_value
                element.next_value = value / 2.0
                assert (value not in used_keys)
            elif index == len(numbers):
                value = append_value
                append_value += 1.0
                assert (value not in used_keys)
            else:
                element = numbers[index]
                value = element.next_value
                element.next_value = (element.next_value + element.key) / 2.0
                assert (value not in used_keys)
            assert (len(numbers) == len(set(numbers)))
            skiplist.insert(value)
            insort(deletable_keys, value)
            used_keys.append(value)
            write_sequence_line(sequence, i, 'insert', value)
        else:
            index = randint(0, len(deletable_keys) - 1)
            value = deletable_keys.pop(index)
            skiplist.delete(value)
            write_sequence_line(sequence, i, 'delete', value)
    sequence.close()

def generate_stable_sequences(size, iterations, repetitions, sequence_file_name):
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]
    for filename in sequence_files:
        generate_stable_sequence(size, iterations, filename)

def write_result_line(file, i, s):
    file.write((str(i) + '; ' + str(s) + "\n").replace('.', ','))

def write_result_line_3(file, x, y, z):
    file.write((str(x) + '; ' + str(y) + '; ' + str(z) + "\n").replace('.', ','))

def write_result_line_4(file, x, y, z, v):
    file.write((str(x) + '; ' + str(y) + '; ' + str(z) + '; ' + str(v) + "\n").replace('.', ','))

def write_sequence_line(file, i, operation, value):
    file.write(str(i)+':' + operation + ':' + str(value) + '\n')

# endregion


def insert_only_no_rebalancing_original_gaps(repetitions, sequence_file_name, result_file_name):
    # Setup
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]

    # Perform experiment
    results = []
    for i, sequence in enumerate(sequence_files):
        print('Repetition = ' + str(i))
        results.append(run_sequence(sequence))

    # Output results
    iteration_numbers, search_path_lengths = zip(*results.pop(0))
    for result in results:
        iteration_numbers, search_path_result = zip(*result)
        search_path_lengths = [sum(x) for x in zip(search_path_lengths, search_path_result)]

    fout = open(result_file_name, 'w')
    for i in range(len(iteration_numbers)):
        write_result_line(fout, iteration_numbers[i], round(search_path_lengths[i] / repetitions, 4))
    fout.close()

def insert_only_standard_rebalancing_original_gaps(repetitions, sequence_file_name, result_file_name):
    # Setup
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]

    # Perform experiment
    results = []
    for i, sequence in enumerate(sequence_files):
        print('Repetition = ' + str(i))
        results.append(run_sequence_standard_mode(sequence))

    # Output results
    iteration_numbers, search_path_lengths, rebalances = zip(*results.pop(0))
    for result in results:
        iteration_numbers, search_path_result, rebalance = zip(*result)
        search_path_lengths = [sum(x) for x in zip(search_path_lengths, search_path_result)]
        rebalances = [sum(x) for x in zip(rebalances, rebalance)]

    fout = open(result_file_name, 'w')
    for i in range(len(iteration_numbers)):
        write_result_line_3(fout, iteration_numbers[i], round(search_path_lengths[i] / repetitions, 4), round(rebalances[i] / repetitions, 4))
    fout.close()

def stable_size_no_rebalancing_original_gaps(repetitions, sequence_file_name, result_file_name):
    # Setup
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]

    # Perform experiment
    results = []
    for i, sequence in enumerate(sequence_files):
        print('Repetition = ' + str(i))
        results.append(run_sequence(sequence))

    # Output results
    iteration_numbers, search_path_lengths = zip(*results.pop(0))
    for result in results:
        iteration_numbers, search_path_result = zip(*result)
        search_path_lengths = [sum(x) for x in zip(search_path_lengths, search_path_result)]

    fout = open(result_file_name, 'w')
    for i in range(len(iteration_numbers)):
        write_result_line(fout, iteration_numbers[i], round(search_path_lengths[i] / repetitions, 4))
    fout.close()

def stable_size_standard_rebalancing_original_gaps(repetitions, sequence_file_name, result_file_name):
    # Setup
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]

    # Perform experiment
    results = []
    for i, sequence in enumerate(sequence_files):
        print('Repetition = ' + str(i))
        results.append(run_sequence_standard_mode(sequence))

    # Output results
    iteration_numbers, search_path_lengths, rebalances = zip(*results.pop(0))
    for result in results:
        iteration_numbers, search_path_result, rebalance = zip(*result)
        search_path_lengths = [sum(x) for x in zip(search_path_lengths, search_path_result)]
        rebalances = [sum(x) for x in zip(rebalances, rebalance)]

    fout = open(result_file_name, 'w')
    for i in range(len(iteration_numbers)):
        write_result_line_3(fout, iteration_numbers[i], round(search_path_lengths[i] / repetitions, 4), round(rebalances[i] / repetitions, 4))
    fout.close()

def stable_size_threshold_rebalancing_original_gaps(repetitions, sequence_file_name, result_file_name):
    # Setup
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]
    thresholds = [float(i / 10) for i in range(10, 21)]

    # Perform experiment
    results = []
    for number, threshold in enumerate(thresholds):
        print('Threshold = ' + str(threshold))
        rebalances = []
        for i, sequence in enumerate(sequence_files):
            if i == 8:
                continue
            print('Repetition = ' + str(i))
            skiplist = SkipList(3, threshold)
            rebalances.append(run_sequence_threshold(skiplist, sequence))
        results.append(rebalances)

    # Output results
    fout = open(result_file_name, 'w')
    for repetition in results:
        search_path_lengths = []
        rebalances = []
        for result in repetition:
            r, s = result
            rebalances.append(r)
            search_path_lengths.append(s)
        search_path_lengths.sort()
        rebalances.sort()
        # print('SPL: ' + str(sum(search_path_lengths[1:-1]) / 7.0))
        # print('REB: ' + str(sum(rebalances[1:-1]) / 7.0))
        write_result_line(fout, sum(rebalances[1:-1]) / 7.0, sum(search_path_lengths[1:-1]) / 7.0)
    fout.close()

def stable_size_ratio_rebalance_original_gaps(repetitions, sequence_file_name, result_file_name):
    # Setup
    sequence_files = [sequence_file_name + str(i) + '.txt' for i in range(repetitions)]
    ratios = [round(0.05 * i, 2) for i in range(21)]

    # Perform experiment
    results = []
    for ratio in ratios:
        print('Ratio = ' + str(ratio))
        sub_result = []
        for i, sequence in enumerate(sequence_files):
            print('Repetition = ' + str(i))
            skiplist = SkipList(3)
            sub_result.append(run_sequence_ratio(skiplist, ratio, sequence))
        results.append(sub_result)

    # Output results
    fout = open(result_file_name, 'w')
    for i, repetition in enumerate(results):
        search_path_lengths_avg = []
        search_path_lengths_worst = []
        rebalances = []
        for result in repetition:
            r, sa, sw = result
            rebalances.append(r)
            search_path_lengths_avg.append(sa)
            search_path_lengths_worst.append(sw)
        search_path_lengths_avg.sort()
        search_path_lengths_worst.sort()
        rebalances.sort()

        ratio = ratios[i]
        reb = sum(rebalances[1:-1]) / (repetitions - 2.0)
        spla = sum(search_path_lengths_avg[1:-1]) / (repetitions - 2.0)
        splw = sum(search_path_lengths_worst[1:-1]) / (repetitions - 2.0)
        write_result_line_4(fout, ratio, reb, spla, splw)
    fout.close()


if __name__ == "__main__":
    insert_only_no_rebalancing_original_gaps(10, 'sequences/insert_5000_', 'insert_5000_no_rebalance.csv')
    insert_only_standard_rebalancing_original_gaps(10, 'sequences/insert_5000_', 'insert_5000_standard_rebalance.csv')
    stable_size_no_rebalancing_original_gaps(10, 'sequences/stable_1000_', 'stable_1000_10000_no_rebalance.csv')
    stable_size_standard_rebalancing_original_gaps(10, 'sequences/stable_1000_', 'stable_1000_10000_standard_rebalance.csv')
    stable_size_ratio_rebalance_original_gaps(10, 'sequences/stable_1000_', 'stable_1000_10000_ratio.csv')
    stable_size_threshold_rebalancing_original_gaps(10, "sequences/stable_1000_", "stable_1000_10000_threshold.csv")
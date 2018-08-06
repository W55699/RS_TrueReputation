#=========================================================================================
# RunAttacks.py file is responsible for performing different recommendation system attacks using .csv generated by the RA.py file.
# It test each algorithm implemented in the ReputationAlgorithms.py file (arithmetic mean, true reputation, true reputation improved)
# compare results and plot the result graph
#=========================================================================================

import ReputationAlgorithms
import re
import copy
import os


RATING_PATH = ".\\u.data"  # path to movielens 100k rating file
MOVIE_INFO_PATH = ".\\u.item"  # path to movielens 100k item information file
ATTACK_RATING_PATH = "D:\\final project\\attacks\\"  # path to directory of attack files (see https://github.com/itaygal/RS_TrueReputation/tree/master/attack%20files for example)

"""load rating .csv file and save results to given data structures 
   Args:
       dataset_path: path to movielens 100k rating file
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
   Returns:
       None.
"""
def load(dataset_path, user_movie_ratings, movie_user_ratings, movies):
    # user id | item id | rating | timestamp
    rating_match = re.compile("\D*(\d+)\D*(\d+)\D*(\d+)\D*(\d+)")
    with open(dataset_path, 'r') as dataset_file:
        for rating_line in dataset_file:
            m = rating_match.match(rating_line)
            if m:
                user_id = m.group(1)
                movie_id = m.group(2)
                rating = m.group(3)
                timestamp = m.group(4)
                if user_id not in user_movie_ratings:
                    user_movie_ratings[user_id] = {}
                user_movie_ratings[user_id][movie_id] = (int(rating), int(timestamp))
                if movie_id not in movie_user_ratings:
                    movie_user_ratings[movie_id] = {}
                movies.add(movie_id)
                movie_user_ratings[movie_id][user_id] = (int(rating), int(timestamp))

"""load_movie_release_year uses movielens 100k item information file to load all movie realse year into movie_release_year
   Args:
       movie_release_year: dic of movie id to release year
   Returns:
       None.
"""
def load_movie_release_year(movie_release_year):
    rating_match = re.compile("\D*(\d+)\|[^\|]*\|\d+\-\w+\-(\d+)\|")
    with open(MOVIE_INFO_PATH, 'r') as dataset_file:
        for rating_line in dataset_file:
            m = rating_match.match(rating_line)
            if m:
                movie_id = m.group(1)
                year = int(m.group(2))
                movie_release_year[movie_id] = year

"""load_attack_file loads attack .csv file and save results to given data structures 
   Args:
       dataset_path: path to movielens 100k rating file
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
   Returns:
       None.
"""
def load_attack_file(dataset_path, user_movie_ratings, movie_user_ratings, movies):
    import csv
    from dateutil import parser
    import time
    with open(dataset_path, 'r') as csvFile:
        dataSet = list(csv.reader(csvFile))
        for rating_list in dataSet:
            if rating_list[0] == "":
                break
            user_id = rating_list[0]
            movie_id = rating_list[1]
            rating = rating_list[2]
            dt = parser.parse(rating_list[3])
            timestamp = time.mktime(dt.timetuple())
            if user_id not in user_movie_ratings:
                user_movie_ratings[user_id] = {}
            user_movie_ratings[user_id][movie_id] = (float(rating), int(timestamp))
            if movie_id not in movie_user_ratings:
                movie_user_ratings[movie_id] = {}
            movies.add(movie_id)
            movie_user_ratings[movie_id][user_id] = (float(rating), int(timestamp))


"""create a plot comparing different reputation algorithms implemented in ReputationAlgorithms.py
   It is used to compare different improvement done for true reputation algorithm in order to verify their necessity.

   compare true_reputation, true_reputation with user age, true_reputation with movie age, true_reputation with user and movie age, true_reputation with user and movie age and percentile cutoff
   for each algorithm this function gets a list of 5 values for number of ratings (["5%", "10%", "15%", "20%", "25%", "30%"]). 
   Each values is the change rate of that algorithm on "attack_name" attack file with the corresponding number of ratings
   For example  base_change_rate may be [0.45,0.2, 0.9, 0, 1] => meaning for 5% attacked rating the change rate was 0.45
      Args:
       attack_name: attack name
       number_of_ratings: list of the number of attacked rating (for example ["5%", "10%", "15%", "20%", "25%", "30%"])
       base_change_rate : true reputation change rate list
       user_age_change_rates : true reputation with user age change rate list
       movie_age_change_rates : true reputation with movie age change rate list
       user_movie_age_change_rates : true reputation with movie and user age  change rate list
       user_movie_age_per_cutoff__change_rates : true reputation with movie and user age and cuttoff change rate list
   Returns:
       None.
"""
def plot_effectivenes_attack_graph_percentile_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, color='red')
    pylab.plot(number_of_ratings,user_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='blue')
    pylab.plot(number_of_ratings,movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='green')
    pylab.plot(number_of_ratings,user_movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='yellow')
    pylab.plot(number_of_ratings,user_movie_age_per_cutoff__change_rates, linewidth=2.5, marker='+', color='black')
    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + " percentile cutoff.png")
    pylab.close()

"""create a plot comparing different reputation algorithms implemented in ReputationAlgorithms.py
   It is used to compare different improvement done for true reputation algorithm in order to verify their necessity.

   compare true_reputation, true_reputation with user age, true_reputation with movie age, true_reputation with user and movie age
   for each algorithm this function gets a list of 5 values for number of ratings (["5%", "10%", "15%", "20%", "25%", "30%"]). 
   Each values is the change rate of that algorithm on "attack_name" attack file with the corresponding number of ratings
   For example  base_change_rate may be [0.45,0.2, 0.9, 0, 1] => meaning for 5% attacked rating the change rate was 0.45
      Args:
       attack_name: attack name
       number_of_ratings: list of the number of attacked rating (for example ["5%", "10%", "15%", "20%", "25%", "30%"])
       base_change_rate : true reputation change rate list
       user_age_change_rates : true reputation with user age change rate list
       movie_age_change_rates : true reputation with movie age change rate list
       user_movie_age_change_rates : true reputation with movie and user age  change rate list
   Returns:
       None.
"""
def plot_effectivenes_attack_graph_no_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, color='red')
    pylab.plot(number_of_ratings,user_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='blue')
    pylab.plot(number_of_ratings,movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='green')
    pylab.plot(number_of_ratings,user_movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='yellow')

    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + ".png")
    pylab.close()

"""create a plot comparing different reputation algorithms implemented in ReputationAlgorithms.py
   It is used to compare different improvement done for true reputation algorithm in order to verify their necessity.
   
   compare true_reputation, true_reputation with user age, true_reputation with movie age, true_reputation with user and movie age, true_reputation with user and movie age and const cutoff
   for each algorithm this function gets a list of 5 values for number of ratings (["5%", "10%", "15%", "20%", "25%", "30%"]). 
   Each values is the change rate of that algorithm on "attack_name" attack file with the corresponding number of ratings
   For example  base_change_rate may be [0.45,0.2, 0.9, 0, 1] => meaning for 5% attacked rating the change rate was 0.45
      Args:
       attack_name: attack name
       number_of_ratings: list of the number of attacked rating (for example ["5%", "10%", "15%", "20%", "25%", "30%"])
       base_change_rate : true reputation change rate list
       user_age_change_rates : true reputation with user age change rate list
       movie_age_change_rates : true reputation with movie age change rate list
       user_movie_age_change_rates : true reputation with movie and user age  change rate list
       plot_effectivenes_attack_graph_const_cutoff : true reputation with movie and user age and cuttoff change rate list
   Returns:
       None.
"""
def plot_effectivenes_attack_graph_const_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, color='red')
    pylab.plot(number_of_ratings,user_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='blue')
    pylab.plot(number_of_ratings,movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='green')
    pylab.plot(number_of_ratings,user_movie_age_change_rates , linewidth=2.5, marker='+', markersize=12, color='yellow')
    pylab.plot(number_of_ratings,user_movie_age_const_cutoff__change_rates , linewidth=2.5, marker='+', color='black')
    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + " const cutoff.png")
    pylab.close()

"""  this function loads attack and runs all improvements reputation algorithms for comparison.
     It is used to compare different improvement done for true reputation algorithm in order to verify their necessity.
     It gets the the reputation vector of each algorithm when ran on original rating file (before attack). 
     It uses to vector to compute the change rate (distance between reputation vectors with and without attacked ratings) 
     
      Args:
       attack_file_path: patch to attack .csv file
       base_reputation_vector: arithmetic mean rating vector on original rating file 
       true_reputation_vector: true reputation rating vector on original rating file 
       true_reputation_user_age_vector: true reputation with user age rating vector on original rating file 
       true_reputation_movie_age_vector: true reputation with movie age rating vector on original rating file 
       true_reputation_user_age_movie_age_vector: true reputation with movie age, user age rating vector on original rating file 
       true_reputation_user_age_movie_age_const_cutoff_vector: true reputation with movie age, user age, const cutoff rating vector on original rating file 
       true_reputation_user_age_movie_age_per_cutoff_vector: true reputation with movie age, user age, per cutoff rating vector on original rating file 

   Returns:
       None.
"""
def load_run_effectivenes_attack_file(attack_file_path, base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                      user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    user_movie_ratings_attacked = copy.deepcopy(user_movie_ratings)
    movie_user_ratings_attacked = copy.deepcopy(movie_user_ratings)
    load_attack_file(attack_file_path, user_movie_ratings_attacked, movie_user_ratings_attacked, movies)

    true_reputation_vector_attacked = ReputationAlgorithms.true_reputation(user_movie_ratings_attacked, movie_user_ratings_attacked, movies)
    base_change_rate = ReputationAlgorithms.vector_distance(true_reputation_vector_attacked, true_reputation_vector)


    true_reputation_user_age_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, False, False)
    user_age_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_vector_attacked,true_reputation_user_age_vector )

    true_reputation_movie_age_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, False, False, False, True)
    movie_age_change_rate = ReputationAlgorithms.vector_distance(true_reputation_movie_age_vector_attacked, true_reputation_movie_age_vector)

    true_reputation_user_age_movie_age_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, False, True)
    user_age_movie_age_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_movie_age_vector_attacked, true_reputation_user_age_movie_age_vector)

    true_reputation_user_age_movie_age_const_cutoff_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, True, False, True)
    user_age_movie_age_const_cutoff_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_movie_age_const_cutoff_vector_attacked, true_reputation_user_age_movie_age_const_cutoff_vector)
    true_reputation_user_age_movie_age_per_cutoff_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, True, True)
    user_age_movie_age_per_cutoff_change_rate = ReputationAlgorithms.vector_distance(true_reputation_user_age_movie_age_per_cutoff_vector_attacked, true_reputation_user_age_movie_age_per_cutoff_vector)


    mean_vector_attacked = ReputationAlgorithms.arithmetic_mean(movie_user_ratings_attacked, movies)
    mean_change_rate = ReputationAlgorithms.vector_distance(mean_vector_attacked, base_reputation_vector)

    return [mean_change_rate, base_change_rate, user_age_change_rate, movie_age_change_rate, user_age_movie_age_change_rate, user_age_movie_age_const_cutoff_change_rate, user_age_movie_age_per_cutoff_change_rate]


""" this function loads all attack files and a given attack each attack file runs all improvements reputation algorithms for comparison.
     For each attack we have several attack files with different rating number

      Args:
       attack_name: attack name
       attack_dir_path: patch to dir coating all attacks 
       base_reputation_vector: arithmetic mean rating vector on original rating file 
       true_reputation_vector: true reputation rating vector on original rating file 
       true_reputation_user_age_vector: true reputation with user age rating vector on original rating file 
       true_reputation_movie_age_vector: true reputation with movie age rating vector on original rating file 
       true_reputation_user_age_movie_age_vector: true reputation with movie age, user age rating vector on original rating file 
       true_reputation_user_age_movie_age_const_cutoff_vector: true reputation with movie age, user age, const cutoff rating vector on original rating file 
       true_reputation_user_age_movie_age_per_cutoff_vector: true reputation with movie age, user age, per cutoff rating vector on original rating file 

   Returns:
       None.
"""
def load_run_all_effectivenes_attack_files(attack_name, attack_dir_path, base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                           user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    number_of_ratings = ["5%", "10%", "15%", "20%", "25%", "30%"]
    base_change_rate = []
    mean_change_rate = []
    user_age_change_rates = []
    movie_age_change_rates = []
    user_movie_age_change_rates = []
    user_movie_age_const_cutoff__change_rates = []
    user_movie_age_per_cutoff__change_rates = []


    for filename in sorted(os.listdir(attack_dir_path+".")):
        if filename.endswith(".csv"):
            change_rates = load_run_effectivenes_attack_file(attack_dir_path+filename, base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                      user_movie_ratings, movie_user_ratings, movies, movie_release_year)
            mean_change_rate.append(change_rates[0])
            base_change_rate.append(change_rates[1])
            user_age_change_rates.append(change_rates[2])
            movie_age_change_rates.append(change_rates[3])
            user_movie_age_change_rates.append(change_rates[4])
            user_movie_age_const_cutoff__change_rates.append(change_rates[5])
            user_movie_age_per_cutoff__change_rates.append(change_rates[6])

    plot_effectivenes_attack_graph_no_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates)
    plot_effectivenes_attack_graph_const_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates)
    plot_effectivenes_attack_graph_percentile_cutoff(attack_name, number_of_ratings, base_change_rate, user_age_change_rates, movie_age_change_rates, user_movie_age_change_rates, user_movie_age_const_cutoff__change_rates, user_movie_age_per_cutoff__change_rates)

""" this function loads all attack files and for a given attack each attack file runs all improvements reputation algorithms for comparison.
     For each attack we have several attack files with different rating number

      Args:
       attack_dir_path: patch to dir coating all attacks 
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
       movie_release_year: movie release year dic
   Returns:
       None.
"""
def comapre_evaluate_parameter_effectiveness(attacks_dir_path, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    base_reputation_vector = ReputationAlgorithms.arithmetic_mean(movie_user_ratings, movies)
    true_reputation_vector = ReputationAlgorithms.true_reputation(user_movie_ratings, movie_user_ratings, movies)
    true_reputation_user_age_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, False, False)
    true_reputation_movie_age_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, False, False, False, True)
    true_reputation_user_age_movie_age_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, False, True)
    true_reputation_user_age_movie_age_const_cutoff_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, True, False, True)
    true_reputation_user_age_movie_age_per_cutoff_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, True, True)

    for attack_dir in ["TargetOnly Nuke 2", "TargetOnly Push 2"]:
        print(attack_dir)
        load_run_all_effectivenes_attack_files(attack_dir, attacks_dir_path + attack_dir + "\\", base_reputation_vector, true_reputation_vector, true_reputation_user_age_vector, true_reputation_movie_age_vector,
                                        true_reputation_user_age_movie_age_vector, true_reputation_user_age_movie_age_const_cutoff_vector, true_reputation_user_age_movie_age_per_cutoff_vector,
                                           user_movie_ratings, movie_user_ratings, movies, movie_release_year)


"""create a plot comparing different reputation algorithms implemented in ReputationAlgorithms.py
   It is used to compare our improved true reputation (user + movie age) with old true reputation.

   for each algorithm this function gets a list of 5 values for number of ratings (["5%", "10%", "15%", "20%", "25%", "30%"]). 
   Each values is the change rate of that algorithm on "attack_name" attack file with the corresponding number of ratings
   For example  base_change_rate may be [0.45,0.2, 0.9, 0, 1] => meaning for 5% attacked rating the change rate was 0.45
      Args:
       attack_name: attack name
       number_of_ratings: list of the number of attacked rating (for example ["5%", "10%", "15%", "20%", "25%", "30%"])
       base_change_rate : true reputation change rate list
       None.
"""
def plot_attack_graph(attack_name, number_of_ratings, base_change_rate, improved_change_rates):
    import pylab
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, label='TRUE-REPUTATION')
    pylab.plot(number_of_ratings, improved_change_rates, linewidth=2.5, marker='^', markersize=12, label='TRUE-REPUTATION++')

    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + ".png")
    pylab.close()

"""create a plot comparing different reputation algorithms implemented in ReputationAlgorithms.py
   It is used to compare our improved true reputation (user + movie age) with old true reputation and arithmetic mean.

   for each algorithm this function gets a list of 5 values for number of ratings (["5%", "10%", "15%", "20%", "25%", "30%"]). 
   Each values is the change rate of that algorithm on "attack_name" attack file with the corresponding number of ratings
   For example  base_change_rate may be [0.45,0.2, 0.9, 0, 1] => meaning for 5% attacked rating the change rate was 0.45
      Args:
       attack_name: attack name
       number_of_ratings: list of the number of attacked rating (for example ["5%", "10%", "15%", "20%", "25%", "30%"])
       base_change_rate : true reputation change rate list
       mean_change_rate : arithmetic mean change rate list
       None.
"""
def plot_attack_graph_with_base(attack_name, number_of_ratings, base_change_rate, improved_change_rates, mean_change_rate):
    import pylab
    pylab.plot(number_of_ratings, mean_change_rate, linewidth=2.5, marker='o', markersize=12, label='ARITHMETIC-MEAN', color='red')
    pylab.plot(number_of_ratings, base_change_rate, linewidth=2.5, marker='x', markersize=12, label='TRUE-REPUTATION')
    pylab.plot(number_of_ratings, improved_change_rates, linewidth=2.5, marker='^', markersize=12, label='TRUE-REPUTATION++')

    pylab.xlabel('of total number of ratings')
    pylab.ylabel('Change Rate')
    pylab.title(attack_name + " rating frequency")
    pylab.grid(True)
    pylab.savefig(attack_name + ".png")
    pylab.close()


"""  this function loads attack and runs reputation algorithms for comparison.
     It is used to compare the improved true reputation with old true reputation algorithm 
     It gets the the reputation vector of each algorithm when ran on original rating file (before attack). 
     It uses to vector to compute the change rate (distance between reputation vectors with and without attacked ratings) 

      Args:
       attack_file_path: patch to attack .csv file
       base_reputation_vector: arithmetic mean rating vector on original rating file 
       true_reputation_vector: true reputation rating vector on original rating file 
       true_reputation_improved_vector: true reputation with user and movie age rating vector on original rating file 
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
       movie_release_year: movie release year dic
       
   Returns:
       None.
"""
def load_run_attack_file(attack_file_path, base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    user_movie_ratings_attacked = copy.deepcopy(user_movie_ratings)
    movie_user_ratings_attacked = copy.deepcopy(movie_user_ratings)
    load_attack_file(attack_file_path, user_movie_ratings_attacked, movie_user_ratings_attacked, movies)

    true_reputation_vector_attacked = ReputationAlgorithms.true_reputation(user_movie_ratings_attacked, movie_user_ratings_attacked, movies)
    base_change_rate = ReputationAlgorithms.vector_distance(true_reputation_vector_attacked, true_reputation_vector)


    true_reputation_improved_vector_attacked = ReputationAlgorithms.true_reputation_improved(user_movie_ratings_attacked, movie_user_ratings_attacked, movies,
                                                                                             movie_release_year, True, False, False, True)
    improved_change_rate = ReputationAlgorithms.vector_distance(true_reputation_improved_vector_attacked, true_reputation_improved_vector)

    mean_vector_attacked = ReputationAlgorithms.arithmetic_mean(movie_user_ratings_attacked, movies)
    mean_change_rate = ReputationAlgorithms.vector_distance(mean_vector_attacked, base_reputation_vector)

    return [base_change_rate, improved_change_rate, mean_change_rate]

""" this function loads all attack files for given attack each attack file runs reputation algorithms for comparison.
    It is used to compare the improved true reputation with old true reputation algorithm 
    For each attack we have several attack files with different rating number

      Args:
       attack_name: attack name
       attack_dir_path: patch to dir coating all attacks 
       base_reputation_vector: arithmetic mean rating vector on original rating file 
       true_reputation_vector: true reputation rating vector on original rating file 
       true_reputation_improved_vector: true reputation with user and movie age rating vector on original rating file 
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
       movie_release_year: movie release year dic
       
   Returns:
       None.
"""
def load_run_all_attack_files(attack_name, attack_dir_path, base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    number_of_ratings = ["5%", "10%", "15%", "20%", "25%", "30%"]
    base_change_rate = []
    improved_change_rates = []
    mean_change_rate = []
    base_change_rate_sum = 0.0
    improved_change_rate_sum = 0.0
    mean_change_rate_sum = 0.0
    for filename in sorted(os.listdir(attack_dir_path+".")):
        if filename.endswith(".csv"):
            change_rates = load_run_attack_file(attack_dir_path+filename, base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year)

            base_change_rate.append(change_rates[0])
            improved_change_rates.append(change_rates[1])
            mean_change_rate.append(change_rates[2])

            base_change_rate_sum += change_rates[0]
            improved_change_rate_sum += change_rates[1]
            mean_change_rate_sum += change_rates[2]

    plot_attack_graph(attack_name, number_of_ratings, base_change_rate, improved_change_rates)
    plot_attack_graph_with_base(attack_name + " with ARITHMETIC-MEAN", number_of_ratings, base_change_rate, improved_change_rates, mean_change_rate)
    print("ARITHMETIC-MEAN Change Rate AVG: %.10f" % (mean_change_rate_sum/5))
    print("True Reputation Change Rate AVG: %.10f" % (base_change_rate_sum/5))
    print("True Reputation++ Change Rate AVG: %.10f" % (improved_change_rate_sum/5))
    improvement = ((base_change_rate_sum/5 - improved_change_rate_sum/5) / (improved_change_rate_sum/5)) * 100
    print("True Reputation++/True Reputation improvement : %.3f%%" % improvement)


"""  Main function function loads all attacks and runs reputation algorithms for comparison.
     It is used to compare the improved true reputation with old true reputation algorithm 
     It gets the the reputation vector of each algorithm when ran on original rating file (before attack). 
     It uses to vector to compute the change rate (distance between reputation vectors with and without attacked ratings) 
     
      Args:
       attack_file_path: patch to attack .csv file
       user_movie_ratings: dic of user to a dic of movie to a rating. user_movie_ratings[user_id][movie_id] = rating
       movie_user_ratings:  dic of movie to a dic of user to a rating. movie_user_ratings[movie_id][user_id] = rating
       movies: set of all movie names
       movie_release_year: movie release year dic

   Returns:
       None.
"""
def run_all_attacks(attacks_dir_path, user_movie_ratings, movie_user_ratings, movies, movie_release_year):
    base_reputation_vector = ReputationAlgorithms.arithmetic_mean(movie_user_ratings, movies)
    true_reputation_vector = ReputationAlgorithms.true_reputation(user_movie_ratings, movie_user_ratings, movies)
    true_reputation_improved_vector = ReputationAlgorithms.true_reputation_improved(user_movie_ratings, movie_user_ratings, movies,
                                                                                             movie_release_year, True, False, False, True)

    for attack_dir in sorted(os.listdir(attacks_dir_path+".")):
        print(attack_dir)
        load_run_all_attack_files(attack_dir, attacks_dir_path + attack_dir + "\\", base_reputation_vector, true_reputation_vector, true_reputation_improved_vector, user_movie_ratings, movie_user_ratings, movies, movie_release_year)


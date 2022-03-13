package hw5;

import java.io.*;
import java.nio.Buffer;
import java.util.*;

public class Recommendation {
    public static Map<Integer, double[]> movieMap = new HashMap<>();
    public static Map<Integer, double[]> userMap = new HashMap<>();
    public static Map<Integer, String> movieNamesMap = new HashMap<>();

    public static Map<Integer, Map<Integer, Integer>> userAndMovieMap = new HashMap<>();

    public static class ReccResult
    {
        String name;
        double predictionValue;
        public ReccResult(String name, double predictionValue)
        {
            this.name = name;
            this.predictionValue = predictionValue;
        }

        @Override
        public String toString()
        {
            return name + " - " + predictionValue;
        }
    }

    public static void parseMovieNamesCSV(String filename)
    {
        try(BufferedReader reader = new BufferedReader(new FileReader(filename)))
        {
            String line;
            while ((line = reader.readLine()) != null) {
               int l = 0;
               int r = 0;
               while(line.charAt(r) != '|')
               {
                   r++;
               }
               int movie_id = Integer.parseInt(line.substring(l, r));
               l = r + 1;
               r = l;
               while(line.charAt(r) != '|')
               {
                   r++;
               }
               String name = line.substring(l, r);
               movieNamesMap.put(movie_id, name);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void parseRatingsCSV(String filename)
    {
        try (Scanner scanner = new Scanner(new File(filename));)
        {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] split = line.split(",");
                int user_id = Integer.parseInt(split[0]);
                int movie_id = Integer.parseInt(split[1]);
                int rating = Integer.parseInt(split[2]);

                Map<Integer, Integer> mapValue = userAndMovieMap.getOrDefault(user_id, new HashMap<>());
                mapValue.put(movie_id, rating);
                userAndMovieMap.put(user_id, mapValue);

                double[] movieMapValues = movieMap.getOrDefault(movie_id, new double[2]);
                movieMapValues[0] += 1;
                movieMapValues[1] = (movieMapValues[1] * (movieMapValues[0] - 1) + rating) / movieMapValues[0];
                movieMap.put(movie_id, movieMapValues);

                double[] userMapValues = userMap.getOrDefault(user_id, new double[2]);
                userMapValues[0] += 1;
                userMapValues[1] = (userMapValues[1] * (userMapValues[0] - 1) + rating) / userMapValues[0];
                userMap.put(user_id, userMapValues);
            }
        } catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }
    }

    public static int highestRatedMovie()
    {
        Queue<Integer> q = new PriorityQueue<>((a, b) -> movieMap.get(a)[1] > movieMap.get(b)[1] ? -1 : 1);
        for(int movie: movieMap.keySet())
        {
            q.add(movie);
        }
        while(!q.isEmpty())
        {
            int movie_id = q.poll();
            if(movieMap.get(movie_id)[0] >= 100)
            {
                return movie_id;
            }
        }
        return -1;
    }

    public static int lowestRatedMovie()
    {
        Queue<Integer> q = new PriorityQueue<>((a, b) -> movieMap.get(a)[1] < movieMap.get(b)[1] ? -1 : 1);
        for(int movie: movieMap.keySet())
        {
            q.add(movie);
        }
        while(!q.isEmpty())
        {
            int movie_id = q.poll();
            if(movieMap.get(movie_id)[0] >= 100)
            {
                return movie_id;
            }
        }
        return -1;
    }

    public static double averageNumberOfMoviesRated()
    {
        double sum = 0;
        double count = 0;
        for(int user: userMap.keySet())
        {
            sum += userMap.get(user)[0];
            count++;
        }
        return sum / count;
    }

    public static double calcAngularDistance(int x, int y, int threshold)
    {
        int numCommon = 0;
        int numerator = 0;
        int xDenom = 0;
        int yDenom = 0;

        Map<Integer, Integer> xMovieRatings = userAndMovieMap.get(x);
        Map<Integer, Integer> yMovieRatings = userAndMovieMap.get(y);

        for(int movie: xMovieRatings.keySet())
        {
            // both have rated the same movie
            if(yMovieRatings.containsKey(movie))
            {
                numerator += (xMovieRatings.get(movie) * yMovieRatings.get(movie));
                xDenom += (xMovieRatings.get(movie) * xMovieRatings.get(movie));
                yDenom += (yMovieRatings.get(movie) * yMovieRatings.get(movie));
                numCommon++;
            }
        }

        if(numCommon >= threshold)
        {
            return 1 - (numerator / (Math.sqrt((double) xDenom) * Math.sqrt((double) yDenom)));
        }
        else
        {
            return 1;
        }
    }

    public static Set<Integer> nearestNeighbors(int uid, Set<Integer> neighbors, int threshold, int k)
    {
        // max heap
        Set<Integer> output = new HashSet<>();
        Queue<Integer> pq = new PriorityQueue<>(
                (uid1, uid2) -> calcAngularDistance(uid, uid1, threshold) > calcAngularDistance(uid, uid2, threshold) ? -1 : 1);
        for(int neighbor: neighbors)
        {
            if(neighbor != uid)
            {
                pq.add(neighbor);
                if(pq.size() > k)
                {
                    pq.poll();
                }
            }
        }
        while(!pq.isEmpty())
        {
            output.add(pq.poll());
        }
        return output;
    }

    public static List<ReccResult> recommend(int uid, int threshold, int k, int r)
    {
        Map<Integer, Double> predictions = new HashMap<>();
        Set<Integer> neighbors = userAndMovieMap.keySet();
        Set<Integer> nearestNeighbors = nearestNeighbors(uid, neighbors, threshold, k);
        Map<Integer, double[]> movieAverageRatings = new HashMap<>();
        Set<Integer> unseenMovies = findUnseenMovies(uid, nearestNeighbors, movieAverageRatings);
        double defaultRating = 3.5;
        for(int movie: unseenMovies)
        {
            double numRatings = movieAverageRatings.get(movie)[0];
            double avgRating = movieAverageRatings.get(movie)[1];
            double smoothedPrediction = (defaultRating + (numRatings * avgRating)) / (1 + numRatings);
            predictions.put(movie, smoothedPrediction);
        }
        Queue<Integer> pq = new PriorityQueue<>((a, b) -> predictions.get(a) < predictions.get(b) ? -1 : 1);
        for(int movie: unseenMovies)
        {
            pq.add(movie);
            if(pq.size() > r)
            {
                pq.poll();
            }
        }
        List<ReccResult> recommendations = new ArrayList<>();
        Stack<ReccResult> stack = new Stack<>();
        while(!pq.isEmpty())
        {
            int movie = pq.poll();
            double predictionValue = predictions.get(movie);
            String name = movieNamesMap.get(movie);
            ReccResult curr = new ReccResult(name, predictionValue);
            stack.add(curr);
        }
        while(!stack.isEmpty())
        {
            recommendations.add(stack.pop());
        }
        return recommendations;
    }

    public static Set<Integer> findUnseenMovies(int uid, Set<Integer> neighbors, Map<Integer, double[]> map)
    {
        Set<Integer> totalSet = new HashSet<>();
        for(int neighbor: neighbors)
        {
            for(int movie: userAndMovieMap.get(neighbor).keySet())
            {
                totalSet.add(movie);
                double rating = userAndMovieMap.get(neighbor).get(movie);
                double[] value = map.getOrDefault(movie, new double[2]);
                value[0] += 1;
                value[1] = (((value[0] - 1) * value[1]) + rating) / value[0];
                map.put(movie, value);
            }
        }
        Set<Integer> userSet = userAndMovieMap.get(uid).keySet();
        totalSet.removeAll(userSet);
        return totalSet;
    }

    public static double calcRMSE(int threshold, int k)
    {
        double sum = 0;
        int counter = 0;
        try (Scanner scanner = new Scanner(new File("test_ratings.csv"));)
        {
            while(scanner.hasNextLine()) {
                counter++;
                String line = scanner.nextLine();
                String split[] = line.split(",");
                int uid = Integer.parseInt(split[0]);
                int movie_id = Integer.parseInt(split[1]);
                int rating = Integer.parseInt(split[2]);

                Set<Integer> neighbors = userAndMovieMap.keySet();
                Set<Integer> nearestNeighbors = nearestNeighbors(uid, neighbors, threshold, k);
                // TODO: to make it efficient, create the average by looping through nearest neighbors for the movie instead of using findUnseenMovies **
                double numRatings = 0;
                double avgRating = 0;
                for(int neighbor: nearestNeighbors)
                {
                    if(userAndMovieMap.get(neighbor).containsKey(movie_id))
                    {
                        int neighborRating = userAndMovieMap.get(neighbor).get(movie_id);
                        numRatings++;
                        avgRating = (avgRating * (numRatings - 1) + neighborRating) / numRatings;
                    }
                }
                double defaultRating = 3.5;
                double smoothedPrediction = (defaultRating + (numRatings * avgRating)) / (1 + numRatings);
                double difference = rating - smoothedPrediction;
                sum = sum + (Math.pow(difference, 2) / 1000);
            }
        } catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }
        System.out.println(counter);
        return Math.sqrt(sum);
    }

    public static void main(String[] args) {
        parseRatingsCSV("ratings.csv");
        parseMovieNamesCSV("movies.txt");
        // Question A
//        System.out.println(highestRatedMovie());
//        System.out.println(movieMap.get(318)[0]);
//        System.out.println(movieMap.get(lowestRatedMovie())[1]);
        // Question B
//        System.out.println(lowestRatedMovie());
//        System.out.println(movieMap.get(lowestRatedMovie())[1]);
        // Question C
//        System.out.println(averageNumberOfMoviesRated());
//        System.out.println(userAndMovieMap.get(196).get(242));
//        System.out.println(calcAngularDistance(200, 500, 3));
//        Set<Integer> neighbors = new HashSet<>();
//        for(int i = 100; i < 111; i++)
//        {
//            neighbors.add(i);
//        }
//        System.out.println(nearestNeighbors(2, neighbors, 3, 5));
//        System.out.println(recommend(0, 3, 30, 5));
        long start = System.nanoTime();
        System.out.println(calcRMSE(3, 100));
        long end = System.nanoTime();
        System.out.println((double) (end - start) / 1_000_000_000);
    }
}

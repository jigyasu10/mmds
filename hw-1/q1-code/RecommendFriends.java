package homeworks.recommend;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;

// import homeworks.hw1.*;

import java.io.Console;
import java.io.IOException;
import java.util.*;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class RecommendFriends extends Configured implements Tool {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
	      int res = ToolRunner.run(new Configuration(), new RecommendFriends(), args);
	      System.exit(res);
	}
	
	@Override
	public int run(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
	    Job job = new Job(getConf(), "RecommendFriends");
	    job.setJarByClass(RecommendFriends.class);
	    job.setOutputKeyClass(IntWritable.class); 
	    job.setOutputValueClass(Text.class);

	    job.setMapperClass(Map.class);
	    job.setReducerClass(Reduce.class);

	    job.setInputFormatClass(TextInputFormat.class);
	    job.setOutputFormatClass(TextOutputFormat.class);

	    FileInputFormat.addInputPath(job, new Path(args[0]));
	    FileOutputFormat.setOutputPath(job, new Path(args[1]));

	    job.waitForCompletion(true);
	      
	    return 0;
	 }
	
	// This is a helper class
	public static class Pair implements Comparable<Pair> {
		public Integer user; // non-friend we may recommend 
		public Integer mutualFriends; // number of mutual friends we have in common 
		
		public Pair(Integer user, Integer mutualFriends) {
			this.user = user;
			this.mutualFriends = mutualFriends;
		}
		
		// XXX: Quick hack to get the right order 
		public int compareTo(Pair p) {
			if (mutualFriends.compareTo(p.mutualFriends) != 0) { return p.mutualFriends.compareTo(mutualFriends); }
			else { return user.compareTo(p.user); }
		}
	}

	// public static class Map extends Mapper<LongWritable, Text, Text, Iterable<IntWritable>> {
	public static class Map extends Mapper<LongWritable, Text, IntWritable, Text>  {
		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			Text mutual = new Text(); // , token = new Text();
			IntWritable token = new IntWritable(0);
			String [] KeyValue = value.toString().split("\t"); // User<TAB>Friend1,Friend2,...,Friendn
			String [] friends = KeyValue.length == 1 ? null : KeyValue[1].split(",");
			if (KeyValue.length == 1) { // Friendless people or people with a single friend do not get recommendations 
				mutual.set("/"); // These require special attention 
				token.set(Integer.parseInt(KeyValue[0]));
				context.write(token, mutual);
			} else if (friends.length == 1) {
				mutual.set(friends[0]); // These require special attention 
				token.set(Integer.parseInt(KeyValue[0]));
				context.write(token, mutual);
				return;
			} else { // Generate all pairs (Fi, (U, Fj)), meaning Fi and Fj have mutual friend U 
				for (int i = 0; i < friends.length; ++i) {
					mutual.set(friends[i]);
					token.set(Integer.parseInt(KeyValue[0]));
					context.write(token, mutual); 
					for (int j = 0; j < i; ++j) {
						String token1 = friends[i], token2 = friends[j];
						if (!token1.equals(token2)) {
							mutual.set(KeyValue[0]+","+token2);
							token.set(Integer.parseInt(token1));
							context.write(token, mutual);
							
							token.set(Integer.parseInt(token2));
							mutual.set(KeyValue[0]+","+token1);
							context.write(token, mutual);
						}
					}
				}
			}
		}
	}
	 
	 public static class Reduce extends Reducer<IntWritable, Text, IntWritable, Text> {
	    @Override
	    public void reduce(IntWritable key, Iterable<Text> values, Context context)
	            throws IOException, InterruptedException {
	       // Remember who are my friends 
	       Hashtable<Integer, Integer> count = new Hashtable<Integer, Integer>(); // Count mutual friends 
		   Hashtable<Integer, Boolean> h = new Hashtable<Integer, Boolean>(); // Mark him who makes them mutual friends 
		   List<Integer> mutualList = new LinkedList<Integer>();
		   for(Text v : values) {
				if (v.toString().equals("/")) { // Friendless guy 
				  context.write(key, new Text(""));
				  return;
				} else if (v.toString().indexOf(",") == -1) { // Guy with a single friend 
					h.put(Integer.parseInt(v.toString()), true);
				}
		    	String [] tmp = v.toString().split(",");
		    	h.put(Integer.parseInt(tmp[0]), true);
		    	if (tmp.length > 1) { mutualList.add(Integer.parseInt(tmp[1])); }
		    }
		    System.out.println("Mutual list: "+mutualList.size());
		    // Now count the number of mutual friends with non-friends 
		    for(Integer fid : mutualList) {
		    	if (!h.containsKey(fid)) { // If they're not friends, then they're mutual friends 
		    		if (!count.containsKey(fid)) { count.put(fid, 1); }
		    		else { count.put(fid, new Integer(count.get(fid)+1)); }
		    	}
		    }

		    System.out.println("Count size: "+count.size());
		    // Recommend 10 non-friends with whom I have most mutual friends 
		    List<Pair> users = new ArrayList<Pair>();
		    for (Integer user : count.keySet()) {
		    	users.add(new Pair(user, count.get(user)));
		    }
		    Collections.sort(users);
		    System.out.println("Number of candidate friends: "+users.size());
		    int n = 0; // users.size()-1;
		    String recommendation = "";
		    if (users.size() > 0) recommendation += users.get(n).user;
		    while (n < 9 && n < users.size()-1) {
		    	recommendation += ","+users.get(++n).user;
		    }
		    context.write(key, new Text(recommendation));
		    count.clear(); h.clear(); 
	    }
	 }
}
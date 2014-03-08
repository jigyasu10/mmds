package homework_hw2.kmeans.kmeans;

import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;

import java.io.IOException;
import java.util.*;
import java.io.BufferedReader;
import java.io.FileReader;

public class KMeans extends Configured implements Tool {
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		Configuration conf = new Configuration();
		// conf.set("centersPath", "/home/cloudera/Documents/hw-2/c1.txt");
		int res = ToolRunner.run(conf, new KMeans(), args);
		System.exit(res);
	}
	public static void loadCenters(ArrayList<Point> centers, String centersPath) {
		BufferedReader br = null;
		try {
			br = new BufferedReader(new FileReader(centersPath));
			String line = null;
			while ((line = br.readLine()) != null) {
				if (!line.startsWith("cost")) { centers.add(new Point(line)); }
			}
			br.close();
		} catch (IOException e) {
			System.err.println("[ERROR] Exception reading centers.");
		}
	}
	@Override
	public int run(String[] arg0) throws Exception {
		// inputDir
		// outputDir
		// centroidDir
		getConf().set("centersPath", "/home/cloudera/Documents/hw-2/c1.txt");
		for (int i = 1; i <= 20; ++i) {
			Job job = new Job(getConf(), "KMeans");
			// Configure job with all parameters 
			job.setMapperClass(Map.class);
			job.setReducerClass(Reduce.class);
			
			job.setOutputKeyClass(Text.class); 
			job.setOutputValueClass(Text.class);
			
			job.setInputFormatClass(TextInputFormat.class);
			job.setOutputFormatClass(TextOutputFormat.class);
			// Set job input/output dirs 
			FileInputFormat.addInputPath(job, new Path("/home/cloudera/Documents/hw-2/hw2-q4/data.txt"));
			FileOutputFormat.setOutputPath(job, new Path("/home/cloudera/Documents/hw-2/c-"+i+"/"));
			// Run job
			job.waitForCompletion(true);
			// centroid Dir := outputDir + i 
			getConf().set("centersPath", "/home/cloudera/Documents/hw-2/c-"+i+"/part-r-00000");
		}
		return 0;
	}
	
	public static class Map extends Mapper<LongWritable, Text, Text, Text> {
		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			ArrayList<Point> centers = new ArrayList<Point>();
			Text center = new Text(), point = new Text();
			
			loadCenters(centers, context.getConfiguration().get("centersPath"));
			Point crrDat = new Point(value.toString());
			Point crrCnt = centers.get(0);
			for(Point p : centers) {
				if (crrDat.dist(crrCnt) > crrDat.dist(p)) { crrCnt = p; }
			}
			
			center.set(crrCnt.toString());
			point.set(crrDat.toString());
			
			context.write(center, point);
		}
	}
	
	public static class Reduce extends Reducer<Text, Text, Text, Text> {
		@Override
		public void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {
			Text value = new Text();
			ArrayList<Point> cluster = new ArrayList<Point>();
			
			Point currCenter = new Point(key.toString());
			double currCost = 0.0;
			
			for (Text x : values) { cluster.add(new Point(x.toString())); }
			
			Point nextCenter = cluster.get(0);
			currCost = currCenter.dist(nextCenter);
			for (int i = 1; i < cluster.size(); ++i) {
				nextCenter.add(cluster.get(i));
				currCost += currCenter.dist(cluster.get(i));
			}
			nextCenter.divide(cluster.size()); // our new centroid 
			
			// output the cost
			Text costKey = new Text(); costKey.set("cost");
			Text costVal = new Text(); costVal.set(String.valueOf(currCost));
			context.write(costKey, costVal);
			// output the new center 
			value.set(nextCenter.toString());
			context.write(key, value);
		 }
	}
}

package homework_hw2.kmeans.kmeans;

public class Point {
	private final int DIM = 58;
	private double [] p;
	public Point(String p) {
		this.p = new double[this.DIM];
		int i = 0;
		p = clean(p); 
		for (String x : p.split(" ")) {
			this.p[i] = Double.parseDouble(x);
			++i;
		}
		// hack to see if all is good 
		if (this.p.length != DIM) { System.err.println("DIMENSION MISMATCH"); }
	}
	// ignore previous centers 
	public static String clean(String p) {
		if (p.indexOf('\t') == -1) { return p; }
		else {
			String [] arr = p.split("\t");
			return arr[1];
		}
	}
	// retrieve i-th component 
	public double get(int i) {
		return p[i];
	}
	// distance between self and p2 
	public double dist(Point p2) {
		double d = 0.0;
		for(int i = 0; i < p.length; ++i) {
			d += (p[i]-p2.get(i))*(p[i]-p2.get(i));
		}
		return d;
	}
	// add p2 to self 
	public void add(Point p2) {
		for (int i = 0; i < p.length; ++i) { p[i] += p2.get(i); }
	}
	// divide self with scalar c
	public void divide(double c) {
		for (int i = 0; i < p.length; ++i) { p[i] /= c; }
	}
	// convert point to string 
	public String toString() {
		String s = "";
		for (int i = 0; i < p.length; ++i) {
			s += p[i]+" ";
		}
		return s;
	}
}

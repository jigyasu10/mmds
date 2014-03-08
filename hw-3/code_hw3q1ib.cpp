// 
// Compile with `g++ -std=c++0x -O3 sgd.cpp -o sgd'
// -- Blaz Sovdat, 18 feb 2014 
// 

#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>
#include <map>
#include <random>
#include <ctime>

class Params {
public:
	Params(const int& k_ = 20) : k(k_) { }
	
	void init(const int& m, const int& n); // pass the number of movies 
	double dot(const int& qi, const int& pu) const;
	double all_norms() const {
		double norms = 0.0;
		for (auto it = p_idxs.begin(); it != p_idxs.end(); ++it) { norms += norm_p(it->second); }
		for (auto it = q_idxs.begin(); it != q_idxs.end(); ++it) { norms += norm_q(it->second); }
		return norms;
	}
	double norm_q(int qi) const { // square of L2 norm 
		double norm = 0.0;
		for (int i = 0; i < k; ++i) { norm += Q[qi+i]*Q[qi+i]; }
		return norm;
	}
	double norm_p(int pi) const { // square of L2 norm 
		double norm = 0.0;
		for (int i = 0; i < k; ++i) { norm += P[pi+i]*P[pi+i]; }
 		return norm;
	}
	void update(const double* q, const int& qi, const double* p, const int& pi);
public:
	const int k;
	double* P;
	double* Q;
	std::map<int, int> p_idxs;
	std::map<int, int> q_idxs;
};

void Params::init(const int& m_, const int& n_) {
	std::default_random_engine generator((int)time(0));
	std::uniform_real_distribution<double> dist(0.0, sqrt(5.0/k));
	const int m = m_+1, n = n_+1;
	Q = new double[m*k];
	for (int i = 0; i < m*k; ++i) { Q[i] = dist(generator); }
	P = new double[n*k];
	for (int i = 0; i < n*k; ++i) { P[i] = dist(generator); }
}

double Params::dot(const int& qi, const int& pu) const {
	double s = 0.0;
	for (int j = 0; j < k; ++j) { s += Q[qi+j]*P[pu+j]; }
	return s;
}

void Params::update(const double* q, const int& qi, const double* p, const int& pi) {
	for (int j = 0; j < k; ++j) { Q[qi+j] = q[j]; P[pi+j] = p[j]; }
}

void sgd(const std::string& fname, Params& params, const int& k, const double& lambda, const int& iterations, const double& eta);
double estimate_error(const std::string &fname, Params& params, const int& k, const double& lambda);

// entry point
int main(int argc, char** argv) {
	Params params(20);
	sgd("ratings.train.txt", params, 20, 0.2, 40, 0.01565);
	return 0;
}

void sgd(const std::string& fname, Params& params, const int& k = 20, const double& lambda = 0.2, const int& iterations = 40, const double& eta = 0.1) {
	double crr_eps = 0.0, tmp_eps = 0.0;
	int p_idx = 0, q_idx = 0;
	int crr_user = 0, crr_movie = 0, crr_rating = 0;
	// preliminary pass to initialize params 
	std::string line; 
	std::ifstream infile(fname.c_str());
	getline(infile, line);
	do {
		int t = line.find_first_of('\t', 0);
		crr_user = atoi(line.substr(0, t).c_str());
		crr_movie = atoi(line.substr(t+1, line.find_last_of('\t')).c_str());
		if (params.p_idxs.find(crr_user) == params.p_idxs.end()) { params.p_idxs[crr_user] = p_idx++; }
		if (params.q_idxs.find(crr_movie) == params.q_idxs.end()) { params.q_idxs[crr_movie] = q_idx++; }
		getline(infile, line);
	} while (!infile.eof());
	infile.close();
	
	params.init(q_idx-1, p_idx-1);
	
	double* p = new double[k]();
	double* q = new double[k]();
	
	// do k iterations of stohastic gradient descent 
	for (int i = 0; i < iterations; ++i) {
		// for each r_{iu} in the data 
		std::ifstream infile(fname.c_str());
		getline(infile, line);
		do {
			int t = line.find_first_of('\t', 0);
			crr_user = atoi(line.substr(0, t).c_str());
			crr_movie = atoi(line.substr(t+1, line.find_last_of('\t')).c_str());
			crr_rating = atoi(line.substr(line.find_last_of('\t')+1).c_str());
			// compute epsilon 
			p_idx = k*params.p_idxs[crr_user];
			q_idx = k*params.q_idxs[crr_movie];
			// update epsilon for next iteration
			crr_eps = crr_rating - params.dot(q_idx, p_idx);
			// now update the vectors q and p
			for (int j = 0; j < k; ++j) {
				q[j] = params.Q[q_idx+j] + eta*(crr_eps*params.P[p_idx+j] - lambda*params.Q[q_idx+j]);
				p[j] = params.P[p_idx+j] + eta*(crr_eps*params.Q[q_idx+j] - lambda*params.P[p_idx+j]);
				if (std::isnan(p[j]) || std::isnan(q[j])) { std::cout << "ISNAN: " << i << "-" << j << std::endl; }
			}
			params.update(q, q_idx, p, p_idx);
			
			getline(infile, line);
		} while (!infile.eof() && line.length() > 2);
		infile.close();
		std::cout << i << ":" << estimate_error(fname, params, k, lambda) << std::endl;
	}
	std::cout << "Using eta=" << eta << std::endl;
}

double estimate_error(const std::string& fname, Params& params, const int& k, const double& lambda) {
	double err = 0.0, crr_err = 0.0;
	std::ifstream infile(fname.c_str());
	std::string line; 
	int crr_movie = 0, crr_user = 0, crr_rating = 0;
	int p_idx = 0, q_idx = 0;
	getline(infile, line);
	do {
		int t = line.find_first_of('\t', 0);
		crr_user = atoi(line.substr(0, t).c_str());
		crr_movie = atoi(line.substr(t+1, line.find_last_of('\t')).c_str());
		crr_rating = atoi(line.substr(line.find_last_of('\t')+1).c_str());
		p_idx = k*params.p_idxs[crr_user];
		q_idx = k*params.q_idxs[crr_movie];
		crr_err = crr_rating - params.dot(q_idx, p_idx);
		err += crr_err*crr_err;
		getline(infile, line);
	} while (!infile.eof() && line.length() > 2);
	infile.close();
	err += lambda*(params.all_norms());
	return err; 
}

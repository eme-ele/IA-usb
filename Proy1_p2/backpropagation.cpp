#include <vector>
#include <stdlib.h>
#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <sstream>
#include <string>
#include <fstream>

using namespace std; 

// carga datos funcion xor
int load_xor(vector<vector<double> >& val, vector<double>& out){
	vector<double> a(2);
	vector<double> b(2);
	vector<double> c(2);
	vector<double> d(2);
	a[0] = 0; a[1] = 0;
	val[0] = a; out[0] = 0;
	b[0] = 0; b[1] = 1;
	val[1] = b; out[1] = 1;
	c[0] = 1; c[1] = 0;
	val[2] = c; out[2] = 1;
	d[0] = 1; d[1] = 1;
	val[3] = d; out[3] = 0;
	return 0;
}

double random(double min, double max){
	double i = (double)rand()/RAND_MAX;
	return min + i * (max - min);
}

int init_weights(vector<double>& weights) {
	for(int i; i < weights.size(); i++){
		weights[i] = random(0.0, 0.5);
	}
	return 0;
}


int neural_net(vector<vector <double> >& val, vector<double>& out, 
				int num_inputs, int num_iter, int hidden_nodes, double learning_rate){
	break;
}



int main(int argc, char ** argv){
	srand (time(NULL));
	vector<vector <double> > val;
	vector<double> out;
	int num_inputs = 2;
	int hidden_nodes = 2; 
	int num_iter = 1000;	
	double learning_rate = 0.001;

	load_xor(data, output);
	neural_net(val, out, num_inputs, num_iter, hidden_nodes, learning_rate);
	return 0;
}

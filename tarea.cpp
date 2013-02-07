#include <vector>
#include <stdlib.h>
#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <sstream>
#include <string>
#include <fstream>


using namespace std;


int load_or(vector<vector<int> >& values, vector<double>& output){
	vector<int> a(2);
	vector<int> b(2);
	vector<int> c(2);
	vector<int> d(2);
	a[0] = 0; a[1] = 0;
	values[0] = a; output[0] = 0;
	b[0] = 0; b[1] = 1;
	values[1] = b; output[1] = 1;
	c[0] = 1; c[1] = 0;
	values[2] = c; output[2] = 1;
	d[0] = 1; d[1] = 1;
	values[3] = d; output[3] = 1;
	return 1;
}

int load_and(vector<vector<int> >& values, vector<double>& output){
	vector<int> a(2);
	vector<int> b(2);
	vector<int> c(2);
	vector<int> d(2);
	a[0] = 0; a[1] = 0;
	values[0] = a; output[0] = 0;	
	b[0] = 0; b[1] = 1; 
	values[1] = b; output[1] = 0;	
	c[0] = 1; c[1] = 0;
	values[2] = c; output[2] = 0;
	d[0] = 1; d[1] = 1;
	values[3] = d; output[3] = 1;
	return 1;
}

int load_xor(vector<vector<int> >& values, vector<double>& output){
	vector<int> a(2);
	vector<int> b(2);
	vector<int> c(2);
	vector<int> d(2);
	a[0] = 0; a[1] = 0;
	values[0] = a; output[0] = 0;
	b[0] = 0; b[1] = 1;
	values[1] = b; output[1] = 1;
	c[0] = 1; c[1] = 0;
	values[2] = c; output[2] = 1;
	d[0] = 1; d[1] = 1;
	values[3] = d; output[3] = 0;
	return 1;
}

int fill_example(vector<string>& tokens, vector<int>& x){
	for (int i=0; i < 5; i++){
		stringstream ss(tokens[i]);
		ss >> x[i];
	}
	return 1;
}

int print(vector<double>& weights){
	for (int i=0; i < weights.size(); i++){
		cout << weights[i] << " ";
	}
	cout << endl;
	return 1;
}

int print_int(vector<int>& weights){
	for (int i=0; i < weights.size(); i++){
		cout << weights[i] << " ";
	}
	cout << endl;
	return 1;
}

int print_values(vector<vector<int> >& values){
	for (int i=0; i < values.size(); i++){
		cout << i << ": ";
		for (int j=0; j < values[i].size(); j++)
			cout << values[i][j] << " ";
	cout << endl;
	}
	return 1;
}


int load_bupa(vector<vector<int> >& train, vector<vector<int> >&  test, 
				vector<double>& out_test, vector<double>& out_train, string filename){
	ifstream myfile;
	string line, word;
	vector<string> tokens(7);
	int i = 0;
	int k = 0;
	double out;

	myfile.open(filename.c_str());	
	if (myfile.is_open()){
		while (myfile.good()){
			getline(myfile, line);
			vector<int> x(5);			
			stringstream line_ss(line);			
			for(int j=0; j<7; j++){
				getline(line_ss, tokens[j], ',');
			}
			stringstream ss(tokens[5]);
			ss >> out;
			if (strcmp(tokens[6].c_str(),"1")==0) {
				fill_example(tokens, x);
				train[i] = x; 
				out_train[i] = out;
				i++;
			} else if (strcmp(tokens[6].c_str(),"2")==0) {
				fill_example(tokens, x);
				test[k] = x;
				out_test[k] = out;
				k++;
			}
		}
		print_values(test);
		myfile.close();
		return 1;
	}
	else {
		return -1;
	}		
}

double dot_product(vector<int> value, vector<double>& weights){
	double sum; 
	sum = value[0] * weights[0];
	sum = sum + value[1] * weights[1];
	return sum;
}

int perceptron(int n, double threshold, double learning_rate, vector<vector<int> >& values, vector<double>& output){
	vector<double> weights(n);	
	int error_count;
	double error;
	int result;
	while(1){
		error_count = 0;
		for(int i=0; i < values.size(); i++){
			print(weights);
			result = dot_product(values[i], weights) > threshold;
			error = output[i] - result;
			if (error != 0){
				error_count++;
				for(int j=0; j < weights.size(); j++){
					weights[j] = weights[j] + learning_rate * error * values[i][j];
				}
			}
		}
		if (error_count == 0) {
			return 1;
		}
	}
}

double error_cuadrado(vector<double>& o, vector<double>& t){
	double sum = 0.0;
	for(int i=0; i < o.size(); i++){
		sum = sum + pow((t[i] - o[i]),2);
		
	}
	return sum/2;
	
}

int adaline(int n, double learning_rate, vector<vector<int> >& values, vector<double>& output){
	vector<double> weights(n);
	vector<double> grad_weights(n);
	double error_count;
	double error;
	double min_error = 1000;
	vector<double> result(values.size());
	// store results
	int num_it;
	vector<double> final_weights(weights);
	
	for(int x=0; x<1000;x++){
		error_count = 0;
		for(int i=0; i < values.size(); i++){
			//print(weights);
			result[i] = dot_product(values[i], weights);
			error = output[i] - result[i];
			for(int j=0; j<grad_weights.size(); j++){
				grad_weights[j] = grad_weights[j] + learning_rate * error * values[i][j];
			}
		}
		for (int k=0; k<weights.size(); k++){
			weights[k] = weights[k] + grad_weights[k];
		}
		error_count = error_cuadrado(result,output);
	
		// si encuentro un peso menor
		if (error_count < min_error) {
			num_it = x;
			final_weights = weights;
			min_error = error_count;
		}
	}
	cout << "Iteraciones: " << num_it << " Error Minimo: " << min_error << endl;
	cout << "Pesos: ";
	print(final_weights);
	return 0;
}

int imprimir_uso(){
	cerr << "Uso: ./tarea -[p | a] -[or | and | xor | liv]" << endl;
	return 1;
}


int main(int argc, char ** argv){
	vector<vector<int> > values(4);
	vector<double> output(4);
	vector<vector<int> > train(145);
	vector<double> out_train(145);	
	vector<vector<int> > test(200);
	vector<double> out_test(200);
 
	if (argc != 3) {
		imprimir_uso();
		return -1;
	}

	if (strcmp(argv[2],"-or")==0){
		load_or(values,output);
	} else if (strcmp(argv[2],"-and")==0) {
		load_and(values,output);
	} else if (strcmp(argv[2],"-xor")==0) {
		load_xor(values,output);
	} else if (strcmp(argv[2],"-liv")==0){
		if (load_bupa(train, test, out_train, out_test, "bupa.data") < 0){
			cerr << "error cargando el archivo bupa.data" << endl;
			return -1;
		}
	} else {
		imprimir_uso();
		return -1;
	}

	if (strcmp(argv[1], "-a")==0 and strcmp(argv[2], "-liv")!=0){
		adaline(2, 0.01, values, output);
	} else if (strcmp(argv[1], "-a")==0 and strcmp(argv[2], "-liv")==0){
		cout << "adaline .." << endl;
		adaline(5, 0.01, train, out_train);
		cout << "adaline2 .." << endl;
		adaline(5, 0.01, test, out_test);
	} else if (strcmp(argv[1], "-p")==0 and strcmp(argv[2],"-liv") != 0){
		perceptron(2, 0.5, 0.01, values, output);
	} else {
		imprimir_uso();
		return -1;
	}

}


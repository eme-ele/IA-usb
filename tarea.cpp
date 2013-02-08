#include <vector>
#include <stdlib.h>
#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <sstream>
#include <string>
#include <fstream>


using namespace std;


int load_or(vector<vector<double> >& values, vector<double>& output){
	vector<double> a(2);
	vector<double> b(2);
	vector<double> c(2);
	vector<double> d(2);
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

int load_and(vector<vector<double> >& values, vector<double>& output){
	vector<double> a(2);
	vector<double> b(2);
	vector<double> c(2);
	vector<double> d(2);
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

int load_xor(vector<vector<double> >& values, vector<double>& output){
	vector<double> a(2);
	vector<double> b(2);
	vector<double> c(2);
	vector<double> d(2);
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

int print(vector<double>& weights){
	for (int i=0; i < weights.size(); i++){
		cout << weights[i] << " ";
	}
	cout << endl;
	return 1;
}

int print_int(vector<double>& weights){
	for (int i=0; i < weights.size(); i++){
		cout << weights[i] << " ";
	}
	cout << endl;
	return 1;
}

int print_values(vector<vector<double> >& values){
	for (int i=0; i < values.size(); i++){
		cout << i << ": ";
		for (int j=0; j < values[i].size(); j++)
			cout << values[i][j] << " ";
	cout << endl;
	}
	return 1;
}


int load_bupa(vector<vector<double> >& values, vector<double>& out, string filename){
	ifstream myfile (filename.c_str());
	string line;
	string token;
	double matrix[345][7];
	int i = 0;
	int j = 0;
	if (myfile.is_open()){
		while(myfile.good()){
			getline(myfile,line);
			stringstream sLinea(line);
			j=0;
			while(getline(sLinea, token, ',')){
				stringstream valor(token);
				valor >> matrix[i][j];
				
				j++;
			}
			i++;
		}		
		for(i=0; i<145;i++){
			vector<double> x(6);
			for(j=0; j<6; j++){
				x[j] = matrix[i][j];
			}
			values[i] = x;
			out[i] = matrix[i][6];
		}
		

	} else {
		// si no pudo abrir archivo
		return -1;
	}
	
	//print_values(values);
	//print(out);
	myfile.close();
	return 1;
}

double dot_product(vector<double> value, vector<double>& weights){
	double sum = 0; 
	//print(value);
	//print(weights);
	for(int i=0; i < value.size();i++){
		sum = sum + value[i] * weights[i];
	}
	//cout << "SUMA " << sum << endl;
	//exit(-1);
	return sum;
}

int perceptron(int n, double threshold, double learning_rate, vector<vector<double> >& values, vector<double>& output){
	vector<double> weights(n);	
	int error_count;
	double error;
	int result;
	for(int t=0;t<1000;t++){
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
	//cout << sum << endl;
	return sum/2;
	
}

int adaline(int n, double learning_rate, vector<vector<double> >& values, vector<double>& output){
	vector<double> weights(n);
	//for(int z=0; z< weights.size();z++ ){
	//	weights[z]= (rand() /(double) RAND_MAX);
	//}
	//print(weights);
	vector<double> grad_weights(n);
	
	double error_count;
	double error;
	double min_error = 1000;
	vector<double> result(values.size());
	// store results
	int num_it;
	int x;
	vector<double> final_weights(weights);
	for(x=0; x<50;x++){
		//print(weights);
		error_count = 0;
		for(int i=0; i < values.size(); i++){
			//print(weights);
			//cout << "values[i]" << endl;
			result[i] = dot_product(values[i], weights);
			error = output[i] - result[i];
			//cout << "Error   " << error << endl;
			for(int j=0; j<grad_weights.size(); j++){
				double nuevoVar = learning_rate * error * values[i][j];
				grad_weights[j] = grad_weights[j] + nuevoVar;
				//cout << "variacion " << nuevoVar;
			}
		}
		for (int k=0; k<weights.size(); k++){
			weights[k] = weights[k] + grad_weights[k];
		}
		error_count = error_cuadrado(result,output);
		//cout << error_count << endl;
		// si encuentro un peso menor
		cout << error_count << endl;
		if (error_count < min_error) {
			num_it = x;
			final_weights = weights;
			min_error = error_count;
		}
		if(error_count < 0){
			break;
		}
	}
	//cout << "Iteraciones: " << num_it << " Error Minimo: " << min_error << endl;
	//cout << "Pesos: ";
	//print(final_weights);
	return 0;
}







int adaline_incremental(int n, double learning_rate, vector<vector<double> >& values, vector<double>& output){
	vector<double> weights(n);
	print(weights);
	vector<double> grad_weights(n);
	double error_count;
	double error;
	double min_error = 1000;
	vector<double> result(values.size());
	int num_it = 0;
	int x;
	vector<double> final_weights(weights);
	for(x=0; x<10;x++){
		error_count = 0;
		for(int i=0; i < values.size(); i++){
			result[i] = dot_product(values[i], weights);
			error = output[i] - result[i];
			for(int j=0 ; j < weights.size(); j++){
				double nuevoVar = learning_rate * error * values[i][j];
				weights[j] = weights[j] + nuevoVar;
			}
			
		}
//		cout << x << ") weights[j]";
//		print_int(weights);
//		cout << "" << endl;
		error_count = error_cuadrado(result,output);
		cout << "ERROR_COUNT: " << error_count << endl;
		if (error_count < min_error) {
			num_it = x;
			final_weights = weights;
			min_error = error_count;
		}
		if(error_count < 0){
			break;
		}
	}
	cout << "Iteraciones: " << num_it << " Error Minimo: " << min_error << endl;
	cout << "Pesos: ";
	print(final_weights);
	return 0;
}




int imprimir_uso(){
	cerr << "Uso: ./tarea -[p | a] -[or | and | xor | liv] [alpha]" << endl;
	return 1;
}


int main(int argc, char ** argv){
	vector<vector<double> > values(4);
	vector<double> output(4);
	vector<vector<double> > in(145);
	vector<double> out(145);	
 
	if (argc != 4) {
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
		if (load_bupa(in, out, "bupa.data") < 0){
			cerr << "error cargando el archivo bupa.data" << endl;
			return -1;
		}
	} else {
		imprimir_uso();
		return -1;
	}

	if (strcmp(argv[1], "-a")==0 and strcmp(argv[2], "-liv")!=0){
		adaline(2, atof(argv[3]), values, output);
	} else if (strcmp(argv[1], "-a")==0 and strcmp(argv[2], "-liv")==0){
		//cout << "adaline .." << endl;
		//adaline(5, 0.01, train, out_train);
		//cout << "adaline2 .." << endl;
		adaline(6, atof(argv[3]), in, out);
		
	} else if (strcmp(argv[1], "-p")==0 and strcmp(argv[2],"-liv") != 0){
		perceptron(2, 0.5, 0.01, values, output);
	} else {
		imprimir_uso();
		return -1;
	}

}


//0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5 y 0.99.


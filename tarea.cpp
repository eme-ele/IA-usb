#include <vector>
#include <stdlib.h>
#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <sstream>
#include <string>
#include <fstream>

/*
Charles Ochoa - 0741286
Maria Leonor Pacheco - 0741302

Tarea de Prog 1:
	Implementacion perceptron + adaline
	para funciones booleanas y datos de UCI

*/

using namespace std;

// carga datos funcion or
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

// carga datos funcion and
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

// carga datos funcion xor
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

// funcion auxiliar de impresion de vectores double
int print(vector<double>& weights){
	for (int i=0; i < weights.size(); i++){
		cout << weights[i] << " ";
	}
	cout << endl;
	return 1;
}

// funcion auxiliar de impresion de vectores int
int print_int(vector<double>& weights){
	for (int i=0; i < weights.size(); i++){
		cout << weights[i] << " ";
	}
	cout << endl;
	return 1;
}

// funcion auxiliar de impresion de ejemplos
int print_values(vector<vector<double> >& values){
	for (int i=0; i < values.size(); i++){
		cout << i << ": ";
		for (int j=0; j < values[i].size(); j++)
			cout << values[i][j] << " ";
	cout << endl;
	}
	return 1;
}

// carga de datos UCI
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
		for(i=0; i<345;i++){
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

// calculo de salida
double dot_product(vector<double> value, vector<double>& weights){
	double sum = 0; 
	for(int i=0; i < value.size();i++){
		sum = sum + value[i] * weights[i];
	}
	return sum;
}

// aprendizaje con un perceptron
int perceptron(int n, double threshold, double learning_rate, vector<vector<double> >& values, 
				vector<double>& output, int num_it){
	vector<double> weights(n);	
	int error_count;
	double error;
	int result;
	for(int t=0;t<num_it;t++){
		error_count = 0;
		for(int i=0; i < values.size(); i++){
			result = dot_product(values[i], weights) > threshold;
			error = output[i] - result;
			if (error != 0){
				error_count++;
				for(int j=0; j < weights.size(); j++){
					weights[j] = weights[j] + learning_rate * error * values[i][j];
				}
			}
		}
		cout << error_count << " ";
		if (error_count == 0) {
			cout << error_count << "\n" << endl;
			return 1;
		}
	}
	cout << error_count << "\n" << endl;
	return 1;
}

// error cuadrado para neurona adaline
double error_cuadrado(vector<double>& o, vector<double>& t){
	double sum = 0.0;
	for(int i=0; i < o.size(); i++){
		sum = sum + pow((t[i] - o[i]),2);
		
	}
	return sum/2;	
}
 
// aprendizaje con una neurona adaline (regla delta)
int adaline(int n, double learning_rate, vector<vector<double> >& values, vector<double>& output, 
			vector<vector<double> >& final_weights, int size){
	int num_it = final_weights.size();
	vector<double> grad_weights(n);	
	double error_count;
	double error;
	vector<double> result(size);
	vector<double> weights(n);
	

	for(int x=0; x<num_it;x++){
		error_count = 0;
		for(int i=0; i < size; i++){
			result[i] = dot_product(values[i], weights);
			error = output[i] - result[i];
			for(int j=0; j<grad_weights.size(); j++){
				double nuevoVar = learning_rate * error * values[i][j];
				grad_weights[j] = grad_weights[j] + nuevoVar;
			}
		}
		for (int k=0; k<weights.size(); k++){
			weights[k] = weights[k] + grad_weights[k];
		}
		error_count = error_cuadrado(result,output);
		final_weights[x] = weights;
		cout << error_count << " ";
	}
	cout << "\n" << endl;
	return 1;
}

// prueba de aprendizaje adaline en datos UCI
int testing(vector<vector<double> >& final_weights, vector<vector<double> >& values, vector<double>& output){
	int num_it = final_weights.size();
	double error_count;
	double error;
	vector<double> result(values.size());

	for(int x=0; x<num_it;x++){
		error_count = 0;
		for(int i=145; i < values.size(); i++){
			result[i-145] = dot_product(values[i], final_weights[x]);
		}
		error_count = error_cuadrado(result,output);
		cout << error_count << " ";
	}
	cout << "\n" << endl;
	return 1;
}



// aprendizaje incremental para la regla delta
int adaline_incremental(int n, double learning_rate, vector<vector<double> >& values, vector<double>& output,
						vector<vector<double> >& final_weights, int size){
	int num_it = final_weights.size();
	vector<double> grad_weights(n);
	double error_count;
	double error;
	vector<double> result(size);
	vector<double> weights(n);		


	for(int x=0; x<num_it;x++){
		error_count = 0;
		for(int i=0; i < size; i++){
			result[i] = dot_product(values[i], weights);
			error = output[i] - result[i];
			for(int j=0 ; j < weights.size(); j++){
				double nuevoVar = learning_rate * error * values[i][j];
				weights[j] = weights[j] + nuevoVar;
			}
			
		}
		final_weights[x] = weights;
		error_count = error_cuadrado(result,output);
		cout << error_count << " ";
	}
	cout << "\n" << endl;
	return 0;
}



// muestra forma de invocar el programa
int imprimir_uso(){
	cerr << "Uso: ./tarea -[p | a | ai] -[or | and | xor | liv] [alpha] [num_it] [filename *opcional*]" << endl;
	return 1;
}


int main(int argc, char ** argv){
	vector<vector<double> > values(4);
	vector<double> output(4);
	vector<vector<double> > in(345);
	vector<double> out(345);	
	string filename;
 
	if (argc < 5 or argc > 6) {
		imprimir_uso();
		return -1;
	}

	int num_it = atoi(argv[4]);
	double alpha = atof(argv[3]);
	if (num_it < 0 || alpha < 0){
		imprimir_uso();
		return -1;
	}


	vector<vector<double> > final_weights(num_it);

	if (strcmp(argv[2],"-or")==0){
		load_or(values,output);
	} else if (strcmp(argv[2],"-and")==0) {
		load_and(values,output);
	} else if (strcmp(argv[2],"-xor")==0) {
		load_xor(values,output);
	} else if (strcmp(argv[2],"-liv")==0){
		if (argc < 6){
			imprimir_uso();
			cout << "Nota: incluir nombre de archivo de datos" << endl;
			return -1;
		}
		else{
			filename = argv[5];
			if (load_bupa(in, out, filename) < 0){
				cerr << "error cargando el archivo" << endl;
				return -1;
			}
		}
	} else {
		imprimir_uso();
		return -1;
	}
	
	if (strcmp(argv[1], "-a")==0 and strcmp(argv[2], "-liv")!=0){
		adaline(2, alpha, values, output, final_weights, values.size());
	} else if (strcmp(argv[1], "-a")==0 and strcmp(argv[2], "-liv")==0){
		adaline(6, alpha, in, out, final_weights,145);
		testing(final_weights, in, out);
	} else if (strcmp(argv[1], "-ai")==0 and strcmp(argv[2], "-liv")!=0){
		adaline_incremental(6, alpha, values, output, final_weights, values.size());
		
	} else if (strcmp(argv[1], "-ai")==0 and strcmp(argv[2], "-liv")==0){
		adaline_incremental(6, alpha, in, out, final_weights, 145);
		testing(final_weights, in, out);
		
	} else if (strcmp(argv[1], "-p")==0 and strcmp(argv[2],"-liv") != 0){
		perceptron(2, 0.5, alpha, values, output, num_it);
	} else {
		imprimir_uso();
		return -1;
	}

}


//0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5 y 0.99.


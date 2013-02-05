#include <vector>
#include <stdlib.h>
#include <iostream>
#include <stdlib.h>

using namespace std;

struct Pair {
  int v1;
  int v2;
};

typedef struct Pair Pair;

int load_or(vector<Pair>& values, vector<int>& output){
  Pair a,b,c,d;
  a.v1 = 0; a.v2 = 0;
  values[0] = a; output[0] = 0;
  b.v1 = 0; b.v2 = 1;
  values[1] = b; output[1] = 1;
  c.v1 = 1; c.v2 = 0;
  values[2] = c; output[2] = 1;
  d.v1 = 1; d.v2 = 1;
  values[3] = d; output[3] = 1;
  return 1;
}

int load_and(vector<Pair>& values, vector<int>& output){
  Pair a,b,c,d;
  a.v1 = 0; a.v2 = 0;
  values[0] = a; output[0] = 0;  
  b.v1 = 0; b.v2 = 1; 
  values[1] = b; output[1] = 0;  
  c.v1 = 1; c.v2 = 0;
  values[2] = c; output[2] = 0;
  d.v1 = 1; d.v2 = 1;
  values[3] = d; output[3] = 1;
  return 1;
}

int load_xor(vector<Pair>& values, vector<int>& output){
  Pair a,b,c,d;
  a.v1 = 0; a.v2 = 0;
  values[0] = a; output[0] = 0;
  b.v1 = 0; b.v2 = 1;
  values[1] = b; output[1] = 1;
  c.v1 = 1; c.v2 = 0;
  values[2] = c; output[2] = 1;
  d.v1 = 1; d.v2 = 1;
  values[3] = d; output[3] = 0;
  return 1;
}

int print(vector<double>& weights){
  cout << "Weights: ";
  for (int i=0; i < weights.size(); i++){
    cout << weights[i] << " ";
  }
  cout << endl;
  return 1;
}

int dot_product(Pair value, vector<double>& weights){
  double sum; 
  sum = value.v1 * weights[0];
  sum = sum + value.v2 * weights[1];
  return sum;
}

int perceptron(int n, double threshold, double learning_rate, vector<Pair>& values, vector<int>& output){
  cout << "perceptron..." << endl;
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
        weights[0] = weights[0] + learning_rate * error * values[i].v1;
        weights[1] = weights[1] + learning_rate * error * values[i].v2;
      }
    }
    if (error_count == 0) {
      return 1;
    }
  }
}

int adaline(){
  return 1;
}

int imprimir_uso(){
  cerr << "Uso: ./tarea -[p|a] [num_entradas] -[or|and|xor]" << endl;
  return 1;
}


int main(int argc, char ** argv){
  vector<Pair> values(4);
  vector<int> output(4);
 
  if (argc != 4) {
    imprimir_uso();
    return -1;
  }
  int n = atoi(argv[2]);

  if (strcmp(argv[3],"-or")==0){
    load_or(values,output);
  } else if (strcmp(argv[3],"-and")==0) {
    load_and(values,output);
  } else if (strcmp(argv[3],"-xor")==0) {
    load_xor(values,output);
  } else {
    imprimir_uso();
    return -1;
  }

  if (strcmp(argv[1], "-a")==0){
    adaline();
  } else if (strcmp(argv[1], "-p")==0){
    perceptron(n, 0.5, 0.01, values, output);
  }

}


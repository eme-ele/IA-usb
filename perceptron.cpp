#include <vector>

struct pair{
  int v1;
  int v2;
};

void load_or(vector<pair>& values){
  struct a,b,c,d;
  a.v1 = 0; a.v2 = 0; a.output = 0;
  values[0] = a;
  b.v1 = 0; b.v2 = 1; b.output = 1;
  values[1] = b;
  c.v1 = 1; c.v2 = 0; c.output = 1;
  values[2] = c;
  d.v1 = 1; d.v2 = 1; d.output = 1;
  values[3] = d;
}

void load_and(vector<pair>& values){
  struct a,b,c,d;
  a.v1 = 0; a.v2 = 0; a.output = 0;
  values[0] = a;
  b.v1 = 0; b.v2 = 1; b.output = 0;
  values[1] = b;
  c.v1 = 1; c.v2 = 0; c.output = 0;
  values[2] = c;
  d.v1 = 1; d.v2 = 1; d.output = 1;
  values[3] = d;
}

void load_xor(vector<pair>& values){
  struct a,b,c,d;
  a.v1 = 0; a.v2 = 0; a.output = 0;
  values[0] = a;
  b.v1 = 0; b.v2 = 1; b.output = 1;
  values[1] = b;
  c.v1 = 1; c.v2 = 0; c.output = 1;
  values[2] = c;
  d.v1 = 1; d.v2 = 1; d.output = 0;
  values[3] = d;
}

int print(vector<int>& weights){
  cout << "Weights: ";
  for (int i; i < weights.size(); i++){
    cout << weights[i] << " ";
  }
  cout << endl;
  return 1;
}

int dot_product(){
  for(int i; )
}

int main(int argc, int * argv){
  int n = argv[1];
  double learning_rate = 0.01;
  int error_count;
  vector<int> weights(n);
  vector<pair> values(4);
  vector<int> output(4);

  load_or(trainset);
  
  while(1){
    error_count = 0;
    for(int i; i < trainset.size(); i++){
      pair input_value = values[i];
      int desired_output = output[i];
      print(weights);
      dot_product

    }
  }
}
